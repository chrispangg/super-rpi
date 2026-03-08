#!/usr/bin/env python3
"""
Extract import dependencies from a Python module to understand architecture.

Usage:
    python extract_dependencies.py <file_path> [--json]
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Set


def extract_imports(file_path: str) -> Dict[str, any]:
    """Extract all imports from a Python file."""
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

    standard_lib_imports = []
    third_party_imports = []
    local_imports = []

    standard_libs = {
        "abc",
        "asyncio",
        "atexit",
        "base64",
        "bisect",
        "builtins",
        "bz2",
        "calendar",
        "cmath",
        "cmd",
        "code",
        "codecs",
        "codeop",
        "collections",
        "colorsys",
        "compileall",
        "concurrent",
        "configparser",
        "contextlib",
        "contextvars",
        "copy",
        "copyreg",
        "cProfile",
        "crypt",
        "csv",
        "ctypes",
        "curses",
        "dataclasses",
        "datetime",
        "dbm",
        "decimal",
        "difflib",
        "dis",
        "distutils",
        "doctest",
        "dummy_thread",
        "email",
        "encodings",
        "enum",
        "errno",
        "faulthandler",
        "fcntl",
        "filecmp",
        "fileinput",
        "fnmatch",
        "fractions",
        "ftplib",
        "functools",
        "gc",
        "getopt",
        "getpass",
        "gettext",
        "glob",
        "graphlib",
        "grp",
        "gzip",
        "hashlib",
        "heapq",
        "hmac",
        "html",
        "http",
        "idlelib",
        "imaplib",
        "imghdr",
        "imp",
        "importlib",
        "inspect",
        "io",
        "ipaddress",
        "itertools",
        "json",
        "keyword",
        "lib2to3",
        "linecache",
        "locale",
        "logging",
        "lzma",
        "mailbox",
        "mailcap",
        "marshal",
        "math",
        "mimetypes",
        "mmap",
        "modulefinder",
        "msilib",
        "msvcrt",
        "multiprocessing",
        "netrc",
        "nis",
        "nntplib",
        "numbers",
        "operator",
        "optparse",
        "os",
        "ossaudiodev",
        "parser",
        "pathlib",
        "pdb",
        "pickle",
        "pickletools",
        "pipes",
        "pkgutil",
        "platform",
        "plistlib",
        "poplib",
        "posix",
        "posixpath",
        "pprint",
        "profile",
        "pstats",
        "pty",
        "pwd",
        "py_compile",
        "pyclbr",
        "pydoc",
        "queue",
        "quopri",
        "random",
        "re",
        "readline",
        "reprlib",
        "resource",
        "rlcompleter",
        "runpy",
        "sched",
        "secrets",
        "select",
        "selectors",
        "shelve",
        "shlex",
        "shutil",
        "signal",
        "site",
        "smtpd",
        "smtplib",
        "sndhdr",
        "socket",
        "socketserver",
        "spwd",
        "sqlite3",
        "ssl",
        "stat",
        "statistics",
        "string",
        "stringprep",
        "struct",
        "subprocess",
        "sunau",
        "sys",
        "sysconfig",
        "syslog",
        "tabnanny",
        "tarfile",
        "telnetlib",
        "tempfile",
        "termios",
        "test",
        "textwrap",
        "threading",
        "time",
        "timeit",
        "tkinter",
        "token",
        "tokenize",
        "trace",
        "traceback",
        "tracemalloc",
        "typing",
        "typing_extensions",
        "unicodedata",
        "unittest",
        "urllib",
        "uu",
        "uuid",
        "venv",
        "warnings",
        "wave",
        "weakref",
        "webbrowser",
        "winreg",
        "winsound",
        "wsgiref",
        "xdrlib",
        "xml",
        "xmlrpc",
        "zipapp",
        "zipfile",
        "zipimport",
        "zlib",
        "__future__",
        "__main__",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split(".")[0]
                import_item = {
                    "type": "import",
                    "module": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                }

                if module_name in standard_libs:
                    standard_lib_imports.append(import_item)
                elif "." not in alias.name or alias.name.startswith("."):
                    local_imports.append(import_item)
                else:
                    third_party_imports.append(import_item)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [alias.name for alias in node.names]

            import_item = {
                "type": "from",
                "module": module,
                "names": names,
                "line": node.lineno,
                "level": node.level,  # for relative imports
            }

            module_root = module.split(".")[0] if module else ""

            if module_root in standard_libs or module in ("__future__",):
                standard_lib_imports.append(import_item)
            elif module.startswith(".") or node.level > 0:
                local_imports.append(import_item)
            else:
                third_party_imports.append(import_item)

    return {
        "file": str(path),
        "standard_library": standard_lib_imports,
        "third_party": third_party_imports,
        "local": local_imports,
    }


def categorize_dependencies(imports: Dict[str, List]) -> Dict[str, any]:
    """Categorize and summarize dependencies."""
    all_imports = (
        imports["standard_library"] + imports["third_party"] + imports["local"]
    )

    std_modules: Set[str] = set()
    third_party_modules: Set[str] = set()
    local_modules: Set[str] = set()

    for imp in imports["standard_library"]:
        if imp["type"] == "import":
            std_modules.add(imp["module"].split(".")[0])
        elif imp["type"] == "from":
            std_modules.add(imp["module"].split(".")[0])

    for imp in imports["third_party"]:
        if imp["type"] == "import":
            third_party_modules.add(imp["module"].split(".")[0])
        elif imp["type"] == "from":
            third_party_modules.add(imp["module"].split(".")[0])

    for imp in imports["local"]:
        if imp["type"] == "import":
            local_modules.add(imp["module"].split(".")[0])
        elif imp["type"] == "from":
            local_modules.add(imp["module"].split(".")[0])

    return {
        "file": imports["file"],
        "total_imports": len(all_imports),
        "categories": {
            "standard_library": {
                "count": len(imports["standard_library"]),
                "modules": sorted(list(std_modules)),
            },
            "third_party": {
                "count": len(imports["third_party"]),
                "modules": sorted(list(third_party_modules)),
            },
            "local": {
                "count": len(imports["local"]),
                "modules": sorted(list(local_modules)),
            },
        },
        "detailed_imports": imports,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_dependencies.py <file_path> [--json]")
        sys.exit(1)

    file_path = sys.argv[1]
    use_json = "--json" in sys.argv

    imports = extract_imports(file_path)
    result = categorize_dependencies(imports)

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        # Pretty print
        print(f"File: {result['file']}")
        print(f"Total Imports: {result['total_imports']}\n")

        cats = result["categories"]
        print("Standard Library:")
        print(f"  Count: {cats['standard_library']['count']}")
        print(f"  Modules: {', '.join(cats['standard_library']['modules'][:10])}")
        if len(cats["standard_library"]["modules"]) > 10:
            print(f"  ... and {len(cats['standard_library']['modules']) - 10} more\n")
        else:
            print()

        print("Third-Party:")
        print(f"  Count: {cats['third_party']['count']}")
        print(f"  Modules: {', '.join(cats['third_party']['modules'][:10])}")
        if len(cats["third_party"]["modules"]) > 10:
            print(f"  ... and {len(cats['third_party']['modules']) - 10} more\n")
        else:
            print()

        print("Local/Relative:")
        print(f"  Count: {cats['local']['count']}")
        print(f"  Modules: {', '.join(cats['local']['modules'][:10])}")
        if len(cats["local"]["modules"]) > 10:
            print(f"  ... and {len(cats['local']['modules']) - 10} more")
