# Calendar Policy
*Configuration for /schedule-query and /morning-brief skills*

## Prerequisites
- Google Calendar with Google Workspace MCP configured
- Calendar IDs retrieved (see "How to Find Calendar IDs" below)
- Primary Gmail: adrien.matray@gmail.com

## How to Find Google Calendar IDs

**Method 1: Using Claude Code (recommended)**
Run this in Claude Code:
```
Ask Claude to call mcp__google_workspace__list_calendars with your email address
```

**Method 2: Google Calendar Settings**
1. Open Google Calendar > Settings (gear icon)
2. Click on each calendar name in the left sidebar
3. Scroll to "Integrate calendar" section
4. Copy the "Calendar ID" value

---

## Calendar IDs

| Calendar Name | Calendar ID | Notes |
|--------------|-------------|-------|
| Primary (Personal) | adrien.matray@gmail.com | Main personal calendar |
| TODO: Fed calendar | TODO@atl.frb.org | Atlanta Fed work calendar |
| TODO: Other calendars | TODO | Add any shared/project calendars |

---

## Scheduling Preferences

### Working Hours
- **Start:** 8:30 AM ET
- **End:** 6:00 PM ET
- **Days:** Monday-Friday

### Timezone
- **Primary:** America/New_York (Atlanta)
- **Abbreviation:** ET
- **UTC offset:** -05:00 (EST) / -04:00 (EDT)

### Buffer Times
- **Between meetings:** 15 minutes minimum
- **Before deep work:** 30 minutes

### Preferences
- Protect morning deep work: avoid scheduling before 10:00 AM when possible
- Prefer Friday PM free: avoid scheduling after 2:00 PM on Fridays
- No back-to-back: don't create 3+ consecutive meetings
- Protect largest free block each day for research/writing
- Reserve time for managing 10-20 active research projects

### Deep Work Protection
- **push_level:** `moderate`
  - `gentle` — just show schedule, no nudges
  - `moderate` — protect largest free block, suggest deep work
  - `assertive` — flag when <2 hours free, suggest declining meetings

---

## Scheduling Reply Tone

### Tier 2 (Most Common — Colleagues, Co-authors, RAs)
```
Hi [Name],

I'm free at these times:
- [Day], [Month] [Date] at [time] ET
- [Day], [Month] [Date] at [time] ET
- [Day], [Month] [Date] at [time] ET

Let me know what works and I'll send a calendar invite.

Best,
Adrien
```

### Tier 1 (Formal — Senior Contacts, External)
```
Hi [Name],

I'd be happy to meet. I have availability at the following times:
- [Day], [Month] [Date] at [time] ET
- [Day], [Month] [Date] at [time] ET
- [Day], [Month] [Date] at [time] ET

Please let me know which works best for you.

Best,
Adrien
```

---

## Slot Scoring (preference order)

1. Mid-morning (10am-12pm) or mid-afternoon (2pm-4pm)
2. Not adjacent to existing long meetings
3. Days with fewer existing meetings
4. Closer dates (sooner is better)

---

## Customization Points

- **Calendar IDs:** Add your Fed calendar and any shared calendars. Missing a calendar = double-booking risk.
- **Working hours:** Adjust if your schedule differs from 8:30-6.
- **Deep work protection:** Increase to `assertive` if you need more protected research time.
- **Reply tone:** Edit templates to match your voice.
