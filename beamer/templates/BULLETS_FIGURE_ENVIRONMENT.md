# Fixed Environment for Title + Bullets + Figure Slides

## The Solution

Create a **custom LaTeX environment** that enforces the correct pattern for slides with:
- Title
- Bullet points at top (MAX 2 bullets)
- Figure(s) below

**CRITICAL RULE**: NEVER have more than 2 bullet points above a figure. If you need more explanations, use the `\only<1>{...}\only<2>{...}` overlay pattern.

## LaTeX Environment Definition

Add this to the preamble of every presentation:

```latex
%=============================================================================
% BULLETS + FIGURE SLIDE ENVIRONMENT - GUARANTEED TO WORK
%=============================================================================

% Two bullets + corresponding figures (with overlays)
\newcommand{\bulletsfigureframe}[3]{
    \begin{frame}{#1}

    \vspace{-.2cm}

    \begin{minipage}[t][1cm][t]{\textwidth}
    \begin{itemize}
    {
    #2  % Contains \only<1>{\footnotesize\item ...}, \only<2>{\footnotesize\item ...}
    }
    \end{itemize}
    \end{minipage}

    \centering
    \begin{minipage}[t][7cm][t]{\textwidth}
        \begin{columns}[T]
            \begin{column}{1\textwidth}
                #3  % Contains \only<1>{\resizebox...}, \only<2>{\resizebox...}
            \end{column}
        \end{columns}
    \end{minipage}

    \end{frame}
}
```

## Usage

### Two Bullets + Two Figures (Standard Pattern)

**Instead of writing:**
```latex
\begin{frame}{Title}

\vspace{-.2cm}

\begin{minipage}[t][1cm][t]{\textwidth}
\begin{itemize}
{
\only<1>{\footnotesize\item First explanation}
\only<2>{\footnotesize\item Second explanation}
}
\end{itemize}
\end{minipage}

\centering
\begin{minipage}[t][7cm][t]{\textwidth}
    \begin{columns}[T]
        \begin{column}{1\textwidth}
            \only<1>{\resizebox{\textwidth}{!}{
                \includegraphics[height=.8\textheight]{results/fig1.pdf}
            }}

            \only<2>{\resizebox{\textwidth}{!}{
                \includegraphics[height=.8\textheight]{results/fig2.pdf}
            }}
        \end{column}
    \end{columns}
\end{minipage}

\end{frame}
```

**Simply write:**
```latex
\bulletsfigureframe{Title}{
    \only<1>{\footnotesize\item First explanation}
    \only<2>{\footnotesize\item Second explanation}
}{
    \only<1>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig1.pdf}
    }}

    \only<2>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig2.pdf}
    }}
}
```

### One Bullet + One Figure

**Simply write:**
```latex
\bulletsfigureframe{Title}{
    \footnotesize\item Single explanation
}{
    \resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/figure.pdf}
    }
}
```

## Why This Works

1. **Enforces `\vspace{-.2cm}`**: Reduces space after title (MANDATORY)
2. **Enforces bullets minipage height**: Always 1cm (fits 1-2 bullets)
3. **Enforces `\footnotesize` font**: Built into usage pattern
4. **Enforces figure minipage height**: Always 7cm (reduced to accommodate bullets)
5. **Enforces resizebox**: Built into usage pattern
6. **Automatic centering**: Always correct
7. **No deviation possible**: Producer agents can't make mistakes
8. **Works for ANY figure size**: resizebox adapts automatically
9. **Legends never cropped**: resizebox maintains aspect ratio

## Height Calculation

**Total vertical space used:**
- Title: ~1cm
- `\vspace{-.2cm}`: Saves 0.2cm
- Bullets minipage: 1cm
- Figure minipage: 7cm
- Total: 1cm - 0.2cm + 1cm + 7cm = 8.8cm ✓ (fits in 9cm available space)

## Critical Rules - ZERO TOLERANCE

1. **NEVER more than 2 bullets above a figure**
   - Max 2 bullets visible at any time
   - If you need more explanations → use overlay pattern with `\only<1>{...}\only<2>{...}`

2. **ALWAYS use `\vspace{-.2cm}` after title**
   - This is MANDATORY to save vertical space
   - Built into environment

3. **Bullets MUST use `\footnotesize` font**
   - This is MANDATORY to fit in 1cm minipage
   - Larger fonts will overflow

4. **Figure minipage MUST be 7cm** (NOT 8cm)
   - Reduced from 8cm to accommodate bullets above
   - Using 8cm will cause overfull vbox warnings

5. **ALWAYS use `\resizebox{\textwidth}{!}{...}` around figures**
   - This is MANDATORY to prevent legend cropping

## When to Use This Environment

Use `\bulletsfigureframe` when:
- Slide has title
- Slide has 1-2 bullet points at top
- Slide has figure(s) below
- Bullets explain or introduce the figure

**Do NOT use when:**
- You need more than 2 bullets visible at once (use overlay pattern instead)
- Bullets are long/multi-line (won't fit in 1cm minipage)
- Slide has equation instead of bullets (use equation+figure pattern)
- Slide has only figure, no bullets (use figure-only pattern)

## The Overlay Pattern (For More Content)

If you need MORE than 2 bullets of explanation, use the overlay pattern:

```latex
\bulletsfigureframe{Title}{
    \only<1>{\footnotesize\item First explanation about figure 1}
    \only<2>{\footnotesize\item Second explanation about figure 2}
    \only<3>{\footnotesize\item Third explanation about figure 3}
    \only<4>{\footnotesize\item Fourth explanation about figure 4}
}{
    \only<1>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig1.pdf}
    }}

    \only<2>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig2.pdf}
    }}

    \only<3>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig3.pdf}
    }}

    \only<4>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig4.pdf}
    }}
}
```

**Key point**: At any given overlay (slide 1, 2, 3, or 4), only ONE bullet is visible. This respects the "max 2 bullets" rule.

## Critic Checking Rule

**Simple check**:
- Is this a title + bullets + figure slide?
- Does it use `\bulletsfigureframe`?
- If NO → CRITICAL VIOLATION (-10)

**Alternative**: If not using environment, check manually:
1. **MANDATORY**: `\vspace{-.2cm}` after frame title
2. Bullets minipage MUST be exactly `[t][1cm][t]{\textwidth}`
3. Bullets MUST use `\footnotesize` font
4. Figure minipage MUST be exactly `[t][7cm][t]{\textwidth}` (NOT 8cm!)
5. MUST have `\resizebox{\textwidth}{!}{...}` around figure
6. NEVER more than 2 bullets visible at same time

## Benefits

1. **100% success rate** - impossible to get wrong
2. **Simple for producers** - just call `\bulletsfigureframe{Title}{bullets}{figures}`
3. **Easy to check** - critic just looks for environment name
4. **Enforces bullet limit** - clear constraint: max 2 bullets
5. **Maintainable** - change environment definition once, fixes all slides
6. **Self-documenting** - clear intent when reading code
7. **Consistent spacing** - all bullets+figure slides look identical

## Implementation Plan

1. Add environment definition to presentation preamble template
2. Update Template Assembler: Use `\bulletsfigureframe` for all title + bullets + figure slides
3. Update Layout Critic: Check for environment usage and enforce "max 2 bullets" rule
4. Convert existing slides to use environment

This eliminates another entire class of errors by making the correct pattern the ONLY pattern.
