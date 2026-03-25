---
name: clean-bib
description: Clean and update BibTeX bibliography files. Removes duplicate entries (matching on normalized author+title, keeping latest year), normalizes journal names (strips leading "The"), and checks whether working papers, techreports, or forthcoming entries have since been published — upgrading them with journal, volume, pages, year, and DOI. Use this skill whenever the user wants to clean a .bib file, deduplicate references, normalize journal names, update publication status, check for outdated working paper entries, or tidy up a bibliography. Also triggers on "bib cleanup", "update references", "check if working papers published", "deduplicate bib", or similar.
argument-hint: "[path-to-bib-file]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "mcp__bib-cleaner__crossref_fuzzy_match", "mcp__bib-cleaner__crossref_doi_lookup", "mcp__bib-cleaner__openalex_search", "mcp__bib-cleaner__resolve_bibtex", "mcp__bib-cleaner__repec_ideas_search", "mcp__bib-cleaner__scopus_search"]
---

# Clean BibTeX

Clean and update a BibTeX bibliography file: deduplicate entries and upgrade working papers that have since been published.

## Input

The user provides a path to a `.bib` file via `$ARGUMENTS`. If no path is given, search the current working directory for `.bib` files and ask which one to clean.

## Workflow

### Phase 1: Parse and analyze

Read the .bib file. For each entry, extract:
- BibTeX key, entry type, title, authors, year, journal, DOI
- Normalize title: lowercase, strip `{}`, collapse whitespace
- Normalize authors: lowercase, extract last names

**Identify duplicates:** Group entries by (normalized first-author-last-name, normalized title). Within each group, if years differ, mark older entries for removal. If years match, keep the entry with more complete metadata.

**Identify upgrade candidates:**
- Type is `@unpublished`, `@techreport`, or `@misc`
- Any field contains "forthcoming", "accepted", "in press", or "working paper"
- Type is `@article` but missing volume/pages and year is 2+ years old
- Note/series contains "NBER Working Paper", "CEPR Discussion Paper", or similar

**Normalize journal names:** For every entry with a `journal` field, if the value starts with "The " (case-insensitive), strip the leading "The ". This is applied automatically — no per-entry confirmation needed.

### Phase 2: Look up publication status

For each upgrade candidate, look up the published version using the bib-cleaner MCP tools:

1. **CrossRef fuzzy match** (primary): Call `crossref_fuzzy_match` with `"author_lastname title_keywords"`.
   - Score > 80 → high confidence, accept
   - Score 50–80 → cross-check with `openalex_search`, flag for review
   - Score < 50 → try `openalex_search` as fallback

2. **OpenAlex search** (secondary): Call `openalex_search` with the title. Check if it returns a DOI and a journal name.

3. **Scopus search** (tertiary): Call `scopus_search` with the title and first author last name. Especially valuable for Elsevier-published journals (JFE, JDE, JIE, etc.) where CrossRef/OpenAlex may have incomplete metadata. Use when steps 1–2 don't resolve the entry.
   - Score > 80 → accept the match
   - Score 50–80 → flag for user review
   - Score < 50 → skip

4. **RePEC/IDEAS** (economics working papers): Call `repec_ideas_search` if the entry looks like an economics working paper. This is especially good at linking NBER/CEPR WPs to their published versions.

5. **Get clean metadata**: Once a DOI is confirmed, call `crossref_doi_lookup` to get the canonical journal, volume, pages, year.

**Rate limiting:** CrossRef and OpenAlex handle 50+ requests/second. Scopus has a 20,000 request/week quota — sufficient for typical .bib files but avoid unnecessary calls (only query Scopus when steps 1–2 fail).

### Phase 3: Present changes

Show a summary with the following sections:

**Journal names cleaned** (informational — these are auto-applied):
```
| # | Key | Old journal | New journal |
|---|-----|------------|------------|
| 1 | grossman1991quality | The Review of Economic Studies | Review of Economic Studies |
```

**Duplicates to remove:**
```
| # | Key (removed) | Key (kept) | Title (truncated) | Reason |
|---|--------------|-----------|-------------------|--------|
| 1 | Smith2019    | Smith2021 | The Effect of...  | Same paper, newer year |
```

**Entries to upgrade:**
```
| # | Key | Old type | New type | Old venue | New venue | New year | DOI |
|---|-----|----------|----------|-----------|-----------|----------|-----|
| 1 | Jones2020wp | @techreport | @article | NBER WP 28000 | AER | 2022 | 10.1257/... |
```

Also report:
- Total entries / duplicates found / upgrade candidates checked / upgrades found / unchanged

If nothing to change, say so and exit.

### Phase 4: Apply changes

**Wait for user confirmation.** They may accept all, skip specific changes, or modify.

Once confirmed:
1. Copy original to `<filename>.bak` as backup
2. Remove duplicate entries
3. For upgraded entries: update the entry type and fields **in place** (preserve the original BibTeX key to avoid breaking `\cite{}` references)
4. Write the cleaned file
5. Report: "Cleaned `<file>`: removed N duplicates, upgraded M entries, cleaned J journal names. Backup at `<file>.bak`."

## Important

- **Never delete without showing the user first.** The summary table is mandatory.
- **Preserve BibTeX keys.** Even if the year changes, keep the original key (e.g., `Jones2020wp` stays `Jones2020wp`).
- **Be conservative with matching.** Only flag duplicates if normalized title AND at least one author last name match. Partial matches are not enough.
- **Flag ambiguous upgrades.** If CrossRef returns multiple plausible matches, show them to the user rather than auto-selecting.
- **Handle encoding.** BibTeX files may contain `{\"o}`, `\'{e}`, etc. Normalize for comparison but preserve original encoding in output.
