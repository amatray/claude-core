# Beamer Polish Skill

This skill refines existing Beamer presentations to ensure style compliance and visual perfection.

## When to Use

Use this skill when:
- User has existing .tex presentation that needs style updates
- Presentation was created without using this pipeline
- User wants to apply Matray style to existing slides
- Presentation needs visual consistency improvements

## File Structure Considerations

**If presentation is a single file:**
1. Offer to restructure into modular format (main.tex + sections/)
2. If user declines, work with single file

**If presentation is already modular:**
1. Work with existing section files
2. Ensure frame separators are present between frames
3. Maintain file organization

**Recommended restructuring:**
```
Old: presentation.tex (single 1000+ line file)
New: main.tex + sections/01_intro.tex, sections/02_motivation.tex, etc.
```

## Workflow

### Phase 1: Analysis

**Analyze existing presentation:**

1. **Read .tex file(s)** (main file and/or section files)
2. **Identify current style patterns**:
   - Color usage
   - Command syntax (\textcolor vs shortcuts)
   - Frame structures
   - Spacing patterns
   - Table formatting
   - Equation formatting

3. **Catalog violations** against style guide:
   - Count `\textcolor` instances
   - Check for `\bigskip\item` vs `\bitem`
   - Verify equation environments
   - Check table formatting
   - Review color conventions

4. **Assess scope**:
   - Total frames to update
   - Severity of violations (critical/important/minor)
   - Estimated time for fixes

**Output**: Analysis report for user approval

---

### Phase 2: Style Compliance

**Agent**: Beamer Style-Critic

**Review entire presentation** systematically:
- All color command usage
- All spacing commands
- All equation formatting
- All table structures
- All citations and hyperlinks

**Generate complete violation list** with:
- Location (frame, line)
- Current code
- Corrected code
- Severity rating

---

### Phase 3: Automated Fixes

**Apply systematic corrections:**

#### 1. Color Command Replacement

```latex
# Find: \textcolor{blue}{([^}]+)}
# Replace: \blue{$1}

# Example:
\textcolor{blue}{Finding} → \blue{Finding}
\textcolor{red}{Problem} → \red{Problem}
```

#### 2. Spacing Command Replacement

```latex
# Find: \\bigskip\\item
# Replace: \\bitem

# Find: \\medskip\\item
# Replace: \\mitem
```

#### 3. Text Formatting

```latex
# Find: \\textbf{([^}]+)}
# Replace: \\bf{$1}

# Find: \\textit{([^}]+)}
# Replace: \\it{$1}
```

#### 4. Equation Environments

```latex
# Find: \\begin{equation}([^*])
# Replace: \\begin{equation*}$1

# Find: \$\$([^\$]+)\$\$
# Replace: \\begin{equation*}$1\\end{equation*}
```

#### 5. Table Lines

```latex
# Find: \\hline
# Replace (context-dependent):
#   - After \begin{tabular}: \toprule
#   - Between header and data: \midrule
#   - Before \end{tabular}: \bottomrule
```

---

### Phase 4: Manual Review

**Present changes to user:**

```
Found and corrected [X] style violations:

Critical fixes ([Y]):
- Replaced [N] instances of \textcolor with shortcuts
- Fixed [M] numbered equation environments

Important fixes ([Z]):
- Updated [P] spacing commands
- Corrected [Q] table formatting issues

Minor improvements ([W]):
- Standardized [R] citation formats
- Improved [S] hyperlink formatting

Would you like me to:
1. Apply all fixes
2. Show detailed diff for review
3. Apply only critical/important fixes
```

---

### Phase 5: Visual Enhancement

**Agent**: Beamer Stylist

**Polish visual aspects:**

1. **Spacing optimization**:
   - Add \vfill for balanced slides
   - Adjust \vspace for consistency
   - Balance frame density

2. **Alignment perfection**:
   - Center figures properly
   - Align equation components
   - Balance column widths

3. **Hyperlink network**:
   - Add missing back links
   - Standardize link formatting
   - Create cross-references

4. **Overlay optimization**:
   - Clean up overlay specifications
   - Ensure sequential numbering
   - Synchronize reveals

---

### Phase 6: Technical Validation

**Agent**: Beamer Technical-Critic

**Verify technical correctness:**
- Compilation viability
- All file references valid
- All hyperlinks functional
- No LaTeX warnings

**Output**: Technical validation report

---

## User Interaction

### At Start

```
I'll analyze your presentation and apply Matray style standards.

Please provide:
1. Path to your .tex file(s)
2. Any specific areas to focus on or avoid
3. Desired level of changes:
   - Conservative (only critical style violations)
   - Standard (critical + important)
   - Comprehensive (all improvements including minor)
```

