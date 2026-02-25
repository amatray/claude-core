# Revised Diagnosis: Equation Slide Minipage Sizing

## The Correct Approach

**Key Insight**: Spacing between equation and text minipages should come from **properly sized minipages**, not from `\medskip` or `\bigskip` commands.

## How Minipage Height Creates Spacing

```latex
\begin{minipage}[t][2cm][t]{\textwidth}
{\small Intro:}
\smallskip
{\footnotesize
$$equation$$
}
\end{minipage}
% ← If equation only takes 1.5cm, there's 0.5cm of natural space at bottom

\begin{minipage}[t][5cm][t]{\textwidth}
% ← Starts here, creating visible gap from equation above
```

**The declared height (2cm) reserves vertical space**, even if content doesn't fill it. This creates natural spacing.

## Current Problem: Minipages Are Undersized

**Current configuration:**
```latex
\begin{minipage}[t][2cm][t]{\textwidth}  % ← Equation minipage
equation content (~1.8cm actual)
\end{minipage}

\medskip  % ← Shouldn't be needed!

\begin{minipage}[t][5.5cm][t]{\textwidth}  % ← Text minipage
```

**Issue**: Equation minipage (2cm) is barely larger than equation content (~1.8cm), leaving almost no buffer space. That's why we needed `\medskip` to create separation.

## The Systematic Solution

### Rule 1: Size Equation Minipage Based on Equation Lines

**One-line equation:**
```latex
\begin{minipage}[t][1.5cm][t]{\textwidth}
{\small Intro sentence:}
\smallskip
{\footnotesize
$$
y = mx + b
$$
}
\end{minipage}
% Actual content: ~1cm (intro + equation)
% Declared: 1.5cm
% Natural spacing at bottom: ~0.5cm ✓
```

**Two-line equation:**
```latex
\begin{minipage}[t][2.5cm][t]{\textwidth}
{\small Intro sentence:}
\smallskip
{\footnotesize
\begin{align*}
equation line 1 \\
equation line 2
\end{align*}
}
\end{minipage}
% Actual content: ~1.8-2cm (intro + 2-line equation)
% Declared: 2.5cm
% Natural spacing at bottom: ~0.5cm ✓
```

### Rule 2: Adjust Text Minipage to Maintain Total Height

**Available space**: ~9cm total

**Calculation:**
```
Title: ~1cm
\smallskip: ~0.15cm
Equation minipage: X cm
(no spacing command)
Text minipage: Y cm
---------------------------
Total must be ≤ 8.8cm
```

**For one-line equation:**
```
1 + 0.15 + 1.5 + Y ≤ 8.8
Y ≤ 6.15cm
Use: Y = 6cm (safe margin)
```

**For two-line equation:**
```
1 + 0.15 + 2.5 + Y ≤ 8.8
Y ≤ 5.15cm
Use: Y = 5cm (safe margin)
```

## Systematic Template Rules

### Template A: One-Line Equation (No Figure)

```latex
\begin{frame}{Title}

\smallskip

\begin{minipage}[t][1.5cm][t]{\textwidth}
{\small
Intro sentence:
}

\smallskip

{\footnotesize
$$
equation
$$
}
\end{minipage}

\begin{minipage}[t][6cm][t]{\textwidth}
{\footnotesize
\begin{itemize}
\item Bullet 1
\item Bullet 2
\end{itemize}
}
\end{minipage}

\end{frame}
```

**Height breakdown:**
- Title: 1cm
- \smallskip: 0.15cm
- Equation minipage: 1.5cm (content ~1cm, buffer 0.5cm creates spacing)
- Text minipage: 6cm
- **Total: 8.65cm ✓**

### Template B: Two-Line Equation (No Figure)

```latex
\begin{frame}{Title}

\smallskip

\begin{minipage}[t][2.5cm][t]{\textwidth}
{\small
Intro sentence:
}

\smallskip

{\footnotesize
\begin{align*}
equation line 1 \\
equation line 2
\end{align*}
}
\end{minipage}

\begin{minipage}[t][5cm][t]{\textwidth}
{\footnotesize
\begin{itemize}
\item Bullet 1
\item Bullet 2
\end{itemize}
}
\end{minipage}

\end{frame}
```

