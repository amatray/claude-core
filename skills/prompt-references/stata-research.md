# Stata Research Output Conventions

*Consult this file when writing Stata code that produces graphs or LaTeX tables.*

---

## Graphs
- Always include `$all_white` early in every plot-producing command (graph bar, graph twoway, etc.)
- Note: `$all_white` must be defined in the project's program file (e.g., `00a_own_programs.do`). If the project doesn't define it, skip this rule.

## esttab → LaTeX
- When a table will be wide (many columns), use `prehead(\resizebox{1\linewidth}{!}{)` and `postfoot(})` in the esttab command to embed the resizebox wrapper in the generated .tex output.
- For narrow tables, omit the resizebox prehead/postfoot.

## Running Stata
- Use the Stata MCP tools (`mcp__stata__run_command`, `mcp__stata__run_do_file`) to execute Stata code. Do not use the Bash tool with `stata -e` or `stata-mp -b do`.
- Never save temporary `.do` files in the project root; always save in `code/`.
- **Never place `.log` files in the project root.** Direct all Stata log output (`log using`) to a `batch_logs/` or `logs/` subfolder. If the subfolder doesn't exist, create it before running. Same applies to temporary `.dta` files: use `_data/` or `temp/`, not the root.

## Script-First Workflow
- When asked to produce any Stata output, always write the code to a `.do` file in the project's `code/` directory before executing it.
- Never run Stata commands interactively without first saving them to a do-file.
- Do-files should be self-contained by default (set globals, load data, produce output). Use a runner pattern only when one already exists in the project.
- Name do-files to match the output they produce (e.g., `reply_R2_aggregate_exports.do` → `reply_R2_aggregate_exports.pdf`).
- If no `code/` directory exists, ask the user where to save the script.

## Referee Reply Workflow
- **Code reuse:** Before writing new analysis code for a referee reply, search ALL existing reply files for similar analyses:
  - `code/reply_*.do`
  - `_revision/replies/reply_*.do`
  If a similar analysis exists, reuse or adapt it. Reference the source in a comment (e.g., `* Adapted from reply_R2.do, line 370`).
- **Results reuse:** Before running Stata for an analysis, check whether the expected output files already exist in `results/`. If found, inform the user and ask whether to regenerate or reuse.
