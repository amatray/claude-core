---
name: seminar-schedule
description: Automate Atlanta Fed seminar scheduling — collect host availability, send date-preference invitations, collect replies, optimize assignments, and send confirmations. Use when user wants to schedule seminar speakers, send invitations, collect date preferences, check host availability, or assign seminar dates.
argument-hint: "availability|send|collect|remind|optimize [semester:Fall2026] [dryrun]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "mcp__google_workspace__search_gmail_messages", "mcp__google_workspace__get_gmail_message_content", "mcp__google_workspace__get_gmail_messages_content_batch", "mcp__google_workspace__get_gmail_thread_content", "mcp__google_workspace__send_gmail_message", "mcp__google_workspace__read_sheet_values", "mcp__google_workspace__get_spreadsheet_info", "mcp__google_workspace__manage_gmail_label", "mcp__google_workspace__draft_gmail_message"]
---

Automate the Atlanta Fed Research Seminar scheduling workflow via email.

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Subcommand** (optional, first word): `availability`, `send`, `collect`, `remind`, or `optimize`
- **semester:X** (optional): e.g., `semester:Fall2026`. Default: infer from current date (Jan–Jul = Spring [year], Aug–Dec = Fall [year])
- **dryrun** (optional flag): preview actions without sending emails or writing files

If no subcommand is provided, show this menu and ask the user to pick:

```
Seminar Scheduling — What would you like to do?

  1. availability — Collect host availability from the email thread where colleagues
                    reported their unavailable dates. Displays a host × date table
                    for review, then saves to host_availability.json.

  2. send     — Send invitation emails to speakers asking for their preferred dates.
               Reads speakers from suggested_names.xlsx, extracts available Thursdays
               from the Google Sheet, filters by host availability, and emails each
               speaker (CC'ing their host).

  3. collect  — Scan Gmail for speaker replies and parse their date preferences.
               Shows a table of parsed preferences for your review before saving.

  4. remind   — Send a gentle reminder to speakers who haven't replied yet.

  5. optimize — Run the optimizer to find the best date assignment, then send
               confirmation emails to speakers with their assigned date.

  Add "dryrun" to any command to preview without sending emails/writing files.
  Add "semester:Fall2026" to target a specific semester.
```

Wait for the user to pick before proceeding.

## Constants

- **Google Sheet ID**: `1dFiNTyXj--kW5eRld-tcj_HnUMHENH7EgNYiWxZ1QtM`
- **Google email**: `adrien.matray@gmail.com`
- **Subject tag**: `SeminarInvite`
- **Seminars base path**: `/Users/adrienmatray/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/_FedStuff/Seminars`
- **xlsx path**: `{base_path}/{year_folder}/suggested_names.xlsx` (e.g., `2026_2027/suggested_names.xlsx` for Fall 2026 or Spring 2027)
- **Data path**: `{base_path}/{year_folder}/data/` (create if missing)
- **Optimizer**: `{base_path}/Building_website/optimizer.py`

## Shared: Date Extraction

At the start of `availability`, `send`, `collect`, and `optimize`, extract available dates:

1. Call `get_spreadsheet_info` to list sheet tabs
2. Find the tab matching the semester (e.g., "Fall 2026")
3. Call `read_sheet_values` on that tab (range `A1:Z300`)
4. Parse rows: find all rows where **column B = "Thursday"** and **column C is empty or blank**
5. Infer year from the "Week ..." header rows (e.g., "Week September 07 to September 13" → year from tab context)
6. Build available dates as ISO strings (e.g., `2026-09-03`)
7. Display the numbered list to the user

If no available dates found, report and stop.

## Shared: Read Speakers from xlsx

1. Read `suggested_names.xlsx` via python/openpyxl (Bash tool)
2. Find columns by **header name** in row 1: `Name Host`, `Host Email`, `Guest`, `Guest Email`, `Paper Suggested`
3. If any required header (`Name Host`, `Host Email`, `Guest`, `Guest Email`) is missing, error with: "Missing column '[name]' in suggested_names.xlsx. Expected headers: Name Host, Host Email, Guest, Guest Email, Paper Suggested"
4. Read all data rows (row 2+), skip rows where Guest is empty
5. Return list of `{host_name, host_email, guest_name, guest_email, paper_title}`

