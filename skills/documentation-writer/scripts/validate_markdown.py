#!/usr/bin/env python3
"""
Validate markdown files for format issues and check for broken links.

Usage:
    python validate_markdown.py <file_path> [--check-links] [--json]
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


def check_markdown_formatting(content: str) -> Dict[str, Any]:
    """Check markdown formatting issues."""
    issues = []
    warnings = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        line_num = i + 1

        # Check for common markdown issues
        if line.startswith("# ") and i > 0 and lines[i - 1].strip() != "":
            warnings.append(
                f"Line {line_num}: Top-level heading (#) should be preceded by blank line"
            )

        # Check for inconsistent spacing in headers
        if re.match(r"^#+\S", line):
            issues.append(f"Line {line_num}: Header should have space after #")

        # Check for unmatched brackets
        open_brackets = line.count("[") - line.count("]")
        if open_brackets != 0:
            # Could be a link with nested brackets, skip for now
            pass

        # Check for code block formatting
        if line.strip().startswith("```"):
            # Check if language is specified for code blocks
            match = re.match(r"^```(\w+)?", line)
            if match and not match.group(1):
                warnings.append(
                    f"Line {line_num}: Consider specifying language for code block"
                )

        # Check for trailing whitespace
        if line.rstrip() != line and line.strip():
            warnings.append(f"Line {line_num}: Trailing whitespace detected")

        # Check for multiple consecutive blank lines
        if i > 0 and line.strip() == "" and lines[i - 1].strip() == "":
            if i + 1 < len(lines) and lines[i + 1].strip() == "":
                issues.append(f"Line {line_num}: Multiple consecutive blank lines")

    return {
        "issues": issues,
        "warnings": warnings,
    }


def extract_links(content: str) -> List[Dict[str, Any]]:
    """Extract all links from markdown content."""
    links = []

    # Markdown links: [text](url)
    markdown_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    for match in re.finditer(markdown_pattern, content):
        text, url = match.groups()
        links.append(
            {
                "type": "markdown",
                "text": text,
                "url": url,
                "position": match.start(),
            }
        )

    # HTML links: <url>
    html_pattern = r"<(https?://[^>]+)>"
    for match in re.finditer(html_pattern, content):
        url = match.group(1)
        links.append(
            {
                "type": "html",
                "url": url,
                "position": match.start(),
            }
        )

    # Reference links: [text][ref]
    ref_pattern = r"\[([^\]]+)\]\[([^\]]+)\]"
    for match in re.finditer(ref_pattern, content):
        text, ref = match.groups()
        links.append(
            {
                "type": "reference",
                "text": text,
                "reference": ref,
                "position": match.start(),
            }
        )

    return links


def categorize_links(links: List[Dict[str, Any]]) -> Dict[str, List]:
    """Categorize links by type."""
    external = []
    internal = []
    anchors = []

    for link in links:
        url = link.get("url", "")

        if url.startswith("http://") or url.startswith("https://"):
            external.append(link)
        elif url.startswith("#"):
            anchors.append(link)
        elif url.startswith("/"):
            internal.append(link)
        else:
            internal.append(link)

    return {
        "external": external,
        "internal": internal,
        "anchors": anchors,
    }


def validate_markdown_file(file_path: str, check_links: bool = False) -> Dict[str, Any]:
    """Validate a markdown file."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check formatting
    formatting_check = check_markdown_formatting(content)

    # Extract and categorize links
    links = extract_links(content)
    link_categories = categorize_links(links)

    # Check for broken internal links
    broken_links = []
    if check_links:
        for link in link_categories["internal"]:
            url = link.get("url", "")
            # Skip URLs with query parameters or hashes for now
            if "?" not in url and "#" not in url:
                target_path = path.parent / url
                if not target_path.exists():
                    broken_links.append(
                        {
                            "url": url,
                            "target": str(target_path),
                        }
                    )

    # Calculate header structure
    lines = content.split("\n")
    headers = []
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+)", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append({"level": level, "title": title})

    # Check header hierarchy
    header_issues = []
    for i, header in enumerate(headers):
        if i > 0:
            prev_level = headers[i - 1]["level"]
            if header["level"] > prev_level + 1:
                header_issues.append(
                    f"Skipped header level: {headers[i - 1]['title']} (h{prev_level}) → {header['title']} (h{header['level']})"
                )

    total_issues = (
        len(formatting_check["issues"]) + len(header_issues) + len(broken_links)
    )

    return {
        "file": str(path),
        "total_issues": total_issues,
        "formatting": {
            "issues": formatting_check["issues"],
            "warnings": formatting_check["warnings"],
        },
        "links": {
            "total": len(links),
            "external": len(link_categories["external"]),
            "internal": len(link_categories["internal"]),
            "anchors": len(link_categories["anchors"]),
            "broken": broken_links,
        },
        "headers": {
            "total": len(headers),
            "issues": header_issues,
        },
        "content_stats": {
            "lines": len(lines),
            "words": len(content.split()),
            "characters": len(content),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_markdown.py <file_path> [--check-links] [--json]")
        sys.exit(1)

    file_path = sys.argv[1]
    check_links = "--check-links" in sys.argv
    use_json = "--json" in sys.argv

    result = validate_markdown_file(file_path, check_links)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"File: {result['file']}")
        print(f"Total Issues: {result['total_issues']}\n")

        # Formatting issues
        if result["formatting"]["issues"]:
            print("Formatting Issues:")
            for issue in result["formatting"]["issues"]:
                print(f"  ✗ {issue}")

        if result["formatting"]["warnings"]:
            print("\nFormatting Warnings:")
            for warning in result["formatting"]["warnings"][:5]:  # Show first 5
                print(f"  ⚠ {warning}")
            if len(result["formatting"]["warnings"]) > 5:
                print(
                    f"  ... and {len(result['formatting']['warnings']) - 5} more warnings"
                )

        # Header issues
        if result["headers"]["issues"]:
            print("\nHeader Structure Issues:")
            for issue in result["headers"]["issues"]:
                print(f"  ⚠ {issue}")

        # Links
        print("\nLinks Summary:")
        print(f"  Total: {result['links']['total']}")
        print(f"  External: {result['links']['external']}")
        print(f"  Internal: {result['links']['internal']}")
        print(f"  Anchors: {result['links']['anchors']}")

        if result["links"]["broken"]:
            print("\n  Broken Links:")
            for link in result["links"]["broken"]:
                print(f"    ✗ {link['url']}")

        # Content stats
        print("\nContent Statistics:")
        print(f"  Lines: {result['content_stats']['lines']}")
        print(f"  Words: {result['content_stats']['words']}")
        print(f"  Characters: {result['content_stats']['characters']}")

        if result["total_issues"] == 0:
            print("\n✓ No issues found!")
