# Weekly Project Review
*v1.2 — 3-marker system, batch updates, emoji placeholders*

Generate a comprehensive weekly summary for the current research project, pulling from multiple sources.

## Overview

This skill collects data from WhatsApp, meeting transcripts, and Gmail, then generates:
1. **Tab 1 content**: High-level project dashboard (updated directly in Google Doc)
2. **Tab 2 content**: Detailed weekly log with thematic synthesis across all sources

## Instructions

### Step 0a: Check Todo Queue (Before Project Work)

Before starting the project review, check for pending todo emails:

1. Search Gmail: `label:@ToSelf is:unread`
2. If emails found: "You have N email(s) in your todo queue. Run /todo-queue to convert them to reminders? [Y/n/skip]"
3. If user says Y: Run the `/todo-queue` workflow, then continue
4. If no emails found: Continue silently

> Requires `/todo-queue` skill. Skip this step if not installed.

### Step 0: Read Project Configuration
- Read `.claude/CLAUDE.md` from the current project folder
- Extract: project name, Google Doc ID, team roster, WhatsApp groups, folder paths
- Extract `project_type` (default: "quantitative"). Look for `project_type: qualitative` in the config.
- If config is missing required fields, inform user and stop

### Step 1: Determine Date Range
- Check `10_AI_Collaboration/Weekly_Reviews/` for most recent `weekly-review-*.md` file
- Use that date as start_date (or 7 days ago if none exists)
- end_date = today
- Tell user: "Generating weekly review for [start_date] to [end_date]"

### Step 1.5: Populate Transcripts (Optional)

If you use `granola-fetch` or another transcript tool:

1. Check the project's configured transcripts folder for existing files
2. Offer: "Fetch recent transcripts? [Y/n]"
3. If yes, run your transcript fetch tool with the date range
4. If no: Continue with existing local files

### Step 2: Collect Data (with graceful degradation)

**2a. WhatsApp Messages**
- For each group in `whatsapp_groups`:
  - Search for group using WhatsApp MCP (`list_chats`)
  - Fetch actual messages using `list_messages` — do NOT rely on metadata for last message dates
  - Filter to messages within date range
- If WhatsApp MCP unavailable: Note "WhatsApp unavailable - skipped" and continue
- Save raw messages to `10_AI_Collaboration/Weekly_Reviews/whatsapp-summary-[date].md`

**2b. Meeting Transcripts**
- Read all transcript files from the configured transcripts folder
- Support multiple formats: Granola JSON, manual markdown, Zoom .vtt files
- Parse meeting date, attendees, and content from each
- If no new transcripts: Note "No new transcripts this period"

**2c. Gmail Threads**
- **Date range**: Same as other sources
- **Filter criteria** (emails must match at least one):
  - Sender OR recipient matches any team member email in roster
  - Subject or body contains project keywords from config
- **Exclusions**: Automated emails, calendar invites, newsletters, bulk mail
- **Grouping**: Group by thread to preserve conversation context
- If Gmail MCP unavailable: Note "Gmail unavailable - skipped" and continue

**2d. Sensitive Content Filtering**

The weekly summary may be shared with the full team. Screen for and exclude:
- Critical performance comments, hiring/firing discussions, pay/compensation
- Personnel-specific funding decisions
- Anything inappropriate for full team viewing

When in doubt: Omit and note "[Some content omitted - PI review recommended]"

### Step 2e: Verify Key Metrics Against Authoritative Sources

Before generating content, verify all quantitative claims. Priority order:
1. Research Design and Progress document (if maintained)
2. Earlier weekly summaries
3. Current week's sources — flag if uncertain

### Step 2f: Read Previous Dashboard as Baseline

**The Project Status Dashboard is a LIVING DOCUMENT.**

1. Read the current dashboard content from the Google Doc (Tab 1)
2. This is your BASELINE - not a blank slate
3. PRESERVE previous content unless explicitly superseded or factually outdated
4. MODIFY existing sections with new information; ADD new items; REMOVE only when completed/superseded

### Step 3: Synthesize

**Detail and Length Requirements**: Scale to meeting length:
- Brief check-ins (under 20 min): 0.5-1 page
- Standard meetings (20-60 min): 1-3 pages
- Long strategy sessions (60+ min): 2-4 pages

**Guiding principle**: Include more detail when in doubt. A reader who wasn't at the meeting should understand WHAT was decided, WHY, WHO said it, and the context.

