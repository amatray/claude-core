Extract seminar speaker suggestions from Gmail emails labeled "SeminarFED" and save to xlsx.

## Instructions

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

4. Call `mcp__google_workspace__get_gmail_messages_content_batch` with the returned message IDs (max 25 per batch — paginate if needed):
   - user_google_email: adrien.matray@gmail.com
   - format: full

5. **Dedup check**: Read the existing xlsx file at the path below using python/openpyxl. Collect all Message IDs from column D (starting row 2). Skip any emails whose message ID is already in the xlsx. If the file doesn't exist or is empty, process all emails.

6. **Extract fields** from each new email:
   - **Name Host**: The person who sent the email. Parse the display name from the `From:` header (e.g., "John Smith <john@frb.gov>" → "John Smith"). If no display name, use the email address.
   - **Guest**: The person being recommended as a seminar speaker. Look in the email body for:
     - Names following phrases like "I suggest", "I recommend", "we should invite", "how about", "I'd like to propose", "consider inviting"
     - Names followed by institutional affiliations (e.g., "Jane Doe from MIT")
     - Names in the subject line if the body is unclear
   - **Paper Suggested**: The paper title, topic description, or URL mentioned in the email. If multiple papers are mentioned, list them semicolon-separated. If none found, use "Not specified".
   - If any extraction is ambiguous or uncertain, prefix with "[?]"

7. Display results as a numbered table:

| # | Name Host | Guest | Paper Suggested |
|---|-----------|-------|-----------------|
| 1 | John Smith | Jane Doe | "Trade Shocks and Labor Markets" |
| 2 | ... | ... | ... |

8. **Write to xlsx**: Run a python script (via Bash) to append the new rows. The script should:
   - Check that openpyxl is available (if not, install it with `pip3 install openpyxl`)
   - Create the file with headers if it doesn't exist
   - Append new rows with columns: Name Host | Guest | Paper Suggested | Message ID
   - Do NOT overwrite existing rows

   Output file path:
   `/Users/adrienmatray/Library/CloudStorage/Dropbox-Matray/_AdrienTeam/_FedStuff/Seminars/2026_2027/suggested_names.xlsx`

9. Report: "Done. Added N new suggestions to suggested_names.xlsx (M already existed, skipped)."
