# Beamer Visual Style Guide

This document defines the visual style standards for academic Beamer presentations based on Adrien Matray's established style.

## Document Class

```latex
\documentclass[notes,11pt,aspectratio=169]{beamer}
% OR for some presentations:
\documentclass[svgnames, 9pt, aspectratio=169]{beamer}
```

**Standard settings:**
- Aspect ratio: **16:9** (widescreen)
- Font size: **9pt** or **11pt**
- Notes: Include speaker notes

## Color Palette

### Primary Colors

Colors are defined with both RGB and rgb formats. Use the RGB format (0-255 scale) as primary:

```latex
% Primary blue (main structural color)
\definecolor{blue}{RGB}{0,76,153}
% Alternate: \definecolor{blue}{RGB}{30, 80, 140}

% Primary red (emphasis, negative findings)
\definecolor{red}{RGB}{140,0,0}
% Alternate: \definecolor{red}{RGB}{150,30,0}

% Green (positive findings, highlights)
\definecolor{vert}{RGB}{30,132,73}
% Alternate: \definecolor{green}{RGB}{50, 120, 40}

% Orange (secondary emphasis)
\definecolor{orange}{RGB}{211,84,0}
% Alternate: \definecolor{orange}{RGB}{220,80,1}
```

### Grayscale Colors

```latex
\definecolor{lightgrey}{RGB}{121,121,121}
\definecolor{grey}{RGB}{80,80,80}
\definecolor{ultralightgrey}{RGB}{220,220,220}  % For backgrounds
```

### Optional Colors

```latex
\definecolor{purple}{RGB}{120, 50, 160}
\definecolor{darkolivegreen}{rgb}{0.33, 0.42, 0.18}
\definecolor{darkorange}{rgb}{1.0, 0.55, 0.0}
```

## Color Command Shortcuts

**CRITICAL:** Always use these shortcuts instead of `\textcolor{}` directly:

```latex
\def\blue{\textcolor{blue}}
\def\red{\textcolor{red}}
\def\green{\textcolor{green}}      % or \vert depending on presentation
\def\orange{\textcolor{orange}}
\def\lightgrey{\textcolor{lightgrey}}
\def\grey{\textcolor{grey}}
\def\white{\textcolor{white}}
\def\black{\textcolor{black}}
\def\purple{\textcolor{purple}}
\def\ultralightgrey{\textcolor{ultralightgrey}}
```

**Usage example:**
```latex
% CORRECT:
\blue{Important text}
\red{Negative finding}

% INCORRECT:
\textcolor{blue}{Important text}
```

## Frame Title Style

```latex
\setbeamertemplate{frametitle}{
    \medskip
    \smallskip
    \hspace{0.05cm}
    {\large{\underline{\insertframetitle\phantom{))))))))}}}
}
% Alternate with negative margin:
% \hspace{-0.3cm}
% {\Large{\underline{\insertframetitle\phantom{))))))))}}}
```

**Key features:**
- Frame titles are **underlined**
- Phantom characters ensure underline extends beyond text
- Use `\large` or `\Large` for title size
- Small left margin (0.05cm or -0.3cm)

## Typography

### Fonts

**Primary font:** Lato (default) or Helvetica

```latex
\usepackage{helvet}
\usepackage[default]{lato}
```

**Math fonts:**
```latex
\usepackage{mathpazo}
\usepackage{amssymb,amsmath,eurosym}
\usepackage{bm}  % Bold math
```

### Text Formatting Shortcuts

```latex
\def\it{\textit}
\def\bf{\textbf}
\def\tsub{\textsubscript}
\def\under{\underline}
```

## Margins and Spacing

```latex
\setbeamersize{text margin left=0.5cm}
\setbeamersize{text margin right=1cm}
% Some presentations use:
% \setbeamersize{text margin left=0.9cm}
% \setbeamersize{text margin left=1.2cm}
```

## Itemize/Enumerate Customization

### Item Bullet Style

```latex
\setbeamertemplate{itemize items}{--}  % Use dashes, not bullets
```

### Spacing Shortcuts

**CRITICAL:** Use these consistently for vertical spacing:

