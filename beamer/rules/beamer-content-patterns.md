# Beamer Content Patterns

This document catalogs the standard content structures and patterns observed across academic presentations.

## Overall Presentation Structure

### Standard Flow

```
1. Title Slide
2. Motivation (1-2 slides)
3. Question (1 slide, centered)
4. "This Paper" / Contributions (1 slide)
5. [Optional] Literature / Contribution to Literature
6. Outline / Roadmap
7. [Optional] Institutional Setting / Context
8. Data & Empirical Strategy
9. Results (multiple slides, graphs first then tables)
10. Mechanism / Additional Analysis
11. Robustness (optional, often in appendix)
12. Conclusion / Take-away
13. Thank You
14. Appendix
```

### Timing Guidelines

- **20-minute talk**: 15-20 substantive slides + appendix
- **45-minute seminar**: 30-40 substantive slides + appendix
- **Job talk**: 50-60 substantive slides + extensive appendix

**Rule of thumb**: 1-2 minutes per substantive slide

---

## Frame Patterns by Type

### 1. Title Slide

```latex
\begin{frame}
\maketitle
\end{frame}
```

**Author format:**
```latex
\author{{\large Author Name}\\{\small Institution} \vskip 0.5cm
        {\large Second Author} \\{\small Institution, Affiliations}}

\title{\Large Paper Title Here}

\date{\textcolor{lightgrey}{{\normalsize {\sc Venue Name}}}}
```

**Key patterns:**
- Author names in `\large`
- Institutions in `\small`
- Affiliations (NBER, CEPR) after institution
- Vertical spacing: `\vskip 0.5cm` between authors
- Date uses `\lightgrey{}` for venue
- Some presentations add disclaimer at bottom

---

### 2. Motivation Slide

**Structure:**
- Start with general statement/context
- Use progressive reveals (`\pause`)
- Narrow to specific issue
- End with implication or example

**Pattern 1: Problem → Implication → Example**

```latex
\begin{frame}{Motivation}

\hspace{.1cm} General phenomenon or context
\medskip
\begin{itemize}
   \bitem[$\Rightarrow$] \blue{Key implication}
   \begin{itemize}
       \onslide<2->{ \bitem[$\Rightarrow$] Specific consequence }
       \onslide<3->{ \bitem[$\Rightarrow$] Potential mechanism }
       \begin{itemize}
           \onslide<3->{\mitem Details or subcases}
       \end{itemize}
   \end{itemize}
\onslide<3>{\bitem Examples: current context, historical episodes, etc.}
\end{itemize}
\end{frame}
```

**Pattern 2: Facts → Questions**

```latex
\begin{frame}{Motivation}

\begin{itemize}
\item Observation about policy/phenomenon:
\begin{itemize}
    \mitem Specific fact or statistic
    \mitem Impact or scope
\end{itemize}

\pause
\vfill\bitem[$\Rightarrow$] \blue{Widespread policy response }
    \begin{itemize}
        \mitem Success?
        \mitem Exact \blue{channels}?
        \mitem \blue{Distributional} effects?
    \end{itemize}
\end{itemize}
\end{frame}
```

---

### 3. Question Slide

**Always centered, always large font:**

```latex
\begin{frame}\frametitle{Question}

\centering
\Large{How does [intervention] affect \blue{outcome} and \blue{mechanism}?}
\end{frame}
```

**Variations:**

```latex
% With sub-questions:
\begin{frame}\frametitle{Questions}
    {\Large \hspace{.2cm} Effect of X on Y?}
    \pause
    \begin{itemize}
        \vfill\item[1.] Specific question one?
        \vfill\item[2.] Specific question two?
        \begin{itemize}
            \mitem Sub-component?
            \mitem Related aspect?
        \end{itemize}
    \end{itemize}
   \bigskip
 {\Large\hspace{.2cm}$\rightarrow$ Matters for \blue{broader implication}}
\end{frame}
```

---

### 4. "This Paper" / Contributions Slide

**Standard pattern with enumerate and progressive reveals:**

```latex
\begin{frame}\frametitle{This paper}
\begin{itemize}
\item[1.] First main finding
\begin{itemize}
\vfill\item Details or magnitude
\end{itemize}
\pause

\vfill\item[2.] Second main finding
    \begin{itemize}
    \mitem Details
    \mitem[$\Rightarrow$] Interpretation
    \end{itemize}
\pause

\vfill\item[3.] Third main finding
\pause

\vfill\item[4.] Mechanism or framework
\end{itemize}
\end{frame}
```

**Advanced pattern with conditional reveals:**

