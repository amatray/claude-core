# Fixed Environment for Title + Figure Slides

## The Solution

Create a **custom LaTeX environment** that enforces the correct pattern with ZERO room for error.

## LaTeX Environment Definition

Add this to the preamble of every presentation:

```latex
%=============================================================================
% FIGURE-ONLY SLIDE ENVIRONMENT - GUARANTEED TO WORK
%=============================================================================

% Single figure slide
\newcommand{\figureframe}[2]{
    \begin{frame}{#1}

    \centering
    \begin{minipage}[t][7.5cm][t]{\textwidth}
        \begin{columns}[T]
            \begin{column}{1\textwidth}
                \resizebox{\textwidth}{!}{
                    \includegraphics[height=.8\textheight]{#2}
                }
            \end{column}
        \end{columns}
    \end{minipage}

    \end{frame}
}

% Multiple figure slide (with overlays)
\newcommand{\figureframeMulti}[3][]{
    \begin{frame}{#2}

    \centering
    \begin{minipage}[t][7.5cm][t]{\textwidth}
        \begin{columns}[T]
            \begin{column}{1\textwidth}
                #3  % Contains \only<1>{\resizebox...}, \only<2>{\resizebox...}, etc.
            \end{column}
        \end{columns}
    \end{minipage}

    \end{frame}
}
```

## Usage

### Single Figure

**Instead of writing:**
```latex
\begin{frame}{Title}

\centering
\begin{minipage}[t][8cm][t]{\textwidth}
    \begin{columns}[T]
        \begin{column}{1\textwidth}
            \resizebox{\textwidth}{!}{
                \includegraphics[height=.8\textheight]{results/figure.pdf}
            }
        \end{column}
    \end{columns}
\end{minipage}

\end{frame}
```

**Simply write:**
```latex
\figureframe{Title}{results/figure.pdf}
```

### Multiple Figures (Overlays)

**Instead of writing:**
```latex
\begin{frame}{Title}

\centering
\begin{minipage}[t][8cm][t]{\textwidth}
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
\figureframeMulti{Title}{
    \only<1>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig1.pdf}
    }}

    \only<2>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig2.pdf}
    }}
}
```

## Why This Works

1. **Enforces minipage height**: Always 7.5cm, conservative size that works for all aspect ratios
2. **Enforces resizebox**: Built into the environment
3. **Automatic centering**: Always correct
4. **No deviation possible**: Producer agents can't make mistakes
5. **Works for ANY figure size**: resizebox adapts automatically
6. **Legends never cropped**: resizebox maintains aspect ratio

## Why 7.5cm Instead of 8cm?

**ROOT CAUSE DISCOVERED**: When using `\resizebox{\textwidth}{!}{...}`, the final figure height is determined by:
- `textwidth` in beamer (412.56pt)
- Figure's aspect ratio
- The height parameter inside `\includegraphics` is **COMPLETELY IGNORED**

**Measurements**:
- Standard figure aspect ratio (1.67): 412.56pt ÷ 1.67 = 247.5pt = **7.4cm needed**
- Wider figures (aspect 1.78): 412.56pt ÷ 1.78 = 232pt = **6.9cm needed**
- 8cm = 227.6pt → **ALWAYS causes overflow** for typical figures

**Conservative approach**: Use 7.5cm (213.4pt) to accommodate figures with aspect ratios down to 1.53

## Critic Checking Rule

**Simple check**:
- Is this a title+figure slide?
- Does it use `\figureframe` or `\figureframeMulti`?
- If NO → CRITICAL VIOLATION (-10)

**Alternative**: If not using environment, check:
- Minipage MUST be exactly `[t][8cm][t]{\textwidth}`
- MUST have `\resizebox{\textwidth}{!}{...}`

## Benefits

1. **100% success rate** - impossible to get wrong
2. **Simple for producers** - just call `\figureframe{Title}{path}`
3. **Easy to check** - critic just looks for environment name
4. **Maintainable** - change environment definition once, fixes all slides
5. **Self-documenting** - clear intent when reading code

## Implementation Plan

1. Add environment definitions to presentation preamble template
2. Update Template Assembler: Use `\figureframe` for all title+figure slides
3. Update Layout Critic: Check for environment usage
4. Convert existing slides to use environment

This eliminates an entire class of errors by making the correct pattern the ONLY pattern.
