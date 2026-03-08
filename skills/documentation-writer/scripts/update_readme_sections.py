#!/usr/bin/env python3
"""
Update specific sections in a README file without manual editing.

Usage:
    python update_readme_sections.py <file_path> --section "Section Name" --content "New content" [--json]
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


def find_section(
    content: str, section_name: str
) -> tuple[Optional[int], Optional[int]]:
    """Find the start and end line numbers of a section."""
    lines = content.split("\n")

    # Find section header
    section_pattern = rf"^#{1, 6}\s+{re.escape(section_name)}\s*$"
    start_line = None

    for i, line in enumerate(lines):
        if re.match(section_pattern, line, re.IGNORECASE):
            start_line = i
            break

    if start_line is None:
        return None, None

    # Find next section header at same or higher level
    section_level = len(re.match(r"^(#+)", lines[start_line]).group(1))
    end_line = len(lines)

    for i in range(start_line + 1, len(lines)):
        if re.match(r"^#+\s", lines[i]):
            header_level = len(re.match(r"^(#+)", lines[i]).group(1))
            if header_level <= section_level:
                end_line = i
                break

    return start_line, end_line


def list_sections(content: str) -> List[Dict[str, Any]]:
    """List all sections in a markdown file."""
    lines = content.split("\n")
    sections = []

    for i, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            sections.append(
                {
                    "level": level,
                    "title": title,
                    "line": i + 1,
                }
            )

    return sections


def update_section(
    file_path: str, section_name: str, new_content: str
) -> Dict[str, Any]:
    """Update a specific section in a README file."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    start_line, end_line = find_section(content, section_name)

    if start_line is None:
        return {
            "file": str(path),
            "success": False,
            "error": f"Section '{section_name}' not found",
            "available_sections": list_sections(content),
        }

    lines = content.split("\n")

    # Keep the header, replace everything else
    updated_lines = (
        lines[: start_line + 1]
        + [""]
        + new_content.split("\n")
        + [""]
        + lines[end_line:]
    )
    updated_content = "\n".join(updated_lines)

    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return {
        "file": str(path),
        "success": True,
        "section_name": section_name,
        "original_lines": end_line - start_line - 1,
        "new_lines": len(new_content.split("\n")),
        "message": f"Updated section '{section_name}' successfully",
    }


def extract_section(file_path: str, section_name: str) -> Dict[str, Any]:
    """Extract a specific section from a README file."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    start_line, end_line = find_section(content, section_name)

    if start_line is None:
        return {
            "file": str(path),
            "success": False,
            "error": f"Section '{section_name}' not found",
            "available_sections": list_sections(content),
        }

    lines = content.split("\n")
    section_content = "\n".join(lines[start_line:end_line])

    return {
        "file": str(path),
        "success": True,
        "section_name": section_name,
        "start_line": start_line + 1,
        "end_line": end_line,
        "content": section_content,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python update_readme_sections.py <file_path> [--section NAME] [--content TEXT] [--extract] [--list] [--json]"
        )
        sys.exit(1)

    file_path = sys.argv[1]
    section_name = None
    new_content = None
    use_json = "--json" in sys.argv
    list_sections_flag = "--list" in sys.argv
    extract_flag = "--extract" in sys.argv

    # Parse arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--section" and i + 1 < len(sys.argv):
            section_name = sys.argv[i + 1]
        elif arg.startswith("--section="):
            section_name = arg.split("=", 1)[1]
        elif arg == "--content" and i + 1 < len(sys.argv):
            new_content = sys.argv[i + 1]
        elif arg.startswith("--content="):
            new_content = arg.split("=", 1)[1]

    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if list_sections_flag:
        sections = list_sections(content)
        result = {
            "file": str(path),
            "sections": sections,
        }
        if use_json:
            import json

            print(json.dumps(result, indent=2))
        else:
            print(f"File: {result['file']}")
            print(f"Sections ({len(sections)}):")
            for sec in sections:
                print(f"  Level {sec['level']}: {sec['title']} (line {sec['line']})")

    elif extract_flag and section_name:
        result = extract_section(file_path, section_name)
        if use_json:
            import json

            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"Extracted section '{section_name}':")
                print(result["content"])
            else:
                print(f"Error: {result['error']}")

    elif section_name and new_content:
        result = update_section(file_path, section_name, new_content)
        if use_json:
            import json

            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(result["message"])
            else:
                print(f"Error: {result['error']}")
                print("\nAvailable sections:")
                for sec in result["available_sections"]:
                    print(f"  - {sec['title']}")

    else:
        print(
            "Usage: python update_readme_sections.py <file_path> [--section NAME] [--content TEXT] [--extract] [--list] [--json]"
        )
        print("\nOptions:")
        print("  --section NAME    Section name to update or extract")
        print("  --content TEXT    New content for the section")
        print("  --extract         Extract section content instead of updating")
        print("  --list           List all available sections")
        print("  --json           Output as JSON")