**Height breakdown:**
- Title: 1cm
- \smallskip: 0.15cm
- Equation minipage: 2.5cm (content ~1.8-2cm, buffer 0.5cm creates spacing)
- Text minipage: 5cm
- **Total: 8.65cm ✓**

### Template C: Three+ Line Equation (No Figure)

```latex
\begin{frame}{Title}

\smallskip

\begin{minipage}[t][3.5cm][t]{\textwidth}
{\small
Intro sentence:
}

\smallskip

{\footnotesize
\begin{align*}
equation line 1 \\
equation line 2 \\
equation line 3
\end{align*}
}
\end{minipage}

\begin{minipage}[t][4cm][t]{\textwidth}
{\footnotesize
\begin{itemize}
\item Bullet 1
\item Bullet 2
\end{itemize}
}
\end{minipage}

\end{frame}
```

**Height breakdown:**
- Title: 1cm
- \smallskip: 0.15cm
- Equation minipage: 3.5cm (content ~2.8-3cm, buffer 0.5-0.7cm creates spacing)
- Text minipage: 4cm
- **Total: 8.65cm ✓**

## Decision Rule for Producer Agent

### Step 1: Count Equation Lines

```
IF equation has 1 line:
    equation_minipage_height = 1.5cm
    text_minipage_height = 6cm

ELSE IF equation has 2 lines:
    equation_minipage_height = 2.5cm
    text_minipage_height = 5cm

ELSE IF equation has 3+ lines:
    equation_minipage_height = 3.5cm
    text_minipage_height = 4cm
```

### Step 2: Apply Template

```latex
\begin{frame}{Title}

\smallskip  % ← Always use \smallskip after title

\begin{minipage}[t][{equation_minipage_height}][t]{\textwidth}
{\small
Intro:
}

\smallskip

{\footnotesize
equation
}
\end{minipage}

% ← NO spacing command here - spacing comes from minipage sizing

\begin{minipage}[t][{text_minipage_height}][t]{\textwidth}
{\footnotesize
bullets
}
\end{minipage}

\end{frame}
```

## For Equation + Figure Slides

Same principle applies:

**One-line equation + figure:**
```latex
\smallskip

\begin{minipage}[t][0.5cm][t]{\textwidth}
\centering
{\small
{\scriptsize equation}
}
\end{minipage}

\centering
\begin{minipage}[t][6.8cm][t]{\textwidth}
    figure
\end{minipage}
```

**Two-line equation + figure:**
```latex
\smallskip

\begin{minipage}[t][0.8cm][t]{\textwidth}
\centering
{\small
{\scriptsize
\begin{align*}
eq line 1 \\
eq line 2
\end{align*}
}
}
\end{minipage}

\centering
\begin{minipage}[t][6.5cm][t]{\textwidth}
    figure
\end{minipage}
```

## Summary

### ❌ Wrong Approach
- Use fixed minipage sizes regardless of equation complexity
- Add `\medskip` or `\bigskip` to create spacing
- Results in cramped appearance or overlap

### ✅ Correct Approach
- **Size equation minipage based on equation lines** (1 line = 1.5cm, 2 lines = 2.5cm, 3+ = 3.5cm)
- **Adjust text minipage to maintain total ≤ 8.8cm**
- **Natural spacing emerges from minipage buffer** (no spacing commands needed)
- **Systematic and deterministic** - clear rules based on equation complexity

## Producer Agent Implementation

**Detection logic:**
1. Parse equation content
2. Count lines (look for `\\` or multiple lines in `align*`)
3. Apply corresponding minipage heights
4. Use `\smallskip` after title (not `\vspace{-.2cm}`)
5. Do NOT add spacing between minipages

**Result**: Clean, systematic templates with natural spacing that scales with equation complexity.
