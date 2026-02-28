---
name: audit-paper
description: Audit academic papers (economics/finance) for typos, grammar, and syntax. Modules 1-3 use clean text, Modules 4-5 use track-changes markup. Use when user asks to audit or review a paper.
disable-model-invocation: false
argument-hint: [path-to-paper-files]
---

# CRITICAL WORKFLOW REQUIREMENTS

**YOU MUST FOLLOW THESE RULES. THEY ARE NON-NEGOTIABLE.**

**Work modularly.** Complete one module at a time. After each module, report the required output and wait for confirmation before proceeding.

**Be explicit about unknowns.** If you are uncertain about something, say so. Do not guess.

**Report only problems.** If text is correct, say nothing about it. Never describe what you checked. Never explain that something is "already fine" or "no change needed."


# CRITICAL FORMATTING REMINDER

| Module | Format for ALL Suggestions (not just implementation) |
|--------|------------------------------------------------------|
| **Modules 1–3** | Provide **CLEAN corrected text only**. NO track-changes markup. |
| **Modules 4–5** | Use **track-changes markup IN YOUR SUGGESTIONS**: `\rsout{deleted text}` and `\red{added text}` |

**Re-read this box before writing suggestions for EACH module.**


# Paper Audit

I want you to audit my academic paper (economics/finance).

The audit should proceed in **five** modules:

- **Module 1**: Check for typos and misspelled words
- **Module 2**: Check for grammar issues (missing articles, subject-verb agreement, etc.)
- **Module 3**: Light syntax review (minor improvements only)
- **Module 4**: Deep syntax review (substantial improvements, identify repetition) — **uses `\rsout{}` and `\red{}`**
- **Module 5**: Polish pass (optional — broader rewrites to improve clarity and flow) — **uses `\rsout{}` and `\red{}`**


## IMPORTANT: Understanding the Input Files

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


## IMPORTANT: Stop-and-Check Points

Throughout this project, there are mandatory **STOP AND CHECK** points. At each of these points, you must:

1. Summarize what you have completed
2. Present your findings for review
3. **Wait for human approval before proceeding**

Do not proceed past a STOP checkpoint without explicit approval.


## IMPORTANT: Format of Suggested Corrections

**All suggested corrections must be in LaTeX format** so they can be directly copy-pasted into the source file.

For each correction, provide:

1. **Location**: File name (if multiple files) and line number
2. **Original**: The exact LaTeX code as it currently appears
3. **Suggested**: The corrected LaTeX code

**Use code blocks for alignment.** Always present Original and Suggested inside a code block so they align vertically for easy comparison.

**CRITICAL FORMATTING RULE:** For multi-line corrections, always include a **blank line** between the end of the Original block and the "Suggested:" label. This makes it easier to visually distinguish where the original ends and the suggestion begins.

**Example (single-line):**

**T3** (intro.tex, line 45)
```
Original : \paragraph{Probem.}

Suggested: \paragraph{Problem.}
```

**Example (multi-line):**

**S5** (intro.tex, lines 12-15)
```
Original : This is the first sentence of the original text.
And this is the second sentence that continues the thought.
Here is a third line to illustrate.

Suggested: This is the revised first sentence.
The second sentence is now tighter.
The third line is also improved.
```

**Do NOT strip LaTeX commands.** If the original has `\textit{recieve}`, the correction should be `\textit{receive}`, not just `receive`.

**CRITICAL: Preserve ALL LaTeX formatting in suggestions.** When rewriting or condensing text, you MUST preserve:
- All LaTeX commands: `\textit{}`, `\textbf{}`, `\underline{}`, `\emph{}`, `\sout{}`, `\rev{}`, `\red{}`, etc.
- All references: `\cite{}`, `\citep{}`, `\citet{}`, `\autoref{}`, `\ref{}`, `\eqref{}`, `\label{}`, etc.
- All special characters and escapes: `\%`, `\&`, `\$`, `~`, `---`, `--`, etc.
- All math mode content: `$...$`, `\[...\]`, equation environments, etc.
- All custom commands defined by the authors

Before finalizing ANY suggestion, verify that every LaTeX command present in the original text is preserved in the suggested text (unless the specific purpose of the edit is to remove that formatting). Failure to preserve LaTeX syntax makes suggestions unusable.


---

## Module 1: Typos and Misspelled Words

Read through the entire paper and identify all typos and misspelled words.

**What counts as a typo:**

