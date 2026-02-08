#!/bin/bash
# Usage: bash ~/claude-workflows/claude-core/link-to-project.sh ~/claude-workflows/paper-review
PROJECT="$1"
CORE="$(cd "$(dirname "$0")" && pwd)"

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
