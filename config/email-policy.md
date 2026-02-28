# Email Policy
*Configuration file for email-related skills (/triage-inbox, /morning-brief)*

## Never Do (Without Explicit Instruction)
- Mark emails as read
- Send emails without approval
- Delete emails
- Make commitments on my behalf

## OK to Do
- Apply Gmail labels
- Draft replies (shown, not sent)
- Create Gmail filters
- Search and read emails

## Graduated Autonomy
- Start with "propose actions" (read-only)
- Graduate to low-risk writes (labels, drafts)
- Only later: medium-risk writes (sending, with guardrails)

---

## Prerequisites
- Gmail account with Google Workspace MCP configured
- Gmail labels created (see "How to Set Up Labels" below)
- Primary Gmail: adrien.matray@gmail.com
- Fed email: adrien.matray@atl.frb.org

## How to Set Up Labels

Create these Gmail labels (Settings > Labels > Create new label):
1. `@ToRead` — newsletters, working papers, long-form content
2. `@Announcements` — institutional announcements, seminar notices, event notifications
3. `@Fed` — Atlanta Fed internal communications
4. `@CEPR` — CEPR communications
5. `Expenses/Expenses-Pending` — receipts awaiting processing
6. `Auto-Archive` — low-priority automated emails

---

## VIP List

VIP emails are never auto-triaged — they always stay in your inbox.

### Tier 1 — Never Touch (friends & family, critical institutional)
| Name | Email | Notes |
|------|-------|-------|
| Aline Matray | aline.matray@gmail.com | Family |
| Luc Matray | luc.matray@gmail.com | Family |
| Louis Matray | louis.matray@gmail.com | Family |
| Chenzi Xu | chenzixu@berkeley.edu, chenzi.xu@gmail.com | Partner + co-author (Berkeley) |
| Juliane Begenau | begenau@stanford.edu, juliane.begenau@gmail.com | Friend (Stanford) |
| Claudia Robles Garcia | croblesga@gmail.com | Friend |
| Nicolas Antraigue | nicolas.antraigue@gmail.com | Friend |
| Bertrand Girard | ber.girard@gmail.com | Friend |
| Constance Valdelièvre | constance.valdelievre@gmail.com | Friend |
| Marion Meissonnier | marion.meissonnier@gmail.com | Friend |
| TODO: Add Fed supervisor | TODO@atl.frb.org | Direct supervisor at Atlanta Fed |

### Tier 2 — High Priority (co-authors, conference co-organizers)
| Name | Email | Notes |
|------|-------|-------|
| Pete Klenow | pete.klenow@gmail.com | Co-organizer, SITE conference (Stanford) |
| Michael Blank | blankm@stanford.edu | Co-organizer, SITE conference (Stanford) |
| Sara Moreira | sara.moreira@kellogg.northwestern.edu | Co-organizer, SITE conference (Kellogg/Northwestern) |
| Tim Schmidt-Eisenlohr | tim.schmidt-eisenlohr@frb.gov, t.schmidteisenlohr@gmail.com | Co-organizer, Industrial Policies (Fed Board) |
| Johan Hombert | hombert@hec.fr | Co-author (HEC Paris) |
| Paul Beaumont | paul.beaumont@mcgill.ca | Co-author (McGill) |
| Karsten Mueller | kmueller@nus.edu.sg | Co-author (NUS Singapore) |
| Camelia Minoiu | minoiu.camelia@gmail.com | Colleague/co-author (Fed) |
| Roberto Robatto | roberto.robatto@gmail.com | Colleague/co-author |
| Andrea Ferrero | andrea.ferrero@economics.ox.ac.uk | Co-author (Oxford) |
| Marc Melitz | mmelitz@harvard.edu | Senior contact (Harvard) |

### Tier 3 — Important (RAs, team members)
| Name | Email | Notes |
|------|-------|-------|
| Felix Brown | Felix.Brown@atl.frb.org | Research assistant (Atlanta Fed) |
| Yachi Tu | yaqitu@berkeley.edu | Research assistant (Berkeley) |
| Zekai Shen | zekai.shen@phd.unibocconi.it | PhD student/RA (Bocconi) |

