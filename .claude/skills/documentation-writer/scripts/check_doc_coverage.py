#!/usr/bin/env python3
"""
Check documentation coverage across a module or multiple modules.

Usage:
    python check_doc_coverage.py <file_or_directory> [--json] [--threshold 80]
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


def check_file_coverage(file_path: str) -> Dict[str, Any]:
    """Check documentation coverage for a single file."""
    path = Path(file_path)

    if not path.exists():
        return {"file": str(path), "error": "File not found"}

    if not path.suffix == ".py":
        return {"file": str(path), "error": "Not a Python file"}

    try:
        with open(path, "r") as f:
            content = f.read()
        tree = ast.parse(content)
    except SyntaxError as e:
        return {"file": str(path), "error": f"Syntax error: {e}"}

    functions = []
    classes = []
    documented_functions = 0
    documented_classes = 0

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            has_doc = docstring is not None and len(docstring.strip()) > 0
            functions.append({"name": node.name, "documented": has_doc})
            if has_doc:
                documented_functions += 1

        elif isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)
            has_doc = docstring is not None and len(docstring.strip()) > 0
            classes.append({"name": node.name, "documented": has_doc})
            if has_doc:
                documented_classes += 1

            # Check methods
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    method_doc = ast.get_docstring(item)
                    has_method_doc = (
                        method_doc is not None and len(method_doc.strip()) > 0
                    )
                    if has_method_doc:
                        documented_classes += 1

    total_items = len(functions) + len(classes)
    documented_items = documented_functions + documented_classes

    coverage = (documented_items / total_items * 100) if total_items > 0 else 100

    return {
        "file": str(path),
        "total_functions": len(functions),
        "documented_functions": documented_functions,
        "total_classes": len(classes),
        "documented_classes": documented_classes,
        "total_items": total_items,
        "documented_items": documented_items,
        "coverage_percentage": coverage,
        "functions": functions,
        "classes": classes,
    }


def check_directory_coverage(dir_path: str) -> Dict[str, Any]:
    """Check documentation coverage across all Python files in a directory."""
    path = Path(dir_path)

    if not path.exists():
        print(f"Error: Directory not found: {dir_path}", file=sys.stderr)
        sys.exit(1)

    if not path.is_dir():
        print(f"Error: Not a directory: {dir_path}", file=sys.stderr)
        sys.exit(1)

    py_files = list(path.rglob("*.py"))

    total_items = 0
    total_documented = 0
    file_results = []

    for py_file in sorted(py_files):
        result = check_file_coverage(str(py_file))

        if "error" not in result:
            file_results.append(result)
            total_items += result["total_items"]
            total_documented += result["documented_items"]

    overall_coverage = (
        (total_documented / total_items * 100) if total_items > 0 else 100
    )

    return {
        "directory": str(path),
        "total_files": len(py_files),
        "files_analyzed": len(file_results),
        "total_items": total_items,
        "total_documented": total_documented,
        "overall_coverage_percentage": overall_coverage,
        "files": file_results,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python check_doc_coverage.py <file_or_directory> [--json] [--threshold 80]"
        )
        sys.exit(1)

    path_arg = sys.argv[1]
    use_json = "--json" in sys.argv
    threshold = 80

    # Parse threshold
    for arg in sys.argv[2:]:
        if arg == "--threshold" and sys.argv.index(arg) + 1 < len(sys.argv):
            threshold = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg.startswith("--threshold="):
            threshold = int(arg.split("=")[1])

    path = Path(path_arg)

    if path.is_file():
        result = check_file_coverage(path_arg)
    elif path.is_dir():
        result = check_directory_coverage(path_arg)
    else:
        print(f"Error: Path not found: {path_arg}", file=sys.stderr)
        sys.exit(1)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        if "directory" in result:
            print(f"Directory: {result['directory']}")
            print(
                f"Files Analyzed: {result['files_analyzed']} / {result['total_files']}"
            )
            print(f"Overall Coverage: {result['overall_coverage_percentage']:.1f}%")
            print(
                f"Documented Items: {result['total_documented']} / {result['total_items']}\n"
            )

            if result["overall_coverage_percentage"] < threshold:
                print(f"⚠️  Coverage below threshold of {threshold}%!")

            # Show files with low coverage
            low_coverage_files = [
                f for f in result["files"] if f["coverage_percentage"] < threshold
            ]

            if low_coverage_files:
                print(f"\nFiles Below {threshold}% Coverage:")
                for file_result in sorted(
                    low_coverage_files, key=lambda x: x["coverage_percentage"]
                ):
                    print(f"  {file_result['file']}")
                    print(
                        f"    Coverage: {file_result['coverage_percentage']:.1f}% ({file_result['documented_items']}/{file_result['total_items']})"
                    )

        else:
            # Single file
            print(f"File: {result['file']}")
            print(f"Coverage: {result['coverage_percentage']:.1f}%")
            print(
                f"Functions: {result['documented_functions']} / {result['total_functions']}"
            )
            print(
                f"Classes: {result['documented_classes']} / {result['total_classes']}\n"
            )

            if result["coverage_percentage"] < threshold:
                print(f"⚠️  Coverage below threshold of {threshold}%!")

            # Show undocumented items
            undocumented_funcs = [f for f in result["functions"] if not f["documented"]]
            undocumented_classes = [c for c in result["classes"] if not c["documented"]]

            if undocumented_funcs:
                print(f"\nUndocumented Functions ({len(undocumented_funcs)}):")
                for func in undocumented_funcs:
                    print(f"  - {func['name']}")

            if undocumented_classes:
                print(f"\nUndocumented Classes ({len(undocumented_classes)}):")
                for cls in undocumented_classes:
                    print(f"  - {cls['name']}")