## Subcommand: `availability`

Collect host availability from the Gmail thread where colleagues reported their unavailable dates.

### Steps

1. **Extract available dates** (shared step above) — this produces the finite set of candidate Thursdays
2. **Load hosts from xlsx** (shared "Read Speakers" step above) — build a **host registry**: `{host_email: {name, suggested_speakers: [...]}}`. This is loaded BEFORE parsing replies, so we know which senders are hosts vs. noise.
3. **Search Gmail** for the availability thread:
   - Query: `subject:"Finance Seminar" subject:"Available Dates"` (keep it loose to avoid em-dash and encoding issues)
   - Expect **exactly one thread**. If zero: error "No availability thread found — check that the subject matches." If multiple: show subjects and ask the user to pick.
   - Read the full thread via `get_gmail_thread_content` (preferred). Fallback: use `search_gmail_messages` to get all message IDs, then `get_gmail_messages_content_batch` to read them.
4. **Match senders to hosts and parse replies**:

   For each message in the thread (excluding messages from adrien.matray@gmail.com):

   a. **Match sender to host registry** using fuzzy matching:
      - First try exact email match against host emails in xlsx
      - Then match on email prefix (everything before `@`)
      - Then match on display name vs. host name
      - If no match: flag as "unknown sender" — show to user but do not parse as host

   b. **Handle multiple replies from same host**: use the most recent reply. Show all replies with timestamps in the raw snippet area so user can verify.

   c. **Strip noise**: Remove quoted text (lines starting with `>`), signature blocks (text after `--` or common sign-offs like "Best," "Thanks,"), and institutional disclaimers/footers.

   d. **Determine reply polarity** — classify whether the responder states:
      - **Unavailability**: "I can't do Oct 1 and Oct 15", "traveling the week of..."
      - **Availability**: "I'm only free Sep 3 and Oct 1", "I can do..."
      - **Full availability**: "All dates work", "I'm flexible"
      - **Unclear**: ambiguous or conditional — flag for manual review

   e. **Match against the finite Thursday list**: Do NOT try to parse arbitrary dates. Match the responder's language against the specific Thursdays from step 1. Output structured data per reply:
      ```json
      {"unavailable_dates": ["2026-09-10", "2026-10-01"], "polarity": "unavailability", "confidence": "high|low"}
      ```

   f. **If polarity = availability**: invert against the full Thursday list to derive unavailable dates.

   g. **If unclear or low confidence**: include in table but mark with `?` for user review.

5. **Display availability table**:

```
HOST AVAILABILITY — [Semester]
(✓ = available, ✗ = unavailable, ? = unclear, · = no reply)

| Host            | Suggested Speaker    | Sep 3 | Sep 10 | Oct 1 | Oct 15 | ... |
|-----------------|----------------------|-------|--------|-------|--------|-----|
| Camelia Minoiu  | Victoria Ivashina    |   ✓   |   ✗    |   ✓   |   ✓    |     |
| Mark Jensen     | Mark Egan            |   ✓   |   ✓    |   ✗   |   ✓    |     |
| Roberto Robatto | Adi Sunderam         |   ·   |   ·    |   ·   |   ·    |     |
```

   Below the table, show:
   - **Raw reply snippets** for each host (with timestamps, so user can verify parsing)
   - **Fuzzy-matched senders**: any sender matched by prefix/name rather than exact email — highlighted for user confirmation
   - **Unknown senders**: replies from people not in the host registry
   - **Hosts with no reply**: listed explicitly with prompt: "Treat as fully available, or hold their speakers?"

6. **STOP and ask** for user approval:
   - User can correct any parsing errors
   - User confirms fuzzy matches
   - User decides what to do about non-responsive hosts (fully available, or hold)

