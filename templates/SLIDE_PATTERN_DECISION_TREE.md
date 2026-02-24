# Slide Pattern Decision Tree

## Purpose

This document provides a systematic decision tree for choosing the correct slide template pattern.

## Decision Tree

```
Start: What content is on the slide?

├─ Title + Figure ONLY (no text, no equation, no bullets)
│  └─ Use: FIGURE-ONLY pattern
│     ├─ Text minipage: NONE
│     ├─ Figure minipage: [t][7.5cm][t]{\textwidth}
│     └─ Environment: \figureframe{Title}{path}
│     └─ WHY 7.5cm: Conservative baseline for all aspect ratios (see below)
│
├─ Title + 1-2 Bullets + Figure
│  └─ Use: BULLETS + FIGURE pattern
│     ├─ \vspace{-.2cm} after title (MANDATORY)
│     ├─ Bullets minipage: [t][1cm][t]{\textwidth}
│     ├─ Font: \footnotesize for each bullet
│     ├─ Figure minipage: [t][7cm][t]{\textwidth}
│     ├─ ZERO TOLERANCE: NEVER more than 2 bullets visible at once
│     ├─ If more content needed: Use overlay pattern (\only<1>, \only<2>, etc.)
│     └─ Environment: \bulletsfigureframe{Title}{bullets}{figures}
│
├─ Title + ONE LINE of text/equation + Figure
│  ├─ Is it an equation?
│  │  ├─ YES → Use: EQUATION + FIGURE pattern (CENTERED)
│  │  │  ├─ Text minipage: [t][0.3cm][t]{\textwidth} WITH \centering
│  │  │  ├─ Font: {\small ...}
│  │  │  ├─ Figure minipage: [t][7cm][t]{\textwidth}
│  │  │  └─ Environment: \equationfigureframe{Title}{$equation$}{path}
│  │  │
│  │  └─ NO → Use: TEXT + FIGURE pattern (LEFT-ALIGNED)
│  │     ├─ Text minipage: [t][0.3cm][t]{\textwidth} NO \centering
│  │     ├─ Font: {\small ...}
│  │     ├─ Figure minipage: [t][7cm][t]{\textwidth}
│  │     └─ Environment: \textfigureframe{Title}{text}{path}
│
├─ Title + Multi-line intro + Equation + Figure
│  └─ Use: EQUATION + FIGURE pattern (SYSTEMATIC SPACING)
│     ├─ \vspace{-.2cm} after title
│     ├─ Equation minipage: [t][0.5cm][t]{\textwidth}
│     │  ├─ Intro: {\small ...}
│     │  └─ Equation: {\scriptsize $...$}
│     ├─ Figure minipage: [t][7cm][t]{\textwidth}
│     └─ See: EQUATION_SLIDE_SPACING_RULES.md
│
├─ Title + Equation + Text/Bullets (NO figure)
│  └─ Use: EQUATION-ONLY pattern
│     ├─ \vspace{-.2cm} after title
│     ├─ Equation minipage: [t][2cm][t]{\textwidth}
│     │  ├─ Intro: {\small ...}
│     │  └─ Equation: {\footnotesize ...}
│     ├─ Text minipage: [t][5.5cm][t]{\textwidth}
│     │  └─ Bullets: {\footnotesize ...}
│     └─ See: EQUATION_SLIDE_SPACING_RULES.md
│
├─ Title + Content Bullets
│  └─ Use: SIMPLE CONTENT pattern
│     └─ Standard itemize with \bitem, \pause, etc.
│
├─ Title + Intro text OUTSIDE itemize + Numbered list
│  └─ Use: NUMBERED LIST pattern
│     ├─ \bigskip after title
│     ├─ Intro text (NO \hspace needed)
│     ├─ \vfill before EVERY item (including [1.])
│     └─ See: beamer-template-assembler.md Template 2
│
└─ Thank You slide
   └─ Use: THANK YOU pattern
      ├─ \begin{frame}{}  ← empty title
      ├─ {\LARGE \blue{Thank you!}}
      └─ See: thankyou.tex template
```

## Quick Reference Table

