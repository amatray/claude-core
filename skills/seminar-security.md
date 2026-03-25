---
description: Generate the confirmed guest list for the next Atlanta Fed seminar (for security clearance)
---

# /seminar-security — External Guest List for Fed Security

Read the "Signups" tab of the Atlanta Seminar – External Signup spreadsheet (ID: `12_jWUTP_9gRG-CDgfFFfVgXIYdmSn3c9957TnhtoSps`) and the "Schedule" tab.

## Steps

1. Read the **Schedule** tab to find the next upcoming Thursday seminar (date ≥ today).
2. Read the **Signups** tab and filter to rows where:
   - `date` matches that Thursday
   - `status` = `confirmed`
3. Check the signup deadline for that session. If the deadline has not passed yet, warn: "Signup deadline has not passed yet — list may change."
4. Output a clean table:

```
GUEST LIST — Atlanta Fed Research Seminar
Date: [date]
Speaker: [speaker] ([affiliation])

| # | Name | Email |
|---|------|-------|
| 1 | ...  | ...   |
```

5. Also output the list as a plain comma-separated format (for easy pasting into security forms):
```
Name1, email1@univ.edu
Name2, email2@univ.edu
```

Use `adrien.matray@gmail.com` as the Google email for all MCP calls.
