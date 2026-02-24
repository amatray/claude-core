# Beamer Math and Equation Notation

This document defines standards for mathematical content, equations, and notation in Beamer presentations.

## Equation Environments

### Display Equations

**Always use `equation*` (unnumbered) for slides:**

```latex
\begin{equation*}
Y_{i,t} = \beta X_i + \varepsilon_{i,t}
\end{equation*}
```

**Never use:**
- `\begin{equation}` (numbered equations inappropriate for slides)
- `$$...$$` (deprecated LaTeX)
- `\[...\]` (use equation* for consistency)

### Alignment

For multi-line equations:

```latex
\begin{equation*}
\begin{split}
\log(wage_{i,c,t}) &= \red{\beta_t} \,.\, ICT_{i,0} \times BoomCohort_c \\
                    &\quad + \delta_t \times ICT_{i,0} + \alpha_i \\
                    &\quad + \gamma_c \times \delta_t \times X_{i,0} + \varepsilon_{i,t}
\end{split}
\end{equation*}
```

### Array Environment for Structure

For presenting equation components:

```latex
\begin{equation*}
\begin{array}{ccccccc}
\Delta\overline{w}_{c,t} &=& \blue{\displaystyle \sum_{\tau=c+1}^t \Delta{dh}_{c,\tau}}
                         &+& \red{\Delta{w}_{t}}
                         &+& \green{\Delta\overline\theta_{c}}\\
\\
&& \blue{\text{accumulated}} && \red{\text{demand}} && \green{\text{selection}} \\
&& \blue{\text{human capital}} && \red{\text{shock}} && \green{\text{effect}} \\
\end{array}
\end{equation*}
```

---

## Color Coding in Equations

### Progressive Reveal Pattern

```latex
\begin{equation*}
Y_{c,p,t} = \beta \ \only<1>{\red{Treated_{c}}\times\lightgrey{Post_t}}
                   \only<2>{\lightgrey{Treated_{c}}\times\green{Post_t}}
                   \only<3->{Treated_{c}\times Post_t}
            + \only<1-2>{\lightgrey{\theta_{c}}}
              \only<3>{\blue{\theta_{c}}}
              \only<4->{\theta_{c}}
            + \delta_{p,t} + \varepsilon_{p,c,t}
\end{equation*}
```

**Pattern:**
1. Highlight new component in color
2. Gray out explained components
3. Return to black once all explained

### Component Highlighting

```latex
\begin{equation*}
\Delta\overline{w}_{c,t} = \blue{\displaystyle \sum_{\tau=c+1}^t \Delta{dh}_{c,\tau}}
                          + \lightgrey{\cancel{\Delta{w}_{t}}}
                          + \red{\Delta\overline\theta_{c}}
\end{equation*}
```

**Conventions:**
- `\blue{}`: Primary component of interest
- `\red{}`: Secondary component or alternative mechanism
- `\green{}`: Third component or result
- `\lightgrey{}`: De-emphasized or ruled-out components
- `\cancel{}`: Ruled out by identification

---

## Subscripts and Superscripts

### Standard Notation

```latex
% Individual index:
X_i, Y_{i,t}, Z_{i,j,t}

% Group index:
\bar{X}_g, \mu_c

% Time:
t, t-1, t+1, \tau

% Treatment indicators:
Treated_i, Post_t
```

### Multi-character Subscripts

**Always use braces for multi-character subscripts:**

```latex
% CORRECT:
ICT_{i,0}
BoomCohort_c
X_{i,0}

% INCORRECT:
ICT_i,0
BoomCohort_c
```

### Interaction Terms

```latex
% Standard format:
Treated_i \times Post_t

% Alternative (in tables):
Treated\(\times\)Post
```

---

## Operators and Symbols

### Common Operators

```latex
% Summation:
\sum_{i=1}^{N}
\displaystyle \sum_{\tau=c+1}^t  % Use \displaystyle in inline

% Products:
\prod_{i=1}^{N}

% Integrals:
\int_{0}^{1}

% Limits:
\lim_{n \to \infty}
```

### Arrows and Implications

```latex
% Rightarrow (implication):
\Rightarrow
\red{$\Rightarrow$}

% Arrows in text:
$\rightarrow$
$\Downarrow$
$\Uparrow$

% Double arrows:
$\Longrightarrow$
```

### Mathematical Relations

```latex
% Approximately:
\approx

% Not equal:
\neq

% Greater/Less:
>, <, \geq, \leq

% Independence:
\independent  % Define in preamble
```

### Custom Symbols

**Independence symbol** (define in preamble):

```latex
\newcommand\independent{\protect\mathpalette{\protect\independenT}{\perp}}
\def\independenT#1#2{\mathrel{\rlap{$#1#2$}\mkern2mu{#1#2}}}
```

---

## Greek Letters

### Common Variables

```latex
% Parameters:
\beta, \gamma, \delta, \theta, \lambda, \mu

% Errors:
\varepsilon, \epsilon (prefer \varepsilon)
\eta, \nu

% Statistics:
\sigma (std dev)
\rho (correlation)
```

### Upright Greek

For constants or specific uses:

