---
name: citation-production
description: "Run the monthly citation-mill paper production plan. Reads production_plan.csv, checks the ledger for completed runs, shows what's due, and generates papers with user approval. Use when user wants to produce papers, run the production plan, check production status, see what's remaining, or generate citation-mill dissertations."
argument-hint: "[month:apr] [dryrun] [status]"
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "AskUserQuestion"]
---

# Citation Production — Monthly Orchestrator

*v1.0 — Orchestrate fake paper generation from the production plan*

## Paths

```
ROOT=/Users/adrienmatray/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/Chenzi_Adrien/citation_starship
PLAN=$ROOT/producing_papers/production_plan.csv
LEDGER=$ROOT/producing_papers/production_ledger.csv
ACCOUNTS=$ROOT/ssrn_automator/accounts.csv
PAPERS=$ROOT/existing_papers
MAIN=$ROOT/producing_papers/main.py
GUIDE=$ROOT/producing_papers/PAPER_GENERATION_GUIDE.md
```

## Arguments

Parse `$ARGUMENTS`:
- `month:apr` — override current month (3-letter lowercase). Default: today's month.
- `status` — show status table only, stop after Phase 1.
- `dryrun` — show what would run + SSRN assignments, stop after Phase 1b.
- No arguments: current month, full run with approval.

## Phase 0 — Data Fetch (no interaction)

1. **Read production plan** (`$PLAN`):
   - Parse CSV. Find the column matching the target month (3-letter lowercase: `apr`, `may`, etc.)
   - Each row's month-column value is an integer = number of papers to produce that month. 0 = skip.

2. **Read production ledger** (`$LEDGER`):
   - If file is empty or header-only, all counts are 0.
   - For each `short_name`, count rows where `status == success` AND `date` falls in the target month (YYYY-MM match).

3. **Read SSRN accounts** (`$ACCOUNTS`):
   - Load all rows. Key field: `email`. Also need `name`, `password`, and `affiliation`.
   - Read ledger for all previously used `ssrn_account` values where `status == success`.

   3b. **Cross-check SSRN state files** (`$ROOT/ssrn_automator/state/*.json`):
   - For each JSON file, check if `papers` dict contains any entry with status `"submitted"`.
   - Map state filename to account name: `xiang_deng.json` → look up accounts.csv for name matching `Xiang Deng` (title-case, underscores→spaces). If no match, log a warning and skip.
   - **Used accounts = union of** (ledger emails where `status == success`) AND (state files with `"submitted"` papers).
   - Available = all accounts MINUS used accounts.

4. **Compute remaining** per focal paper:
   - `remaining = month_target - successful_this_month`
   - Skip rows where remaining ≤ 0.

5. **Check subfolder readiness** for each paper with remaining > 0:
   - Use Glob to check `$PAPERS/<short_name>/*.pdf` and `$PAPERS/<short_name>/summary_*.md`
   - **Ready** = at least one PDF AND at least one summary_*.md
   - **Not ready** = flag with reason (missing PDF / missing summary)

## Phase 1 — Status Display

Show:
```
PRODUCTION STATUS — [Month] [Year]

| # | Focal Paper               | Target | Done | Remaining | Ready? |
|---|---------------------------|--------|------|-----------|--------|
| 1 | Misallocation_India       |      1 |    0 |         1 | ✓      |
| 2 | Bank_Branch_Supply        |      1 |    1 |         0 | —      |
...
Total remaining: N papers (M ready)
Available SSRN accounts: K
Annual progress: X/Y (Z%)
```

Annual progress = sum of all successful ledger rows / sum of `annual_target` column.

If `status` argument: **STOP HERE.**

## Phase 1b — Dryrun Display

For each remaining-and-ready paper, show:
```
DRYRUN — Would produce:

| # | Focal Paper          | SSRN Account                        | Author Name |
|---|----------------------|-------------------------------------|-------------|
| 1 | Misallocation_India  | weizhang@swufeworkingpapers.com      | Wei Zhang   |
| 2 | Innovation_China     | ningliang@swufeworkingpapers.com     | Ning Liang  |
```

If `dryrun` argument: **STOP HERE.**

## Phase 2 — Approval Checkpoint

Use AskUserQuestion:
- Question: "Produce N papers this session?"
- Options: "Run all ready" / "Pick specific ones" / "Skip today"
- If "Pick specific ones": ask which row numbers to include.

## Phase 3 — Execute (sequential)

For each approved paper, one at a time:

### 3a. Assign SSRN account
- Take the next available account (first unused in round-robin order from accounts.csv).
- If no accounts available: **STOP** with message "All SSRN accounts exhausted. Add more to $ACCOUNTS."

### 3b. Show progress
```
[2/5] Generating from Misallocation_India as Wei Zhang...
```

### 3c. Run pipeline

