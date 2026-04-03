# /prompt output

## Phase 1: Formatted Prompt

**Depth:** Light (simple formatting/layout change, no analysis required)
**Role:** Omitted (trivial code-layout task)

```
Formatted prompt:

Task: In the Stata table-generating do-files, move the "second layer" metadata
(e.g., the exposure measure being used) from the bottom of the table header to
the second or third line at the top, directly below the table title. Follow the
same header ordering convention already used in [reference model table].

Constraints:
- Only reorder existing header elements; do not add or remove content.
- The exposure-level definition line should appear as line 2 or 3, immediately
  after the main title line.
- Keep all other header lines in their current relative order.

Output: Modified do-file(s) with the updated header ordering.
```

## Phase 2: Execution

Since no project files are available in this test run, here is what I would do:

1. **Locate the relevant do-files.** Search the project's `code/` directory for
   do-files that generate tables, looking for commands like `esttab`, `outreg2`,
   `estout`, or custom LaTeX table-writing code.

2. **Identify the "second layer" metadata.** In the table header block, find the
   line that defines the exposure measure (e.g., a `prehead()` or `posthead()`
   option in `esttab`, or a manually written LaTeX `\multicolumn` line describing
   the exposure variable).

3. **Move it up.** Relocate that line from its current position near the bottom
   of the header block to be the second or third line, right after the main table
   title. For example, in an `esttab` call, this would mean reordering elements
   within the `prehead()` option so the exposure definition appears early.

4. **Verify against the reference model.** Confirm the new ordering matches the
   convention in the reference table the user mentioned.

5. **Save and re-run.** Save the modified do-file, then execute it via
   `mcp__stata__run_do_file` to regenerate the table and confirm the layout is
   correct.

No files were modified (test run only).