- Misspelled words
- Repeated words
- Missing spaces (but NOT extra spaces — LaTeX collapses multiple spaces)
- Transposed letters
- Wrong word in context (real word, but clearly not intended)
- Extra words
- Inconsistent spelling of the same word across the document

**What does NOT count as a typo:**

- LaTeX commands or syntax
- Extra spaces or double spaces (LaTeX collapses these — they are not errors)
- Intentional abbreviations or acronyms
- Technical terms, variable names, or jargon specific to the field
- Author names or proper nouns (unless clearly wrong)

**How to check for typos:**

For EVERY word, verify:

1. **Spelling**: Is the word spelled correctly?
2. **Intended word**: Is this the word the author meant, or is it a different word that happens to be spelled correctly?
3. **Duplication**: Is this word accidentally repeated?
4. **Consistency**: Is this word spelled/formed the same way elsewhere in the document?

**OUTPUT ORDER REQUIREMENT:**  
List all typos in order of appearance in the document (by file, then by line number).

**Labeling:** Label each typo as T1, T2, T3, ... (T for Typo)

**Do NOT proceed to Module 2 yet.** Wait until Modules 1 and 2 are both complete to present the combined report.


---

## Module 2: Grammar Issues

Read through the entire paper and identify all grammar issues.

**What counts as a grammar issue:**

- Missing or incorrect articles (a, an, the)
- Subject-verb agreement errors
- Incorrect verb tenses
- Incorrect prepositions
- Run-on sentences or comma splices
- Sentence fragments
- Pronoun-antecedent disagreement
- Dangling or misplaced modifiers
- Incorrect idioms
- Missing or incorrect plurals

**What does NOT count as a grammar issue:**

- Stylistic choices that are grammatically acceptable
- Field-specific conventions
- Minor preferences between equally correct options

**How to check for grammar issues:**

For EVERY sentence, systematically verify:

1. **Subject-verb agreement**: Identify the subject of each verb. Verify they agree in number.
   - Be careful when words appear between subject and verb
   - Be careful with abstract or collective nouns — they are usually singular
   - Be careful with compound subjects

2. **Noun number**: For each noun, verify singular vs. plural is correct for the context.
   - After words like "across", "among", "between", "various", "different", "multiple", "several", "each", "every" — check whether the following noun should be singular or plural
   - Check that parallel nouns have consistent number

3. **Prepositions**: Check each preposition fits its context.
   - Movement/destination typically requires "to" (move to, add to, send to)
   - Location typically requires "in", "at", or "on"
   - Check for missing prepositions

4. **Articles**: For each noun phrase, check whether it needs "a", "an", "the", or no article.
   - Check for missing articles
   - Check for extra articles (especially before clauses starting with "whether", "how", "what", etc.)

5. **Verb forms**: Check that each verb has the correct form.
   - Correct tense for context
   - Correct form after auxiliaries (e.g., "made us realize" not "made us realized")

**OUTPUT ORDER REQUIREMENT:**  
List all grammar issues in order of appearance in the document (by file, then by line number).

**Labeling:** Label each grammar issue as G1, G2, G3, ... (G for Grammar)


---

## Combined Report: Modules 1 & 2

After completing BOTH Module 1 and Module 2, present a single report with two clearly separated sections.

**Format each item using a code block for alignment:**

```
## TYPOS (Module 1)

**T1** (filename.tex, line XX)
```
Original : ...

Suggested: ...
```

**T2** (filename.tex, line XX)
```
Original : ...

Suggested: ...
```

[etc.]

---

## GRAMMAR (Module 2)

**G1** (filename.tex, line XX)
```
Original : ...

Suggested: ...
```

**G2** (filename.tex, line XX)
```
Original : ...

Suggested: ...
```

[etc.]
```

If a module has no issues, simply state "No typos found" or "No grammar issues found."

**STOP and wait for approval.**

When you stop, write:

```
STOPPED - AWAITING YOUR INPUT

You may:
- Ask questions or request clarifications
- Tell me which corrections to implement (e.g., "implement T1, T3, G2, G5")
- Say "move to next" to proceed to Module 3
```

**Do NOT proceed to Module 3 until I explicitly say "move to next"**


### CRITICAL: Maintaining Consistency Based on User Feedback

**If you provide ANY corrections, clarifications, or modifications to my audit approach at any stop point, I MUST apply those same corrections/modifications consistently to ALL remaining modules and sections in the audit.**

