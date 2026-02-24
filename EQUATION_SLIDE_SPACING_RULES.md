# Equation Slide Spacing Rules - SYSTEMATIC IMPLEMENTATION

## The Problem

Equation slides were having spacing issues:
1. Too much space between title and first sentence on dense slides
2. Too much space between first sentence and equation
3. Minipage overlap - equation minipage + text minipage heights exceeded available space

## The Systematic Solution

### Rule 1: Dense Slides - Reduce Title Spacing

**When slide is full/dense, reduce space between title and content:**

```latex
\begin{frame}{Title}

\vspace{-.2cm}  % ← MANDATORY for dense slides

[content]
```

**When to use:**
- Equation + figure slides (always dense)
- Equation-only slides with multiple bullet points
- Any slide where vertical space is tight

### Rule 2: Minimal Spacing Between Intro and Equation

**Eliminate or minimize spacing between intro sentence and equation:**

**WRONG** (too much space):
```latex
{\small
Intro sentence:

\medskip  % ← TOO MUCH SPACE

{\footnotesize
equation
}}
```

**CORRECT** (minimal space):
```latex
{\small
Intro sentence:
}

\smallskip  % ← Minimal spacing, or none at all

{\footnotesize
equation
}
```

### Rule 3: Systematic Minipage Height Calculation

**Available content height:** ~9cm (after accounting for title ~1cm)

**With \vspace{-.2cm}:** Saves 0.2cm → Available: 9cm + 0.2cm = 9.2cm

#### Pattern A: Equation + Figure

**Structure:**
```latex
\begin{frame}{Title}

\vspace{-.2cm}

\begin{minipage}[t][0.5cm][t]{\textwidth}
\centering
{\small
Intro sentence:
{\scriptsize or \footnotesize
equation
}}
\end{minipage}

\centering
\begin{minipage}[t][7cm][t]{\textwidth}
    [figure columns]
\end{minipage}

\end{frame}
```

**Height calculation:**
- Title: ~1cm
- vspace: -0.2cm (saved)
- Equation minipage: 0.5cm
- Figure minipage: 7cm
- Total: 1cm - 0.2cm + 0.5cm + 7cm = 8.3cm ✓ (fits in 9cm)

**Why 0.5cm for equation minipage?**
- VERY small - just enough for intro + single-line equation
- No extra spacing inside
- Keeps equation compact

**Why 7cm for figure minipage?**
- Calculated as: 9.2cm (available) - 0.5cm (equation) - spacing = ~7cm
- Leaves buffer for spacing between minipages

#### Pattern B: Equation-Only (No Figure)

**Structure:**
```latex
\begin{frame}{Title}

\vspace{-.2cm}

\begin{minipage}[t][2cm][t]{\textwidth}
{\small
Intro sentence:
}

\smallskip

{\footnotesize
multi-line equation (align*)
}
\end{minipage}

\medskip

\begin{minipage}[t][5.5cm][t]{\textwidth}
{\footnotesize
\begin{itemize}
    [bullet points explaining terms]
\end{itemize}
}
\end{minipage}

\end{frame}
```

**Height calculation:**
- Title: ~1cm
- vspace: -0.2cm (saved)
- Equation minipage: 2cm (for intro + multi-line equation)
- \medskip: ~0.2cm
- Text minipage: 5.5cm
- Total: 1cm - 0.2cm + 2cm + 0.2cm + 5.5cm = 8.5cm ✓ (fits in 9cm)

**Why 2cm for equation minipage?**
- Enough for intro sentence + 2-line align* equation
- With \smallskip spacing inside

**Why 5.5cm for text minipage?**
- Calculated as: 9.2cm (available) - 2cm (equation) - 0.2cm (medskip) = 7cm
- But use 5.5cm to leave margin for safety
- Enough for 6-7 bullet points with \footnotesize

### Rule 4: Font Sizes

**Equation + figure slides:**
- Intro text: `{\small ...}`
- Equation: `{\scriptsize ...}` (very compact)

**Equation-only slides:**
- Intro text: `{\small ...}`
- Equation: `{\footnotesize ...}` (more readable)
- Bullet points: `{\footnotesize ...}` in itemize wrapper

## Detection Rules for Layout Critic

**MANDATORY CHECK - 100% hit rate:**

```bash
pdflatex -interaction=nonstopmode presentation.tex 2>&1 | grep "Overfull.*vbox"
```

**If ANY overfull vbox warnings → FAIL (-10 per warning)**

**Common causes:**
1. Minipage heights too large (sum > 9cm)
2. Missing `\vspace{-.2cm}` on dense slides
3. Too much spacing between elements (\medskip instead of \smallskip)
4. Font sizes too large (not using \scriptsize or \footnotesize)

## Template Summary

| Slide Type | Title Space | Eq Minipage | Spacing | Text/Fig Minipage | Eq Font | Text Font |
|------------|-------------|-------------|---------|-------------------|---------|-----------|
| Eq + Fig | `\vspace{-.2cm}` | `0.5cm` | none | `7cm` | `\scriptsize` | `\small` |
| Eq only | `\vspace{-.2cm}` | `2cm` | `\smallskip` + `\medskip` | `5.5cm` | `\footnotesize` | `\small` + `\footnotesize` |

## Critical Rules - Zero Tolerance

1. **ALWAYS** use `\vspace{-.2cm}` after frame title on equation slides
2. **NEVER** use `\medskip` between intro and equation - use `\smallskip` or nothing
3. **ALWAYS** calculate: equation_minipage + spacing + text/fig_minipage ≤ 8.5cm
4. **ALWAYS** verify with pdflatex - ZERO overfull vbox warnings acceptable
5. **ALWAYS** use `\centering` for equation minipage on eq+fig slides (not on eq-only)

## Implementation in Agents

### Equation Writer Agent:
- MUST use these exact minipage dimensions
- MUST use `\vspace{-.2cm}` on all equation slides
- MUST use `\smallskip` or no spacing between intro and equation
- MUST use correct font sizes (\scriptsize for eq+fig, \footnotesize for eq-only)

### Layout Critic Agent:
- MUST check pdflatex warnings FIRST
- MUST verify minipage height calculations
- MUST check for `\vspace{-.2cm}` presence
- MUST check spacing between elements
- ANY overfull vbox → automatic -10 violation

This systematic approach eliminates ALL spacing and overlap issues on equation slides.
