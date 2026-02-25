# Common Violation: Text + Figure Slides Using `\bigskip` Pattern

## The Problem

Slides with title + single line of text + figure are frequently generated INCORRECTLY using the old `\bigskip` pattern instead of the systematic minipage pattern.

## Example of WRONG Pattern (Frequently Generated)

```latex
\begin{frame}{Title}

\bigskip

Some text here

\bigskip

\centering
\begin{minipage}[t][6cm][t]{\textwidth}
	\begin{columns}[T]
		\begin{column}{1\textwidth}
			\includegraphics[height=.75\textheight]{figure.pdf}
		\end{column}
	\end{columns}
\end{minipage}

\end{frame}
```

## Why This Is Wrong

### Problem 1: Text Not in `{\small}` Font
- Text appears at normal size (too large)
- Takes excessive vertical space
- Pushes figure down

### Problem 2: Using `\bigskip` Instead of Minipage
- `\bigskip` adds arbitrary spacing
- No control over exact vertical space
- Inconsistent with systematic rules

### Problem 3: Figure Minipage Too Small
- Often 6cm or 6.5cm (too small)
- Should be 7cm to accommodate text above
- Results in figure legend cropping

### Problem 4: Missing `\resizebox` Wrapper
- Figure not properly scaled
- Legend cropping likely

## The CORRECT Pattern (Template 3A)

```latex
\begin{frame}{Title}

\begin{minipage}[t][0.3cm][t]{\textwidth}
{\small
Some text here
}
\end{minipage}

\centering
\begin{minipage}[t][7cm][t]{\textwidth}
	\begin{columns}[T]
		\begin{column}{1\textwidth}
			\resizebox{\textwidth}{!}{
				\includegraphics[height=.8\textheight]{figure.pdf}
			}
		\end{column}
	\end{columns}
\end{minipage}

\end{frame}
```

## Systematic Rules

### Rule 1: Text Minipage
- **Height**: `[t][0.3cm][t]{\textwidth}` - EXACTLY 0.3cm for single line
- **Font**: `{\small ...}` wrapper - MANDATORY
- **Alignment**: LEFT-ALIGNED (no `\centering` for text)

### Rule 2: Figure Minipage
- **Height**: `[t][7cm][t]{\textwidth}` - Reduced from 7.5cm to accommodate text
- **Wrapper**: `\resizebox{\textwidth}{!}{...}` - MANDATORY
- **Figure height**: `.8\textheight` inside resizebox

### Rule 3: No `\bigskip`
- Do NOT use `\bigskip` before or after text
- Systematic spacing is built into minipage pattern
- `\bigskip` adds unnecessary vertical space

## Height Calculation

```
Total vertical space: ~9cm available

With CORRECT pattern:
- Title: ~1cm
- Text minipage: 0.3cm
- Figure minipage: 7cm
- Total: 8.3cm ✓ (fits comfortably)

With WRONG pattern (\bigskip):
- Title: ~1cm
- \bigskip: ~0.5cm
- Text (normal size): ~0.4cm
- \bigskip: ~0.5cm
- Figure minipage: 6cm
- Total: 8.4cm (but figure is too small → legend crops)
```

## Critic Agent Detection Rules

### Check 1: Detect `\bigskip` + Text + Figure Pattern

```
IF slide has:
    - \bigskip after frame title
    - Text line (not in itemize, not in minipage)
    - \centering
    - Figure minipage
THEN:
    CRITICAL VIOLATION (-10)
    "Text+figure slides MUST use minipage pattern, NOT \bigskip"
```

### Check 2: Text Not Wrapped in `{\small}`

```
IF slide has text line + figure:
    Check if text wrapped in {\small ...}
    IF NOT:
        CRITICAL VIOLATION (-10)
        "Text above figure MUST be wrapped in {\small ...}"
```

### Check 3: Wrong Minipage Heights

```
IF slide has text + figure:
    Check text minipage height
    IF != 0.3cm:
        CRITICAL VIOLATION (-10)

    Check figure minipage height
    IF < 6.9cm OR > 7cm:
        CRITICAL VIOLATION (-10)
```

## When This Pattern Applies

Use Template 3A (single line text + figure) when:
- Slide has title
- Slide has ONE line of text (subtitle, explanation, etc.)
- Slide has figure(s) below
- Text is NOT an equation (equations use Template 3A with centering)
- Text is NOT bullets (bullets use Template 2B)

## Real Example That Was Wrong

### Original (WRONG):
```latex
\begin{frame}{\green{Western Creditors} are Willing to Abstract from \blue{OECD Rules}}

\bigskip

For Their Aligned Creditors

\bigskip

\centering
\begin{minipage}[t][6cm][t]{\textwidth}
	\begin{columns}[T]
		\begin{column}{1\textwidth}
			\only<1>{\resizebox{\textwidth}{!}{
				\includegraphics[height=.75\textheight]{results/lp_risk_score.pdf}
			}}
		\end{column}
	\end{columns}
\end{minipage}

\end{frame}
```

**Problems:**
- ❌ Text "For Their Aligned Creditors" NOT in `{\small}`
- ❌ Using `\bigskip` pattern instead of minipage
- ❌ Figure minipage only 6cm (should be 7cm)
- ❌ Result: Legend cropped at bottom

### Fixed (CORRECT):
```latex
\begin{frame}{\green{Western Creditors} are Willing to Abstract from \blue{OECD Rules}}

\begin{minipage}[t][0.3cm][t]{\textwidth}
{\small
For Their Aligned Creditors
}
\end{minipage}

\centering
\begin{minipage}[t][6.9cm][t]{\textwidth}
	\begin{columns}[T]
		\begin{column}{1\textwidth}
			\resizebox{\textwidth}{!}{
				\includegraphics[height=.75\textheight]{results/lp_risk_score.pdf}
			}
		\end{column}
	\end{columns}
\end{minipage}

\end{frame}
```

**Benefits:**
- ✅ Text in `{\small}` - consistent, compact
- ✅ Systematic minipage pattern - exact vertical control
- ✅ Figure minipage 6.9cm - appropriate with text above
- ✅ Result: Legend fully visible, no overflow

## Producer Agent Instructions Update

Template Assembler Template 4 has been updated to:
1. **Recognize** subtitle/text + figure as Template 3A pattern
2. **Use** text minipage `[t][0.3cm][t]` with `{\small}`
3. **Use** figure minipage `[t][7cm][t]` with `\resizebox`
4. **Eliminate** `\bigskip` pattern entirely

## Implementation Status

✅ **Template Assembler** - Template 4 updated with systematic rules
✅ **Layout Critic** - Check 0C added to catch `\bigskip` violations
✅ **This document** - Explains common violation pattern
✅ **Presentation** - Fixed problematic slide

## Summary

The `\bigskip` pattern for text + figure slides is a **systematic error** that causes:
1. Text not in small font (too large)
2. Inconsistent spacing
3. Figure minipage too small
4. Legend cropping

The **systematic solution** is Template 3A: text minipage 0.3cm + figure minipage 7cm with proper font sizes and resizebox wrapper.

Producer agents must use this pattern 100% of the time for single-line text + figure slides.