7. **Save** to `{data_path}/host_availability.json`:
   - If file already exists, note "Overwriting previous host_availability.json"
   - Structure:
     ```json
     {
       "Fall 2026": {
         "camelia.minoiu@atl.frb.org": {
           "name": "Camelia Minoiu",
           "unavailable_dates": ["2026-09-10"],
           "assumed_fully_available": false,
           "raw_reply": "I'll be traveling Sep 10...",
           "reply_email": "camelia.minoiu@gmail.com",
           "parsed_at": "2026-03-24T10:00:00Z"
         },
         "roberto.robatto@atl.frb.org": {
           "name": "Roberto Robatto",
           "unavailable_dates": [],
           "assumed_fully_available": true,
           "raw_reply": null,
           "reply_email": null,
           "parsed_at": "2026-03-24T10:00:00Z"
         }
       }
     }
     ```
   - All dates in ISO 8601 format
   - `reply_email` captures the actual sender address (may differ from xlsx host email)
   - If **dryrun**: display table but skip file write, print `[DRYRUN] Would save host_availability.json`

---

## Subcommand: `send`

### Steps

1. **Extract available dates** (shared step above)
2. **Read speakers** from xlsx (shared step above)
3. **Load host availability**: Read `{data_path}/host_availability.json` for the current semester.
   - If file doesn't exist: warn "No host availability data found. Run `/seminar-schedule availability` first, or proceed with unfiltered dates?" Wait for user decision.
   - If `parsed_at` timestamps are older than 14 days: warn "Host availability data is [N] days old. Consider re-running `/seminar-schedule availability`."
   - For each speaker, filter the available dates list to **exclude** dates where their host is unavailable.
   - If a host is marked `assumed_fully_available: true`, use all dates (no filtering).
   - If filtering leaves zero dates for a speaker: flag "No available dates for [Speaker] — all dates conflict with host [Host]. Skip or override?" Wait for user decision.
   - Display the per-speaker filtered date counts so the user can see the impact before sending.
4. **Load sent log**: Read `{data_path}/invitations_sent.json`. If file doesn't exist, start with `{}`. The structure is: `{semester: {guest_email: {status, sent_at, reminded_at?}}}`
5. **Filter**: Skip speakers already in the log for this semester with status = "sent". Include speakers with status = "failed" (retry).
6. **Draft email** for the first speaker and show it for approval. Note: the date list is **per-speaker** (filtered by host availability), so different speakers may see different dates:

```
Subject: SeminarInvite — [Semester] Date Preferences
To: [guest_email]
CC: [host_email]

Dear [Guest Name],

We would be delighted to have you present your paper "[Paper Title]"
at the Atlanta Fed Research Seminar during [Semester].

The seminar takes place on Thursdays. The following dates are available:

  1. [Thursday, September 3, 2026]
  2. [Thursday, October 1, 2026]
  ...

Could you please reply with your top 3 preferred dates using the
numbers above? For example: "1st choice: 4, 2nd choice: 6, 3rd choice: 2"

Best regards,
Adrien and [Host First Name]
(Sent from personal email for scheduling logistics)
```

7. **STOP and ask**: "Send this invitation to N speakers? (dryrun: no emails will be sent)" or "Send this invitation to N speakers?"
8. After approval, for each speaker:
   - If **dryrun**: print `[DRYRUN] Would send to [guest_name] <[guest_email]> (CC: [host_email])`
   - Otherwise: call `send_gmail_message` with to, cc, subject, body
   - **Immediately** write the speaker to `invitations_sent.json` with status "sent" and timestamp
   - If send fails, record status "failed"
9. Report: "Sent N invitations (M skipped as already sent, K failed)."

## Subcommand: `collect`

### Steps

1. **Extract available dates** (shared step)
2. **Read speakers** from xlsx (shared step) — build set of known guest emails
3. **Search Gmail**: `subject:SeminarInvite` via `search_gmail_messages`
4. **Read messages**: Use `get_gmail_messages_content_batch` (max 25 per batch)
5. **Filter replies**:
   - Keep only messages where the sender (From:) matches a known guest email
   - Exclude the original outgoing invitations (sent by adrien.matray@gmail.com)
6. **Parse each reply** — read the reply text in context of the available dates list. For each reply, determine:

