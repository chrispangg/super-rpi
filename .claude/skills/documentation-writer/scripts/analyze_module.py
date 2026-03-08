#!/usr/bin/env python3
"""
Analyze Python module to extract functions, classes, signatures, and type hints.

Usage:
    python analyze_module.py <file_path> [--json]
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


def extract_type_hint(annotation: Any) -> str:
    """Extract string representation of a type annotation."""
    if annotation is None:
        return "None"
    if isinstance(annotation, ast.Name):
        return annotation.id
    if isinstance(annotation, ast.Constant):
        return repr(annotation.value)
    if isinstance(annotation, ast.Attribute):
        return f"{extract_type_hint(annotation.value)}.{annotation.attr}"
    if isinstance(annotation, ast.Subscript):
        value = extract_type_hint(annotation.value)
        slice_val = extract_type_hint(annotation.slice)
        return f"{value}[{slice_val}]"
    if isinstance(annotation, ast.Tuple):
        elements = ", ".join(extract_type_hint(e) for e in annotation.elts)
        return f"({elements})"
    return ast.unparse(annotation) if hasattr(ast, "unparse") else str(annotation)


def extract_function_info(node: ast.FunctionDef) -> Dict[str, Any]:
    """Extract information about a function."""
    args = node.args
    params = []

    for arg in args.args:
        param_type = extract_type_hint(arg.annotation) if arg.annotation else "Any"
        params.append({"name": arg.arg, "type": param_type})

    return_type = extract_type_hint(node.returns) if node.returns else "None"

    return {
        "type": "function",
        "name": node.name,
        "lineno": node.lineno,
        "parameters": params,
        "return_type": return_type,
        "docstring": ast.get_docstring(node),
        "is_private": node.name.startswith("_"),
        "decorators": [ast.unparse(d) for d in node.decorator_list],
    }


def extract_class_info(node: ast.ClassDef) -> Dict[str, Any]:
    """Extract information about a class."""
    methods = []
    attributes = []

    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            methods.append(extract_function_info(item))
        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    attributes.append(
                        {
                            "name": target.id,
                            "lineno": item.lineno,
                            "docstring": ast.get_docstring(item)
                            if isinstance(item, ast.Expr)
                            else None,
                        }
                    )

    bases = [ast.unparse(b) for b in node.bases]

    return {
        "type": "class",
        "name": node.name,
        "lineno": node.lineno,
        "docstring": ast.get_docstring(node),
        "bases": bases,
        "methods": methods,
        "attributes": attributes,
        "is_private": node.name.startswith("_"),
    }


def analyze_module(file_path: str) -> Dict[str, Any]:
    """Analyze a Python module and extract all definitions."""
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

    module_docstring = ast.get_docstring(tree)

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(
                    {
                        "type": "from",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                    }
                )

    # Get top-level definitions only
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(extract_function_info(node))
        elif isinstance(node, ast.ClassDef):
            classes.append(extract_class_info(node))

    return {
        "file": str(path),
        "module_docstring": module_docstring,
        "imports": imports,
        "functions": functions,
        "classes": classes,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_module.py <file_path> [--json]")
        sys.exit(1)

    file_path = sys.argv[1]
    use_json = "--json" in sys.argv

    result = analyze_module(file_path)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"Module: {result['file']}")
        print(f"Docstring: {result['module_docstring']}\n")

        if result["functions"]:
            print("Functions:")
            for func in result["functions"]:
                params = ", ".join(
                    f"{p['name']}: {p['type']}" for p in func["parameters"]
                )
                print(f"  - {func['name']}({params}) -> {func['return_type']}")
                if func["docstring"]:
                    print(f"    {func['docstring'][:60]}...")

        if result["classes"]:
            print("\nClasses:")
            for cls in result["classes"]:
                print(
                    f"  - {cls['name']}{tuple(cls['bases']) if cls['bases'] else '()'}"
                )
                if cls["docstring"]:
                    print(f"    {cls['docstring'][:60]}...")
                for method in cls["methods"]:
                    params = ", ".join(
                        f"{p['name']}: {p['type']}" for p in method["parameters"]
                    )
                    print(
                        f"    - {method['name']}({params}) -> {method['return_type']}"
                    )
