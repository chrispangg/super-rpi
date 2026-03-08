#!/usr/bin/env python3
"""
Generate a table of contents from markdown file headers.

Usage:
    python generate_toc.py <file_path> [--max-level 3] [--json]
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any


def extract_headers(content: str, max_level: int = 3) -> List[Dict[str, Any]]:
    """Extract headers from markdown content."""
    headers = []
    lines = content.split("\n")

    for line in lines:
        # Match markdown headers (# to ######)
        match = re.match(r"^(#{1,6})\s+(.+?)(?:\s*\{.*\})?$", line)
        if match:
            level = len(match.group(1))
            if level > max_level:
                continue

            title = match.group(2).strip()

            # Generate anchor ID (same as GitHub)
            anchor_id = title.lower()
            anchor_id = re.sub(r"[^\w\s-]", "", anchor_id)
            anchor_id = re.sub(r"[-\s]+", "-", anchor_id)
            anchor_id = anchor_id.strip("-")

            headers.append(
                {
                    "level": level,
                    "title": title,
                    "anchor": anchor_id,
                    "line": len([line for line in lines[: lines.index(line)] if line])
                    + 1,
                }
            )

    return headers


def generate_toc_markdown(headers: List[Dict[str, Any]]) -> str:
    """Generate markdown table of contents from headers."""
    if not headers:
        return ""

    toc_lines = ["## Table of Contents\n"]

    for header in headers:
        indent = "  " * (header["level"] - 1)
        anchor = header["anchor"]
        title = header["title"]
        toc_lines.append(f"{indent}- [{title}](#{anchor})")

    return "\n".join(toc_lines)


def generate_toc_html(headers: List[Dict[str, Any]]) -> str:
    """Generate HTML table of contents from headers."""
    if not headers:
        return ""

    html_lines = ["<nav>\n  <h2>Table of Contents</h2>\n  <ul>"]

    current_level = 0
    for header in headers:
        level = header["level"]

        # Close lists if going up levels
        while current_level > level:
            html_lines.append(
                "  " * (current_level - 1) + "  </ul>\n  " * (current_level - level)
            )
            current_level -= 1

        # Open lists if going down levels
        while current_level < level:
            if current_level > 0:
                html_lines[-1] = (
                    html_lines[-1].rstrip() + "\n" + "    " * current_level + "<ul>"
                )
            else:
                html_lines.append("    <ul>")
            current_level += 1

        anchor = header["anchor"]
        title = header["title"]
        html_lines.append(
            "    " * current_level + f'<li><a href="#{anchor}">{title}</a></li>'
        )

    # Close remaining lists
    while current_level > 0:
        html_lines.append("    " * (current_level - 1) + "  </ul>")
        current_level -= 1

    html_lines.append("  </ul>\n</nav>")
    return "\n".join(html_lines)


def process_markdown_file(
    file_path: str, max_level: int = 3, format_type: str = "markdown"
) -> Dict[str, Any]:
    """Process a markdown file and generate table of contents."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() not in [".md", ".markdown"]:
        print(
            f"Warning: File does not appear to be markdown: {file_path}",
            file=sys.stderr,
        )

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    headers = extract_headers(content, max_level)

    if format_type == "html":
        toc_output = generate_toc_html(headers)
    else:
        toc_output = generate_toc_markdown(headers)

    return {
        "file": str(path),
        "max_level": max_level,
        "format": format_type,
        "total_headers": len(headers),
        "headers": headers,
        "table_of_contents": toc_output,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_toc.py <file_path> [--max-level 3] [--format markdown|html] [--json]"
        )
        sys.exit(1)

    file_path = sys.argv[1]
    max_level = 3
    format_type = "markdown"
    use_json = False

    # Parse optional arguments
    for i, arg in enumerate(sys.argv[2:], 1):
        if arg == "--max-level" and i + 1 < len(sys.argv):
            max_level = int(sys.argv[i + 1])
        elif arg.startswith("--max-level="):
            max_level = int(arg.split("=")[1])
        elif arg == "--format" and i + 1 < len(sys.argv):
            format_type = sys.argv[i + 1]
        elif arg.startswith("--format="):
            format_type = arg.split("=")[1]
        elif arg == "--json":
            use_json = True

    result = process_markdown_file(file_path, max_level, format_type)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"File: {result['file']}")
        print(f"Format: {result['format']}")
        print(f"Max Level: {result['max_level']}")
        print(f"Total Headers: {result['total_headers']}\n")
        print(result["table_of_contents"])