This includes but is not limited to:

- **Classification changes**: If you say "this is not a typo, it's correct terminology," I must not flag similar terminology anywhere else
- **Scope clarifications**: If you say "don't flag X as an issue," I must never flag X in any remaining modules
- **Style preferences**: If you indicate you prefer a certain phrasing or construction, I must not suggest changing it in later sections
- **Technical term exceptions**: If you clarify that a term is field-specific jargon, I must not flag it as a typo or suggest changing it later
- **Grammar conventions**: If you approve a certain grammatical construction (e.g., singular vs. plural usage), I must apply that standard throughout
- **Threshold adjustments**: If you say "only flag sentences longer than 50 words," I must apply that threshold in all remaining modules

**Before proceeding to each new module, I must review all feedback you have provided on previous modules and ensure I apply it consistently.**

**I must NEVER flag the same issue type again after you have indicated it should not be flagged.**


### Implementing Corrections in Modules 1 & 2

When I say **"implement correction XX"** (e.g., "implement T1, G3"), you must apply the change by **directly replacing** the original text with the corrected text.

**Example:**

If the original is:
```
This sentance has a typo.
```

And the suggested correction is:
```
This sentence has a typo.
```

Then the **implemented version** should simply be:
```
This sentence has a typo.
```

**Rules for implementation:**

1. Show the full corrected line(s) ready to copy-paste into the LaTeX source
2. Preserve all surrounding LaTeX commands and formatting
3. Provide the file name and line number(s) for reference
4. **Do NOT use track-changes markup** (`\rsout{}`, `\red{}`, etc.) — just provide the clean corrected text


---

## Module 3: Light Syntax Review

Read through the entire paper and suggest **minor** syntax improvements.

**Scope of "light" review:**

- Sentences that are too long and could be split
- Awkward phrasing that has a simple fix
- Unclear sentences where a small rewording helps
- Passive voice that would be clearer as active (only if the fix is simple)
- Word choice improvements (only if clearly better, not just different)

**Constraints:**

- **Do NOT rewrite paragraphs** — suggest sentence-level changes only
- **Do NOT change the author's voice or style** — preserve tone
- **Do NOT make changes for the sake of change** — only flag genuine improvements
- **Minimize changes** — if a sentence is acceptable, leave it alone
- **Be conservative** — when in doubt, do not include it

**OUTPUT ORDER REQUIREMENT:**  
List all suggestions in order of appearance in the document (by file, then by line number).

**Labeling:** Label each suggestion as S1, S2, S3, ... (S for Syntax-light)

**Report format (use code blocks for alignment):**

```
## LIGHT SYNTAX SUGGESTIONS (Module 3)

**S1** (filename.tex, line XX)
```
Original : ...

Suggested: ...
```
Reason: [brief explanation — e.g., "sentence too long", "unclear referent"]

**S2** (filename.tex, line XX)
```
Original : ...

Suggested: ...
```
Reason: [brief explanation]

[etc.]
```

If no suggestions, state "No light syntax suggestions."

**STOP and wait for approval.**

When you stop, write:

```
STOPPED - AWAITING YOUR INPUT

You may:
- Ask questions or request clarifications
- Tell me which corrections to implement (e.g., "implement S1, S4, S7")
- Say "move to next" to proceed to Module 4
```

**Do NOT proceed to Module 4 until I explicitly say "move to next"**

### Implementing Suggestions in Module 3

When I say **"implement suggestion XX"** (e.g., "implement S2, S5"), you must apply the change by **directly replacing** the original text with the suggested text.

**Example:**

If the original is:
```
The model, which we describe in the next section, is important.
```

And the suggested rewrite is:
```
The model described in the next section is important.
```

Then the **implemented version** should simply be:
```
The model described in the next section is important.
```

**Rules for implementation:**

1. Show the full corrected line(s) ready to copy-paste into the LaTeX source
2. Preserve all surrounding LaTeX commands and formatting
3. Provide the file name and line number(s) for reference
4. **Do NOT use track-changes markup** (`\rsout{}`, `\red{}`, etc.) — just provide the clean corrected text


---

## ⚠️ STOP: FORMAT CHANGE FOR MODULES 4–5 ⚠️

**Starting with Module 4, ALL suggestions must use track-changes markup.**

This applies to BOTH the suggestions you write AND the implementations.

