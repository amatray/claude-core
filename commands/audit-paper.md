---
name: audit-paper
description: Audit academic papers (economics/finance) for typos, grammar, style, and polish. Default uses track-changes markup in Modules 2-3; use --clean for clean text throughout. Use when user asks to audit or review a paper.
disable-model-invocation: false
argument-hint: "[--clean] [path-to-paper-files]"
---

# A. MODE DETECTION

**Parse `$ARGUMENTS` for the `--clean` flag.** If `--clean` appears anywhere in the arguments, use **CLEAN MODE**. Otherwise, use **TRACK-CHANGES MODE** (default). The remainder of the arguments (after removing `--clean`) is the file path(s).

| Mode | Module 1 | Modules 2–3 |
|------|----------|-------------|
| **Default (track-changes)** | Clean corrected text | `\rsout{deleted text}` and `\red{added text}` markup |
| **`--clean`** | Clean corrected text | Clean corrected text |

**Re-read this box before writing suggestions for EACH module.**


# B. CRITICAL WORKFLOW REQUIREMENTS

**YOU MUST FOLLOW THESE RULES. THEY ARE NON-NEGOTIABLE.**

**Work modularly.** Complete one module at a time. After each module, report the required output and wait for confirmation before proceeding.

**Be explicit about unknowns.** If you are uncertain about something, say so. Do not guess.

**Report only problems.** If text is correct, say nothing about it. Never describe what you checked. Never explain that something is "already fine" or "no change needed."


# C. Paper Audit

I want you to audit my academic paper (economics/finance).

The audit should proceed in **three** modules:

- **Module 1 — Correctness**: Check for typos, misspelled words, and grammar issues
- **Module 2 — Style**: Syntax improvements (light and deep), repetition detection
- **Module 3 — Polish** (optional): Substantive rewriting to improve clarity and flow


## D. IMPORTANT: Understanding the Input Files

### LaTeX Format

The paper is written in LaTeX. You should:

- **Ignore LaTeX commands** — focus only on the actual text content
- **Understand** that commands like `\textit{}`, `\textbf{}`, `\cite{}`, `\ref{}`, `\label{}`, `\section{}`, `\paragraph{}`, etc. are formatting — read through them to the text
- **Not flag** LaTeX syntax as errors (e.g., do not flag `\&` as a typo)
- **Preserve** all LaTeX formatting in your suggested corrections

### Comments and Markup

The paper may contain:

- LaTeX comments (lines starting with `%`)
- Coauthor comments or tracked changes
- Margin notes or TODO markers

**Ignore all comments and markup.** Do not audit them. Focus only on the actual paper text.

### LaTeX Rendering Rules — Do NOT Flag as Issues

LaTeX handles whitespace differently than word processors. The following are **NOT problems** and should **NEVER be flagged**:

- **Extra spaces**: Multiple spaces in LaTeX source are collapsed to a single space in output. `word  word` and `word word` render identically. **NEVER flag double spaces or extra spaces as typos.**
- **Single line breaks**: A single line break in the source is treated as a space, not a paragraph break. Text can be broken across multiple lines in the source without affecting the output.
- **Paragraph breaks**: Only a blank line (or explicit commands like `\\` or `\par`) creates an actual paragraph break.

In other words: focus on how the text will **render**, not how it appears in the source file. Do not flag whitespace or line break "issues" unless they would actually affect the compiled output.

### Multiple Files

The paper may be split across multiple `.tex` files. These should be read in the order they appear in the document structure (typically: introduction, literature, model, data, results, conclusion, appendix). If the order is unclear, ask before proceeding.


## E. IMPORTANT: Stop-and-Check Points

Throughout this project, there are mandatory **STOP AND CHECK** points. At each of these points, you must:

1. Summarize what you have completed
2. Present your findings for review
3. **Wait for human approval before proceeding**

Do not proceed past a STOP checkpoint without explicit approval.


## F. IMPORTANT: Format of Suggested Corrections

**All suggested corrections must be in LaTeX format** so they can be directly copy-pasted into the source file.

For each correction, provide:

1. **Location**: File name (if multiple files) and line number
2. **Original**: The exact LaTeX code as it currently appears
3. **Suggested**: The corrected LaTeX code

**Do NOT use code blocks or blockquotes for Original/Suggested pairs.** Use bold labels (**Original:**, **Suggested:**) on their own line, with the text on the next line. Separate each suggestion from the next with a horizontal rule (`---`). **Reason:** and **Note:** labels MUST always be bold.

**Example (single-line):**

**T3** (intro.tex, line 45)

**Original:**
\paragraph{Probem.}

**Suggested:**
\paragraph{Problem.}

---

**Example (multi-line with reason):**

**S5** (intro.tex, lines 12-15)