**FORMATTING RULES**:
- **NO MARKDOWN TABLES** — use bullet/sub-bullet format for ALL structured data
- Bold labels followed by content on same line or as sub-bullets
- **ALWAYS bold team member names** throughout both Tab 1 and Tab 2 (do NOT use `**` markdown markers in the text — track bold ranges separately and apply formatting via the Google Docs API)
- **Do NOT include** direct quotes. Paraphrase instead.
- **ASCII emoji placeholders**: Use `[RED]`, `[GREEN]`, `[YELLOW]` instead of real emoji in generated text. Real emoji are supplementary-plane Unicode that break Google Docs index calculations. They are swapped to real emoji via `find_and_replace_doc` after all content is written.

**Generate Tab 1 (Dashboard)**: Start from previous dashboard, update with this week's info. Structure:
- Project overview and status
- Strategic objectives and progress
- Operational objectives serving each strategic goal
- Team member to-do items
- Critical success factors with status (green/yellow/red)
- Funding pipeline

**Generate Tab 2 (Weekly Log)**: New entry prepended (reverse chronological). Structure:
- Date range header
- Weekly Activity Summary (thematic synthesis across all sources)
- Detailed Meeting Records (full summaries of each meeting)

### Step 4: Save Local Copies
- Save to `10_AI_Collaboration/Weekly_Reviews/weekly-review-[date].md`

### Step 5: Update Google Doc

**First-Time Setup**: Before first use, add these three marker lines to your Google Doc (Tab 1), each on its own line:

```
=== PROJECT STATUS DASHBOARD ===
[your dashboard content]
=== DASHBOARD END ===

=== WEEKLY SUMMARIES START ===
[weekly logs go here, newest on top]
```

**Precondition Check**: Before any writes, verify all 3 markers exist in the doc. If `DASHBOARD END` is missing, STOP and report — do not attempt to write.

**Why 3 markers**: The explicit `DASHBOARD END` marker prevents boundary corruption that occurred with the original 2-marker approach.

**6-Phase Protocol**:
1. **Preparation** — Generate text with `[RED]`/`[GREEN]`/`[YELLOW]` ASCII placeholders; strip `**` markdown bold markers (bold is applied via API, not text)
2. **Dashboard Replacement** — Delete content between `DASHBOARD` and `DASHBOARD END` markers, then insert new dashboard text (atomic batch operation)
3. **Verification** — Confirm all 3 markers are intact after the dashboard write
4. **Weekly Log Prepend** — Insert new entry at `WEEKLY SUMMARIES START` marker (newest on top)
5. **Emoji Swap** — Use `find_and_replace_doc` to replace `[RED]` with real red circle, `[GREEN]` with green circle, `[YELLOW]` with yellow circle
6. **Formatting** — Apply heading sizes and team name bolding using API-reported indices (from `inspect_doc_structure`), not calculated offsets

**Batch operations**: Use `batch_update_doc` to combine delete + insert + format operations into a single call — this reduces 19-29 sequential API calls to 1-3.

### Step 6: Final Confirmation
1. Confirm: "Weekly review complete. Google Doc updated."
2. Provide link: "Check Google Doc: [link]"
3. Note any issues or manual fixes needed

### Step 7: Archive Processed Transcripts (Optional)

1. Create archive folder if needed: `[project]/10_AI_Collaboration/Transcripts/archive/`
2. Move processed transcript files to archive
3. Confirm: "Archived X transcript(s)"

## Arguments

`$ARGUMENTS` can include:
- `nosave` — Don't save intermediate files (WhatsApp summaries, local weekly review copy)
- `tab1only` — Only generate Tab 1 dashboard
- `tab2only` — Only generate Tab 2 detailed log
- `days:N` — Override date range to last N days
- `since:YYYY-MM-DD` — Override start date
- `skipwhatsapp` — Skip WhatsApp even if available
- `skipemail` — Skip email even if configured
- `skiparchive` — Don't archive transcripts after processing

## Examples

```
/weekly-review                    # Full review, default date range
/weekly-review days:14            # Last 14 days
/weekly-review tab1only           # Quick dashboard update
/weekly-review skipwhatsapp       # Skip WhatsApp if it's being flaky
```

## Error Handling

- If project config missing: "No .claude/CLAUDE.md found. Please run from a configured project folder."
- If WhatsApp unavailable: Continue with other sources, note in output
- If no transcripts folder: Create it, note "No transcripts folder found - created"
- If Google Doc update fails: Save content locally, provide manual instructions
- Flag any ambiguities: "Unclear who said X - please clarify"
