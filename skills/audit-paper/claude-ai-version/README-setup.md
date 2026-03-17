# Paper Audit Tool — Setup Guide for Claude.ai

This tool audits academic papers (economics/finance) for typos, grammar, style, and polish. It works as a **Claude Project** — set it up once, then use it for every paper.

## What You Need

- A Claude account (free accounts get 5 Projects; paid plans get unlimited)
- Your paper as `.tex` source files (not PDF)
- 2 files from this folder:
  - `audit-paper-project-instructions.md` — the audit instructions
  - `audit-paper-checklists.md` — detailed verification checklists

## Setup (one-time, ~5 minutes)

### Step 1: Create a Project

1. Go to [claude.ai](https://claude.ai)
2. In the left sidebar, click **Projects** (or the folder icon)
3. Click **+ New Project**
4. Name it **"Paper Audit"** (or any name you prefer)

### Step 2: Add Custom Instructions

1. Open your new Project
2. On the right sidebar, find **Instructions** and click the **+** button next to it
3. Open `audit-paper-project-instructions.md` in a text editor
4. **Copy the entire contents** and paste into the Instructions field
5. Save

### Step 3: Upload the Checklists

1. On the right sidebar, find **Files** and click the **+** button next to it
2. Click **Upload from device**
3. Select `audit-paper-checklists.md`
3. This file will be available in every conversation within the Project

## How to Use

1. Open your **Paper Audit** Project
2. Start a **new conversation**
3. **Upload your `.tex` file(s)** using the attachment button
4. Type: **"Audit my paper"**
5. Claude will ask you two setup questions (correction format and delivery method), then begin the audit

### The Audit Process

The audit runs in 3 modules:

| Module | What it checks | When it runs |
|--------|---------------|--------------|
| **1. Correctness** | Typos + grammar | Always |
| **2. Style** | Sentence improvements + repetition | After Module 1 |
| **3. Polish** | Substantive rewriting | Optional, on request |

After each module, Claude stops and waits for your input. You can:
- Ask questions
- Tell Claude which corrections to apply (e.g., "implement T1, T3, G2")
- Say "apply all" to apply everything
- Say "move to next" to proceed to the next module
- Say "done" to end the audit

## Limitations & Troubleshooting

**Requires .tex source files.** PDFs cannot be audited because Claude needs the LaTeX source to provide copy-pasteable corrections. If you only have a PDF, you'll need to get the .tex files from your coauthors or Overleaf.

**Best for papers up to ~60 pages.** Longer papers may exhaust the conversation's context window. For very long papers, upload one .tex file per conversation and run the audit on each file separately.

**If context runs out mid-audit.** Start a new conversation within the same Project. Upload the remaining .tex file(s) and say "Continue the audit from Module X" — Claude will have the same instructions but won't remember the prior conversation.

**Track-changes mode requires LaTeX preamble additions.** If you choose track-changes markup, Claude will provide the required `\rsout{}` and `\red{}` command definitions. If your paper already defines commands with these names (or uses packages like `changes.sty`), you may need to adjust the command names to avoid conflicts.

**Processing time.** The initial read-through of a 50-60 page paper takes approximately 15-20 minutes. This is normal — Claude is reading carefully.
