#!/usr/bin/env python3
"""
Generate docstring templates for functions with type information pre-filled.

Usage:
    python generate_function_docs.py <file_path> [--format google|numpy|sphinx] [--json]
"""

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


def extract_type_hint(annotation: Any) -> str:
    """Extract string representation of a type annotation."""
    if annotation is None:
        return ""
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
    return ast.unparse(annotation) if hasattr(ast, "unparse") else str(annotation)


def generate_google_style(func: ast.FunctionDef) -> str:
    """Generate Google-style docstring template."""
    args = func.args
    params = []

    for arg in args.args:
        if arg.arg == "self" or arg.arg == "cls":
            continue
        param_type = extract_type_hint(arg.annotation) if arg.annotation else "type"
        params.append(f"    {arg.arg} ({param_type}): Description of {arg.arg}.")

    return_type = extract_type_hint(func.returns) if func.returns else "type"

    docstring = '    """Brief description of the function.\n\n'

    if params:
        docstring += "    Args:\n"
        docstring += "\n".join(params)
        docstring += "\n\n"

    docstring += f"    Returns:\n        {return_type}: Description of return value.\n"

    if any(d.id == "Exception" for d in ast.walk(func) if isinstance(d, ast.Name)):
        docstring += "\n    Raises:\n        ExceptionType: Description of when this exception is raised.\n"

    docstring += '    """\n'

    return docstring


def generate_numpy_style(func: ast.FunctionDef) -> str:
    """Generate NumPy-style docstring template."""
    args = func.args
    params = []

    for arg in args.args:
        if arg.arg == "self" or arg.arg == "cls":
            continue
        param_type = extract_type_hint(arg.annotation) if arg.annotation else "type"
        params.append(
            f"    {arg.arg} : {param_type}\n        Description of {arg.arg}."
        )

    return_type = extract_type_hint(func.returns) if func.returns else "type"

    docstring = '    """Brief description of the function.\n\n'

    if params:
        docstring += "    Parameters\n"
        docstring += "    ----------\n"
        docstring += "\n".join(params)
        docstring += "\n\n"

    docstring += f"    Returns\n    -------\n    {return_type}\n        Description of return value.\n"

    docstring += '    """\n'

    return docstring


def generate_sphinx_style(func: ast.FunctionDef) -> str:
    """Generate Sphinx-style docstring template."""
    args = func.args
    params = []

    for arg in args.args:
        if arg.arg == "self" or arg.arg == "cls":
            continue
        param_type = extract_type_hint(arg.annotation) if arg.annotation else "type"
        params.append(
            f"    :param {arg.arg}: Description of {arg.arg}.\n    :type {arg.arg}: {param_type}"
        )

    return_type = extract_type_hint(func.returns) if func.returns else "type"

    docstring = '    """Brief description of the function.\n\n'

    if params:
        docstring += "\n".join(params)
        docstring += "\n"

    docstring += (
        f"    :returns: Description of return value.\n    :rtype: {return_type}\n"
    )

    docstring += '    """\n'

    return docstring


def generate_docstring_templates(
    file_path: str, style: str = "google"
) -> Dict[str, Any]:
    """Generate docstring templates for all functions in a module."""
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

    generators = {
        "google": generate_google_style,
        "numpy": generate_numpy_style,
        "sphinx": generate_sphinx_style,
    }

    if style not in generators:
        print(
            f"Error: Unknown style '{style}'. Choose from: {', '.join(generators.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    generator = generators[style]
    templates = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            has_docs = docstring is not None

            template = {
                "name": node.name,
                "lineno": node.lineno,
                "has_existing_docstring": has_docs,
                "existing_docstring": docstring,
                "template": generator(node),
                "style": style,
            }
            templates.append(template)

    return {
        "file": str(path),
        "style": style,
        "total_functions": len(templates),
        "templates": templates,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_function_docs.py <file_path> [--format google|numpy|sphinx] [--json]"
        )
        sys.exit(1)

    file_path = sys.argv[1]
    style = "google"

    # Parse optional arguments
    for arg in sys.argv[2:]:
        if arg.startswith("--format"):
            if "=" in arg:
                style = arg.split("=")[1]
            else:
                idx = sys.argv.index(arg)
                if idx + 1 < len(sys.argv):
                    style = sys.argv[idx + 1]

    use_json = "--json" in sys.argv

    result = generate_docstring_templates(file_path, style)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"File: {result['file']}")
        print(f"Style: {result['style']}")
        print(f"Total Functions: {result['total_functions']}\n")

        for template in result["templates"]:
            print(f"Function: {template['name']} (line {template['lineno']})")
            print(f"Has existing docstring: {template['has_existing_docstring']}")
            print("Template:")
            print(template["template"])
            print()