### Friends & Family Addresses
- aline.matray@gmail.com
- luc.matray@gmail.com
- louis.matray@gmail.com
- chenzixu@berkeley.edu
- chenzi.xu@gmail.com
- begenau@stanford.edu
- juliane.begenau@gmail.com
- croblesga@gmail.com
- nicolas.antraigue@gmail.com
- ber.girard@gmail.com
- constance.valdelievre@gmail.com
- marion.meissonnier@gmail.com

---

## Auto-Archive Rules

Emails matching these patterns are archived and marked read automatically.

### Stage 1 — High Confidence (exact sender match)
| Sender | Action | Notes |
|--------|--------|-------|
| noreply@github.com | Archive + mark read | GitHub notifications |
| no-reply@accounts.google.com | Archive + mark read | Account alerts |
| notifications@github.com | Archive + mark read | GitHub notifications |
| noreply@dropbox.com | Archive + mark read | Dropbox notifications |
| no-reply@zoom.us | Archive + mark read | Zoom recordings/notifications |
| noreply@slack.com | Archive + mark read | Slack email notifications |
| noreply@overleaf.com | Archive + mark read | Overleaf compile notifications |
| do-not-reply@stackexchange.com | Archive + mark read | Stack Exchange digests |

### Stage 2 — Medium Confidence (domain/pattern match)
| Pattern | Action | Notes |
|---------|--------|-------|
| *@notifications.google.com | Archive + mark read | Google product notifications |
| *@info.arxiv.org | Route to @ToRead | arXiv new submission alerts |
| *@noreply.github.com | Archive + mark read | GitHub automated emails |
| *@linkedin.com | Archive + mark read | LinkedIn notifications |
| *@quora.com | Archive + mark read | Quora digests |
| *@academia-mail.com | Archive + mark read | Academia.edu notifications |
| *@researchgate.net | Archive + mark read | ResearchGate notifications |

---

## Academic & Research Routing

### Route to @ToRead (newsletters, working papers)
| Sender/Pattern | Notes |
|---------------|-------|
| *@substack.com | Substack newsletters |
| *@nber.org | NBER working paper digests |
| *@cepr.org | CEPR discussion papers |
| *@ssrn.com | SSRN paper alerts |
| *@beehiiv.com | Newsletter platform |
| *@convertkit.com | Newsletter platform |
| *@mailchimp.com | Newsletter platform |
| *@buttondown.email | Newsletter platform |

### Route to @Announcements (seminars, events, institutional)
| Sender/Pattern | Notes |
|---------------|-------|
| *@aeaweb.org | AEA announcements |
| *@econjobmarket.org | Job market announcements |
| *@nber.org (conference/event) | NBER conference announcements |
| TODO: Add seminar mailing lists | Departmental seminars |

### Route to @Fed
| Sender/Pattern | Notes |
|---------------|-------|
| *@atl.frb.org | Atlanta Fed internal (non-VIP) |
| *@frb.gov | Federal Reserve system-wide |

---

## Skip-Inbox Labels

Emails routed to these labels skip the inbox:
- @ToRead — skip inbox, leave unread
- @Announcements — skip inbox, leave unread
- @Fed — skip inbox, leave unread (except VIP senders)
- @CEPR — skip inbox, leave unread
- Auto-Archive — skip inbox, mark read

---

## Customization Points

- **VIP tiers:** Fill in all TODO entries with actual names and emails. Tier 1 = untouchable, Tier 2 = high priority but can be labeled, Tier 3 = important team.
- **Auto-archive rules:** Start conservative. Add senders after you see them repeatedly in triage reports.
- **Label names:** You can rename labels — just update the label IDs in `triage-config.md` to match.
- **Friends & family addresses:** Used for safety checks. Emails from friends & family are never auto-triaged.
- **Academic routing:** Add specific seminar mailing lists and working paper series you subscribe to.