```latex
\def\bitem{\bigskip\item}      % Big space before item
\def\mitem{\medskip\item}      % Medium space before item
\def\vitem{\vfill\item}        % Vertical fill before item

% Environment shortcuts:
\def\bi{\begin{itemize}}
\def\ei{\end{itemize}}
\def\bnum{\begin{enumerate}}
\def\enum{\end{enumerate}}
```

### Enhanced Spacing

Some presentations add extra itemsep:

```latex
\let\olditemize\itemize
\renewcommand{\itemize}{\olditemize\addtolength{\itemsep}{.4em}}

\let\oldenumerate\enumerate
\renewcommand{\enumerate}{\oldenumerate\addtolength{\itemsep}{1em}\addtolength{\parsep}{1em}}
```

## Beamer Theme Settings

```latex
\usecolortheme[named=blue]{structure}
\setbeamercolor{structure}{fg=blue!90}
\setbeamertemplate{navigation symbols}{}  % Remove navigation
```

## Special Commands

### Check/Cross Marks

```latex
\usepackage{pifont}
\newcommand{\cmark}{\ding{51}}  % ✓
\newcommand{\xmark}{\ding{55}}  % ✗
```

### Reference Formatting

```latex
% Grey citations in small font
\newcommand{\refgrey}[1]{\textcolor{gray}{{\footnotesize \hspace{.2cm} (#1)}}}

% Bottom note formatting
\newcommand{\buttom}[1]{\textcolor{lightgrey}{{\hspace{.2cm} \footnotesize [#1]}}}
```

### Fixed Width Colors

For overlays where text changes color:

```latex
\usepackage{calc}
\newcommand{\fixedwidthcolor}[2]{\makebox[\widthof{#2}][l]{\textcolor<1>{#1}{#2}}}
```

## Block Dimensions

```latex
\newlength{\blockheight}
\setlength{\blockheight}{0.6cm}
\newlength{\blockwidth}
\setlength{\blockwidth}{25cm}
```

## Color Usage Guidelines

### By Meaning

- **\blue{}**: Main points, structural elements, questions, institutional focus
- **\red{}**: Negative findings, problems, criticism, emphasis on issues
- **\green{}**: Positive findings, solutions, policy names, approval
- **\orange{}**: Secondary emphasis, technical terms
- **\lightgrey{}**: Citations, back references, de-emphasized content
- **\grey{}**: Less important text, crossed-out ideas

### In Equations

Use colors to highlight specific components during reveals:

```latex
\begin{equation*}
    Y_{i,t} = \blue{\beta} \times \red{Treatment_i} \times \green{Post_t} + \varepsilon_{i,t}
\end{equation*}
```

### Progressive Reveals

Combine with overlays to gray out previous content:

```latex
\only<1>{\blue{New information}}
\only<2>{\lightgrey{Previous information}}
\only<2>{\blue{Newer information}}
```

## Common Patterns

### Hyperlinks

Always provide "back" links in appendix slides:

```latex
\hyperlink{target_label}{{\tiny \lightgrey{[Link text]}}}
```

### Scalebox for Tables

```latex
\scalebox{.7}{
    \begin{tabular}{...}
    ...
    \end{tabular}
}
```

### Figure Sizing

```latex
\includegraphics[width=0.8\textwidth]{figure.pdf}
% OR
\includegraphics[height=.7\textheight]{figure.pdf}
```

## Package Loading Order

Critical packages to load (in order):

```latex
\usepackage{upgreek}
\usepackage[normalem]{ulem}
\usepackage{comment}
\usepackage{helvet}
\usepackage[default]{lato}
\usepackage{array}
\usepackage{mathpazo}
\usepackage{bbm}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{bm}
\usepackage[makeroom]{cancel}
\usepackage{wrapfig,graphicx}
\usepackage{subcaption}
\usepackage{xcolor,soul}
\usepackage{tikz}
\usepackage{booktabs}
\usepackage{[authoryear]{natbib}
\usepackage{tabu}
\usepackage{color, colortbl}
\usepackage{hyperref}  % Load last
```

---

**Usage Note:** This style guide should be referenced by all producer and critic agents to ensure visual consistency across all generated frames.
