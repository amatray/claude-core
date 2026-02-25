# Beamer Presentation Pipeline

A comprehensive pipeline for creating publication-quality academic Beamer presentations with producer-critic agent architecture.

## Overview

This pipeline generates Beamer presentations that are:
- **Style-compliant**: Adheres to established academic presentation standards
- **Visually consistent**: Uniform colors, spacing, and formatting throughout
- **Technically sound**: Compiles cleanly with no warnings or errors
- **High quality**: Professional polish suitable for conferences, seminars, and job talks

## Directory Structure

```
beamer-pipeline/
├── README.md                  # This file
├── rules/                     # Style guide documentation
│   ├── beamer-visual-style.md        # Colors, commands, formatting
│   ├── beamer-content-patterns.md    # Slide structures and patterns
│   └── beamer-math-notation.md       # Equation formatting standards
├── agents/                    # Agent definitions
│   ├── producer/              # Content creation agents
│   │   ├── beamer-architect.md       # Creates structure
│   │   ├── beamer-writer.md          # Writes LaTeX
│   │   └── beamer-stylist.md         # Applies polish
│   └── critic/                # Quality control agents
│       ├── beamer-structure-critic.md   # Reviews organization
│       ├── beamer-style-critic.md       # Checks compliance
│       └── beamer-technical-critic.md   # Validates code
├── templates/                 # Reusable templates
│   ├── preamble.tex           # Standard preamble
│   └── frames/                # Frame templates by type
│       ├── title.tex
│       ├── motivation.tex
│       ├── question.tex
│       ├── this-paper.tex
│       ├── results-graph.tex
│       ├── results-table.tex
│       ├── specification.tex
│       ├── takeaway.tex
│       └── thankyou.tex
├── skills/                    # Workflow orchestration
│   ├── beamer-generate.md     # Full generation workflow
│   ├── beamer-compile.md      # Compilation workflow
│   └── beamer-polish.md       # Refinement workflow
└── scripts/                   # Utility scripts
    ├── extract_style.py       # Extract patterns from existing presentations
    ├── validate_beamer.py     # Check style compliance
    └── compile_beamer.sh      # Compile presentations
```

## Producer-Critic Architecture

### Producer Agents

**Beamer Architect** → Creates structure
- Converts bullet points to frame-by-frame outline
- Allocates content appropriately
- Plans progressive reveals and timing

**Beamer Writer** → Writes LaTeX code
- Generates complete LaTeX for each frame
- Uses proper style commands
- Formats equations, tables, and figures

**Beamer Stylist** → Polishes presentation
- Perfects spacing and alignment
- Optimizes overlays
- Creates hyperlink network

### Critic Agents

**Beamer Structure-Critic** → Reviews organization
- Checks logical flow
- Evaluates pacing and density
- Ensures balanced sections

**Beamer Style-Critic** → Checks compliance
- Verifies color command usage
- Validates formatting standards
- Ensures pattern adherence

**Beamer Technical-Critic** → Validates code
- Tests compilation
- Checks file references
- Validates cross-references

## Workflow

### Option 1: Full Generation (from scratch)

```
1. Provide: Research outline in bullet points
2. Architect: Creates frame-by-frame structure
3. Structure-Critic: Reviews organization → iterate if needed
4. Writer: Generates LaTeX code
5. Style-Critic: Checks compliance → iterate if needed
6. Stylist: Applies final polish
7. Technical-Critic: Validates code → iterate if needed
8. Output: Complete, polished presentation
```

**Use when**: Starting from scratch with research content

### Option 2: Polish Existing (refinement)

```
1. Provide: Existing .tex presentation
2. Style-Critic: Analyzes current state
3. Writer: Applies systematic fixes
4. Stylist: Enhances visual quality
5. Technical-Critic: Validates improvements
6. Output: Style-compliant version
```

**Use when**: Updating existing presentations to match standards

### Option 3: Compile Only

```
1. Provide: .tex file
2. Run: Proper compilation sequence (xelatex × 3)
3. Output: PDF + compilation report
```

**Use when**: Just need to generate PDF

## Usage

### With Claude Code

The pipeline is designed to integrate with Claude Code through skills:

```bash
# Generate new presentation
/beamer-generate

# Polish existing presentation
/beamer-polish path/to/presentation.tex

# Compile presentation
/beamer-compile path/to/presentation.tex
```

### Standalone Scripts

#### Extract Style Patterns

```bash
python scripts/extract_style.py path/to/existing_presentation.tex

# Output:
# - Console report of colors, commands, patterns
# - extracted_patterns.json
```

