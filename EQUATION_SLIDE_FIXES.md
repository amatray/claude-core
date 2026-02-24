# Equation Slide Fixes: Three Critical Issues

## Problem 1: Not Enough Space Between Equation and Text Minipages

**Current configuration:**
```latex
\begin{minipage}[t][2.5cm][t]{\textwidth}
equation content (~2.3cm actual)
\end{minipage}

\begin{minipage}[t][5cm][t]{\textwidth}
text bullets
\end{minipage}
```

**Issue**: Equation content fills almost entire 2.5cm minipage, leaving minimal buffer (only ~0.2cm). This creates cramped appearance.

**Root cause**: While the systematic sizing (2 lines = 2.5cm) is correct for preventing overlap, the visual spacing is insufficient.

**Solution**: Increase equation minipage to create more visual buffer:
- 2-line equation: Change from 2.5cm → **2.8cm**
- Text minipage: Change from 5cm → **4.7cm**
- Total: 1 + 0.15 + 2.8 + 4.7 = 8.65cm ✓
- Result: 0.5cm buffer between equation and text (comfortable)

## Problem 2: Color Handling - Lightgrey Doesn't Override Term Colors

**Current pattern (WRONG):**
```latex
\only<1>\blue{\only<2->\lightgrey{\mathbb{1}[\text{Perm}_o]}}
```

**How this renders:**
- Slide 1: `\blue{...}` active → term shows in **blue** ✓
- Slide 2+: `\lightgrey{...}` active, BUT if term internally has `\blue{...}`, the blue overrides grey → term shows in **blue** ❌

**Root cause**: LaTeX color commands don't override nested colors. Inner color always wins.

**Example of the bug:**
```latex
\textcolor{gray}{\blue{text}}  % Renders as BLUE, not gray!
```

**CORRECT pattern:**
```latex
\only<1>{\blue{\mathbb{1}[\text{Perm}_o]}}\only<2->{\lightgrey{\mathbb{1}[\text{Perm}_o]}}
```

**How this renders:**
- Slide 1: `\blue{term}` → term shows in **blue** ✓
- Slide 2+: `\lightgrey{term}` → term shows in **grey** ✓
- NO nested colors - each overlay completely replaces the term

## Problem 3: Last Term Should Not Gray Out

**Current pattern (WRONG):**
```latex
\only<6>\purple{\only<7->\lightgrey{\delta_{e,t}}}
```

**Issue**: Last term explained (purple delta on slide 6) turns grey on slide 7+. But there's no slide 7 - slide 6 is the last explanation.

**User requirement**: "once you have reached the end of the different element of the equation, the last one does not need to turn gray"

**Root cause**: Mechanical application of graying pattern to all terms, without considering which is the final term.

**CORRECT pattern for last term:**
```latex
\only<6->{\purple{\delta_{e,t}}}
```

**Logic:**
- On slides 1-5: Term is in `\lightgrey` (not yet explained)
- On slide 6+: Term is in `\purple` (being explained) and **stays purple** forever
- NO graying out transition - this is the finale

## Systematic Fix

### For Intermediate Terms (will gray out later):

```latex
% Pattern for term explained on slide N (N < final slide):
\only<1-N-1>{\lightgrey{term}}  % Before explanation: grey
\only<N>{\color{term}}           % During explanation: colored
\only<N+1->{\lightgrey{term}}    % After explanation: grey again
```

### For Final Term (stays highlighted):

```latex
% Pattern for term explained on slide N (N = final slide):
\only<1-N-1>{\lightgrey{term}}  % Before explanation: grey
\only<N->{\color{term}}          % During and after explanation: colored FOREVER
```

## Implementation Rules for Producer Agent

### Rule 1: Calculate Buffer Space for 2-Line Equations

```
IF equation has 2 lines:
    equation_minipage = 2.8cm  (increased from 2.5cm)
    text_minipage = 4.7cm      (decreased from 5cm)
```

### Rule 2: No Nested Colors - Use Sequential \only

**WRONG:**
```latex
\only<1>\blue{\only<2->\lightgrey{term}}
```

**RIGHT:**
```latex
\only<1>{\blue{term}}\only<2->{\lightgrey{term}}
```

### Rule 3: Detect Final Term and Don't Gray It Out

**Detection:**
```
IF term is explained on slide N:
    Check if N is the maximum overlay number (final slide)
    IF N == final_slide:
        Pattern: \only<1-N-1>{\lightgrey{term}}\only<N->{\color{term}}
    ELSE:
        Pattern: \only<1-N-1>{\lightgrey{term}}\only<N>{\color{term}}\only<N+1->{\lightgrey{term}}
```

## Summary

| Issue | Current | Fixed |
|-------|---------|-------|
| **Spacing** | Equation 2.5cm, text 5cm (cramped) | Equation 2.8cm, text 4.7cm (comfortable) |
| **Color nesting** | `\only<1>\blue{\only<2->\lightgrey{term}}` | `\only<1>{\blue{term}}\only<2->{\lightgrey{term}}` |
| **Last term** | Grays out on final slide | Stays highlighted: `\only<N->{\color{term}}` |

## Test Case

**Before (WRONG):**
```latex
\only<5>\orange{\only<6->\lightgrey{\alpha_{o,d,e}}}
\only<6>\purple{\only<7->\lightgrey{\delta_{e,t}}}
```
- Slide 5: alpha is orange
- Slide 6: alpha turns grey, delta is purple
- Slide 7+: BOTH are grey ❌ (but slide 7 doesn't exist!)

**After (CORRECT):**
```latex
\only<5>{\orange{\alpha_{o,d,e}}}\only<6->{\lightgrey{\alpha_{o,d,e}}}
\only<6->{\purple{\delta_{e,t}}}
```
- Slide 5: alpha is orange
- Slide 6+: alpha is grey, delta is purple ✓
- Final term (delta) stays purple forever ✓
