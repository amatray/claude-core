# Claude Context: Adrien Matray

## Who I Am
Research Economist and Associate Policy Advisor at the Federal Reserve Bank of Atlanta. CEPR affiliate. French native speaker. Research interests in applied macroeconomics and finance, focusing on misallocation, development, trade, and entrepreneurship.

- adrien.matray@atl.frb.org
- adrien.matray@gmail.com
- [Website](https://sites.google.com/view/adrienmatray/home)
- [Atlanta Fed page](https://www.atlantafed.org/research/economists/matray-adrien)
- Assistant: Shenelle Heard (shenelle.heard@atl.frb.org)

## My Primary Work
- Research papers in applied macro/finance
- Organizing seminars and conferences at the Atlanta Fed
- Data analysis and empirical work (Stata, R, Python)
- Writing and compiling LaTeX documents
- Managing email, calendar, and professional correspondence

## Tools and Software

| Tool | What I Use It For | Where Files Live |
|------|-------------------|------------------|
| Stata 18 | Primary analysis | Dropbox |
| LaTeX | Papers, slides, documents | Dropbox |
| R | Visualization, some analysis | Dropbox |
| Python | Scripting, automation | Dropbox |
| Google Workspace | Email, calendar, docs, sheets | Google (MCP connected) |
| Dropbox | All project files | ~/Library/CloudStorage/Dropbox-Matray/ |

## Where My Files Are Stored
- Main working directory: `~/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/`
- Seminars: `~/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/_FedStuff/Seminars/`
- Claude workflows: `~/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/_claude_workflows/`
- Sensitive/internal Fed data: Claude cannot access

## What I Need Help With
- Stata code: debugging, optimization, auditing
- LaTeX: writing, compiling, formatting
- Email management: inbox triage, drafting replies, seminar coordination
- Research workflows: paper auditing, data analysis
- Skill creation and improvement for Claude Code
- Scheduling and calendar queries

## My Skill Level
- Stata: Advanced
- LaTeX: Advanced
- Python: Intermediate
- R: Intermediate
- Git: Basic workflow
- Terminal/Claude Code: Very comfortable

## How I Prefer to Work
- **I use dictation (Wispr Flow)**. I am French, so my accent sometimes causes transcription errors — infer the intended word from context rather than taking misspellings literally.
- Be concise. No over-explanation, no unnecessary back-and-forth.
- Ask before modifying or deleting files.
- Don't add features or refactor beyond what was asked.
- Make atomic git commits as you go along.
- When creating or modifying skills, always use `/skill-creator`.
- **Run Stata via MCP.** Use the `mcp__stata__run_command` and `mcp__stata__run_do_file` tools to execute Stata code. Do not use the Bash tool with `stata-mp -b do`. Do not ask me to run code manually. Check the output for errors after execution.
- **Script-first workflow:** When I ask you to produce any output (graph, table, dataset), always write the generating code to a script file (`.do`, `.R`, `.py`) in the project's `code/` directory first, then execute that file. Never run analysis code interactively or inline without saving it. If no `code/` directory exists, ask me where to save the script. This ensures every result is traceable and reproducible across conversations.
- **Incremental execution:** When I ask for variations or tweaks to code, only rerun the specific part that changed. If intermediate data is already saved, load it and run from there. Never rerun an entire pipeline just to change a graph option or tweak one step.
- **No clutter in project root:** Never place `.log` files, temporary `.dta` files, or other intermediate output in the project root directory. Direct logs to `batch_logs/` or `logs/`, and temp data to `_data/` or `temp/`. Create the subfolder if it doesn't exist.

## Writing Style
- **NEVER use em dashes (---).** Use commas, parentheses, semicolons, or restructure the sentence instead. This is a hard rule with no exceptions. Parentheses are acceptable but should be kept to a minimum.

## Research Output Conventions
- **Wide tables:** When a LaTeX table risks overflowing margins (many columns, regression tables), wrap in `\resizebox{1\linewidth}{!}{ ... }`. Do not apply to narrow tables.
- For full LaTeX conventions: read `~/.claude/commands/prompt-references/latex-research.md`
- For Stata output conventions: read `~/.claude/commands/prompt-references/stata-research.md`

## Custom Skills Available
audit-code, audit-paper, checkin, compile-latex, done, goals-review, inbox, morning-brief, optimize-code, pdf-chunker, prompt, prompt-only, prompt-refine, reply, review-plan, schedule-query, seminar-extract, skill-creator, solving-model, todo-add, todo-queue, todo-review, triage-inbox, weekly-review

## Current Projects
| Project | Role | Current Phase |
|---------|------|---------------|
| Atlanta Fed Seminars | Organizer | Ongoing coordination |
| SITE Misallocation Session | Co-organizer (with M. Blank, P. Klenow, S. Moreira) | Stanford, Aug 31–Sep 1 2026 |
| Industrial Policies Conference | Co-organizer (with C. Xu, T. Schmidt-Eisenlohr) | Atlanta Fed, 2026 |