**Original:**
This is the first sentence of the original text. And this is the second sentence that continues the thought. Here is a third line to illustrate.

**Suggested:**
This is the revised first sentence. The second sentence is now tighter. The third line is also improved.

**Reason:** [brief explanation]

---

**Do NOT strip LaTeX commands.** If the original has `\textit{recieve}`, the correction should be `\textit{receive}`, not just `receive`.

**CRITICAL: Preserve ALL LaTeX formatting in suggestions.** When rewriting or condensing text, you MUST preserve:
- All LaTeX commands: `\textit{}`, `\textbf{}`, `\underline{}`, `\emph{}`, `\sout{}`, `\rev{}`, `\red{}`, etc.
- All references: `\cite{}`, `\citep{}`, `\citet{}`, `\autoref{}`, `\ref{}`, `\eqref{}`, `\label{}`, etc.
- All special characters and escapes: `\%`, `\&`, `\$`, `~`, `---`, `--`, etc.
- All math mode content: `$...$`, `\[...\]`, equation environments, etc.
- All custom commands defined by the authors

Before finalizing ANY suggestion, verify that every LaTeX command present in the original text is preserved in the suggested text (unless the specific purpose of the edit is to remove that formatting). Failure to preserve LaTeX syntax makes suggestions unusable.


## G. CHUNKING RULE

**Multi-file chunking:** If the paper has 3 or more `.tex` files, process each module **one file at a time**. This means: produce your audit output (typos, grammar, style suggestions, etc.) for ONE file only, then STOP. Wait for approval before producing output for the next file. You may read all files upfront for context, but your output in each response must cover only one file.

**Section-based chunking:** For any paper over ~5,000 words (regardless of file count), process **ALL modules** by `\section{}` groups — batch 2-3 sections per response, and stop between batches for approval. This prevents output token overflow.

**Short papers** (under ~5,000 words with 1-2 files): process the whole paper per module.

**HARD LIMIT: If your output is growing long, STOP and break it into chunks. It is always better to stop early and continue in the next response than to hit the output token limit. Aim for no more than ~40 suggestions per response.**


## H. IMPLEMENTATION RULES: MODULE 1

When I say **"implement correction XX"** (e.g., "implement T1, G3"), apply the change by **directly replacing** the original text with the corrected text.

**Rules:**

1. Show the full corrected line(s) ready to copy-paste into the LaTeX source
2. Preserve all surrounding LaTeX commands and formatting
3. Provide the file name and line number(s) for reference
4. **Do NOT use track-changes markup** (`\rsout{}`, `\red{}`, etc.) — just provide the clean corrected text


## I. IMPLEMENTATION RULES: MODULES 2–3

**IF CLEAN MODE** (`--clean` was specified):
Same as Module 1 — directly replace with clean corrected text. No markup.

**IF TRACK-CHANGES MODE** (default):
Provide the full text with `\rsout{}` and `\red{}` markup ready to copy-paste. Since your suggestions already use this markup, implementation means providing the "Suggested" line with full context.

**Rules:**

1. Show the full implemented line(s) ready to copy-paste into the LaTeX source
2. Preserve all surrounding LaTeX commands and formatting
3. In track-changes mode: only mark the changed portion with `\rsout{}` and `\red{}`
4. Provide the file name and line number(s) for reference


---

## Module 1: Correctness (Typos + Grammar)

Read through the entire paper and identify all typos, misspelled words, and grammar issues.

**See `references/audit-checklists.md`:**
- **Typo Checklist** — what counts/doesn't count, 4-step verification (spelling, intended word, duplication, consistency)
- **Grammar Checklist** — what counts/doesn't count, 5-step verification (subject-verb agreement, noun number, prepositions, articles, verb forms)

Key exclusions: do NOT flag LaTeX commands, extra spaces (LaTeX collapses them), technical terms, proper nouns, stylistic choices, or field-specific conventions.

**Labeling:**
- Typos: T1, T2, T3, ...
- Grammar: G1, G2, G3, ...

**OUTPUT ORDER REQUIREMENT:**
List all issues in order of appearance in the document (by file, then by line number). Typos first, then grammar.

**Report format:**

## TYPOS

**T1** (filename.tex, line XX)

**Original:**
...
**Suggested:**
...

---

[etc.]

## GRAMMAR

**G1** (filename.tex, line XX)

**Original:**
...
**Suggested:**
...

---

[etc.]

If no issues in a category, state "No typos found." or "No grammar issues found."

**STOP and wait for approval.**

When you stop, write:

```
STOPPED - AWAITING YOUR INPUT (Module 1: Correctness)

You may:
- Ask questions or request clarifications
- Tell me which corrections to implement (e.g., "implement T1, T3, G2")
- Say "move to next" to proceed to Module 2
```

**Do NOT proceed to Module 2 until I explicitly say "move to next"**


---

