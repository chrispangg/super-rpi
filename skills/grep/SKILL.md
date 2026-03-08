---
name: grep
description: Skills for searching code across millions of public GitHub repositories using Grep's MCP server
---

# Grep MCP

The Grep MCP server provides programmatic access to search code across millions of public GitHub repositories using grep.app's infrastructure.

**MCP Server URL**: <https://mcp.grep.app>

## Usage

Use the `--http-url` flag to call directly without saving configuration:

```bash
bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"useState(" language:='["TypeScript"]'
```

## Search Code

Search for code patterns across public GitHub repositories with filtering by language, repository, and file path.

- `bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"search pattern"`
- e.g. `bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"useState("`
- e.g. with language filter: `bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"async function" language:='["TypeScript"]'`
- e.g. with multiple languages: `language:='["TypeScript","TSX"]'`
- e.g. with regexp: `useRegexp:=true`
- e.g. with repo filter: `repo="vercel/ai"`
- e.g. with path filter: `path="components/"`

## Schema

```typescript
/**
 * Find real-world code examples from over a million public GitHub repositories
 * 
 * @param query The literal code pattern to search for (e.g., 'useState(', 'export function')
 * @param matchCase Whether the search should be case sensitive (default: false)
 * @param matchWholeWords Whether to match whole words only (default: false)
 * @param useRegexp Whether to interpret the query as a regular expression (default: false)
 * @param repo Filter by repository (e.g., 'facebook/react', 'vercel/ai')
 * @param path Filter by file path (e.g., 'src/components/', 'README.md')
 * @param language Filter by programming language as array (e.g., ['TypeScript', 'TSX'])
 */
function searchGitHub(
  query: string,
  matchCase?: boolean,
  matchWholeWords?: boolean,
  useRegexp?: boolean,
  repo?: string,
  path?: string,
  language?: string[]
): object;
```

## Response Format

Search results include:

- **Repository**: The GitHub repository containing the match
- **Path**: File path within the repository
- **URL**: Direct link to the file on GitHub
- **License**: License information for the repository
- **Snippets**: Code snippets showing the matched content with line numbers

## Important Notes

- **Search for code patterns, not keywords**: This tool searches for literal code patterns (like grep), not keywords or questions
  - ✅ Good: `'useState(', 'import React from', 'async function', '(?s)try {.*await'`
  - ❌ Bad: `'react tutorial', 'best practices', 'how to use'`
- **Language parameter is an array**: Use `language:='["TypeScript","TSX"]'` format
- **Use regexp for flexible patterns**: Prefix with `(?s)` to match across multiple lines

## Example Use Cases

1. **Find React useState patterns**:

   ```bash
   bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"useState(" language:='["TypeScript","TSX"]'
   ```

2. **Search for error handling in MCP servers**:

   ```bash
   bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"isError: true" language:='["TypeScript","JavaScript"]'
   ```

3. **Find specific function implementations**:

   ```bash
   bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"async function handle" useRegexp:=true language:='["TypeScript"]'
   ```

4. **Search within specific repository**:

   ```bash
   bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"MCPClient" repo="vercel/ai"
   ```

5. **Find useEffect hook usage**:

   ```bash
   bunx -y mcporter call --http-url https://mcp.grep.app searchGitHub query:"useEffect(()" language:='["TypeScript","TSX"]'
   ```