- **Deleted text**: `\rsout{deleted text}`
- **Added text**: `\red{added text}`

**Example of CORRECT Module 4/5 suggestion:**

```
**D1** (intro.tex, line 12)
```
Original : This is a verbose and unnecessarily wordy sentence.

Suggested: This is a \rsout{verbose and unnecessarily wordy}\red{concise} sentence.
```
```

**Example of WRONG Module 4/5 suggestion:**

```
**D1** (intro.tex, line 12)
```
Original : This is a verbose and unnecessarily wordy sentence.

Suggested: This is a concise sentence.
```
```

The WRONG example fails because it does not show which text is deleted and which is added. **Always use `\rsout{}` and `\red{}` in Modules 4–5.**

---

## Module 4: Deep Syntax Review

**⚠️ FORMATTING: Use `\rsout{}` and `\red{}` markup in ALL suggestions below.**

Read through the entire paper and suggest **substantial** syntax improvements.

**Scope of "deep" review:**

- Paragraphs that could be restructured for clarity
- Sections where the argument flow is confusing
- **Repetition across the paper** — flag where the same idea is stated multiple times in different sections
- **Repetition within paragraphs** — flag where the same point is made twice in slightly different words
- Sentences that should be combined or reordered
- Transitions between paragraphs that are missing or weak
- Places where the writing is verbose and could be tightened significantly
- Wordy phrases that have simple replacements (e.g., "in order to" → "to", "due to the fact that" → "because")
- Weak or vague language (e.g., "makes a lot of sense", "is related to an important dimension")
- Informal language inappropriate for academic writing (e.g., "copy-paste", "with horror")
- Filler phrases that add nothing (e.g., "After carefully reviewing", "It is important to note that")
- Unnecessary hedging (e.g., "We think that..." when you can just state the point)

**How to handle repetition:**

When you identify repetition, report:

1. All locations where the repeated content appears
2. Which instance (if any) should be kept
3. Suggested deletions or consolidations

**Labeling:** Label each suggestion as D1, D2, D3, ... (D for Deep syntax)

**For repetition issues:** Label as R1, R2, R3, ... (R for Repetition)

**OUTPUT ORDER REQUIREMENT:**  
- List D suggestions in order of appearance
- List R suggestions separately at the end, grouped by the repeated content

**Report format — MUST USE `\rsout{}` AND `\red{}`:**

```
## DEEP SYNTAX SUGGESTIONS (Module 4)

**D1** (filename.tex, line XX)
```
Original : This sentence is too wordy and could be tightened up significantly.

Suggested: This sentence \rsout{is too wordy and could be tightened up significantly}\red{could be tightened}.
```
Reason: [explanation]

**D2** (filename.tex, lines XX-YY)
```
Original : We think that the results are interesting. The results show that...

Suggested: \rsout{We think that the results are interesting. The results}\red{The results are interesting and} show that...
```
Reason: [explanation]

[etc.]

---

## REPETITION ISSUES (Module 4)

R1: [Brief description of what is repeated]
- Location 1: filename.tex, line XX — `[text]`
- Location 2: filename.tex, line YY — `[text]`
- Location 3: filename.tex, line ZZ — `[text]`
Suggestion: Keep location 1, delete locations 2 and 3 (or consolidate as follows: `...`)

R2: [Brief description]
...

[etc.]
```

If no suggestions, state "No deep syntax suggestions" and/or "No repetition issues found."

**STOP and wait for approval.**

When you stop, write:

```
STOPPED - AWAITING YOUR INPUT

You may:
- Ask questions or request clarifications
- Tell me which corrections to implement
- Say "move to next" to proceed to Module 5 (Polish Pass)
- Say "done" to end the audit here
```

**Do NOT proceed to Module 5 until I explicitly say "move to next"**

### Implementing Suggestions in Module 4

When I say **"implement suggestion XX"** (e.g., "implement D3"), provide the full text with track-changes markup ready to copy-paste.

Since your suggestions already use `\rsout{}` and `\red{}`, implementation is straightforward: just provide the "Suggested" line with full context.

**Example:**

Your suggestion was:
```
Suggested: This sentence \rsout{is too wordy and could be tightened up significantly}\red{could be tightened}.
```

The **implemented version** is the same:
```
This sentence \rsout{is too wordy and could be tightened up significantly}\red{could be tightened}.
```

**Rules for implementation:**

