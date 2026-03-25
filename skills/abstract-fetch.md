---
name: abstract-fetch
description: Fetch missing abstracts for BibTeX entries. Checks local Zotero database first, then falls back to CrossRef, Scopus, OpenAlex, Semantic Scholar, NBER direct lookup, and web search. Use when user wants to add abstracts to a .bib file, fetch missing abstracts, or enrich bibliography entries. Also triggers on "add abstracts", "get abstracts", "enrich bib", or similar.
argument-hint: "[path-to-bib-file]"
---

# Fetch Missing Abstracts

Fetch missing abstracts for BibTeX entries using local Zotero, CrossRef, Scopus, OpenAlex, Semantic Scholar, NBER direct lookup, and web search as fallbacks.

## Input

The user provides a path to a `.bib` file via `$ARGUMENTS`. If no path is given, search the current working directory for `.bib` files and ask which one to process.

## Workflow

### Phase 1: Parse and identify

Read the .bib file. For each entry, check if the `abstract` field is absent or empty. Report: "Found N entries, M missing abstracts." If none missing, say so and exit.

### Phase 2: Fetch abstracts

**Pre-check:** Test that `crossref_doi_lookup` MCP tool is available by calling it with a known DOI. If unavailable, warn the user that only Zotero lookup will be used.

For each entry missing an abstract, try these sources in order:

**1. Zotero (local, first)**

Query the local Zotero SQLite database. **Always use immutable URI mode** to avoid locking conflicts when Zotero is running:

```bash
sqlite3 "file:/Users/adrienmatray/Zotero/zotero.sqlite?mode=ro&immutable=1"
```

**Batch DOI lookup** — collect all DOIs from entries missing abstracts and query in a single call:

```sql
SELECT idv_doi.value AS doi, idv_abs.value AS abstract
FROM itemData id_abs
JOIN itemDataValues idv_abs ON id_abs.valueID = idv_abs.valueID
JOIN fields f_abs ON f_abs.fieldID = id_abs.fieldID
JOIN itemData id_doi ON id_doi.itemID = id_abs.itemID
JOIN itemDataValues idv_doi ON id_doi.valueID = idv_doi.valueID
JOIN fields f_doi ON f_doi.fieldID = id_doi.fieldID
WHERE f_abs.fieldName = 'abstractNote'
AND f_doi.fieldName = 'DOI'
AND idv_doi.value IN ('doi1', 'doi2', ...)
AND id_abs.itemID NOT IN (SELECT itemID FROM deletedItems);
```

For entries without a DOI, fall back to **title matching**. Normalize both BibTeX and Zotero titles: strip `{}` braces, lowercase, collapse whitespace. Use a `LIKE` query on the Zotero `title` field.

**2. CrossRef (online, fallback)**

If Zotero has no abstract and the entry has a DOI, call `crossref_doi_lookup` with the DOI. It returns abstracts for ~60% of entries. If the MCP tool is unavailable, use the REST API directly:

```bash
curl -s "https://api.crossref.org/works/{DOI}" -H "User-Agent: ClaudeBibCleaner/1.0 (mailto:adrien.matray@gmail.com)"
```

Extract the `abstract` field from `.message.abstract`.

**3. Scopus (online, Elsevier coverage)**

If CrossRef has no abstract and the entry has a DOI, try the Scopus Abstract Retrieval API. Elsevier journals often have abstracts here but not in CrossRef.

**API key resolution:** The `ELSEVIER_API_KEY` may be available as a shell environment variable OR stored in `~/.claude/settings.json` under `.mcpServers.bib-cleaner.env.ELSEVIER_API_KEY`. Check both locations. To read from settings.json:

```python
import json, os
api_key = os.environ.get('ELSEVIER_API_KEY')
if not api_key:
    try:
        with open(os.path.expanduser('~/.claude/settings.json')) as f:
            settings = json.load(f)
        api_key = settings.get('mcpServers', {}).get('bib-cleaner', {}).get('env', {}).get('ELSEVIER_API_KEY')
    except Exception:
        pass
```

If a key is found, call the Scopus Abstract Retrieval API:

```bash
curl -s "https://api.elsevier.com/content/abstract/doi/{DOI}?view=META_ABS" \
  -H "X-ELS-APIKey: $ELSEVIER_API_KEY" \
  -H "Accept: application/json"
```

Extract the abstract from `.abstracts-retrieval-response.coredata.dc:description`. If no API key is found from either source, skip this step silently.

**4. OpenAlex (online, third fallback)**

If CrossRef has no abstract, query OpenAlex. It stores abstracts as an inverted index with broad coverage.

**Budget awareness:** OpenAlex has a $1/day free credit per API key. Each call costs a fraction of a cent, but large files (200+ entries) can exhaust the daily budget. To maximize coverage:
- **Batch by DOI first** (cheapest calls): Query entries that have DOIs using the single-work endpoint.
- **Then title search** (more expensive): For entries without DOIs, use the search endpoint.
- **If you get a 402/429 response**, stop all OpenAlex calls immediately and move to the next source. Do NOT retry — the daily budget is exhausted.
- **When running in parallel** (multiple agents processing different .bib files), only ONE agent should use OpenAlex at a time. If you are a subagent running in parallel with others, prefer CrossRef and web search over OpenAlex to avoid burning the shared daily budget.

