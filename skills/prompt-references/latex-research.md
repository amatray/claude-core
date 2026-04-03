# LaTeX Research Output Conventions

*Consult this file when producing or editing LaTeX for research papers, appendices, or reply letters.*

---

## Tables
- **Caption placement:** `\caption{Title}` goes **above** the table content. The caption should contain only the title (short, descriptive). Detailed notes go **below** the table in a `\textit{Notes:}` block (typically in `\scriptsize` or `\footnotesize`).
- When a table risks overflowing page margins (many columns, wide regression tables), wrap the tabular environment in `\resizebox{1\linewidth}{!}{ ... }`. Do NOT apply to narrow tables that fit within margins.
- **Table header rows:** The rows between `\toprule` and the column numbers follow a consistent pattern. Each metadata row has an italicized label in the first column and values spanning the data columns. Standard order:
  1. `\textit{Dependent variable} & \multicolumn{N}{c}{Variable Name} \\` + `\cmidrule(r){2-N}`
  2. Additional metadata rows (e.g., `\textit{EXIM exposure}`, `\textit{Level of aggregation}`, `\textit{Sample}`) with column-group `\multicolumn` spans
  3. `\cmidrule` separators under column groups
  4. Column numbers `(1) (2) ...`
  5. `\midrule` separating the header from the coefficient body (in `esttab`, use `posthead(\midrule)`)
  
  Do NOT place metadata like exposure level, sample definition, or level of aggregation at the bottom of the table as stats. They belong in the header. Do NOT embed labels inside the multicolumn (e.g., do NOT write `& \multicolumn{N}{c}{\textit{Dep. var.: ...}} \\`).
- Exception: skip resizebox if the table already uses `\adjustbox`, `\scalebox`, or another sizing wrapper.
- Use `\toprule`, `\midrule`, `\bottomrule` (booktabs) instead of `\hline`.
- **Fixed effects section:** Fixed effects must be visually separated from coefficients. The first FE row must be preceded by `\\[-1.8ex]\hline\addlinespace\textit{Fixed Effects} \\`. Each individual FE is indented with `\hspace{1.5em}`. FE indicators use `$\checkmark$` / `---`. In `esttab`/`estfe`, the first FE label carries the full prefix (e.g., `"\\[-1.8ex]\hline\addlinespace\textit{Fixed Effects} \\ \hspace{1.5em}Year"`); subsequent FEs use only `"\hspace{1.5em}..."`. Do NOT place FE indicators inline with coefficients without the separator line and header.

## Figures

**Every figure must pass ALL THREE checks independently. Do not stop after fixing one.**

1. **Caption position:** `\caption{...}` goes ABOVE the figure content (before `\includegraphics`).
2. **Caption content:** The `\caption{...}` must contain ONLY a short title (typically under 15 words). If the caption contains methodology, data descriptions, variable definitions, or any sentence longer than a title, it is WRONG. Move that text to the notes block below.
3. **Notes below:** Detailed description goes BELOW the figure in a notes block with `\justify` to cancel `\centering`.

**Correct pattern:**
```latex
\begin{figure}[htbp]
\caption{Short Title Only}
\label{fig:xxx}
\centering
\includegraphics[width=0.8\textwidth]{...}
\justify
{\scriptsize
\begin{singlespace}
\textit{Notes:} Full description goes here...
\end{singlespace}}
\end{figure}
```

**Wrong (description in caption):**
```latex
% BAD - everything crammed into \caption
\caption{Event study: impact of X on Y. Each point represents the coefficient on...
  with product x year and importer x year fixed effects. Clustered at...}
```

- **Event study / CI figures:** Start the note with: "This figure plots the point estimates and 95\% confidence intervals..." Do NOT say "whiskers denote 95\% confidence intervals" separately.
- Use `\includegraphics[width=\linewidth]{...}` unless a specific size is needed.

## Cross-references
- For figures, tables, and sections: use `\autoref{XX}` instead of `Figure~\ref{XX}`, `Table~\ref{XX}`, or `Section~\ref{XX}`.
- `\autoref` must produce capitalized names (Section, Figure, Table). If the preamble does not already define them, add:
  ```latex
  \def\sectionautorefname{Section}
  \def\subsectionautorefname{Section}
  \def\subsubsectionautorefname{Section}
  \def\figureautorefname{Figure}
  \def\tableautorefname{Table}
  ```

## Citations
- Use `\cite{key}` for in-text citations: produces "Author (Year)".
- Use `\citep{key}` for parenthetical citations: produces "(Author, Year)".
- `\citet{key}` should also produce "Author (Year)" — verify the preamble definition matches this.
- Always verify bib keys exist in the `.bib` file before using them.
- **Conjugation with citations:** A citation refers to a *paper* (singular), not to the authors (plural). Use third-person singular verb forms: "\citet{SmithJones2020} **shows**" not "show", "\citet{ABC2021} **formalizes**" not "formalize", etc.
- **No "see" before "e.g." in citations:** Write `\citep[e.g.,][]{key}`, never `\citep[see, e.g.,][]{key}`. The "see" is redundant.

## Fonts and compilation
- When compiling with xelatex, ensure bold fonts are available. If using `mathpazo` (Palatino), add `\usepackage{fontspec}` and `\setmainfont{Palatino}` to get bold/italic support in TU encoding.