```latex
\begin{frame}<1-7>\frametitle{This paper}

\begin{enumerate}
    \item<1-> Question one? \only<1-2>{\white{Yes!}}{\only<3->{\bf{\green{Yes}}}}

    \begin{itemize}
        \mitem<2->[\alt<4->{\textcolor{gray}{--}}{--}]
        \alt<4->{\grey{Finding detail}}{\only<2>{Finding detail}}

        \mitem<2->[\alt<4->{\textcolor{gray}{--}}{--}]
        \alt<4->{\grey{More detail}}{\only<2>{More detail}}
    \end{itemize}

    \bitem<4-> Next major finding? \alt<1-3>{\white{Yes}}{\green{\textbf{Yes}}}
    \begin{itemize}
        \mitem<5-> Details with specific magnitudes
    \end{itemize}

    \bitem<6-> Framework? \alt<1-6>{\white{Name}}{\green{\textbf{Framework Name}}}
\end{enumerate}
\end{frame}
```

---

### 5. Literature / Contribution Slide

```latex
\begin{frame}\frametitle{Contribution to the Literature}
\begin{enumerate}
    \item \blue{\bf{Literature strand name}}.
    {\scriptsize Key papers in strand
    \grey{(Author Year; Author Year)}}

    \vfill\item \blue{\bf{Second literature strand}}.
    {\scriptsize Description
    \grey{(Author Year)}}

    \vfill\item \blue{\bf{Third strand}}.
    {\scriptsize Context
    \grey{(Citations)}}

    \vfill\item \blue{\bf{Fourth strand}}
    {\scriptsize \grey{(More citations)}}
\end{enumerate}
\end{frame}
```

**Key patterns:**
- Literature name in `\blue{\bf{}}`
- Citations in `\grey{}` and `\scriptsize`
- Use `\vfill` between items
- Keep description very brief, let citations speak

---

### 6. Outline / Roadmap Slides

**Simple version:**

```latex
\begin{frame}{Outline}
\begin{enumerate}
    \bitem[1.] Section Name
    \bitem[\lightgrey{2.}] \lightgrey{Section Name}
    \bitem[\lightgrey{3.}] \lightgrey{Section Name}
    \bitem[\lightgrey{4.}] \lightgrey{Section Name}
\end{enumerate}
\end{frame}
```

**Automated with sections:**

```latex
% In preamble:
\AtBeginSection[]{
    \begin{frame}
        \frametitle{Outline}
        \tableofcontents[currentsection,hideallsubsections]
    \end{frame}
}
```

---

### 7. Context / Institutional Setting Slides

**Pattern: Statement → Details → Visual**

```latex
\begin{frame}[t]{Context}
    \blue{\textbf{Year--Year Event}} description
    \vspace{.5cm}
    \only<1>{

    \bigskip
    Background information:
    \begin{itemize}
        \mitem Details
    \end{itemize}
    }

    \uncover<2->{
        \begin{columns}
            \begin{column}{.4\textwidth}
                \begin{itemize} \small
                    \item [-] Description:
                    \item [] \red{Cause}
                \end{itemize}
                \medskip
                \resizebox{\linewidth}{!}{
                  \includegraphics[height=5cm]{figure.png}
                }
            \end{column}
            \uncover<3->{
                \begin{column}{.45\textwidth}
                    % Second column
                \end{column}
            }
        \end{columns}
    }
\end{frame}
```

---

### 8. Data Slides

```latex
\begin{frame}\frametitle{Data}

\begin{itemize}
    \vfill \item \blue{Dataset name:} Source
    \begin{itemize}
        \mitem Level: granularity
        \item Coverage: time period
    \end{itemize}

    \vfill \item \blue{Second dataset:} Source
    \begin{itemize}
        \mitem Details
    \end{itemize}

    \vfill\item \blue{Third dataset:} Source
    \begin{itemize}
        \mitem Details
    \end{itemize}
\end{itemize}

\end{frame}
```

---

### 9. Empirical Strategy Slide

**Pattern: Equation → Progressive explanation**

```latex
\begin{frame}{Specification: description}

\vspace{1cm}
\begin{itemize}
\item[] City $c$, belonging to pair $p$ in year $t$
\end{itemize}
\bigskip

\begin{equation*}
Y_{c,p,t} = \beta \ \only<1>{\red{Treated_{c}}\times\lightgrey{Post_t}}
            \only<2>{\lightgrey{Treated_{c}}\times\green{Post_t}}
            \only<3->{Treated_{c}\times Post_t}
            + \only<1-2>{\lightgrey{\theta_{c}}}
            \only<3>{\blue{\theta_{c}}}
            \only<4>{\theta_{c}}
            + \delta_{p,t} + \varepsilon_{p,c,t}
\end{equation*}

\bigskip\bigskip
\begin{minipage}[t][10cm][t]{\textwidth}
\begin{itemize}

\only<1>{
\item \red{Treated}\hspace{2.3cm}: Description
\item[]\white{Treated}\hspace{2.4cm} $\rightarrow$ Implication
}

\only<2->{
\mitem \only<2>{\green{Post}}\only<3->{\lightgrey{Post}}\hspace{2.9cm}:
       \only<2>{Description}\only<3->{\lightgrey{Description}}
}

\only<3->{
\mitem \only<3>{\blue{City}}\only<4>{\lightgrey{City}} FE:
       \only<3>{Purpose}\only<4>{\lightgrey{Purpose}}
}

\end{itemize}
\end{minipage}
\end{frame}
```