```latex
\usepackage{upgreek}
\upbeta, \upgamma
```

---

## Text in Math Mode

### Descriptions

```latex
% Use \text{} for words:
\text{accumulated human capital}

% For small font text:
{\small \text{description}}
{\footnotesize \text{note}}
```

### Color Text in Math

```latex
\blue{\text{mechanism}}
\red{\text{demand shock}}
\lightgrey{\text{ruled out}}
```

---

## Brackets and Delimiters

### Sizing

```latex
% Auto-sizing (preferred):
\left( \frac{a}{b} \right)
\left[ \sum_{i} x_i \right]
\left\{ a, b, c \right\}

% Manual sizing (when needed):
\big( \Big( \bigg( \Bigg(
```

### Underbrace/Overbrace

```latex
\underbrace{\text{Expression}}_{\text{Label}}

% Example:
\underbrace{X_i + Y_i}_{\text{Total effect}}
```

---

## Fractions

### Display Style

```latex
% In equation* environment:
\frac{numerator}{denominator}

% Force display style in inline:
\displaystyle \frac{a}{b}
```

### Alternatives

```latex
% For simple fractions in text:
a/b

% For complex inline fractions:
\tfrac{a}{b}  % text-style fraction
```

---

## Matrices and Tables in Math

### Small Matrices

```latex
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}

\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
```

---

## Special Formatting

### Bold Math

```latex
\usepackage{bm}

% Bold symbols:
\bm{\beta}
\bm{X}

% Bold text in math:
\mathbf{X}
```

### Strikethrough

```latex
\usepackage{cancel}

% Cross out:
\cancel{X_i}

% Cross out with custom angle:
\sout{deprecated term}
```

### Colored Math

```latex
% Entire expression:
{\blue{expression}}

% Mixed:
\beta_{\blue{treated}}
```

---

## Statistical Notation

### Expectations and Variance

```latex
E[X_i]
\mathbb{E}[X_i]  % Blackboard bold

Var(X_i)
Cov(X_i, Y_i)
```

### Probability

```latex
P(X > x)
Pr(Event)
```

### Distributions

```latex
X_i \sim N(\mu, \sigma^2)
Y_i \sim F
```

---

## Estimation Notation

### Estimators

```latex
% Hat for estimates:
\hat{\beta}
\hat{Y}_i

% Tilde for alternatives:
\tilde{\beta}

% Bar for means:
\bar{X}
\overline{Treatment}  % For text
```

### Standard Errors

In tables, parentheses below coefficients:

```latex
0.054*** \\
(0.015)
```

### Significance Stars

```latex
*** \quad p < 0.01
**  \quad p < 0.05
*   \quad p < 0.10
```

---

## Spacing in Equations

### Fine-tuning

```latex
% Small space:
\,

% Medium space:
\:

% Large space:
\;

% Quad space:
\quad
\qquad

% Example usage:
\beta \,.\, X_i  % Subtle spacing around dot
```

### Phantom

For alignment without content:

```latex
\phantom{text}

% Example:
\underline{\insertframetitle\phantom{)))))))))}}
```

---

## Common Patterns

### Difference-in-Differences

```latex
Y_{i,t} = \beta \cdot Treatment_i \times Post_t + \alpha_i + \delta_t + \varepsilon_{i,t}
```

### Event Study

```latex
Y_{i,t} = \sum_{\tau \neq -1} \beta_\tau \cdot Treatment_i \times 1\{t = \tau\} + \alpha_i + \delta_t + \varepsilon_{i,t}
```

### First Differences

```latex
\Delta Y_{c,j,t} = \beta \cdot Treatment_c \times Post_t + \delta_{j,p,t} + \varepsilon_{c,j,t}
```

### Interaction Terms

```latex
% Two-way:
X_i \times Z_i

% Three-way:
Treatment_i \times Post_t \times HighIntensity_i
```

---

## Fixed Effects Notation

### Common Abbreviations

```latex
\alpha_i  % Individual FE
\delta_t  % Time FE
\gamma_c  % City/Group FE
\theta_{i,t}  % Individual-time FE
\delta_{j,p,t}  % Industry-pair-time FE
```

### In Text

```latex
% List FEs:
\text{with } \alpha_i, \delta_t \text{ and } \gamma_c \times \delta_t
```

---

## Robustness and Specification

### Conditional Expectations

```latex
E[Y_i | X_i, Treatment_i]
```

### Instrument Variables

```latex
% First stage:
X_i = \pi Z_i + \nu_i

% Second stage:
Y_i = \beta \hat{X}_i + \varepsilon_i
```

---

## Best Practices

1. **Consistency**: Use same notation throughout presentation
2. **Color strategically**: Only highlight what's being discussed
3. **Spacing**: Use `\,` around operators for readability
4. **Subscripts**: Always brace multi-character subscripts
5. **Alignment**: Align equals signs in multi-line equations
6. **Labels**: Use `\text{}` for word labels in math mode
7. **Size**: Use `\displaystyle` sparingly in inline math

---

**Usage Note:** This guide should be referenced by Writer and Style-Critic agents to ensure mathematical notation consistency.
