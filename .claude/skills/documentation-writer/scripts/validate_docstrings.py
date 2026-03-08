#!/usr/bin/env python3
"""
Validate docstrings for convention compliance (PEP 257, Google, NumPy styles).

Usage:
    python validate_docstrings.py <file_path> [--style google|numpy|pep257] [--json]
"""

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict


def check_pep257_compliance(docstring: str | None, name: str) -> Dict[str, Any]:
    """Check PEP 257 docstring compliance."""
    if not docstring:
        return {
            "compliant": False,
            "issues": ["Missing docstring"],
            "recommendations": ["Add a docstring following PEP 257"],
        }

    issues = []
    recommendations = []

    lines = docstring.split("\n")

    # Check first line
    if not lines[0]:
        issues.append("First line is empty")
        recommendations.append("Start with a summary line")

    if len(lines[0]) > 79:
        issues.append(f"First line too long ({len(lines[0])} chars, max 79)")
        recommendations.append("Keep summary line under 79 characters")

    # One-liner docstring should end with period
    if len(lines) == 1 and not lines[0].endswith((".", "!", "?")):
        issues.append("One-liner docstring doesn't end with period")
        recommendations.append("End one-liner docstrings with a period")

    # Multi-line should have blank line after summary
    if len(lines) > 2 and lines[1].strip() != "":
        issues.append("Multi-line docstring missing blank line after summary")
        recommendations.append("Add blank line between summary and description")

    return {
        "compliant": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
    }


def check_google_style_compliance(docstring: str | None, name: str) -> Dict[str, Any]:
    """Check Google-style docstring compliance."""
    if not docstring:
        return {
            "compliant": False,
            "issues": ["Missing docstring"],
            "recommendations": ["Add a docstring in Google style"],
        }

    issues = []
    recommendations = []

    lines = docstring.split("\n")

    # Check summary line
    if not lines[0]:
        issues.append("Missing summary line")
        recommendations.append("Start with a brief description")

    # Look for Google-style sections
    has_args = "Args:" in docstring
    has_returns = "Returns:" in docstring
    has_raises = "Raises:" in docstring

    # Check for proper formatting of sections
    for line in lines:
        if re.match(r"^\s+(Args|Returns|Raises|Yields|Examples):\s*$", line):
            # Section header found
            pass
        elif re.match(r"^\s+\w+\s+\([^)]+\):\s+", line):
            # Parameter or return type formatting
            pass

    if not (has_args or has_returns):
        recommendations.append("Consider adding Args/Returns sections for clarity")

    return {
        "compliant": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
        "sections_found": {
            "args": has_args,
            "returns": has_returns,
            "raises": has_raises,
        },
    }


def check_numpy_style_compliance(docstring: str | None, name: str) -> Dict[str, Any]:
    """Check NumPy-style docstring compliance."""
    if not docstring:
        return {
            "compliant": False,
            "issues": ["Missing docstring"],
            "recommendations": ["Add a docstring in NumPy style"],
        }

    issues = []
    recommendations = []

    lines = docstring.split("\n")

    # Check summary line
    if not lines[0]:
        issues.append("Missing summary line")
        recommendations.append("Start with a brief description")

    # Look for NumPy-style sections
    numpy_sections = [
        "Parameters",
        "Returns",
        "Raises",
        "Yields",
        "Examples",
        "Notes",
        "See Also",
    ]
    found_sections = []

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if line_stripped in numpy_sections:
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("-"):
                found_sections.append(line_stripped)

    if not found_sections:
        recommendations.append(
            "Consider adding NumPy-style sections (Parameters, Returns, etc.)"
        )

    return {
        "compliant": len(issues) == 0,
        "issues": issues,
        "recommendations": recommendations,
        "sections_found": found_sections,
    }


def validate_module_docstrings(file_path: str, style: str = "pep257") -> Dict[str, Any]:
    """Validate all docstrings in a module."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Error: Could not parse {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    style_checkers = {
        "pep257": check_pep257_compliance,
        "google": check_google_style_compliance,
        "numpy": check_numpy_style_compliance,
    }

    if style not in style_checkers:
        print(
            f"Error: Unknown style '{style}'. Choose from: {', '.join(style_checkers.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    checker = style_checkers[style]
    results = []
    compliant_count = 0
    issues_count = 0

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            check_result = checker(docstring, node.name)

            item = {
                "type": "function" if isinstance(node, ast.FunctionDef) else "class",
                "name": node.name,
                "lineno": node.lineno,
                "has_docstring": docstring is not None,
                "compliance": check_result,
            }

            results.append(item)

            if check_result["compliant"]:
                compliant_count += 1
            else:
                issues_count += 1

    compliance_percentage = (compliant_count / len(results) * 100) if results else 0

    return {
        "file": str(path),
        "style": style,
        "total_items": len(results),
        "compliant": compliant_count,
        "non_compliant": issues_count,
        "compliance_percentage": compliance_percentage,
        "results": results,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python validate_docstrings.py <file_path> [--style google|numpy|pep257] [--json]"
        )
        sys.exit(1)

    file_path = sys.argv[1]
    style = "pep257"
    use_json = "--json" in sys.argv

    # Parse optional arguments
    for arg in sys.argv[2:]:
        if arg == "--style" and sys.argv.index(arg) + 1 < len(sys.argv):
            style = sys.argv[sys.argv.index(arg) + 1]
        elif arg.startswith("--style="):
            style = arg.split("=")[1]

    result = validate_module_docstrings(file_path, style)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"File: {result['file']}")
        print(f"Style: {result['style']}")
        print(
            f"Compliance: {result['compliance_percentage']:.1f}% ({result['compliant']}/{result['total_items']})\n"
        )

        non_compliant = [
            r for r in result["results"] if not r["compliance"]["compliant"]
        ]

        if non_compliant:
            print(f"Issues Found ({len(non_compliant)}):")
            for item in non_compliant:
                print(
                    f"\n  {item['type'].upper()}: {item['name']} (line {item['lineno']})"
                )
                for issue in item["compliance"]["issues"]:
                    print(f"    ✗ {issue}")
                for rec in item["compliance"]["recommendations"]:
                    print(f"    → {rec}")
        else:
            print("✓ All docstrings are compliant!")
