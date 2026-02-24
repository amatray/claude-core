# Diagnosis: Equation Slide Spacing Issues

## Problems Identified

### Problem 1: Too Aggressive Title Spacing
**Current pattern:**
```latex
\begin{frame}{Title}

\vspace{-.2cm}  % ← Too aggressive - removes ALL space

\begin{minipage}[t][2cm][t]{\textwidth}
```

**Issue**: `\vspace{-.2cm}` removes ALL space between title and equation minipage. There is ZERO visual separation.

**User requirement**: "Reduce a bit the space" - not eliminate it entirely.

### Problem 2: Insufficient Space Between Equation and Text Minipages
**Current pattern:**
```latex
\end{minipage}  % ← End of equation minipage

\medskip  % ← Only ~3mm of space

\begin{minipage}[t][5.5cm][t]{\textwidth}  % ← Start of text minipage
```

**Issue**: `\medskip` provides only ~3mm of vertical space. With equation content potentially extending to bottom of its minipage, and text starting immediately at top of next minipage, they can appear to overlap visually.

## Height Calculation Analysis

**Current configuration:**
```
Available space: ~9cm total

Breakdown:
- Title: ~1cm
- vspace(-.2cm): -0.2cm (saves space)
- Equation minipage: 2cm
- \medskip: ~0.2cm
- Text minipage: 5.5cm
Total: 1 - 0.2 + 2 + 0.2 + 5.5 = 8.5cm ✓ (fits)
```

**The math works**, but the **visual spacing is poor**.

## Root Cause

The systematic rules were optimized for **maximum content density** but sacrificed **visual breathing room**:

1. **`\vspace{-.2cm}`** was chosen to save maximum vertical space
2. **`\medskip`** was chosen as minimal spacing between minipages
3. **Result**: Slides feel cramped, minipages appear to overlap

## Proposed Solution

### Solution 1: Less Aggressive Title Spacing

**Replace `\vspace{-.2cm}` with `\vspace{-.1cm}` OR `\smallskip`**

Options:
```latex
% Option A: Smaller negative vspace
\vspace{-.1cm}  % ← Reduces space by half of -.2cm

% Option B: Use smallskip (positive space, but small)
\smallskip  % ← ~3mm of space (less than default \bigskip)
```

**Recommendation**: Use `\smallskip`
- Provides consistent, positive space
- Less aggressive than removing space
- More intuitive than negative vspace

### Solution 2: More Space Between Minipages

**Replace `\medskip` with `\bigskip`**

```latex
\end{minipage}  % ← End of equation minipage

\bigskip  % ← ~6mm of space (double medskip)

\begin{minipage}[t][5.5cm][t]{\textwidth}  % ← Start of text minipage
```

**Impact on height:**
```
- Title: ~1cm
- \smallskip: +0.15cm (instead of -.2cm)
- Equation minipage: 2cm
- \bigskip: ~0.4cm (instead of .2cm medskip)
- Text minipage: 5.5cm
Total: 1 + 0.15 + 2 + 0.4 + 5.5 = 9.05cm
```

**Problem**: 9.05cm exceeds 9cm available → Need to adjust minipage heights

### Solution 3: Adjust Minipage Heights + Better Spacing

**Balanced approach:**
```latex
\begin{frame}{Title}

\smallskip  % ← ~3mm space after title (not too much, not zero)

\begin{minipage}[t][1.8cm][t]{\textwidth}  % ← Reduced from 2cm
{\small
Intro text:
}

\smallskip

{\footnotesize
\begin{align*}
equation
\end{align*}
}
\end{minipage}

\bigskip  % ← ~6mm space between minipages (clear separation)

\begin{minipage}[t][5.3cm][t]{\textwidth}  % ← Reduced from 5.5cm
{\footnotesize
\begin{itemize}
bullets
\end{itemize}
}
\end{minipage}

\end{frame}
```