| Content Structure | Content Minipage | Figure Minipage | Special Rules |
|------------------|------------------|-----------------|---------------|
| **Figure only** | NONE | `[t][7.5cm][t]` | Always use `\resizebox`, 7.5cm = conservative baseline |
| **1-2 bullets + figure** | `[t][1cm][t]` | `[t][7cm][t]` | `\vspace{-.2cm}`, bullets `\footnotesize`, MAX 2 bullets |
| **Single line text + figure** | `[t][0.3cm][t]` | `[t][7cm][t]` | Text: `{\small ...}`, NO centering |
| **Single line equation + figure** | `[t][0.3cm][t]` | `[t][7cm][t]` | Equation: `{\small ...}`, WITH centering |
| **Multi-line intro + equation + figure** | `[t][0.5cm][t]` | `[t][7cm][t]` | `\vspace{-.2cm}`, intro `{\small}`, eq `{\scriptsize}` |
| **Equation only (no figure)** | `[t][2cm][t]` | Text: `[t][5.5cm][t]` | `\vspace{-.2cm}`, eq `{\footnotesize}` |

## Height Calculation Formula

**Available vertical space**: ~9cm (title to bottom margin)

**General formula**:
```
Title height: ~1cm (fixed)
+ Content above figures: X cm
+ Figure minipage: Y cm
= Total must be ≤ 8.5-9cm
```

**Specific cases**:

1. **Figure only**:
   - Total: 1cm + 0cm + 7.5cm = 8.5cm ✓

2. **Bullets + figure**:
   - Total: 1cm (title) - 0.2cm (vspace) + 1cm (bullets) + 7cm (fig) = 8.8cm ✓

3. **Single line + figure**:
   - Total: 1cm + 0.3cm + 7cm = 8.3cm ✓

4. **Multi-line intro + equation + figure**:
   - Total: 1cm (title) - 0.2cm (vspace) + 0.5cm (eq) + 7cm (fig) = 8.3cm ✓

5. **Equation only (no figure)**:
   - Total: 1cm (title) - 0.2cm (vspace) + 2cm (eq) + 5.5cm (text) + 0.2cm (medskip) = 8.5cm ✓

## Critical Rules - Zero Tolerance

1. **ALWAYS use `\resizebox{\textwidth}{!}{...}` around figures**
   - Exception: Full-bleed pattern with `{1.3\textwidth}`
   - **CRITICAL**: The `[height=.8\textheight]` inside `\includegraphics` is **IGNORED** by resizebox
   - Final height = `textwidth` ÷ figure_aspect_ratio

2. **Figure minipage = 7.5cm baseline for figure-only slides**
   - This is CONSERVATIVE: works for aspect ratios down to 1.53
   - Standard figures (aspect 1.67) need 7.4cm, so 7.5cm provides margin
   - ANY content above figure → reduce to 7cm or less

3. **Equations are centered, text is left-aligned**
   - Equation: Add `\centering` to text minipage
   - Text: NO `\centering`

4. **Font sizes are systematic**:
   - Single line text/equation: `{\small ...}`
   - Multi-line intro + equation + figure: intro `{\small}`, equation `{\scriptsize}`
   - Equation only: intro `{\small}`, equation `{\footnotesize}`

5. **Total heights must sum to ≤ 8.5cm**
   - Use systematic calculations, not guesswork
   - ANY overfull vbox warning = CRITICAL VIOLATION

## Common Violations

❌ **Using 8cm figure minipage when content exists above**
- Fix: Reduce to 7cm or calculate exact height needed

❌ **Forgetting `\resizebox` wrapper**
- Fix: ALWAYS wrap `\includegraphics` in `\resizebox{\textwidth}{!}{...}`

❌ **Centering text or not centering equations**
- Fix: Equations centered, text left-aligned

❌ **Wrong font sizes**
- Fix: Follow systematic rules in table above

❌ **Minipage heights that exceed 8.5cm total**
- Fix: Calculate total, reduce as needed

## Documentation References

- **Figure-only slides**: See `FIGURE_ONLY_ENVIRONMENT.md`
- **Single line + figure**: See `TEXT_FIGURE_ENVIRONMENT.md`
- **Equation slides**: See `EQUATION_SLIDE_SPACING_RULES.md`
- **Template details**: See `beamer-template-assembler.md`
- **Critic checks**: See `beamer-layout-critic.md`
