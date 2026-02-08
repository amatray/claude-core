# Claude Workflows - Core Configuration

This repository contains shared agents, rules, and skills used across multiple Claude Code projects.

## Structure

```
claude-core/
├── agents/          # Shared agent definitions
│   └── proofreader.md
├── rules/           # Shared rules and conventions
│   ├── quality-gates.md
│   ├── review-conventions.md
│   ├── latex-conventions.md
│   └── pdf-processing.md
├── scripts/         # Supporting scripts
│   └── extract_pdf.py
├── skills/          # Shared skills
│   └── compile-latex.md
└── link-to-project.sh  # Automation script
```

## Usage

### Link to a new project

```bash
bash ~/claude-workflows/claude-core/link-to-project.sh ~/path/to/your/project
```

This will create symlinks from the project's `.claude/` folder to all files in `claude-core`.

### Edit shared files

Edit files in `claude-core/` — all projects using symlinks will see the updates immediately.

```bash
vim ~/claude-workflows/claude-core/agents/proofreader.md
```

## Projects Using This Core

- `~/claude-workflows/paper-review/`
- `~/claude-workflows/empirical-research/`

## Adding New Shared Content

1. Create the file in the appropriate `claude-core/` subdirectory
2. Run the linking script for each project that should use it
3. Commit and push changes to keep everything version-controlled