**DOI lookup:**
```bash
curl -s "https://api.openalex.org/works/doi:{DOI}?select=doi,abstract_inverted_index&mailto=adrien.matray@gmail.com"
```

**Title search (fallback for entries without DOI):**
```bash
curl -s "https://api.openalex.org/works?search={URL-encoded title}&select=doi,abstract_inverted_index&mailto=adrien.matray@gmail.com"
```

Reconstruct the abstract from the inverted index: keys are words, values are arrays of positions. Sort by position and join with spaces.

**5. Semantic Scholar (online, fourth fallback)**

If OpenAlex has no abstract, try Semantic Scholar:

```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:{DOI}?fields=abstract"
```

Extract the `abstract` field from the JSON response. Note: Semantic Scholar has rate limits (~100 requests/5 min without an API key), so batch requests with brief pauses if needed.

**6. NBER direct lookup**

For entries that look like NBER working papers — journal contains "NBER", institution contains "National Bureau of Economic Research", or note/series contains "NBER" — extract the NBER WP number and fetch the page directly. NBER pages are reliable, never blocked, and always contain the abstract.

**WP number extraction:** Look in `number`, `note`, `series` fields for patterns like `w12345`, `W12345`, `No. 12345`, or bare 4-5 digit numbers in NBER context. Then fetch:

```
WebFetch https://www.nber.org/papers/wXXXXX
```

Extract only the text from the clearly labeled abstract section on the NBER page.

**No WP number available:** Use WebSearch for `"{first author last name}" "{title keywords}" site:nber.org` to find the NBER page URL, then WebFetch it.

**Important:** This step should also be tried for ANY remaining entry without an abstract, not just those explicitly tagged as NBER — many published journal articles started as NBER working papers and have an NBER page with an abstract even though the bib entry doesn't mention NBER.

**7. Web search + WebFetch (last resort)**

For all entries still missing an abstract after steps 1–6, use WebSearch with `"{first author last name}" "{short title}" abstract` to find the paper on SSRN, author websites, RePEc, or other sources. Then use WebFetch on the top result to extract the abstract.

**SSRN workaround:** SSRN often blocks direct WebFetch with 403 errors. If the first result is SSRN and WebFetch fails, try the next search result or the author's personal website instead.

**Only use text explicitly labeled as an abstract or summary on the source page. Do NOT fabricate or paraphrase.**

**8.** If no source has an abstract, skip silently.

### Post-fetch cleaning

Apply to ALL fetched abstracts regardless of source:

- **Strip JATS/HTML tags:** CrossRef often returns `<jats:p>`, `<jats:italic>`, etc. Remove all XML/HTML tags (`<[^>]*>`) and collapse resulting whitespace.
- **Escape BibTeX special characters:** Replace `%` → `\%`, `&` → `\&`, `$` → `\$`, `_` → `\_`, `#` → `\#` to prevent LaTeX compilation errors. Do NOT escape characters that are already escaped (e.g., don't turn `\&` into `\\&`).

### Phase 3: Present results

Show a summary table:

```
| # | Key | Source | Abstract (first 80 chars...) |
|---|-----|--------|------------------------------|
| 1 | autor2013china | Zotero | We analyze the effect of rising... |
| 2 | valta2012competition | CrossRef | This paper examines how... |
```

Report: "Fetched M abstracts (K from Zotero, L from CrossRef, S from Scopus, J from OpenAlex, I from Semantic Scholar, N from NBER, W from web search). P entries still missing."

If nothing was fetched, say so and exit.

### Phase 4: Apply

**Wait for user confirmation.** They may accept all, skip specific entries, or modify.

Once confirmed:
1. Copy original to `<filename>.bak` as backup
2. Add `abstract` field as the **last field before the closing `}`** of each entry
3. Write the updated file
4. Report: "Added M abstracts to `<file>`. Backup at `<file>.bak`."

## Important

- **Never modify without showing the user first.** The summary table is mandatory.
- **Always use immutable URI mode** for Zotero queries — never open the DB in read-write mode.
- **Always clean abstracts** before insertion — strip tags, escape special characters.
- **Preserve existing formatting.** Match the indentation style of the existing .bib file when inserting the abstract field.

## Parallel execution notes

When this skill is invoked by multiple subagents processing different .bib files simultaneously:
- **OpenAlex** has a shared $1/day budget across all agents (same API key). Only the first agent should use OpenAlex aggressively; others should prefer CrossRef + web search to avoid exhausting the budget. If you receive a 402 or 429 from OpenAlex, stop and move on.
- **Semantic Scholar** has a 100 req/5 min rate limit. If you get a 429, skip Semantic Scholar entirely — do not retry.
- **CrossRef** is generous (50 req/sec with mailto header) and safe for parallel use.
- **Web search** (NBER, RePEc, journal sites) has no shared quota and is the best fallback when API budgets are exhausted.
