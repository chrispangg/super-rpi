---
name: documentation-writer
description: This skill analyzes code, generates documentation, and applies best practices to create comprehensive project documentation. Should be used when creating or improving README files, API documentation, architecture documentation, code docstrings, and user guides. Supports Python, TypeScript/JavaScript, and Next.js projects through analysis scripts and templates.
---

# Documentation Writer

## Overview

The Documentation Writer skill transforms code into well-structured, user-friendly documentation. It analyzes code, generates docstring templates, validates existing documentation quality, and provides templates for all major documentation types.

This skill is designed to help create and maintain documentation for:
- **Project README files** - Project overviews, setup, and usage
- **API Documentation** - Endpoint reference, data types, and examples
- **Architecture Documentation** - System design and component interactions
- **Code Documentation** - Function/class docstrings and inline comments
- **User Guides** - End-user tutorials and how-to guides

## When to Use This Skill

Trigger this skill with requests like:
- "Document this Python module"
- "Create a README for my project"
- "Generate API documentation for these endpoints"
- "Analyze docstring compliance in my codebase"
- "Write a user guide for this feature"
- "Check documentation coverage across my project"
- "Improve the documentation in this code"

## Quick Start

### Basic Documentation Workflow

1. **Analyze your code** to understand structure and identify documentation gaps
2. **Choose appropriate template** for your documentation type
3. **Apply documentation principles** from best practices reference
4. **Generate or write content** following the template structure
5. **Validate quality** using validation scripts

### Example: Document a Python Module

```bash
# Step 1: Analyze the module structure
python scripts/analyze_module.py src/services/user_service.py --json

# Step 2: Find undocumented functions
python scripts/find_undocumented.py src/services/user_service.py --json

# Step 3: Check docstring compliance
python scripts/validate_docstrings.py src/services/user_service.py --style google

# Step 4: Generate docstring templates
python scripts/generate_function_docs.py src/services/user_service.py --format google
```

## Core Capabilities

### 1. Code Analysis Scripts

These scripts extract structured information from your codebase:

#### `analyze_module.py`
Extracts all functions, classes, their signatures, and type hints from a Python file.

```bash
python scripts/analyze_module.py <file_path> [--json]
```

**Output includes:** Functions, classes, methods, parameters, return types, imports, and module docstring.

**Use when:** You need to understand the structure of a module before documenting it.

#### `find_undocumented.py`
Identifies functions and classes that lack docstrings or have incomplete documentation.

```bash
python scripts/find_undocumented.py <file_path> [--json]
```

**Output includes:** Coverage percentage, undocumented items, and what's missing.

**Use when:** You need to prioritize which items to document first.

#### `extract_dependencies.py`
Maps imports and module relationships to understand architecture.

```bash
python scripts/extract_dependencies.py <file_path> [--json]
```

**Output includes:** Standard library, third-party, and local imports organized by category.

**Use when:** Documenting architecture or understanding module relationships.

### 2. Documentation Generation Scripts

These scripts create templates and documentation structure:

#### `generate_function_docs.py`
Creates docstring templates with type information pre-filled in multiple styles.

```bash
python scripts/generate_function_docs.py <file_path> --format google|numpy|sphinx
```

**Docstring Styles:**
- **Google** - Most popular, readable (recommended)
- **NumPy** - Scientific computing standard
- **Sphinx** - For Sphinx documentation generation

**Use when:** You want templates to fill in for each function.

#### `generate_toc.py`
Builds a table of contents from markdown headers.

```bash
python scripts/generate_toc.py <file_path> --format markdown|html
```

**Use when:** Creating or updating markdown documentation files.

### 3. Validation Scripts

These scripts ensure documentation quality and consistency:

#### `validate_docstrings.py`
Checks docstring compliance with chosen style (PEP 257, Google, or NumPy).

```bash
python scripts/validate_docstrings.py <file_path> --style google|numpy|pep257
```

**Output includes:** Compliance percentage, issues found, and recommendations.

