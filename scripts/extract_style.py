#!/usr/bin/env python3
"""
Extract Style Patterns from Existing Beamer Presentations

This script analyzes existing .tex files to extract:
- Color definitions and usage patterns
- Custom commands
- Frame structure patterns
- Common code patterns

Usage:
    python extract_style.py /path/to/presentation.tex
    python extract_style.py /path/to/presentations/*.tex

Output:
    - Style report (console)
    - extracted_patterns.json (structured data)
"""

import re
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict


class BeamerStyleExtractor:
    def __init__(self):
        self.colors = {}
        self.commands = {}
        self.frame_patterns = []
        self.color_usage = Counter()
        self.command_usage = Counter()

    def extract_from_file(self, filepath):
        """Extract style patterns from a single .tex file"""
        print(f"\nAnalyzing: {filepath}")

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extract color definitions
        self._extract_colors(content)

        # Extract custom commands
        self._extract_commands(content)

        # Analyze color usage
        self._analyze_color_usage(content)

        # Extract frame patterns
        self._extract_frame_patterns(content)

    def _extract_colors(self, content):
        """Extract color definitions"""
        # RGB format: \definecolor{name}{RGB}{R,G,B}
        rgb_pattern = r'\\definecolor{(\w+)}{RGB}{(\d+),\s*(\d+),\s*(\d+)}'
        for match in re.finditer(rgb_pattern, content):
            name, r, g, b = match.groups()
            self.colors[name] = {
                'type': 'RGB',
                'values': (int(r), int(g), int(b))
            }

        # rgb format: \definecolor{name}{rgb}{r,g,b}
        rgb_float_pattern = r'\\definecolor{(\w+)}{rgb}{([\d.]+),\s*([\d.]+),\s*([\d.]+)}'
        for match in re.finditer(rgb_float_pattern, content):
            name, r, g, b = match.groups()
            self.colors[name] = {
                'type': 'rgb',
                'values': (float(r), float(g), float(b))
            }

    def _extract_commands(self, content):
        """Extract custom command definitions"""
        # \def\name{definition}
        def_pattern = r'\\def\\(\w+){([^}]+)}'
        for match in re.finditer(def_pattern, content):
            name, definition = match.groups()
            self.commands[name] = {
                'type': 'def',
                'definition': definition
            }

        # \newcommand{\name}[args]{definition}
        newcommand_pattern = r'\\newcommand{?\\(\w+)}?(?:\[(\d+)\])?{([^}]+)}'
        for match in re.finditer(newcommand_pattern, content):
            name, args, definition = match.groups()
            self.commands[name] = {
                'type': 'newcommand',
                'args': int(args) if args else 0,
                'definition': definition
            }

    def _analyze_color_usage(self, content):
        """Analyze how colors are used in content"""
        # Find \color{name}{text} usage
        for color_name in self.colors.keys():
            # Pattern: \colorname{...}
            pattern = rf'\\{color_name}{{[^}}]+}}'
            count = len(re.findall(pattern, content))
            if count > 0:
                self.color_usage[color_name] = count

    def _extract_frame_patterns(self, content):
        """Extract common frame structure patterns"""
        # Extract all frames
        frame_pattern = r'\\begin{frame}(?:\[([^\]]*)\])?(?:{([^}]*)})?.*?\\end{frame}'
        frames = re.findall(frame_pattern, content, re.DOTALL)

        # Analyze frame options and titles
        for options, title in frames[:10]:  # Sample first 10
            self.frame_patterns.append({
                'options': options if options else None,
                'title': title if title else None
            })

    def generate_report(self):
        """Generate human-readable report"""
        print("\n" + "="*60)
        print("STYLE EXTRACTION REPORT")
        print("="*60)

        # Colors
        print("\n--- Color Definitions ---")
        for name, info in sorted(self.colors.items()):
            if info['type'] == 'RGB':
                r, g, b = info['values']
                print(f"  \\definecolor{{{name}}}{{RGB}}{{{r},{g},{b}}}")
            else:
                r, g, b = info['values']
                print(f"  \\definecolor{{{name}}}{{rgb}}{{{r},{g},{b}}}")

        # Color usage
        if self.color_usage:
            print("\n--- Color Usage Frequency ---")
            for color, count in self.color_usage.most_common():
                print(f"  {color}: {count} times")

        # Commands
        print("\n--- Custom Commands ---")
        for name, info in sorted(self.commands.items()):
            if info['type'] == 'def':
                print(f"  \\def\\{name}{{{info['definition']}}}")
            else:
                args_str = f"[{info['args']}]" if info['args'] > 0 else ""
                print(f"  \\newcommand{{\\{name}}}{args_str}{{{info['definition']}}}")

        # Common command usage
        common_commands = [name for name in self.commands.keys() if name in ['bitem', 'mitem', 'vitem', 'blue', 'red', 'green']]
        if common_commands:
            print("\n--- Style Shortcuts Detected ---")
            for cmd in common_commands:
                print(f"  ✓ \\{cmd} defined")

        # Frame patterns
        print("\n--- Frame Patterns (first 10) ---")
        for i, pattern in enumerate(self.frame_patterns[:10], 1):
            print(f"\nFrame {i}:")
            if pattern['options']:
                print(f"  Options: {pattern['options']}")
            if pattern['title']:
                print(f"  Title: {pattern['title']}")

    def export_json(self, output_path):
        """Export extracted patterns to JSON"""
        data = {
            'colors': {
                name: {
                    'type': info['type'],
                    'values': list(info['values']) if isinstance(info['values'], tuple) else info['values']
                }
                for name, info in self.colors.items()
            },
            'commands': self.commands,
            'color_usage': dict(self.color_usage),
            'frame_patterns': self.frame_patterns
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n✓ Exported patterns to: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_style.py <path_to_tex_file(s)>")
        print("Example: python extract_style.py presentation.tex")
        print("Example: python extract_style.py presentations/*.tex")
        sys.exit(1)

    extractor = BeamerStyleExtractor()

    # Process all provided files
    for arg in sys.argv[1:]:
        path = Path(arg)

        if path.is_file() and path.suffix == '.tex':
            extractor.extract_from_file(path)
        elif '*' in str(path):
            # Handle glob pattern
            parent = path.parent
            pattern = path.name
            for tex_file in parent.glob(pattern):
                if tex_file.is_file():
                    extractor.extract_from_file(tex_file)
        else:
            print(f"Warning: {arg} is not a .tex file or valid pattern")

    # Generate reports
    extractor.generate_report()
    extractor.export_json('extracted_patterns.json')


if __name__ == "__main__":
    main()
