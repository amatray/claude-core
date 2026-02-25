# How to Prevent Figure Legend Cropping - Complete Solution

## The Problem

Figures with legends at the bottom were being cropped - the legend was cut off at the slide margin.

## Root Cause Analysis

**What I was doing wrong:**
```latex
\includegraphics[height=.85\textheight]{figure.pdf}
```

**Why this caused cropping:**
1. `height=.85\textheight` FIXES the figure height rigidly to 85% of text height
2. LaTeX scales the ENTIRE PDF to this height
3. If the figure PDF has:
   - Plot area taking 80% of vertical space
   - Legend taking 20% at bottom
4. And I make the figure too tall → the bottom 20% (the legend) gets cropped by the slide margin
5. Different figures have different aspect ratios and internal layouts → one-size-fits-all fails

**The fundamental error**: Using height-based sizing without inspecting each figure's internal content distribution.

## The Complete Solution

### Pattern A: Standard Width Figures (PREFERRED - 100% PREVENTS CROPPING)

**State-of-the-art pattern from existing presentations:**

```latex
\begin{frame}{Title}

\centering
\begin{minipage}[t][8cm][t]{\textwidth}
	\begin{columns}[T]
		\begin{column}{1\textwidth}
			\only<1>{\resizebox{\textwidth}{!}{
				\includegraphics[height=.8\textheight]{figure.pdf}
			}}
		\end{column}
	\end{columns}
\end{minipage}

\end{frame}
```

**How `\resizebox` prevents cropping:**
- `\resizebox{\textwidth}{!}{...}` scales content to fit `\textwidth` width
- The `!` means: maintain aspect ratio, auto-calculate height
- Inner `\includegraphics[height=.8\textheight]{}` provides suggested size
- **Result**: Width is primary constraint, height adjusts automatically to figure's aspect ratio
- If figure has legend → total height increases naturally → **legend never cropped**

**Critical rule**: ALWAYS use `\resizebox{\textwidth}{!}{...}` for standard-width figures. NEVER use `\includegraphics[height=...]` directly.

### Pattern B: Full-Bleed Figures (For Maximum Size)

When you need figures to use the full slide width including margins:

```latex
\begin{frame}{Title}

\begin{minipage}[t][.5cm][t]{\textwidth}
{\small
    \only<1>{\centering{[subtitle text]}}
}
\end{minipage}

\hspace*{-1.cm}
\begin{minipage}[t][9cm][t]{1.3\textwidth}
    \begin{columns}[T]
        \begin{column}{1\textwidth}
            \only<1>{
                \includegraphics[height=.85\textheight]{figure.pdf}
            }
        \end{column}
    \end{columns}
\end{minipage}

\end{frame}
```

**When to use Pattern B:**
- When figures need maximum size to show detail
- When the `{1.3\textwidth}` provides enough width that direct height sizing works
- This is the ONLY acceptable case for using `\includegraphics[height=...]` without `\resizebox`

### Pattern C: Equation/Text + Figure (Narrower Column)

When you have text/bullets above figure:

```latex
\begin{frame}{Title}

\vspace{-.2cm}
\begin{minipage}[t][1cm][t]{\textwidth}
\begin{itemize}
{
\only<1>{\footnotesize\item Explanation}
}
\end{itemize}
\end{minipage}

\centering
\begin{minipage}[t][9cm][t]{\textwidth}
\begin{columns}[T]
\begin{column}{.70\textwidth}
    \only<1>{\resizebox{\textwidth}{!}{
      \includegraphics[height=1.46cm,width=2cm]{figure.pdf}
    }}
\end{column}
\end{columns}
\end{minipage}

\vspace{-1cm}
\end{frame}
```

**Key features:**
- Text minipage: `[t][1cm][t]` (small height)
- Figure minipage: `[t][9cm][t]` (tall to accommodate figures)
- Column: `.70\textwidth` (narrower than full width)
- Still uses `\resizebox{\textwidth}{!}{...}` wrapper

## Systematic Prevention Strategy

### 1. Layout Critic MUST Check pdflatex Warnings FIRST

**MANDATORY FIRST STEP - 100% HIT RATE REQUIRED:**

```bash
# Compile presentation
pdflatex -interaction=nonstopmode presentation.tex 2>&1 > compile.log

# Check for warnings
grep "Overfull\|Underfull" compile.log
```

**Detection rules - ZERO TOLERANCE:**
- **ANY `Overfull \vbox` warning, even 1pt → AUTOMATIC CRITICAL VIOLATION (-10)**
- **ANY `Overfull \hbox` warning → AUTOMATIC IMPORTANT VIOLATION (-5)**
- LaTeX compiler tells you EXACTLY when content doesn't fit
- 100% reliable signal - NO excuse for missing
- **There is NO such thing as an "acceptable" overfull vbox warning**
- Even 1-3pt overfull means figure legends are being cropped
- The ONLY acceptable outcome is ZERO overfull vbox warnings

**Example warnings:**
```
Overfull \vbox (16.0747pt too high) detected at line 535
  → Figure/minipage is 16pt too tall, encroaching on bottom margin
  → Fix: Use \resizebox or reduce dimensions

Overfull \vbox (1.71634pt too high) detected at line 466
  → Minor overfull (< 3pt) - usually acceptable
  → But can still be fixed with \resizebox pattern
```

### 2. Template Assembler Must Use Correct Patterns

**Checklist for every figure slide:**
- [ ] Is this standard width (`\textwidth`) or full-bleed (`{1.3\textwidth}`)?
- [ ] If standard width: MUST use `\resizebox{\textwidth}{!}{...}` wrapper
- [ ] If full-bleed: Can use direct `\includegraphics[height=...]` with `\hspace*{-1.cm}`
- [ ] Use minipage `[t][8cm][t]{\textwidth}` for figure-only slides
- [ ] Use minipage `[t][7cm][t]{\textwidth}` for equation+figure slides
- [ ] NO `\centering` inside column when using `\resizebox`

### 3. Why This Approach Works

**The key insight**:
- **Width-based sizing** (via `\resizebox{\textwidth}{!}{...}`) makes width the primary constraint
- Height adjusts automatically based on figure's aspect ratio
- If figure has legend at bottom → height naturally increases → legend visible
- If figure has no legend → height naturally decreases → no wasted space
- One pattern works for ALL figures regardless of internal layout

**Contrast with height-based sizing:**
- `\includegraphics[height=.85\textheight]{}` FIXES height
- Doesn't adapt to figure's internal layout
- Legend gets cropped if height is too aggressive
- Requires manual inspection of each figure → error-prone

## Summary

**Never again crop legends:**
1. **Use `\resizebox{\textwidth}{!}{...}` for all standard-width figures**
2. **Layout Critic checks pdflatex warnings FIRST**
3. **Any overfull vbox = automatic fail**
4. **100% hit rate achievable and expected**

The solution is systematic, reliable, and eliminates the entire class of legend-cropping errors.
