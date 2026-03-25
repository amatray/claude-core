---
name: seminar-extract
description: Extract seminar speaker suggestions from Gmail emails labeled "SeminarFED", verify papers, find emails, and save to xlsx
argument-hint: "[days:N] [limit:N]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "WebSearch", "WebFetch", "mcp__google_workspace__search_gmail_messages", "mcp__google_workspace__get_gmail_messages_content_batch", "mcp__google_workspace__get_gmail_thread_content", "mcp__google_workspace__get_gmail_threads_content_batch"]
---

Extract seminar speaker suggestions from Gmail emails labeled "SeminarFED" and save to xlsx.

## Instructions

### Phase 1 — Search & Read

1. Parse `$ARGUMENTS`:
   - If empty: query = `label:SeminarFED`, limit = 50
   - If `days:N` (e.g., `days:30`): append `after:YYYY/MM/DD` (computed as today minus N days) to the query
   - If `limit:N` (e.g., `limit:20`): use as page_size
   - Arguments can be combined: `days:60 limit:100`

2. Call `mcp__google_workspace__search_gmail_messages` with:
   - query: the resolved query
   - user_google_email: adrien.matray@gmail.com
   - page_size: the resolved limit

3. If 0 results: say "No emails found with label SeminarFED." and stop.

4. **Expand to full threads**: Gmail labels often only apply to the initially labeled message, not to later replies in the same thread. To catch all replies:
   - Collect the unique **Thread IDs** from the search results (step 2 returns both Message IDs and Thread IDs)
   - For each unique Thread ID, call `mcp__google_workspace__get_gmail_thread_content` (or use `get_gmail_threads_content_batch` for multiple threads)
   - This returns ALL messages in each thread, including unlabeled replies from colleagues
   - Use the full set of thread messages for extraction, not just the labeled ones

5. Filter out messages sent by `adrien.matray@gmail.com` (these are outgoing solicitations/replies, not suggestions). Keep only messages from other senders that contain speaker suggestions.

### Phase 2 — Dedup & Extract

6. **Dedup check**: Read the existing xlsx file using python/openpyxl. Find the column with header "Message ID" (regardless of position). Collect all Message IDs from that column (starting row 2). Categorize each existing entry:
   - **Fully processed** = has Guest Email, Paper Status, AND Host Email all filled → skip entirely
   - **Needs enrichment** = Message ID exists but Guest Email, Paper Status, or Host Email is empty/missing → include in enrichment (use existing fields from the xlsx row; fill Host Email from the email's `From:` header)
   - **New** = Message ID not in xlsx → process normally
   If the file doesn't exist or is empty, process all emails.

7. **Extract fields** from each new email:
   - **Name Host**: The person who sent the email. Parse the display name from the `From:` header (e.g., "John Smith <john@frb.gov>" → "John Smith"). If no display name, use the email address.
   - **Host Email**: The email address from the `From:` header (e.g., "John Smith <john@frb.gov>" → "john@frb.gov").
   - **Guest**: The person being recommended as a seminar speaker. Look in the email body for:
     - Names following phrases like "I suggest", "I recommend", "we should invite", "how about", "I'd like to propose", "consider inviting"
     - Names followed by institutional affiliations (e.g., "Jane Doe from MIT")
     - Names in the subject line if the body is unclear
   - **Paper Suggested**: The paper title, topic description, or URL mentioned in the email. If multiple papers are mentioned, list them semicolon-separated. If none found, use "Not specified".
   - If any extraction is ambiguous or uncertain, prefix with "[?]"

8. If no new suggestions AND no entries needing enrichment, report "No new suggestions." and stop.

### Phase 3 — Verify & Enrich

For each extracted suggestion, run two lookups:

9. **Find Guest Email** (two-step pipeline):
   a. `WebSearch` for `"[Guest Name]" faculty page [affiliation if known]`
   b. From search results, identify the most likely faculty/personal page URL
   c. `WebFetch` on that URL with prompt: "Find the email address for [Guest Name] on this page"
   d. If not found, try one more query: `"[Guest Name]" email [university/institution]`
   e. Max 2 attempts. If still not found, set to "Not found"

10. **Verify Paper**:
   a. If Paper Suggested is "Not specified" → set Paper Status to "N/A", skip search
   b. Otherwise, `WebSearch` for `"[Paper Title]" [Guest Name]`
   c. Classification:
      - **"Verified"** = search result with closely matching title on Scholar, SSRN, NBER, or journal site
      - **"Partial match"** = similar but not exact title match
      - **"Not found"** = no plausible match after 2 search attempts
   d. Max 2 attempts. If tool errors or times out, set to "Not found" and continue.

### Phase 4 — Review

11. Display the enriched table (hide Message ID):

| # | Name Host | Host Email | Guest | Paper Suggested | Guest Email | Paper Status |
|---|-----------|------------|-------|-----------------|-------------|--------------|
| 1 | John Smith | john@frb.gov | Jane Doe | "Trade Shocks..." | jane.doe@mit.edu | Verified |

12. **STOP and ask**: "Does this look correct? Type 'yes' to save, or tell me what to change."

### Phase 5 — Write

13. After user confirms, run a python script (via Bash) to write:
   - Check that openpyxl is available (if not, install it with `pip3 install openpyxl`)
   - **Migration**: If file exists and has fewer columns than expected (check header count):
     a. Save backup as `suggested_names_backup.xlsx`
     b. Add any missing columns (Host Email, Guest Email, Paper Status) in the correct positions
     c. Ensure final column order matches: Name Host | Host Email | Guest | Paper Suggested | Guest Email | Paper Status | Message ID
     d. Set missing fields to "" for existing rows
   - Create the file with headers if it doesn't exist
   - Columns: **Name Host | Host Email | Guest | Paper Suggested | Guest Email | Paper Status | Message ID**
   - Append new rows only — do NOT overwrite existing rows

   Output file path:
   `/Users/adrienmatray/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/_FedStuff/Seminars/2026_2027/suggested_names.xlsx`

14. Report: "Done. Added N new suggestions to suggested_names.xlsx (M already existed, skipped)."
