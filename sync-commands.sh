#!/bin/bash
# Sync ~/.claude/commands/ to ~/claude-core/commands/ and push to GitHub
# Called automatically by Claude Code hook after skill edits

REPO_DIR="$HOME/claude-core"
SOURCE_DIR="$HOME/.claude/commands"

cd "$REPO_DIR" || exit 1

# Sync commands (exclude confidential files)
rsync -a --delete --exclude='citation-production.md' "$SOURCE_DIR/" "$REPO_DIR/commands/"

# Also sync CLAUDE.md
cp "$HOME/.claude/CLAUDE.md" "$REPO_DIR/CLAUDE.md" 2>/dev/null

# Check if there are changes
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    exit 0
fi

# Commit and push
git add -A
git commit -m "Auto-sync commands and CLAUDE.md"
git push origin main 2>/dev/null

echo "claude-core synced to GitHub"
