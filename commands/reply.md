Reply to a Gmail message. Draft in chat for approval before sending.

## Instructions

### Step 1: Identify the message

Parse `$ARGUMENTS`:
- **If a Message ID is provided** (e.g., from `/inbox` output): use it directly
- **If a search description is provided** (e.g., "Julia's email about tariffs"): search Gmail with `mcp__google_workspace__search_gmail_messages`, show the top result, and ask "Is this the right email?" before proceeding
- **If a number is provided** (e.g., `3`): tell the user to provide the Message ID from the `/inbox` table, or describe the email

### Step 2: Show the email

Call `mcp__google_workspace__get_gmail_message_content` with the message_id. Display:
- **From:** [sender]
- **Date:** [date]
- **Subject:** [subject]
- **Body:** [full text]

Note the **Message-ID** header, **thread_id**, and any existing **References** header — you'll need these for Step 4.

### Step 3: Draft the reply

Ask: "What would you like to say?"

The user will dictate or type their reply. Format it into a clean, concise email reply (no quoted text from the original unless the user asks). Show the draft:

> **To:** [sender]
> **Subject:** Re: [subject]
>
> [Draft body]

Ask: "Send this reply?"

### Step 4: Send (only after approval)

Call `mcp__google_workspace__send_gmail_message` with:
- to: [original sender's email]
- subject: Re: [original subject] (keep existing Re: if already present)
- body: [approved draft]
- user_google_email: adrien.matray@gmail.com
- from_name: Adrien Matray
- thread_id: [from Step 2]
- in_reply_to: [Message-ID header from Step 2]
- references: [existing References + Message-ID from Step 2]

Confirm: "Reply sent."