| Category | Signal | Cost mapping |
|----------|--------|-------------|
| **Ranked** | Numbers like "1st: 4, 2nd: 6, 3rd: 2" or "Oct 1, Sep 10, Nov 5" | rank 1 → cost 0, rank 2 → cost 1, ..., unranked → cost 100 |
| **Open** | "Any date works", "I'm flexible", "all good" | cost 1 for all available dates |
| **Exclusions** | "Not Sep 3", "anything except Oct", "I can't do December" | cost 100 for excluded, cost 1 for rest |
| **Unclear** | Ambiguous, partial, conditional, or off-topic reply | Flag for manual review — do NOT auto-parse |
| **Decline** | "I can't make it", "not this semester", "I'll pass" | Remove from pool |

7. **Display parsed preferences** as a table:

```
| # | Speaker          | Category | Rank 1     | Rank 2     | Rank 3     | Raw reply snippet |
|---|------------------|----------|------------|------------|------------|-------------------|
| 1 | Victoria Ivashina| Ranked   | Oct 1      | Sep 10     | Nov 5      | "1st: 3, 2nd: ..." |
| 2 | John Smith       | Open     | (all)      |            |            | "Any date works"  |
| 3 | Jane Doe         | Unclear  | —          | —          | —          | "Let me check..." |
```

8. **STOP and ask**: "Save these parsed preferences? (Unclear entries will be flagged for follow-up)"
9. After approval:
   - If **dryrun**: print `[DRYRUN] Would save preferences for N speakers`
   - Otherwise: save to `{data_path}/preferences.json` keyed by semester. Structure: `{semester: {guest_name: {category, rankings: {date: cost}, raw_reply, parsed_at}}}`
10. **Report**: "X/Y speakers have responded. Non-respondents: [list names]"

## Subcommand: `remind`

### Steps

1. **Read sent log** and **preferences** for the current semester
2. **Identify non-respondents**: speakers in sent log (status = "sent") but NOT in preferences
3. **Display list** and ask for approval
4. For each non-respondent:
   - If **dryrun**: print `[DRYRUN] Would remind [guest_name] <[guest_email]>`
   - Otherwise: send reminder email (reply-style subject `Re: SeminarInvite — [Semester] Date Preferences`):

```
Dear [Guest Name],

Just a gentle reminder — we are still finalizing the seminar schedule
for [Semester] and would love to have your date preferences.

Could you reply with your top 3 preferred dates from the list in the
original email?

Best regards,
Adrien and [Host First Name]
```

   - Log `reminded_at` timestamp in `invitations_sent.json`
5. Report: "Sent N reminders."

## Subcommand: `optimize`

### Steps

1. **Extract available dates** (shared step)
2. **Load preferences** from `{data_path}/preferences.json` for the current semester
3. If no preferences: "No preferences collected yet. Run `/seminar-schedule collect` first." Stop.
4. **Build cost dict** from preferences (already stored as `{date: cost}` per speaker)
5. **Run optimizer**: Execute `optimizer.py` via Bash:

```bash
python3 "{base_path}/Building_website/optimizer.py"
```

Or inline: read the optimizer module and call `optimize_assignment(preferences, available_dates)` via a python snippet.

6. **Display results**:

```
OPTIMAL ASSIGNMENT
==================================================
  Thursday, September 3, 2026     → Alice (choice #1)
  Thursday, October 1, 2026      → Bob (choice #2)
  Thursday, October 15, 2026     → Carol (choice #1)

UNFILLED DATES (5)
  Thursday, September 10, 2026
  ...

UNASSIGNED SPEAKERS (0)
```

7. **STOP and ask**: "Send confirmation emails to assigned speakers?"
8. After approval, for each assignment:
   - If **dryrun**: print `[DRYRUN] Would confirm [speaker] for [date]`
   - Otherwise: send confirmation email:

```
Subject: Re: SeminarInvite — [Semester] Date Preferences
To: [guest_email]
CC: [host_email]

Dear [Speaker Name],

Thank you for your date preferences. We are pleased to confirm your
seminar presentation on:

  [Assigned Date, e.g., Thursday, October 15, 2026]

[Host First Name] will be in touch with further details about
logistics and your paper.

Best regards,
Adrien and [Host First Name]
```

9. Report: "Sent N confirmation emails."