**Use when:** You want to ensure docstrings follow your project's standards.

#### `check_doc_coverage.py`
Reports documentation coverage percentage across a file or directory.

```bash
python scripts/check_doc_coverage.py <file_or_directory> --threshold 80
```

**Output includes:** Coverage percentage, undocumented items, and coverage by file.

**Use when:** You want to track documentation completeness over time.

#### `validate_markdown.py`
Validates markdown formatting, checks for broken links, and header hierarchy.

```bash
python scripts/validate_markdown.py <file_path> --check-links
```

**Output includes:** Formatting issues, header structure problems, and link status.

**Use when:** You're finalizing markdown documentation files.

### 4. Documentation Section Update

#### `update_readme_sections.py`
Updates specific sections in README files without manual editing.

```bash
# Update a section
python scripts/update_readme_sections.py README.md --section "Installation" --content "new content"

# Extract a section
python scripts/update_readme_sections.py README.md --section "Installation" --extract

# List all sections
python scripts/update_readme_sections.py README.md --list
```

**Use when:** You want to programmatically update specific README sections.

## Documentation Templates

Choose the appropriate template based on your documentation need:

### README Template
**File:** `assets/templates/README-template.md`

Use for project overview, installation, usage, and getting started guides. Includes:
- Quick start section
- Features overview
- Installation instructions
- Usage examples
- API reference overview
- Troubleshooting section
- Contributing guidelines

**When to use:** Creating documentation for any project

### API Documentation Template
**File:** `assets/templates/API-docs-template.md`

Use for REST API, GraphQL, or SDK documentation. Includes:
- Authentication methods
- Error handling and codes
- Comprehensive endpoint reference
- Data type definitions
- Examples for each endpoint
- Rate limiting information
- Webhook documentation

**When to use:** Documenting APIs and endpoints

### Architecture Documentation Template
**File:** `assets/templates/architecture-template.md`

Use for system design, component overview, and technical architecture. Includes:
- System component descriptions
- Architecture diagrams
- Data flow diagrams
- Technology stack table
- Deployment architecture
- Scalability considerations
- Security architecture

**When to use:** Documenting system design and infrastructure

### User Guide Template
**File:** `assets/templates/user-guide-template.md`

Use for end-user documentation and tutorials. Includes:
- Getting started sections
- Step-by-step instructions
- Feature explanations
- Troubleshooting guide
- FAQ section
- Tips and tricks
- Keyboard shortcuts

**When to use:** Creating documentation for end users

## Reference Materials

### Documentation Principles
**File:** `references/documentation-principles.md`

Core principles for writing good documentation:
- Making docs easy to skim
- Writing techniques for clarity
- Being broadly helpful
- When to break the rules

**Use when:** You need guidance on writing quality documentation

### Python Docstring Conventions
**File:** `references/python-docstring-conventions.md`

Standards for Python docstrings:
- PEP 257 (official standard)
- Google style
- NumPy style
- Type hint conventions

**Use when:** Writing or reviewing Python docstrings

### Next.js/TypeScript Conventions
**File:** `references/nextjs-typescript-conventions.md`

Documentation conventions for TypeScript and Next.js:
- JSDoc comments
- Server/Client components
- API routes
- Server actions
- Custom hooks
- Type documentation

**Use when:** Documenting Next.js and TypeScript code

## Typical Documentation Workflows

### Workflow 1: Complete Project Documentation

1. Use `analyze_module.py` to understand project structure
2. Check coverage with `check_doc_coverage.py`
3. Generate README using template
4. Generate API docs using template
5. Use `generate_function_docs.py` to create docstring templates
6. Fill in docstrings in code
7. Validate with `validate_docstrings.py`
8. Generate architecture documentation
9. Validate markdown with `validate_markdown.py`

### Workflow 2: Improve Existing Documentation

