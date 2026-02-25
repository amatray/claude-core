# Master File Structure for Beamer Presentations

## Overview

This structure organizes Beamer presentations into modular files for easier development, debugging, and collaboration.

## File Structure

```
presentation/
├── main.tex                    # Master file (compile this)
├── preamble.tex               # Standard preamble with packages and settings
└── sections/                  # Section files
    ├── 00_title.tex          # Title slide
    ├── 01_introduction.tex   # Introduction section
    ├── 02_motivation.tex     # Motivation section
    ├── 03_data.tex           # Data section
    ├── 04_empirical_strategy.tex  # Empirical strategy
    ├── 05_results.tex        # Results section
    ├── 06_robustness.tex     # Robustness checks
    ├── 07_conclusion.tex     # Conclusion section
    └── 99_thankyou.tex       # Thank you slide
```

## Usage

### Compiling the Presentation

Always compile `main.tex`:

```bash
xelatex main.tex
xelatex main.tex
xelatex main.tex
```

Or use the compile script:

```bash
bash ~/claude-workflows/claude-core/beamer/scripts/compile_beamer.sh main.tex
```

### Working on Specific Sections

1. Open the relevant section file (e.g., `sections/05_results.tex`)
2. Make edits to that section only
3. Recompile `main.tex` to see changes
4. All sections remain independent and modular

### Debugging

When you get compilation errors:
1. Check the error message for the section file name
2. Open that specific section file
3. Fix the error in isolation
4. Recompile main.tex

### Adding New Sections

1. Create a new file in `sections/` (e.g., `sections/08_discussion.tex`)
2. Add section frames to that file
3. Add `\input{sections/08_discussion.tex}` to `main.tex` in the appropriate location
4. Add `\section{Discussion}` before the `\input` command

## Section File Format

Each section file should:

1. Start with a comment header identifying the section
2. Contain only `\begin{frame}...\end{frame}` blocks
3. Use comment dividers between frames for clarity
4. NOT include `\section{}` commands (those go in main.tex)

Example:

```latex
% Section: Results
%=============================================================================

%-----------------------------------------------------------------------------
% Frame: Main Result 1
%-----------------------------------------------------------------------------

\begin{frame}
\frametitle{Main Finding}
...
\end{frame}

%-----------------------------------------------------------------------------
% Frame: Main Result 2
%-----------------------------------------------------------------------------

\begin{frame}
\frametitle{Supporting Evidence}
...
\end{frame}
```

## Benefits

1. **Modularity**: Work on one section without scrolling through entire presentation
2. **Debugging**: Errors point to specific section files
3. **Collaboration**: Multiple people can work on different sections simultaneously
4. **Version control**: Git diffs show changes to specific sections
5. **Reusability**: Sections can be reordered or reused across presentations
6. **Focus**: Compile just the sections you're working on (comment out others in main.tex)

## Tips

### Temporarily Disable Sections

Comment out sections in main.tex during development:

```latex
% \input{sections/04_empirical_strategy.tex}  % Skip for now
```

### Section Naming Convention

Use numerical prefixes for ordering:
- `00_` - Title slide
- `01-09_` - Main sections
- `10-19_` - Additional sections if needed
- `99_` - Thank you slide

### Preamble Organization

Keep `preamble.tex` in the presentation directory alongside `main.tex`, or use:

```latex
\input{~/path/to/shared/preamble.tex}
```

for a shared preamble across presentations.
