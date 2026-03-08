#!/usr/bin/env python3
"""
Find functions and classes in a module that lack docstrings or have incomplete documentation.

Usage:
    python find_undocumented.py <file_path> [--json]
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


def is_private(name: str) -> bool:
    """Check if a name is private (starts with _)."""
    return name.startswith("_")


def analyze_docstring_completeness(docstring: str | None) -> Dict[str, Any]:
    """Analyze whether a docstring is complete."""
    if not docstring:
        return {
            "has_docstring": False,
            "complete": False,
            "issues": ["Missing docstring"],
        }

    issues = []
    lines = docstring.split("\n")

    # Check if it has a summary line
    if not lines[0].strip():
        issues.append("Missing summary line")

    # Check if it's too short (likely incomplete)
    if len(lines) == 1 and len(lines[0]) < 10:
        issues.append("Summary too short (likely incomplete)")

    return {
        "has_docstring": True,
        "complete": len(issues) == 0,
        "issues": issues,
        "length": len(docstring),
    }


def check_function(node: ast.FunctionDef) -> Dict[str, Any]:
    """Check a function for documentation."""
    docstring = ast.get_docstring(node)
    analysis = analyze_docstring_completeness(docstring)

    # Extract parameters for checking if they're documented
    params = [arg.arg for arg in node.args.args]

    return {
        "type": "function",
        "name": node.name,
        "lineno": node.lineno,
        "is_private": is_private(node.name),
        "parameters": params,
        "has_return_annotation": node.returns is not None,
        "docstring_analysis": analysis,
        "needs_documentation": not analysis["complete"] and not is_private(node.name),
    }


def check_class(node: ast.ClassDef) -> Dict[str, Any]:
    """Check a class for documentation."""
    docstring = ast.get_docstring(node)
    analysis = analyze_docstring_completeness(docstring)

    methods = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and not is_private(item.name):
            method_docstring = ast.get_docstring(item)
            method_analysis = analyze_docstring_completeness(method_docstring)
            if not method_analysis["complete"]:
                methods.append(
                    {
                        "name": item.name,
                        "lineno": item.lineno,
                        "docstring_analysis": method_analysis,
                    }
                )

    return {
        "type": "class",
        "name": node.name,
        "lineno": node.lineno,
        "docstring_analysis": analysis,
        "undocumented_methods": methods,
        "needs_documentation": not analysis["complete"],
    }


def find_undocumented(file_path: str) -> Dict[str, Any]:
    """Find undocumented functions and classes in a module."""
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

    undocumented_functions = []
    undocumented_classes = []
    fully_documented = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            check = check_function(node)
            if check["needs_documentation"]:
                undocumented_functions.append(check)
            elif not is_private(check["name"]):
                fully_documented.append(check)
        elif isinstance(node, ast.ClassDef):
            check = check_class(node)
            if check["needs_documentation"] or check["undocumented_methods"]:
                undocumented_classes.append(check)
            else:
                fully_documented.append(check)

    total_items = (
        len(undocumented_functions) + len(undocumented_classes) + len(fully_documented)
    )
    coverage = (len(fully_documented) / total_items * 100) if total_items > 0 else 0

    return {
        "file": str(path),
        "total_items": total_items,
        "documented_items": len(fully_documented),
        "coverage_percentage": coverage,
        "undocumented_functions": undocumented_functions,
        "undocumented_classes": undocumented_classes,
        "fully_documented": fully_documented,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_undocumented.py <file_path> [--json]")
        sys.exit(1)

    file_path = sys.argv[1]
    use_json = "--json" in sys.argv

    result = find_undocumented(file_path)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"File: {result['file']}")
        print(
            f"Documentation Coverage: {result['coverage_percentage']:.1f}% ({result['documented_items']}/{result['total_items']})\n"
        )

        if result["undocumented_functions"]:
            print(f"Undocumented Functions ({len(result['undocumented_functions'])}):")
            for func in result["undocumented_functions"]:
                print(f"  - {func['name']} (line {func['lineno']})")
                for issue in func["docstring_analysis"]["issues"]:
                    print(f"    Issue: {issue}")

        if result["undocumented_classes"]:
            print(f"\nUndocumented Classes ({len(result['undocumented_classes'])}):")
            for cls in result["undocumented_classes"]:
                print(f"  - {cls['name']} (line {cls['lineno']})")
                for issue in cls["docstring_analysis"]["issues"]:
                    print(f"    Issue: {issue}")
                if cls["undocumented_methods"]:
                    print(
                        f"    Undocumented methods: {', '.join(m['name'] for m in cls['undocumented_methods'])}"
                    )