1. Run `find_undocumented.py` to identify gaps
2. Generate templates with `generate_function_docs.py`
3. Add missing docstrings to code
4. Validate with `validate_docstrings.py`
5. Check coverage with `check_doc_coverage.py`
6. Update README sections with `update_readme_sections.py`

### Workflow 3: API Documentation

1. Analyze API structure with `analyze_module.py`
2. Use API documentation template
3. Document each endpoint following the template structure
4. Include examples for each endpoint
5. Document data types and error codes
6. Validate markdown documentation

### Workflow 4: Create Architecture Docs

1. Map dependencies with `extract_dependencies.py`
2. Use architecture template
3. Document components and their relationships
4. Add data flow descriptions
5. Include deployment architecture
6. Validate with `validate_markdown.py`

## Best Practices

### ✓ DO

- Run analysis scripts first to understand structure
- Use templates as starting points, customize as needed
- Apply documentation principles consistently
- Include code examples in documentation
- Keep documentation close to code
- Validate documentation regularly

### ✗ DON'T

- Write vague or incomplete docstrings
- Document obvious parameters
- Ignore documentation gaps
- Leave TODOs in production documentation
- Mix documentation styles inconsistently
- Skip examples for complex features

## Examples

### Example 1: Document a Python Function

```bash
# Analyze the module
python scripts/analyze_module.py mymodule.py

# Generate Google-style docstring template
python scripts/generate_function_docs.py mymodule.py --format google

# Output shows:
# Function: calculate_revenue(units: int, price: float) -> float
# Template:
# """Brief description of the function.
#
# Args:
#     units (int): Description of units
#     price (float): Description of price
#
# Returns:
#     float: Description of return value
# """
```

### Example 2: Check Documentation Coverage

```bash
python check_doc_coverage.py src/ --threshold 80

# Output:
# Directory: src/
# Files Analyzed: 24 / 24
# Overall Coverage: 75.5%
# Documented Items: 185 / 245
#
# ⚠️  Coverage below threshold of 80%!
```

### Example 3: Validate Documentation

```bash
python validate_docstrings.py mymodule.py --style google

# Output:
# File: mymodule.py
# Style: google
# Compliance: 80.0% (8/10)
#
# Issues Found (2):
#   FUNCTION: calculate_revenue (line 15)
#     ✗ Missing Args section
#     → Add Args: section with parameter descriptions
```

## Troubleshooting

### Scripts showing errors

**Check Python version:** Scripts require Python 3.8+
```bash
python --version
```

**Check file permissions:** Ensure Python files are readable
```bash
ls -la scripts/
```

### Generated docstrings aren't quite right

This is normal. Templates provide structure - you'll fill in specific descriptions.

### Documentation coverage shows 0%

Likely means no docstrings exist. Use `generate_function_docs.py` to create templates, then add the actual docstrings to your code.

### Template sections aren't applicable to my project

Don't use sections that don't apply. Templates are guidelines, not requirements. Adapt based on your project needs.

## Integration with Your Project

### Setting up scripts

1. Copy scripts to your project tools directory (or keep in this skill)
2. Make scripts executable: `chmod +x scripts/*.py`
3. Run scripts from project root directory

### Using in CI/CD

Add documentation checks to your CI pipeline:

```bash
# Check docstring compliance
python scripts/validate_docstrings.py src/ --style google

# Check documentation coverage
python scripts/check_doc_coverage.py src/ --threshold 80

# Validate markdown files
python scripts/validate_markdown.py docs/*.md --check-links
```

### Automating template selection

1. Use analysis script to understand project type
2. Choose appropriate template
3. Customize template for your use case
4. Add to CI/CD for validation

## For More Information

- **Documentation Principles**: See `references/documentation-principles.md`
- **Python Standards**: See `references/python-docstring-conventions.md`
- **TypeScript Standards**: See `references/nextjs-typescript-conventions.md`
- **Templates**: See `assets/templates/`

---

This skill provides automated analysis and validation, but remember: **good documentation is ultimately about empathy for your readers**. Write with your users in mind.
