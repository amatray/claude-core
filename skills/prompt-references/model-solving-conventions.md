# Model-Solving LaTeX Conventions

*Consult this file before writing any LaTeX output in the solve-model workflow. For general LaTeX conventions (resizebox, booktabs, autoref), also read `prompt-references/latex-research.md`.*

---

## Notation Table

Use this format in `model_setup.tex` for the variable/parameter listing:

```latex
\begin{table}[h]
\caption{Model Notation}
\begin{tabular}{llll}
\toprule
Symbol & Name & Type & Domain \\
\midrule
$k$ & Capital & Choice & $\mathbb{R}_+$ \\
$\theta$ & Pledgeability & Parameter & $[0,1]$ \\
\bottomrule
\end{tabular}
\end{table}
```

Type is one of: Choice, State, Parameter, Price, Multiplier. Domain uses standard math notation ($\mathbb{R}_+$, $(0,1)$, $[0,1]$, etc.).

---

## Assumption Numbering

Number assumptions sequentially with `\paragraph{}`:

```latex
\paragraph{Assumption A1:} Production is Cobb-Douglas: $f(k) = Ak^\alpha$, $\alpha \in (0,1)$.

\paragraph{Assumption A2:} The firm can pledge at most fraction $\theta$ of capital as collateral.
```

Reference assumptions in derivation steps as "by A1" or "using Assumption A2."

---

## Derivation Step Format

Each step in `derivation.tex` uses this template:

```latex
\paragraph{Step N: [Short description]}
\textit{Operation: [Plain English description of the algebraic operation. Reference source equations by step number.]}

\begin{align}
  [display math showing the operation and result] \label{eq:stepN}
\end{align}

\textit{Simplification: [Explain what was simplified and how.]} % omit if no simplification

\begin{align}
  [simplified result] \label{eq:stepN-simplified}
\end{align}
```

Rules:
- One algebraic operation per step. If more than one manipulation is needed, use substeps (Step 4a, 4b, ...).
- Every substitution references its source: "Substitute $\lambda$ from Step 3."
- No shortcuts: never write "it can be shown that" or "by inspection."

---

## `% VERIFY` Marker Convention

Place the `% VERIFY` marker at the end of the `\paragraph` line for flagged steps:

```latex
\paragraph{Step 4: Substitute $\lambda$ into capital FOC} % VERIFY
```

Flag any step that involves:
- Sign determinations or inequality claims
- Multi-step simplifications
- Theorem applications (envelope, IFT, Leibniz)
- Concavity/convexity claims
- Existence/uniqueness arguments
- Limit or L'Hopital applications

Also flag any step containing weasel phrases ("clearly", "trivially", "obviously", "straightforward", "by inspection", "by symmetry", "without loss of generality", "immediately follows", "it can be shown", "one can verify that", "a simple calculation shows", "it is easy to see").

---

## Verification Log Format

In `verification_log.tex`, use this format for each checked step:

```latex
\paragraph{Verification: Step N}
\begin{itemize}
  \item \textbf{Dimensional check}: PASS/FAIL --- [unit breakdown]
  \item \textbf{Limiting cases}: PASS/FAIL --- [parameter $\to$ limit, result, intuition]
  \item \textbf{Numerical spot-check}: PASS/FAIL --- [LHS=X, RHS=Y, diff=Z]
  \item \textbf{Oracle re-derivation}: AGREE / DISAGREE / NOT SELECTED --- [details]
\end{itemize}
```

Always show all 4 rows. Steps not sent to Oracle use "NOT SELECTED."

---

## Comparative Statics Table

In `comparative_statics.tex`, use booktabs with a Condition column:

```latex
\begin{table}[h]
\caption{Comparative Statics Summary}
\begin{tabular}{llclp{6cm}}
\toprule
Parameter & Variable & Sign & Condition & Intuition \\
\midrule
$\theta$ $\uparrow$ & $k$ & $+$ & Constrained & More pledgeable capital allows more borrowing \\
$\theta$ $\uparrow$ & $k$ & $0$ & Unconstrained & First-best unaffected by constraint \\
\bottomrule
\end{tabular}
\end{table}
```

Wrap in `\resizebox{1\linewidth}{!}{}` only if the table is too wide for the page.

---

## `full_model.tex` Skeleton

The final assembled document uses `\input{}` for each phase file:

```latex
\documentclass[12pt]{article}
\usepackage{amsmath,amssymb,amsthm,booktabs,graphicx,hyperref}

\title{Model: [Name] \\ \large Derivation and Verification Document}
\author{[User] \\ \small Generated with Claude Code + Oracle verification}
\date{\today}

\begin{document}
\maketitle
\tableofcontents

\section{Model Environment}
\input{model_setup.tex}

\section{Derivation}
\input{derivation.tex}

\section{Verification Log}
\input{verification_log.tex}

\section{Comparative Statics}
\input{comparative_statics.tex}

\appendix
\section{Parameter Values Used in Numerical Checks}
[Table of parameter values used in spot-checks]

\section{Oracle Session Transcripts}
[Summary of Oracle calls: what was sent, what was received]

\end{document}
```

Per-phase `.tex` files are fragments (no `\documentclass`). Only `full_model.tex` is compilable. Compile with `cd solving_models/[name]/ && xelatex full_model.tex` since `\input{}` paths are relative.