## Module 2: Style (Syntax + Repetition)

**⚠️ FORMAT REMINDER: Re-read section A (Mode Detection) now. If `--clean` was specified, provide clean corrected text. Otherwise, use `\rsout{}` and `\red{}` markup.**

**⚠️ CHUNKING REMINDER: If this paper is over ~5,000 words, process by `\section{}` groups (2-3 sections per response). Stop between batches.**

Read through the paper and suggest syntax improvements and flag repetition.

**See `references/audit-checklists.md` → Style Checklist** for the full scope.

### Light syntax (sentence-level fixes)

- Sentences that are too long and could be split
- Awkward phrasing that has a simple fix
- Unclear sentences where a small rewording helps
- Passive voice that would be clearer as active (only if the fix is simple)
- Word choice improvements (only if clearly better, not just different)

**Constraints:** Do NOT rewrite paragraphs — sentence-level changes only. Do NOT change the author's voice or style. Be conservative — if acceptable, leave it alone.

### Deep syntax (structural improvements)

- Paragraphs that could be restructured for clarity
- Verbose phrases with simple replacements (e.g., "in order to" → "to", "due to the fact that" → "because")
- Weak or vague language (e.g., "makes a lot of sense", "is related to an important dimension")
- Informal language inappropriate for academic writing
- Filler phrases that add nothing (e.g., "It is important to note that")
- Unnecessary hedging (e.g., "We think that..." when you can just state the point)
- Sentences that should be combined or reordered
- Transitions between paragraphs that are missing or weak

### Repetition

- **Across the paper**: same idea stated multiple times in different sections
- **Within paragraphs**: same point made twice in slightly different words

When you identify repetition, report all locations, which instance to keep, and suggested deletions or consolidations.

**Labeling:**
- Style suggestions: S1, S2, S3, ... with severity tag `[minor]` or `[substantial]`
- Repetition issues: R1, R2, R3, ...

**OUTPUT ORDER REQUIREMENT:**
- List S suggestions in order of appearance, with sub-headers `### Light Syntax`, `### Deep Syntax`
- List R suggestions separately at the end under `### Repetition`

**Report format:**

**IF TRACK-CHANGES MODE** (default):

## STYLE SUGGESTIONS (Module 2)

### Light Syntax

**S1** [minor] (filename.tex, line XX)

**Original:**
This sentence is awkward and hard to follow.
**Suggested:**
This sentence \rsout{is awkward and hard to follow}\red{reads more clearly now}.
**Reason:** [brief explanation]

---

### Deep Syntax

**S4** [substantial] (filename.tex, line XX)

**Original:**
This sentence is too wordy and could be tightened up significantly.
**Suggested:**
This sentence \rsout{is too wordy and could be tightened up significantly}\red{could be tightened}.
**Reason:** [explanation]

### Repetition

R1: [Brief description of what is repeated]
- Location 1: filename.tex, line XX — `[text]`
- Location 2: filename.tex, line YY — `[text]`
Suggestion: Keep location 1, delete location 2.

**IF CLEAN MODE** (`--clean` was specified):
Same structure, but use clean corrected text instead of `\rsout{}`/`\red{}` markup.

If no suggestions, state "No style suggestions" and/or "No repetition issues found."

**STOP and wait for approval.**

When you stop, write:

```
STOPPED - AWAITING YOUR INPUT (Module 2: Style)

You may:
- Ask questions or request clarifications
- Tell me which corrections to implement (e.g., "implement S1, S4, R1")
- Say "move to next" to proceed to Module 3 (Polish Pass)
- Say "done" to end the audit here
```

**Do NOT proceed to Module 3 until I explicitly say "move to next"**


---

## Module 3: Polish (Optional — Substantive Rewriting)

**⚠️ FORMAT REMINDER: Re-read section A (Mode Detection) now. If `--clean` was specified, provide clean corrected text. Otherwise, use `\rsout{}` and `\red{}` markup.**

This module is optional. Only proceed if explicitly requested.

In this module, you have **freedom to rewrite substantially**. The goal is to make the writing as clear, direct, and elegant as possible.

**See `references/audit-checklists.md` → Polish Checklist** for the full list of what you can do (rewrite paragraphs, restructure, cut, reorganize) and the 5 things to look for (convoluted explanations, buried key points, unnecessary complexity, weak openings, passive voice).

**Constraints:**

- **Preserve the author's meaning** — rewrites must convey the same information
- **Preserve technical accuracy** — do not simplify in ways that lose precision
- **Preserve academic tone** — do not make the writing casual
- **Preserve ALL LaTeX formatting** — every `\underline{}`, `\textit{}`, `\autoref{}`, `\cite{}`, and other LaTeX command in the original MUST appear in the rewritten version (unless the edit specifically intends to remove it). This is critical: suggestions that strip LaTeX commands are unusable.
- **Flag uncertainty** — if a rewrite might alter meaning, note this explicitly
- **Focus on rendered output** — do not flag LaTeX source formatting (whitespace, line breaks)

