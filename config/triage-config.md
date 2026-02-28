# Triage Configuration
*Technical configuration for /triage-inbox and /morning-brief skills*

## Prerequisites
- Gmail labels created (see email-policy.md)
- Label IDs retrieved (see "How to Find Label IDs" below)
- Primary Gmail: adrien.matray@gmail.com

## How to Find Gmail Label IDs

**Method 1: Using Claude Code (recommended)**
Run this in Claude Code:
```
Ask Claude to call mcp__google_workspace__list_gmail_labels with your email address
```

**Method 2: Gmail API Explorer**
1. Go to https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list
2. Click "Try it" and authorize
3. Copy the label IDs from the response

---

## Label IDs

| Label Name | Label ID | Notes |
|------------|----------|-------|
| @ToRead | Label_48 | Newsletters, working papers |
| @Announcements | Label_49 | Seminar notices, events |
| @Fed | Label_50 | Atlanta Fed internal |
| @FYI | Label_51 | For your information |
| @ToDo | Label_52 | Action items |
| @ToSelf | Label_53 | Self-sent items for todo processing |
| Expenses-Pending | Label_54 | Under Expenses/ parent label |
| Expenses-Personal | Label_55 | Under Expenses/ parent label |
| Expenses-Uncertain | Label_56 | Under Expenses/ parent label |
| Auto-Archive | Label_57 | Low-priority automated emails |

---

## Label Application Rules

| Routing Tier | Add Label | Remove From | Read Status |
|-------------|-----------|-------------|-------------|
| @ToRead | Label ID | INBOX | Leave UNREAD |
| @Announcements | Label ID | INBOX | Leave UNREAD |
| @Fed | Label ID | INBOX | Leave UNREAD |
| @CEPR | Label ID | INBOX | Leave UNREAD |
| Expenses-Pending | Label ID | INBOX | Leave UNREAD |
| Expenses-Personal | Label ID | INBOX | Leave UNREAD |
| Expenses-Uncertain | Label ID | INBOX | Leave UNREAD |
| Auto-Archive | Label ID | INBOX | Mark as READ |

---

## Expense Vendor Domains

| Domain | Vendor Type | Notes |
|--------|------------|-------|
| uber.com | Transport | Uber rides |
| lyft.com | Transport | Lyft rides |
| amazon.com | Retail | Amazon purchases |
| paypal.com | Payment | PayPal transactions |
| square.com | Payment | Square receipts |
| stripe.com | Payment | Stripe payments |
| delta.com | Airline | Delta flights (Atlanta hub) |
| united.com | Airline | United flights |
| aa.com | Airline | American Airlines |
| marriott.com | Hotel | Marriott stays |
| hilton.com | Hotel | Hilton stays |
| hotels.com | Hotel | Hotel bookings |
| expedia.com | Travel | Travel bookings |
| dropbox.com | Software | Dropbox subscription |
| overleaf.com | Software | Overleaf subscription |
| TODO: Add other vendors | TODO | Restaurants, local vendors |

---

## Expense Subject Keywords

Subjects containing these words (from vendor-like senders) are flagged as expenses:
- receipt, invoice, payment, order confirmation, transaction, purchase, charge, booking confirmation, itinerary, reservation

## Expense Skip Patterns

NOT expenses even if from a vendor domain:
- "welcome", "verify your email", "password reset", "account update", "terms of service", "we miss you", "sale", "deal", "promotion"

---

## Newsletter Platform Domains

Emails from these domains are routed to @ToRead:
- substack.com
- beehiiv.com
- convertkit.com
- mailchimp.com
- buttondown.email
- revue.email

---

## Academic/Research Domains

### Route to @ToRead (working papers, research content)
- nber.org (working paper digests)
- cepr.org (discussion paper alerts)
- ssrn.com (paper alerts, author updates)
- arxiv.org (new submission alerts)
- repec.org (NEP alerts)
- voxeu.org (VoxEU columns)

### Route to @Announcements (seminars, conferences, job market)
- aeaweb.org (AEA announcements)
- econjobmarket.org (job market)
- econometricsociety.org (Econometric Society)
- TODO: Add seminar mailing lists (department seminars, Fed seminars)

### Route to @Fed (Federal Reserve system)
- atl.frb.org (Atlanta Fed — non-VIP senders)
- frb.gov (Federal Reserve Board)
- frbsf.org (San Francisco Fed)
- newyorkfed.org (New York Fed)
- TODO: Add other regional Fed domains as needed

---

## @ToRead Sender Whitelist

Specific senders always routed to @ToRead (regardless of other signals):
| Sender | Notes |
|--------|-------|
| TODO: Add specific newsletter senders | E.g., Matt Levine, Marginal Revolution, etc. |

---

## Classification Score Thresholds

| Score | Classification |
|-------|---------------|
| Newsletter platform domain | @ToRead (immediate) |
| @ToRead whitelist match | @ToRead (immediate) |
| Academic paper alert domain | @ToRead (immediate) |
| Newsletter score >= 3 | @Announcements |
| Announcement score >= 2 + .edu | @Announcements |
| Fed domain (non-VIP) | @Fed |
| CEPR domain | @CEPR |
| Receipt/notification from noreply | Auto-Archive |
| Score 1-2 mixed signals | SKIP (uncertain) |
| Score 0 or no match | SKIP (leave in inbox) |

---

## Classification Overrides

Manual overrides that take precedence over scoring. Add entries here when triage misclassifies a sender.

| Sender Pattern | Override To | Notes |
|---------------|-------------|-------|
| TODO: Add as needed | TODO | Add after running triage a few times |

---

## Classification Priority (Tiebreaking)

When multiple categories match, use this priority order:
1. VIP (always wins — stays in inbox)
2. Family (always wins — stays in inbox)
3. Expenses (financial takes priority)
4. @ToRead (user-subscribed content)
5. @Fed (institutional)
6. @CEPR (institutional)
7. @Announcements (general)
8. Auto-Archive (lowest priority)

---

## Customization Points

- **Label IDs:** You MUST replace all TODO values with actual Gmail label IDs before using triage skills. Run `mcp__google_workspace__list_gmail_labels` to get them.
- **Vendor domains:** Add airlines, hotels, and restaurants you use for Fed travel.
- **Academic domains:** Add working paper series and seminar lists you subscribe to.
- **Fed domains:** Add regional Fed domains for colleagues you interact with.
- **Classification overrides:** Add entries as you correct triage mistakes — this is the feedback loop.