---

### 10. Results Slides

#### Graph Results

```latex
\begin{frame}[label=result_name]{Effect on \bf{Outcome}}
\vspace{-.2cm}
\begin{minipage}[t][1cm][t]{\textwidth}
\begin{itemize}
{
\only<1>{\footnotesize\item First interpretation}
\only<2>{\footnotesize\item Second interpretation}
\only<3>{\footnotesize\item Final interpretation \hyperlink{table_result}{{\tiny\lightgrey{Table}}}}
}
\end{itemize}
\end{minipage}

\centering
\begin{minipage}[t][9cm][t]{\textwidth}
\begin{columns}[T]
\begin{column}{.70\textwidth}
    \only<1>{\resizebox{\textwidth}{!}{
      \includegraphics[width=2cm]{result1.pdf}
    }}
    \only<2>{\resizebox{\textwidth}{!}{
      \includegraphics[width=2cm]{result2.pdf}
    }}
    \only<3>{\resizebox{\textwidth}{!}{
      \includegraphics[width=2cm]{result3.pdf}
    }}
\end{column}
\end{columns}
\end{minipage}
\end{frame}
```

#### Table Results

```latex
\begin{frame}\frametitle{Effect on Outcome}

\begin{itemize}
{\footnotesize
\only<1>{\item Column 1 interpretation}
\only<2>{\item Column 2 interpretation}
\only<3>{\item Column 3 interpretation}
}
\end{itemize}

\begin{center}
\scalebox{.8}{
\begin{tabular}{l c <{\onslide<2->}c<{\onslide<3->}c<{\onslide}}

\toprule\addlinespace
& \multicolumn{3}{c}{Outcome Variable}\\
\addlinespace\midrule\addlinespace

Treated$\times$Post  &  0.054*** &  0.042**  &  0.111*** \\
                     & (0.015)   & (0.017)   & (0.028)   \\

\addlinespace\midrule\addlinespace
Controls             & \checkmark& \checkmark& \checkmark\\
FE                   & \checkmark& \checkmark& \checkmark\\
Observations         & 10,000    & 10,000    & 10,000    \\
\addlinespace\bottomrule
\end{tabular}}
\end{center}
\end{frame}
```

---

### 11. Takeaway / Conclusion Slide

```latex
\begin{frame}\frametitle{Take-away \& final thoughts}
\only<1>{
\hspace{.3cm} \bf{Two main results}:
\begin{enumerate}
    \bitem Finding one with \blue{mechanism}
    \begin{itemize}
        \mitem Magnitude or detail
        \mitem Not explained by alternative
    \end{itemize}

    \bitem Finding two \blue{amplified by factor}
\end{enumerate}
}

\only<2>{
\bigskip
\hspace{.3cm} \bf{Implications}:
\begin{itemize}
    \bitem \blue{Broader question?}
    \begin{itemize}
        \mitem \red{Our paper}: answer
    \end{itemize}

    \mitem \blue{Policy question?}
    \begin{itemize}
        \mitem Evidence
    \end{itemize}
\end{itemize}
}
\end{frame}
```

---

### 12. Thank You Slide

```latex
\begin{frame}\frametitle{}
\centering

{\LARGE \blue{Thank you!}}

\bigskip
contact: email@institution.edu
\end{frame}
```

---

## Special Patterns

### Progressive Table Reveals

```latex
% Column-by-column reveal:
<{\onslide<2->}c<{\onslide<3->}c<{\onslide}}

% Row-by-row with color change:
\only<1>{Finding}\only<2>{\red{Finding}}
```

### Conditional Formatting

```latex
\alt<4->{\grey{Old info}}{\blue{New info}}
```

### Frame References

```latex
\begin{frame}[label=main_result]
...
\end{frame}

% Later, return to frame:
\againframe<5->{main_result}
```

### Hyperlink Patterns

```latex
% In main slide:
\hyperlink{appendix_detail}{{\tiny \lightgrey{[Details]}}}

% In appendix:
\begin{frame}\label{appendix_detail}
...
\hfill \hyperlink{main_slide}{\tiny \lightgrey{Back}}
\end{frame}
```

---

## Content Guidelines

### Text Density

- **Maximum bullets per slide**: 10 (preferably 5-7)
- **Nesting depth**: Maximum 3 levels
- **Equation complexity**: One main equation per slide

### Progressive Reveals

- Use `\pause` for simple reveals
- Use `\only<>` for replacing content
- Use `\onslide<>` for cumulative reveals
- Use `\alt<>{}{}` for conditional formatting

### Emphasis Patterns

- **\blue{}**: Main findings, institutional features
- **\red{}**: Problems, negative findings, critical issues
- **\green{}**: Solutions, positive findings, policies
- `\bf{}`: Key terms first mention
- `\it{}`: Emphasis or definition

---

**Usage Note:** These patterns should guide the Beamer Architect and Writer agents in structuring content appropriately.