### After Analysis

```
Analysis complete for [presentation_name].tex:

Current status:
- Total frames: [X]
- Style violations found: [Y]
  - Critical: [C] (prevent compilation or severe style breaks)
  - Important: [I] (notable style inconsistencies)
  - Minor: [M] (small improvements)

Major issues:
- [List top 3-5 most significant problems]

Estimated time for fixes: [N] minutes

Proceed with corrections?
```

### After Fixes

```
Applied [X] corrections:

Summary of changes:
- Color commands: [N] fixed
- Spacing: [M] improved
- Equations: [P] standardized
- Tables: [Q] reformatted

Would you like me to:
1. Compile to verify changes
2. Show before/after comparison
3. Make additional adjustments
```

## Special Cases

### Preserving Custom Content

**Don't change:**
- Custom commands defined by user (unless violating style)
- Specific color choices for data visualization
- User's mathematical notation (if consistent)
- Frame-specific formatting for special slides

**Do change:**
- Standard style violations
- Inconsistent patterns
- Technical errors

### Handling Conflicts

If user's style conflicts with standard:

```
Found conflict:
- Standard style: \blue{} for main findings
- Your usage: \textcolor{purple}{} for main findings

Options:
1. Apply standard (recommended for consistency)
2. Keep your style (preserve existing)
3. Define new rule for your presentation
```

### Partial Updates

Allow user to specify scope:

```
Update only:
- [ ] Title and introduction slides
- [ ] Results slides
- [ ] All slides
- [ ] Specific frames: [list]
```

## Before/After Comparison

Generate side-by-side comparison:

```latex
% BEFORE:
\begin{frame}{Results}
\item \textcolor{blue}{Finding 1}
\bigskip\item \textcolor{red}{Finding 2}
\end{frame}

% AFTER:
\begin{frame}{Results}

\bitem \blue{Finding 1}
\mitem \red{Finding 2}
\end{frame}
```

## Backup Creation

**Always create backup before modifications:**

```bash
cp presentation.tex presentation_original.tex
cp presentation.tex presentation_backup_[timestamp].tex
```

**Provide rollback option:**

```
Changes saved to: presentation.tex
Original backed up to: presentation_original.tex

To revert changes:
  mv presentation_original.tex presentation.tex
```

## Output Deliverables

1. **Updated .tex file(s)** with style fixes applied
2. **Change log** documenting all modifications
3. **Original backup** for safety
4. **Compilation test results** (if requested)
5. **Remaining issues list** (if any unfixed)

## Quality Assurance

Before delivering:

- [ ] All critical violations fixed
- [ ] Important violations addressed (or user-approved to skip)
- [ ] Presentation compiles successfully
- [ ] No new errors introduced
- [ ] Original content preserved
- [ ] Backup created

## Integration

Invokable as:

```
/beamer-polish [path/to/presentation.tex]
```

Or:

```
Skill("beamer-polish", args="path/to/presentation.tex --level=comprehensive")
```

**Arguments:**
- `--level=conservative|standard|comprehensive`: Scope of changes
- `--dry-run`: Show changes without applying
- `--no-backup`: Skip backup creation (not recommended)
- `--frames=1,5,10-15`: Update only specified frames

## Common Polish Tasks

### 1. Color Standardization

Replace all color variants with standard palette:
- `\textcolor{blue}` → `\blue{}`
- `\color{red}` → in text use `\red{}`
- RGB values → named colors

### 2. Spacing Consistency

Add systematic spacing:
- `\bitem` for major points
- `\mitem` for sub-points
- `\vfill` for balanced frames

### 3. Table Modernization

Update to booktabs:
- `\hline\hline` → `\toprule`
- `\hline` → `\midrule`
- `\cline` → `\cmidrule`

### 4. Citation Formatting

Standardize citations:
- `(Author, 2020)` → `{\scriptsize \grey{(Author 2020)}}`
- Inline refs → `\refgrey{Author 2020}`

### 5. Hyperlink Enhancement

Add systematic linking:
- Main results → appendix tables
- Appendix → back to main slides
- Related content cross-refs

## Notes

- **Preservation priority**: Don't break working presentations
- **User approval**: Always show major changes before applying
- **Reversibility**: Maintain backups, allow rollback
- **Compilation testing**: Verify fixes don't introduce errors
- **Incremental approach**: Fix critical issues first, then improve

---

**Goal**: Transform existing presentations to match style standards while preserving content and functionality.
