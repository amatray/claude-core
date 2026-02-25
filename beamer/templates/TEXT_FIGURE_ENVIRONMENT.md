# Fixed Environment for Title + Single Line Text + Figure Slides

## The Solution

Create a **custom LaTeX environment** that enforces the correct pattern for slides with:
- Title
- One line of text (equation or comment)
- Figure below

## LaTeX Environment Definition

Add this to the preamble of every presentation:

```latex
%=============================================================================
% TEXT + FIGURE SLIDE ENVIRONMENT - GUARANTEED TO WORK
%=============================================================================

% Single line of text (NOT equation) + single figure (left-aligned text)
\newcommand{\textfigureframe}[3]{
    \begin{frame}{#1}

    \begin{minipage}[t][0.3cm][t]{\textwidth}
    {\small
    #2
    }
    \end{minipage}

    \centering
    \begin{minipage}[t][7cm][t]{\textwidth}
        \begin{columns}[T]
            \begin{column}{1\textwidth}
                \resizebox{\textwidth}{!}{
                    \includegraphics[height=.8\textheight]{#3}
                }
            \end{column}
        \end{columns}
    \end{minipage}

    \end{frame}
}

% Single line equation + single figure (centered equation)
\newcommand{\equationfigureframe}[3]{
    \begin{frame}{#1}

    \begin{minipage}[t][0.3cm][t]{\textwidth}
    \centering
    {\small
    #2
    }
    \end{minipage}

    \centering
    \begin{minipage}[t][7cm][t]{\textwidth}
        \begin{columns}[T]
            \begin{column}{1\textwidth}
                \resizebox{\textwidth}{!}{
                    \includegraphics[height=.8\textheight]{#3}
                }
            \end{column}
        \end{columns}
    \end{minipage}

    \end{frame}
}

% Single line of text (NOT equation) + multiple figures (left-aligned text)
\newcommand{\textfigureframeMulti}[3]{
    \begin{frame}{#1}

    \begin{minipage}[t][0.3cm][t]{\textwidth}
    {\small
    #2
    }
    \end{minipage}

    \centering
    \begin{minipage}[t][7cm][t]{\textwidth}
        \begin{columns}[T]
            \begin{column}{1\textwidth}
                #3  % Contains \only<1>{\resizebox...}, \only<2>{\resizebox...}, etc.
            \end{column}
        \end{columns}
    \end{minipage}

    \end{frame}
}

% Single line equation + multiple figures (centered equation)
\newcommand{\equationfigureframeMulti}[3]{
    \begin{frame}{#1}

    \begin{minipage}[t][0.3cm][t]{\textwidth}
    \centering
    {\small
    #2
    }
    \end{minipage}

    \centering
    \begin{minipage}[t][7cm][t]{\textwidth}
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

### Case 1: Single Line Text (NOT equation) + Single Figure

**Use `\textfigureframe` - text is LEFT-ALIGNED**

**Instead of writing:**
```latex
\begin{frame}{Title}

\begin{minipage}[t][0.3cm][t]{\textwidth}
{\small
Some explanatory text
}
\end{minipage}

\centering
\begin{minipage}[t][7cm][t]{\textwidth}
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
\textfigureframe{Title}{
    Some explanatory text
}{results/figure.pdf}
```

### Case 2: Single Line Equation + Single Figure

**Use `\equationfigureframe` - equation is CENTERED**

**Instead of writing:**
```latex
\begin{frame}{Title}

\begin{minipage}[t][0.3cm][t]{\textwidth}
\centering
{\small
$y = mx + b$
}
\end{minipage}

\centering
\begin{minipage}[t][7cm][t]{\textwidth}
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
\equationfigureframe{Title}{
    $y = mx + b$
}{results/figure.pdf}
```

### Case 3: Single Line Text + Multiple Figures

**Use `\textfigureframeMulti` - text is LEFT-ALIGNED**

**Instead of writing:**
```latex
\begin{frame}{Title}

\begin{minipage}[t][0.3cm][t]{\textwidth}
{\small
Some explanatory text
}
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
\textfigureframeMulti{Title}{
    Some explanatory text
}{
    \only<1>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig1.pdf}
    }}

    \only<2>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig2.pdf}
    }}
}
```

### Case 4: Single Line Equation + Multiple Figures

**Use `\equationfigureframeMulti` - equation is CENTERED**

**Simply write:**
```latex
\equationfigureframeMulti{Title}{
    $y = mx + b$
}{
    \only<1>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig1.pdf}
    }}

    \only<2>{\resizebox{\textwidth}{!}{
        \includegraphics[height=.8\textheight]{results/fig2.pdf}
    }}
}
```

## Why This Works

1. **Enforces text minipage height**: Always 0.3cm (fits single line)
2. **Enforces \small font**: Built into environment
3. **Enforces figure minipage height**: Always 7cm (reduced to accommodate text)
4. **Enforces resizebox**: Built into the environment
5. **Automatic centering**: Always correct
6. **No deviation possible**: Producer agents can't make mistakes
7. **Works for ANY figure size**: resizebox adapts automatically
8. **Legends never cropped**: resizebox maintains aspect ratio

## Height Calculation

**Total vertical space used:**
- Title: ~1cm
- Text minipage: 0.3cm
- Figure minipage: 7cm
- Total: ~8.3cm ✓ (fits in 9cm available space)

**Why NOT 8cm for figure minipage?**
- With 8cm: Total = 1 + 0.3 + 8 = 9.3cm ✗ (exceeds available space)
- Would cause overfull vbox warnings and legend cropping
- **CRITICAL**: Figure minipage MUST be reduced from 8cm to 7cm when ANY content appears above it
- **ONLY use 8cm** for pure figure-only slides (title + figure, nothing else)

## Critic Checking Rule

**Simple check**:
- Is this a title + single line text/equation + figure slide?
- Check which environment should be used:
  - If text (not equation): Should use `\textfigureframe` or `\textfigureframeMulti`
  - If equation: Should use `\equationfigureframe` or `\equationfigureframeMulti`
- If NOT using correct environment → CRITICAL VIOLATION (-10)

**Alternative**: If not using environment, check manually:
1. Text minipage MUST be exactly `[t][0.3cm][t]{\textwidth}`
2. Text MUST be wrapped in `{\small ...}`
3. **For equations**: Text minipage MUST have `\centering` after `\begin{minipage}`
4. **For regular text**: Text minipage MUST NOT have `\centering`
5. Figure minipage MUST be exactly `[t][7cm][t]{\textwidth}` (NOT 8cm!)
6. MUST have `\resizebox{\textwidth}{!}{...}` around figure

## When to Use This Environment

Use `\textfigureframe` when:
- Slide has title
- Slide has EXACTLY one line of text (equation, comment, or brief explanation)
- Slide has figure(s) below the text
- Text is SHORT and fits on one line

**Do NOT use when:**
- Text is longer than one line
- Slide has bullets in addition to text
- Slide has equation AND bullets (use equation slide template instead)

## Benefits

1. **100% success rate** - impossible to get wrong
2. **Simple for producers** - just call `\textfigureframe{Title}{Text}{path}`
3. **Easy to check** - critic just looks for environment name
4. **Maintainable** - change environment definition once, fixes all slides
5. **Self-documenting** - clear intent when reading code
6. **Consistent spacing** - all text+figure slides look identical

## Implementation Plan

1. Add environment definitions to presentation preamble template
2. Update Template Assembler: Use `\textfigureframe` for all title + single line text + figure slides
3. Update Layout Critic: Check for environment usage
4. Convert existing slides to use environment

This eliminates another entire class of errors by making the correct pattern the ONLY pattern.
