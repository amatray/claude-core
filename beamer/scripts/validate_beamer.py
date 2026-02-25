#!/usr/bin/env python3
"""
Validate Beamer Presentation Style Compliance

This script checks a .tex file for compliance with Matray style standards:
- Color command usage (\blue{} vs \textcolor{blue}{})
- Spacing commands (\bitem vs \bigskip\item)
- Equation environments (equation* vs equation)
- Table formatting (booktabs compliance)
- And more...

Usage:
    python validate_beamer.py presentation.tex
    python validate_beamer.py presentation.tex --fix

Output:
    - Violation report (console)
    - Optional: Fixed version (if --fix flag used)
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict


class StyleViolation:
    def __init__(self, line_num, violation_type, message, current_code, fixed_code=None, severity="Important"):
        self.line_num = line_num
        self.violation_type = violation_type
        self.message = message
        self.current_code = current_code
        self.fixed_code = fixed_code
        self.severity = severity

    def __str__(self):
        result = f"\n[{self.severity}] Line {self.line_num}: {self.violation_type}"
        result += f"\n  Issue: {self.message}"
        result += f"\n  Current: {self.current_code}"
        if self.fixed_code:
            result += f"\n  Fix: {self.fixed_code}"
        return result


class BeamerValidator:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.violations = []
        self.lines = []
        self.load_file()

    def load_file(self):
        """Load .tex file into memory"""
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.lines = f.readlines()

    def validate_all(self):
        """Run all validation checks"""
        print(f"Validating: {self.filepath}")
        print("="*60)

        self.check_color_commands()
        self.check_spacing_commands()
        self.check_text_formatting()
        self.check_equations()
        self.check_table_lines()
        self.check_subscripts()

    def check_color_commands(self):
        """Check for \textcolor usage (should use shortcuts)"""
        pattern = r'\\textcolor\{(\w+)\}\{([^}]+)\}'

        for i, line in enumerate(self.lines, 1):
            matches = re.finditer(pattern, line)
            for match in matches:
                color, text = match.groups()
                self.violations.append(StyleViolation(
                    line_num=i,
                    violation_type="Color Command",
                    message=f"Use \\{color}{{}} shortcut instead of \\textcolor",
                    current_code=match.group(0),
                    fixed_code=f"\\{color}{{{text}}}",
                    severity="Critical"
                ))

    def check_spacing_commands(self):
        """Check for \bigskip\item, \medskip\item usage"""
        patterns = {
            r'\\bigskip\s*\\item': ('\\bitem', 'Important'),
            r'\\medskip\s*\\item': ('\\mitem', 'Important'),
            r'\\vfill\s*\\item': ('\\vitem', 'Minor'),
        }

        for i, line in enumerate(self.lines, 1):
            for pattern, (replacement, severity) in patterns.items():
                if re.search(pattern, line):
                    self.violations.append(StyleViolation(
                        line_num=i,
                        violation_type="Spacing Command",
                        message=f"Use {replacement} shortcut",
                        current_code=line.strip(),
                        fixed_code=re.sub(pattern, replacement, line.strip()),
                        severity=severity
                    ))

    def check_text_formatting(self):
        """Check for \textbf, \textit usage"""
        patterns = {
            r'\\textbf\{([^}]+)\}': ('\\bf{}', 'Important'),
            r'\\textit\{([^}]+)\}': ('\\it{}', 'Important'),
        }

        for i, line in enumerate(self.lines, 1):
            for pattern, (replacement, severity) in patterns.items():
                matches = re.finditer(pattern, line)
                for match in matches:
                    text = match.group(1)
                    self.violations.append(StyleViolation(
                        line_num=i,
                        violation_type="Text Formatting",
                        message=f"Use {replacement} shortcut",
                        current_code=match.group(0),
                        fixed_code=f"\\{replacement[1:-2]}{{{text}}}",
                        severity=severity
                    ))

    def check_equations(self):
        """Check for numbered equations, deprecated $$"""
        for i, line in enumerate(self.lines, 1):
            # Check for numbered equations
            if re.search(r'\\begin\{equation\}[^*]', line):
                self.violations.append(StyleViolation(
                    line_num=i,
                    violation_type="Equation Environment",
                    message="Slides should use equation* (unnumbered)",
                    current_code=line.strip(),
                    fixed_code=line.strip().replace(r'\begin{equation}', r'\begin{equation*}'),
                    severity="Critical"
                ))

            # Check for deprecated $$
            if '$$' in line:
                self.violations.append(StyleViolation(
                    line_num=i,
                    violation_type="Equation Syntax",
                    message="Use \\begin{equation*}...\\end{equation*} instead of $$",
                    current_code=line.strip(),
                    fixed_code="Use equation* environment",
                    severity="Important"
                ))

    def check_table_lines(self):
        """Check for \hline usage (should use booktabs)"""
        for i, line in enumerate(self.lines, 1):
            if '\\hline' in line and '\\hline\\hline' not in line:
                self.violations.append(StyleViolation(
                    line_num=i,
                    violation_type="Table Formatting",
                    message="Use \\toprule, \\midrule, or \\bottomrule instead of \\hline",
                    current_code=line.strip(),
                    fixed_code="Use booktabs commands",
                    severity="Important"
                ))

            if '\\hline\\hline' in line:
                self.violations.append(StyleViolation(
                    line_num=i,
                    violation_type="Table Formatting",
                    message="Use \\toprule instead of \\hline\\hline",
                    current_code=line.strip(),
                    fixed_code=line.strip().replace('\\hline\\hline', '\\toprule'),
                    severity="Important"
                ))

    def check_subscripts(self):
        """Check for unbraced multi-character subscripts"""
        # Pattern: _letter,digit (should be _{letter,digit})
        pattern = r'_([a-zA-Z]{2,}|[a-zA-Z],\d+)'

        for i, line in enumerate(self.lines, 1):
            # Skip if in math environment might be complex
            matches = re.finditer(pattern, line)
            for match in matches:
                subscript = match.group(1)
                self.violations.append(StyleViolation(
                    line_num=i,
                    violation_type="Math Notation",
                    message="Multi-character subscripts must be braced",
                    current_code=match.group(0),
                    fixed_code=f"_{{{subscript}}}",
                    severity="Important"
                ))

    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)

        if not self.violations:
            print("\n✓ No violations found! Presentation is style-compliant.")
            return

        # Group by severity
        by_severity = defaultdict(list)
        for v in self.violations:
            by_severity[v.severity].append(v)

        # Summary
        print(f"\nTotal violations: {len(self.violations)}")
        print(f"  Critical: {len(by_severity['Critical'])}")
        print(f"  Important: {len(by_severity['Important'])}")
        print(f"  Minor: {len(by_severity['Minor'])}")

        # Detailed violations
        for severity in ['Critical', 'Important', 'Minor']:
            if severity in by_severity:
                print(f"\n--- {severity} Violations ---")
                for violation in by_severity[severity]:
                    print(violation)

    def apply_fixes(self, output_path=None):
        """Apply automatic fixes and save to file"""
        if not output_path:
            output_path = self.filepath.parent / f"{self.filepath.stem}_fixed.tex"

        fixed_lines = self.lines.copy()

        # Sort violations by line number (reverse) to maintain line numbers during fixes
        sorted_violations = sorted(self.violations, key=lambda v: v.line_num, reverse=True)

        fixes_applied = 0
        for violation in sorted_violations:
            if violation.fixed_code and violation.severity in ['Critical', 'Important']:
                line_idx = violation.line_num - 1
                # Simple replacement (this is a basic implementation)
                fixed_lines[line_idx] = fixed_lines[line_idx].replace(
                    violation.current_code.strip(),
                    violation.fixed_code.strip()
                )
                fixes_applied += 1

        # Write fixed file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)

        print(f"\n✓ Applied {fixes_applied} fixes")
        print(f"✓ Fixed file saved to: {output_path}")

        return output_path


def main():
    parser = argparse.ArgumentParser(description='Validate Beamer presentation style compliance')
    parser.add_argument('filepath', help='Path to .tex file')
    parser.add_argument('--fix', action='store_true', help='Apply automatic fixes')
    parser.add_argument('--output', help='Output path for fixed file')

    args = parser.parse_args()

    # Validate file exists
    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    if not filepath.suffix == '.tex':
        print(f"Error: Not a .tex file: {filepath}")
        sys.exit(1)

    # Run validation
    validator = BeamerValidator(filepath)
    validator.validate_all()
    validator.generate_report()

    # Apply fixes if requested
    if args.fix:
        print("\n" + "="*60)
        print("APPLYING FIXES")
        print("="*60)
        validator.apply_fixes(args.output)


if __name__ == "__main__":
    main()
