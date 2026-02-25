#!/bin/bash
# Usage: bash ~/claude-workflows/claude-core/link-to-project.sh ~/claude-workflows/paper-review
PROJECT="$1"
CORE="$(cd "$(dirname "$0")" && pwd)"

# Link general shared files from root level
for dir in agents rules skills; do
    mkdir -p "$PROJECT/.claude/$dir"
    for file in "$CORE/$dir"/*.md; do
        [ -f "$file" ] || continue
        target="$PROJECT/.claude/$dir/$(basename "$file")"
        if [ -f "$target" ] && [ ! -L "$target" ]; then
            echo "SKIP (local file): $target"
        else
            ln -sf "$file" "$target"
            echo "LINKED: $target"
        fi
    done
done

# Link Beamer pipeline files (flattened into .claude/ structure)
# This links files from beamer/agents/{producer,critic,orchestrator}/ to .claude/agents/
for subdir in producer critic orchestrator; do
    for file in "$CORE/beamer/agents/$subdir"/*.md; do
        [ -f "$file" ] || continue
        target="$PROJECT/.claude/agents/$(basename "$file")"
        if [ -f "$target" ] && [ ! -L "$target" ]; then
            echo "SKIP (local file): $target"
        else
            ln -sf "$file" "$target"
            echo "LINKED: $target"
        fi
    done
done

# Link beamer rules
for file in "$CORE/beamer/rules"/*.md; do
    [ -f "$file" ] || continue
    target="$PROJECT/.claude/rules/$(basename "$file")"
    if [ -f "$target" ] && [ ! -L "$target" ]; then
        echo "SKIP (local file): $target"
    else
        ln -sf "$file" "$target"
        echo "LINKED: $target"
    fi
done

# Link beamer skills
for file in "$CORE/beamer/skills"/*.md; do
    [ -f "$file" ] || continue
    target="$PROJECT/.claude/skills/$(basename "$file")"
    if [ -f "$target" ] && [ ! -L "$target" ]; then
        echo "SKIP (local file): $target"
    else
        ln -sf "$file" "$target"
        echo "LINKED: $target"
    fi
done