For EVERY paragraph, ask: **"What is the clearest, most direct way to say this?"** If your answer differs significantly, propose a rewrite.

**Minimum expectation:**

Academic writing almost always benefits from tightening. If you find fewer than 5 substantive suggestions on a multi-page document, you are not engaging deeply enough. Re-read and ask: "How would I rewrite this to be clearer?"

**Labeling:** Label each suggestion as P1, P2, P3, ... (P for Polish)

**Report format:**

**IF TRACK-CHANGES MODE** (default):

**P1** (filename.tex, lines XX-YY)

**Original:**
Thank you for your thoughtful comments. We appreciate the opportunity to revise our paper. Below we describe the changes.
**Suggested:**
Thank you for your \rsout{thoughtful }comments\rsout{. We appreciate the opportunity to revise our paper. Below we}\red{; we} describe the changes\red{ below}.
**Reason:** [what you improved]

**IF CLEAN MODE** (`--clean` was specified):

**P1** (filename.tex, lines XX-YY)

**Original:**
Thank you for your thoughtful comments. We appreciate the opportunity to revise our paper. Below we describe the changes.
**Suggested:**
Thank you for your comments; we describe the changes below.
**Reason:** [what you improved]

If no suggestions, state "No rewriting suggestions" — but this should be rare. Most academic writing can be improved.

**STOP and wait for final approval.**

When you stop, write:

```
STOPPED - PAPER AUDIT COMPLETE

You may:
- Ask questions or request clarifications
- Tell me which corrections to implement
- Request additional review of specific sections
```


---

## Consistency Rules

### Maintaining Consistency Based on User Feedback

**If you provide ANY corrections, clarifications, or modifications to my audit approach at any stop point, I MUST apply those same corrections/modifications consistently to ALL remaining modules and sections in the audit.**

This includes but is not limited to:

- **Classification changes**: If you say "this is not a typo, it's correct terminology," I must not flag similar terminology anywhere else
- **Scope clarifications**: If you say "don't flag X as an issue," I must never flag X in any remaining modules
- **Style preferences**: If you indicate you prefer a certain phrasing or construction, I must not suggest changing it in later sections
- **Technical term exceptions**: If you clarify that a term is field-specific jargon, I must not flag it as a typo or suggest changing it later
- **Grammar conventions**: If you approve a certain grammatical construction, I must apply that standard throughout
- **Threshold adjustments**: If you say "only flag sentences longer than 50 words," I must apply that threshold in all remaining modules

**Before proceeding to each new module, I must review all feedback you have provided on previous modules and ensure I apply it consistently.**

**I must NEVER flag the same issue type again after you have indicated it should not be flagged.**


## General Rules for All Modules

### How to write the audit

- **Think first, write second.** Before writing ANY suggestion, verify it is an actual problem requiring a change.
- **Never withdraw or revise suggestions mid-response.** If you write a suggestion and then realize it's not valid, you have already failed. Do not write "I withdraw this" or "actually this is fine" — those phrases should never appear.
- **Each suggestion you write is final.** If you are unsure whether something is a problem, do not include it.

### What NOT to include in the audit

- **Only report actual problems or changes needed.** Do NOT list things that are already correct.
- Do NOT say things like "this sentence is fine" or "no change needed here"
- If the text is fine, do not mention it at all
- Every item in your audit should be something that requires action or a decision from me
- **NEVER describe your review process.** Do not say "I checked X and it was fine" or "After reviewing, I found no issues with Y"
- **ABSOLUTE PROHIBITION: NEVER suggest using `---` (em dash). Under no circumstances should you propose inserting, adding, or replacing anything with an em dash. This is a hard rule with zero exceptions. Violations of this rule make the entire audit unusable.**

### Technical terms and jargon

Economics and finance papers use field-specific terminology. Do NOT flag as errors:

- Standard econometric terms (heteroskedasticity, endogeneity, etc.)
- Financial terms (yield spread, basis points, etc.)
- Variable names and notation
- Standard abbreviations (OLS, IV, GMM, CAPM, etc.)

If you are unsure whether something is a technical term, do not flag it.

### Consistency rule

When you find ANY error, immediately search the entire document for:

1. The exact same error elsewhere
2. The same pattern applied to different words (e.g., if you find one subject-verb disagreement, re-check ALL subject-verb pairs; if you find "Earning" should be "Earnings", check ALL similar words throughout)

This prevents inconsistent corrections and missed duplicates.

### Second-pass requirement

Within each module, after your first pass through the document, do a second pass applying the systematic checks from the checklists. The first pass catches obvious errors; the second pass catches errors that require careful analysis.