1. Show the full implemented line(s) ready to copy-paste into the LaTeX source
2. Preserve all surrounding LaTeX commands and formatting
3. If only part of a sentence changes, only mark the changed portion with `\rsout{}` and `\red{}`
4. Provide the file name and line number(s) for reference


---

## Module 5: Substantive Rewriting (Optional)

**⚠️ FORMATTING: Use `\rsout{}` and `\red{}` markup in ALL suggestions below.**

This module is optional. Only proceed if explicitly requested.

In this module, you have **freedom to rewrite substantially**. The goal is to make the writing as clear, direct, and elegant as possible.

**What you can do in Module 5:**

- Rewrite entire paragraphs from scratch if the original is unclear or convoluted
- Restructure explanations to be easier to follow
- Propose significantly shorter versions of verbose passages
- Combine multiple weak sentences into one strong sentence
- Suggest cutting content that is unnecessary or redundant
- Reorganize the order of ideas within a section
- Replace jargon-heavy or abstract passages with concrete, direct prose

**Constraints:**

- **Preserve the author's meaning** — rewrites must convey the same information
- **Preserve technical accuracy** — do not simplify in ways that lose precision
- **Preserve academic tone** — do not make the writing casual
- **Preserve ALL LaTeX formatting** — every `\underline{}`, `\textit{}`, `\autoref{}`, `\cite{}`, and other LaTeX command in the original MUST appear in the rewritten version (unless the edit specifically intends to remove it). This is critical: suggestions that strip LaTeX commands are unusable.
- **Flag uncertainty** — if a rewrite might alter meaning, note this explicitly
- **Focus on rendered output** — do not flag LaTeX source formatting (whitespace, line breaks)

**How to do substantive rewriting:**

For EVERY paragraph, ask yourself: **"What is the clearest, most direct way to say this?"**

If your answer differs significantly from what's written, propose a rewrite.

Look especially for:
1. **Convoluted explanations**: Is there a simpler way to explain this?
2. **Buried key points**: Is the main takeaway clear, or hidden in subordinate clauses?
3. **Unnecessary complexity**: Is the author using three sentences where one would do?
4. **Weak openings**: Does the paragraph start with the point, or does it throat-clear first?
5. **Passive obscuring agent**: Would active voice make the sentence clearer?

**Minimum expectation:**

Academic writing almost always benefits from tightening. If you find fewer than 5 substantive suggestions on a multi-page document, you are not engaging deeply enough. Re-read and ask: "How would I rewrite this to be clearer?"

**Labeling:** Label each suggestion as P1, P2, P3, ... (P for Polish)

**Report format — MUST USE `\rsout{}` AND `\red{}`:**

For each suggestion, show the original and your proposed rewrite using track-changes markup. For substantial rewrites, briefly explain what you changed and why.

```
**P1** (filename.tex, lines XX-YY)
```
Original : Thank you for your thoughtful comments. We appreciate the opportunity to revise our paper. Below we describe the changes.

Suggested: Thank you for your \rsout{thoughtful }comments\rsout{. We appreciate the opportunity to revise our paper. Below we}\red{; we} describe the changes\red{ below}.
```
Reason: [what you improved — e.g., "restructured for clarity", "cut redundancy", "made key point explicit"]
```

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

### Implementing Suggestions in Module 5

When I say **"implement suggestion XX"** (e.g., "implement P3"), provide the full text with track-changes markup ready to copy-paste.

Since your suggestions already use `\rsout{}` and `\red{}`, implementation is straightforward: just provide the "Suggested" line with full context.

**Example:**

Your suggestion was:
```
Suggested: Thank you for your \rsout{thoughtful }comments\rsout{. We appreciate the opportunity to revise our paper. Below we}\red{; we} describe the changes\red{ below}.
```

The **implemented version** is the same:
```
Thank you for your \rsout{thoughtful }comments\rsout{. We appreciate the opportunity to revise our paper. Below we}\red{; we} describe the changes\red{ below}.
```

**Rules for implementation:**

1. Show the full implemented line(s) ready to copy-paste into the LaTeX source
2. Preserve all surrounding LaTeX commands and formatting
3. If only part of a sentence changes, only mark the changed portion with `\rsout{}` and `\red{}`
4. Provide the file name and line number(s) for reference


---

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

After completing your first pass through Modules 1 and 2, do a second pass through the entire document applying the systematic checks described above. The first pass catches obvious errors; the second pass catches errors that require careful grammatical analysis.