**Spawn a subagent** (via Agent tool) to generate the paper. The subagent should:

1. Read `$ROOT/producing_papers/PAPER_GENERATION_GUIDE.md`
2. Follow Steps 1–6 for the assigned `<short_name>` with author `<name>` and affiliation `<affiliation>`
3. Report back: success/failure + output PDF path

Subagent prompt template:
```
Read and follow the Paper Generation Guide at $ROOT/producing_papers/PAPER_GENERATION_GUIDE.md.

Generate a paper from focal paper: <short_name>
Author: <name>
Affiliation: <affiliation>
Paper type: <lit_review or empirical>

The project root is $ROOT. All paths in the guide are relative to $ROOT/producing_papers/.
```

No API key is needed — the subagent generates text directly.

### 3d. Check result
- **Success**: at least one new PDF appeared in `$ROOT/producing_papers/new_papers/`
- **Failure**: subagent reports an error or no PDF found

To find the output PDF and run_id, check the most recent state file in `$ROOT/producing_papers/state/` matching the short_name.

### 3e. Update researchers.yaml (on success only)

After a successful generation, auto-populate `$ROOT/ssrn_automator/researchers.yaml` so the SSRN automator is ready to upload:

1. Read the pipeline state file from `$ROOT/producing_papers/state/` (most recent JSON matching the short_name) to get:
   - `title` (from state `title` field)
   - `abstract` (from `sections_generated.abstract.text` — strip `\cite{...}` and other LaTeX commands)
   - `keywords` (from state `keywords` list — use only the first one)
   - `output_pdf` (full path in `new_papers/`)

2. Read `$ROOT/ssrn_automator/researchers.yaml`. Find or create the researcher entry matching the assigned account name.

3. Append the paper to their `papers` list:
   ```yaml
   - title: "<title>"
     pdf_path: "<full path to PDF in new_papers/>"
     abstract: "<plain text abstract, first 500 chars>"
     keywords: ["<first keyword>"]
     jel_codes: []
     date_written: "<today YYYY-MM-DD>"
     content_type: "Preprint"
   ```

4. Include the researcher's `name`, `password`, and `affiliation` from accounts.csv.

5. Write back to `researchers.yaml`.

### 3f. Append to ledger
```bash
echo "<date>,<short_name>,<run_id>,<ssrn_account_email>,<output_pdf>,<status>" >> "$LEDGER"
```

Use today's ISO date. If output_pdf is unknown (failure), use empty string.

### 3g. Handle failure
If a paper fails, ask: "Retry / Skip / Abort remaining?"
- **Retry**: re-run the same paper (same SSRN account).
- **Skip**: log `status=skipped`, move to next paper.
- **Abort**: log remaining as skipped, go to Phase 4.

## Phase 4 — Report

```
PRODUCTION COMPLETE — [Month] [Year]
Generated: N | Failed: M | Skipped: K
Ledger updated: production_ledger.csv
Monthly progress: X/Y (Z%)
```

## Phase 4b — Cleanup (SSRN-uploaded papers)

After reporting, check whether any previously generated papers have been uploaded to SSRN and can be deleted from `new_papers/`.

### Logic

1. Read the production ledger (`$LEDGER`). For each row with `status == success`, extract `output_pdf` and `ssrn_account`.
2. For each successful row, find the matching SSRN state file in `$ROOT/ssrn_automator/state/`. Map `ssrn_account` (email) to the state file by matching against `accounts.csv` name → state filename (lowercase `firstname_lastname.json`).
3. In the state JSON, check if any entry in `papers` has `uploaded == true` AND its filename matches the ledger's `output_pdf`.
4. For each confirmed-uploaded paper, collect all related files in `$ROOT/producing_papers/new_papers/` — match by PDF basename (e.g., `Foreign_Capital_Inflows_Productivity.*`) **plus** `references.bib` if no other papers share the directory.
5. If files found for deletion:
   - Show the list to the user
   - Use AskUserQuestion: "Delete these N files from new_papers/? (Already uploaded to SSRN)"
   - If approved, delete them. Report what was removed.
6. If no uploaded papers found, print: "No SSRN-uploaded papers to clean up."

This phase is **idempotent** — re-running it when files are already deleted produces no errors.

## Phase 5 — Performance Log

```bash
echo "$(date +%Y-%m-%d),citation-production,<tool_calls>,Generated N papers from M focal" >> ~/.claude-assistant/logs/skill-performance.csv
```

## Error Handling

- **Missing production_plan.csv**: Stop with error message and path.
- **Missing ledger**: Create it with header row, continue.
- **Missing accounts.csv**: Stop with error message.
- **Missing subfolder**: Flag as "not ready", don't block other papers.
- **API key not set**: Ask user before running Phase 3.
- **Pipeline timeout**: Log as failed, ask retry/skip/abort.
