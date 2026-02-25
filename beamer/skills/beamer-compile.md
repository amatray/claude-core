# Beamer Compile Skill

This skill handles compilation of Beamer presentations with proper LaTeX build sequence.

## When to Use

Use this skill when:
- User has existing .tex file that needs compilation
- After beamer-generate completes
- User requests PDF generation

## Compilation Sequence

Standard Beamer compilation requires multiple passes:

```bash
xelatex main.tex       # First pass - generates aux files
bibtex main            # Process bibliography (if citations present)
xelatex main.tex       # Second pass - incorporates bibliography
xelatex main.tex       # Third pass - resolves cross-references
```

### Why Multiple Passes?

1. **First xelatex pass**: Identifies structure, creates .aux file with reference placeholders
2. **Bibtex**: Processes citations, creates .bbl file
3. **Second xelatex pass**: Incorporates bibliography, updates references
4. **Third xelatex pass**: Resolves all cross-references, ensures stable output

## Pre-Compilation Checks

Before compiling, verify:

### 1. File Existence

```bash
# Check main file exists:
ls main.tex

# Check input files exist:
ls 0_packages.tex sections/*.tex (if using \input)
```

### 2. Graphics Files

```bash
# Verify all graphics exist:
find . -name "*.pdf" -o -name "*.png" -o -name "*.jpg"

# Cross-reference with \includegraphics commands in .tex
```

### 3. Required Packages

Standard packages should be available. If compilation fails, check:
- LaTeX distribution is up to date (TeXLive 2023+ or MikTeX)
- Required packages installed: beamer, booktabs, tikz, xcolor, etc.

## Compilation Options

### Basic Compilation

```bash
xelatex -interaction=nonstopmode main.tex
```

**Options:**
- `-interaction=nonstopmode`: Don't stop on errors, continue to end
- `-halt-on-error`: Stop immediately on first error (for debugging)
- `-file-line-error`: Show file and line number for errors

### With Bibliography

```bash
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### With Output Control

```bash
xelatex -interaction=nonstopmode -output-directory=output main.tex
```

## Output Interpretation

### Success

```
Output written on main.pdf (25 pages, 1234567 bytes).
Transcript written on main.log.
```

**Indicators:**
- PDF file created
- Page count reasonable
- No errors in log
- Warnings acceptable if < 5

### Compilation Errors

```
! Undefined control sequence.
l.47 \customcommand
                   {text}
```

**Action:**
1. Note error line number (l.47)
2. Identify problem (undefined command)
3. Report to user with fix suggestion

### Common Warnings

**Overfull \hbox**:
```
Overfull \hbox (12.3pt too wide) in paragraph at lines 52--53
```

**Action:**
- If < 5pt: Ignore (usually invisible)
- If 5-10pt: Note to user, likely visible
- If > 10pt: Critical, must fix

**Underfull \hbox**:
```
Underfull \hbox (badness 10000) in paragraph at lines 60--61
```

**Action:**
- Usually cosmetic
- Note if excessive (badness > 10000)
- Suggest rewording or \sloppy if needed

## Error Handling

### Missing Files

```
! LaTeX Error: File `figure1.pdf' not found.
```

**Solution:**
1. List required files for user
2. Suggest checking file paths
3. Offer placeholder compilation (comment out \includegraphics)

### Package Errors

```
! LaTeX Error: File `tikz.sty' not found.
```

**Solution:**
1. Identify missing package (tikz)
2. Provide installation command:
   - TeXLive: `tlmgr install tikz`
   - MikTeX: Automatic installation on first use
3. Suggest updating LaTeX distribution

### Font Errors (XeLaTeX specific)

```
! Package fontspec Error: The font "Lato" cannot be found.
```

**Solution:**
1. Check if font installed on system
2. Suggest alternative: `\usepackage{helvet}` instead
3. Or install Lato font system-wide

## Post-Compilation

### Verify Output

```bash
# Check PDF was created:
ls -lh main.pdf

# Check page count matches expected:
pdfinfo main.pdf | grep Pages

# Check file size reasonable (not tiny = compilation failed partially):
# Typical: 100KB - 5MB depending on graphics
```

### Review Log

```bash
# Check for errors:
grep "Error" main.log

# Check for warnings:
grep "Warning" main.log

# Count overfull boxes:
grep "Overfull" main.log | wc -l

# Extract overfull box locations:
grep -A 1 "Overfull" main.log
```

## Cleanup

After successful compilation:

```bash
# Remove auxiliary files (optional):
rm -f main.aux main.log main.nav main.out main.snm main.toc main.bbl main.blg

# Keep only:
# - main.tex (source)
# - main.pdf (output)
# - figures/ (graphics)
```

## Compilation Script

Generate this script for user:

```bash
#!/bin/bash
# Beamer Presentation Compilation Script

echo "Compiling Beamer presentation..."

# First pass
echo "Pass 1/3: Initial compilation..."
xelatex -interaction=nonstopmode main.tex

# Bibliography (if needed)
if grep -q "\\bibliography" main.tex; then
    echo "Processing bibliography..."
    bibtex main
fi

# Second pass
echo "Pass 2/3: Incorporating references..."
xelatex -interaction=nonstopmode main.tex

# Third pass
echo "Pass 3/3: Final compilation..."
xelatex -interaction=nonstopmode main.tex

# Check for errors
if [ -f main.pdf ]; then
    echo "✓ Compilation successful!"
    echo "  Output: main.pdf"
    pages=$(pdfinfo main.pdf | grep "Pages" | awk '{print $2}')
    echo "  Pages: $pages"
    size=$(ls -lh main.pdf | awk '{print $5}')
    echo "  Size: $size"

    # Check for warnings
    warnings=$(grep -c "Warning" main.log)
    overfull=$(grep -c "Overfull" main.log)
    echo "  Warnings: $warnings"
    echo "  Overfull boxes: $overfull"

    if [ $overfull -gt 5 ]; then
        echo "  ⚠ Multiple overfull boxes detected. Review main.log"
    fi
else
    echo "✗ Compilation failed!"
    echo "  Check main.log for errors"
    exit 1
fi
```

## Usage in Skill

When this skill is invoked:

1. **Locate .tex file**
   - Ask user for path if not obvious
   - Default to current directory main.tex or presentation.tex

2. **Run pre-flight checks**
   - File exists
   - Graphics exist (warn if missing, don't fail)
   - No obvious syntax errors (quick scan)

3. **Execute compilation**
   - Run full xelatex sequence
   - Capture output and errors

4. **Report results**
   - Success: Show PDF info, page count, file size
   - Warnings: List overfull boxes, missing references
   - Errors: Explain issue, suggest fixes

5. **Deliver output**
   - Provide PDF file
   - Include compilation log if errors
   - Offer cleanup of auxiliary files

## Integration

Invokable as:

```
/beamer-compile [optional: path/to/presentation.tex]
```

Or:

```
Skill("beamer-compile", args="path/to/presentation.tex")
```

## Notes

- **Compilation time**: Typically 5-30 seconds depending on complexity
- **Resource usage**: Minimal, but large graphics can slow compilation
- **Incremental compilation**: Not supported for Beamer (always full rebuild)
- **Watch mode**: Not implemented (manual recompilation required)

---

**Goal**: Reliably compile Beamer presentations with proper error handling and user feedback.
