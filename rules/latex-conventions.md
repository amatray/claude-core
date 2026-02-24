# LaTeX Conventions

## Understanding the Input Files

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

## Format of Suggested Corrections

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
