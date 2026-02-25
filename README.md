# Claude Workflows - Core Configuration

Shared agents, rules, and skills used across multiple Claude Code projects.

## Overview

This repository contains:
- **General shared configuration**: Rules and agents for LaTeX, PDF processing, code review, etc.
- **Beamer pipeline**: Complete system for generating academic presentations (see `beamer/`)

## Directory Structure

```
claude-core/
├── README.md                  # This file
├── link-to-project.sh         # Script to link content to projects
├── agents/                    # Shared general agents
│   └── proofreader.md
├── rules/                     # Shared general rules
│   ├── quality-gates.md
│   ├── review-conventions.md
│   ├── latex-conventions.md
│   ├── markdown-to-pdf.md
│   ├── pdf-processing.md
│   ├── replication-guidelines.md
│   ├── stata-to-r-conversion.md
│   └── wait-for-approval.md
├── skills/                    # Shared general skills
│   ├── audit-paper.md
│   └── compile-latex.md
├── scripts/                   # Supporting scripts
│   └── extract_pdf.py
└── beamer/                    # Beamer presentation pipeline
    ├── README.md
    ├── agents/
    │   ├── producer/
    │   ├── critic/
    │   └── orchestrator/
    ├── rules/
    ├── templates/
    ├── skills/
    └── scripts/
```

## General Shared Content

### Agents
- **proofreader.md**: Agent for proofreading academic papers

### Rules
- **latex-conventions.md**: General LaTeX formatting standards
- **review-conventions.md**: Code review and paper review guidelines
- **quality-gates.md**: Quality control checkpoints
- **pdf-processing.md**: PDF extraction and processing guidelines
- **markdown-to-pdf.md**: Markdown to PDF conversion standards
- **replication-guidelines.md**: Research replication workflow
- **stata-to-r-conversion.md**: Converting Stata code to R
- **wait-for-approval.md**: User approval workflow

### Skills
- **audit-paper.md**: Academic paper auditing workflow
- **compile-latex.md**: LaTeX compilation workflow

### Scripts
- **extract_pdf.py**: Python script for PDF text extraction

## Beamer Pipeline

See `beamer/README.md` for complete documentation on the Beamer presentation pipeline.

**Quick overview:**
- Producer-critic architecture for generating academic presentations
- Full generation, polish existing, or compile-only workflows
- Complete style enforcement and quality control
- Skills: `/beamer-generate`, `/beamer-polish`, `/beamer-compile`

## Usage

### Link to a New Project

To use this shared configuration in a project:

```bash
bash ~/claude-workflows/claude-core/link-to-project.sh ~/path/to/your/project
```

This creates symlinks from the project's `.claude/` folder to all files in `claude-core`, flattening the structure:

**Result in your project:**
```
your-project/
└── .claude/
    ├── agents/
    │   ├── proofreader.md → ~/claude-workflows/claude-core/agents/proofreader.md
    │   ├── beamer-architect.md → ~/claude-workflows/claude-core/beamer/agents/producer/beamer-architect.md
    │   ├── beamer-writer.md → ~/claude-workflows/claude-core/beamer/agents/producer/beamer-writer.md
    │   └── ...
    ├── rules/
    │   ├── latex-conventions.md → ~/claude-workflows/claude-core/rules/latex-conventions.md
    │   ├── beamer-visual-style.md → ~/claude-workflows/claude-core/beamer/rules/beamer-visual-style.md
    │   └── ...
    └── skills/
        ├── audit-paper.md → ~/claude-workflows/claude-core/skills/audit-paper.md
        ├── beamer-generate.md → ~/claude-workflows/claude-core/beamer/skills/beamer-generate.md
        └── ...
```

### Edit Shared Files

Edit files in `claude-core/` and all linked projects see the updates immediately:

```bash
vim ~/claude-workflows/claude-core/rules/latex-conventions.md
```

### Projects Using This Core

- `~/claude-workflows/paper-review/`
- `~/claude-workflows/empirical-research/`

### Adding New Shared Content

1. Create the file in the appropriate `claude-core/` subdirectory
2. Run the linking script for each project that should use it
3. Commit and push changes to keep everything version-controlled

## Available Skills

### General Skills
- `/audit-paper` - Audit academic papers for typos, grammar, syntax
- `/compile-latex` - Compile LaTeX documents

### Beamer Skills
- `/beamer-generate` - Generate new presentation from outline
- `/beamer-polish` - Refine existing presentation
- `/beamer-compile` - Compile presentation to PDF

## Extending

### Add a New General Agent

1. Create `agents/new-agent.md`
2. Document its purpose and usage
3. Run linking script to update projects

### Add a New Beamer Component

1. Add to appropriate `beamer/` subdirectory
2. Update `beamer/BEAMER_PIPELINE_README.md` if needed
3. Run linking script to update projects

## License

For academic and research use.

---

**Questions or Issues?**

Refer to individual agent files for detailed instructions, or consult the rules documentation.