**Height calculation:**
```
- Title: ~1cm
- \smallskip: +0.15cm
- Equation minipage: 1.8cm
- \bigskip: ~0.4cm
- Text minipage: 5.3cm
Total: 1 + 0.15 + 1.8 + 0.4 + 5.3 = 8.65cm ✓ (fits comfortably)
```

**Benefits:**
1. ✅ Visual space after title (not zero)
2. ✅ Clear separation between equation and text minipages
3. ✅ Total height fits within 9cm
4. ✅ Slightly reduced minipage heights compensate for better spacing

## Recommended Template Update

### For Equation-Only Slides (no figure)

```latex
\begin{frame}{Title}

\smallskip  % ← NEW: Small space after title (not \vspace{-.2cm})

\begin{minipage}[t][1.8cm][t]{\textwidth}  % ← NEW: Reduced from 2cm
{\small
Intro sentence:
}

\smallskip

{\footnotesize
\begin{align*}
equation
\end{align*}
}
\end{minipage}

\bigskip  % ← NEW: Changed from \medskip for clearer separation

\begin{minipage}[t][5.3cm][t]{\textwidth}  % ← NEW: Reduced from 5.5cm
{\footnotesize
\begin{itemize}
\item Explanation 1
\item Explanation 2
\end{itemize}
}
\end{minipage}

\end{frame}
```

### For Equation + Figure Slides

**Current pattern (needs review):**
```latex
\begin{frame}{Title}

\vspace{-.2cm}  % ← Should change to \smallskip

\begin{minipage}[t][0.5cm][t]{\textwidth}
\centering
{\small
Intro:
{\scriptsize
equation
}}
\end{minipage}

\centering  % ← No spacing command here - might need \smallskip or \medskip
\begin{minipage}[t][7cm][t]{\textwidth}
```

**Height with current pattern:**
```
- Title: ~1cm
- vspace(-.2cm): -0.2cm
- Equation minipage: 0.5cm
- (no spacing)
- Figure minipage: 7cm
Total: 1 - 0.2 + 0.5 + 7 = 8.3cm ✓
```

**Proposed update:**
```latex
\begin{frame}{Title}

\smallskip  % ← NEW: Change from \vspace{-.2cm}

\begin{minipage}[t][0.5cm][t]{\textwidth}
\centering
{\small
Intro:
{\scriptsize
equation
}}
\end{minipage}

\smallskip  % ← NEW: Add explicit small spacing

\centering
\begin{minipage}[t][6.8cm][t]{\textwidth}  % ← NEW: Reduced from 7cm
```

**Height with proposed:**
```
- Title: ~1cm
- \smallskip: +0.15cm
- Equation minipage: 0.5cm
- \smallskip: +0.15cm
- Figure minipage: 6.8cm
Total: 1 + 0.15 + 0.5 + 0.15 + 6.8 = 8.6cm ✓
```

## Implementation Plan

### Step 1: Update Equation Writer Agent
- Replace `\vspace{-.2cm}` with `\smallskip`
- Replace `\medskip` between minipages with `\bigskip`
- Adjust minipage heights:
  - Equation-only: 1.8cm (from 2cm)
  - Text: 5.3cm (from 5.5cm)
  - Equation+figure: equation 0.5cm, figure 6.8cm (from 7cm)

### Step 2: Update Equation Critic Agent
- Check for `\smallskip` after title (not `\vspace{-.2cm}`)
- Check for `\bigskip` between minipages (not `\medskip`)
- Verify updated minipage heights

### Step 3: Update Documentation
- EQUATION_SLIDE_SPACING_RULES.md
- beamer-equation-writer.md
- beamer-equation-critic.md

## Summary

**Problems:**
1. `\vspace{-.2cm}` too aggressive - zero space after title
2. `\medskip` too small - minipages appear to overlap

**Solutions:**
1. Use `\smallskip` after title - provides breathing room
2. Use `\bigskip` between minipages - clear visual separation
3. Reduce minipage heights slightly to compensate - equation 1.8cm, text 5.3cm

**Result**: Better visual spacing while maintaining total height within bounds.
