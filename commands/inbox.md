Show my recent Gmail inbox messages in a table. Also supports trashing emails by row number.

## Instructions

1. Parse `$ARGUMENTS`:
   - If empty: query = `in:inbox`, page_size = 15
   - If `unread`: query = `in:inbox is:unread`, page_size = 15
   - If numeric (e.g., `20`): use as page_size, query = `in:inbox`
   - If text (e.g., `from:julia`): use as query (prepend `in:inbox` if no folder specified)
   - If mixed (e.g., `from:julia 20`): extract the number as page_size, rest as query
   - If starts with `drop`: → go to **Drop Mode** below

2. Call `mcp__google_workspace__search_gmail_messages` with:
   - query: the resolved query
   - user_google_email: adrien.matray@gmail.com
   - page_size: the resolved count

3. Call `mcp__google_workspace__get_gmail_messages_content_batch` with the returned message IDs (format: `metadata` to keep it fast). Extract From, Subject, and Date from each message.

4. Display results as a numbered table:

| # | From | Subject | Date | ID |
|---|------|---------|------|----|
| 1 | Julia Cage | Re: Tariff data | Mar 5 | `18e4a2b3c` |
| 2 | ... | ... | ... | `...` |

Show the Message ID in backticks (monospace) — the user needs it for `/reply`.

5. If results are empty, say "No messages found" (or "No messages matching [query]").

---

## Drop Mode

Usage: `/inbox drop 1 3 5` — trashes emails #1, #3, #5 from the most recent `/inbox` table.

1. Parse the numbers after `drop` (e.g., `1 3 5`).
2. Scan the conversation for the most recent `/inbox` table output. Map each row number (#) to its Message ID. If no prior `/inbox` table is found in the conversation, run a fresh inbox search first, show the table, and ask which messages to trash.
3. Show the emails to be trashed:
   - **#1** — From: [sender] | Subject: [subject]
   - **#3** — From: [sender] | Subject: [subject]
   Ask: "Trash these N emails?"
4. After user confirms, for each message call `mcp__google_workspace__modify_gmail_message_labels` with:
   - message_id: [the resolved ID]
   - user_google_email: adrien.matray@gmail.com
   - add_label_ids: ["TRASH"]
5. Confirm: "Trashed N emails."