#### Validate Presentation

```bash
# Check compliance:
python scripts/validate_beamer.py presentation.tex

# Check and auto-fix:
python scripts/validate_beamer.py presentation.tex --fix
```

#### Compile Presentation

```bash
# Standard compilation:
./scripts/compile_beamer.sh presentation.tex

# With cleanup:
./scripts/compile_beamer.sh presentation.tex --clean

# Quiet mode:
./scripts/compile_beamer.sh presentation.tex --quiet
```

## Style Standards

### Color Usage

- **\blue{}**: Main findings, questions, mechanisms
- **\red{}**: Problems, negative findings, emphasis
- **\green{}**: Solutions, positive outcomes, policies
- **\orange{}**: Secondary emphasis
- **\lightgrey{}**: Citations, de-emphasized content
- **\grey{}**: Struck-through or ruled-out ideas

### Spacing Commands

- **\bitem**: `\bigskip\item` - Major points
- **\mitem**: `\medskip\item` - Sub-points
- **\vitem**: `\vfill\item` - Vertically balanced points

### Formatting Commands

- **\bf{}**: Bold text
- **\it{}**: Italic text
- **\under{}**: Underlined text

### Equations

- Always use `\begin{equation*}...\end{equation*}` (unnumbered)
- Color-code components during progressive reveals
- Brace multi-character subscripts: `_{i,t}` not `_i,t`

### Tables

- Use `booktabs`: `\toprule`, `\midrule`, `\bottomrule`
- Column reveals: `<{\onslide<2->}c<{\onslide<3->}c`
- Scale with `\scalebox{.8}{...}` if too wide
- Add `\addlinespace` for breathing room

## Reference Documents

- **Visual Style**: `rules/beamer-visual-style.md`
- **Content Patterns**: `rules/beamer-content-patterns.md`
- **Math Notation**: `rules/beamer-math-notation.md`

## Templates

All standard frame types have templates in `templates/frames/`:

- Title slide
- Motivation
- Question
- Contributions ("This paper")
- Results (graphs and tables)
- Specification/empirical strategy
- Takeaway/conclusion
- Thank you

Use these as starting points or reference for correct structure.

## Integration with claude-core

To use with your existing claude-core setup:

```bash
# From claude-core repository:
ln -s path/to/beamer-pipeline beamer
```

Then in your `.claude/` project directories, you can reference these agents and skills.

## Extending the Pipeline

### Adding New Frame Templates

1. Create template in `templates/frames/new-frame-type.tex`
2. Document pattern in `rules/beamer-content-patterns.md`
3. Update Writer agent to recognize pattern

### Adding New Style Rules

1. Document rule in appropriate rules file
2. Add check to Style-Critic agent
3. Add fix pattern to Stylist agent

### Adding New Validations

1. Add check to `scripts/validate_beamer.py`
2. Document in Technical-Critic agent

## Troubleshooting

### Compilation Errors

**Missing files:**
```
! LaTeX Error: File `figure1.pdf' not found.
```
→ Check file paths, ensure graphics exist

**Missing packages:**
```
! LaTeX Error: File `booktabs.sty' not found.
```
→ Update LaTeX distribution: `tlmgr install booktabs`

**Font errors:**
```
! Package fontspec Error: The font "Lato" cannot be found.
```
→ Install Lato font or use `\usepackage{helvet}` instead

### Style Violations

Run validation script to identify all issues:

```bash
python scripts/validate_beamer.py presentation.tex
```

Review output and apply fixes systematically.

### Overfull Boxes

If compilation log shows overfull boxes:

- **Tables**: Reduce `\scalebox` value or abbreviate headers
- **Equations**: Split with `\begin{split}` or use `\resizebox`
- **Text**: Rephrase or use `\sloppy` environment

## Best Practices

1. **Start with structure**: Get organization right before writing code
2. **Use critic feedback**: Iterate based on reviews
3. **Compile frequently**: Catch errors early
4. **Test progressive reveals**: Ensure overlays work as intended
5. **Check hyperlinks**: Verify all cross-references functional
6. **Review final PDF**: Visual check before delivery

## License

This pipeline is designed for academic use. Adapt and extend as needed for your presentations.

## Credits

Developed based on analysis of existing presentations by Adrien Matray, incorporating best practices for academic Beamer presentations.

---

**Questions or Issues?**

Refer to individual agent files in `agents/` for detailed instructions, or consult the rules documentation in `rules/`.
