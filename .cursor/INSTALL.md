# SUPER-RPI Installation Guide for Cursor

## Steps

1. make sure Cursor IDE is installed (download from <https://cursor.com>)
1. ask if user (using the question tool) want to install this in project-scoped or user-scoped.
1. **Choose your installation scope:**
   - **User-scoped**: Rules are stored in Cursor Settings and apply globally
   - **Project-scoped** (`.cursor/rules/` in repo): Shared with all collaborators. Create `.cursor/rules/` in project root.
1. clone this repo (<https://github.com/chrispangg/super-rpi.git>) and place it in the scoped directory
1. For project-scoped installation, create the `.cursor/rules/` directory structure in the project root
1. Then move the agents/rules to the appropriate locations:
   - For project-scoped: `.cursor/rules/` directory
   - For user-scoped: Import rules via Cursor Settings → Rules, Commands
1. Because agents and commands are generic by default so they can be adaptable for each harness, we will need to modify the metadata for the following agents to align them with Cursor. Cursor uses Rules which are markdown files with YAML frontmatter. Here's an example of how metadata should look like:
        ```markdown
        ---
        description: Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components.
        globs:
        alwaysApply: false
        ---

        Your rule content here...
        ```
    Now apply this metadata to the following agents:
    - codebase-analyzer - read-only agent for analyzing code details
      - name: codebase-analyzer
      - description: "Analyzes codebase implementation details"
      - alwaysApply: false (or true if you want it always applied)
      - Rule type: Apply Intelligently (based on description) or Apply Manually
      - model: composer-1.5
      - readonly: true
    - codebase-locator - fast read-only agent for finding files
      - name: codebase-locator
      - description: "Locates files and components in the codebase"
      - globs: [] (optional file patterns)
      - model: composer-1.5
      - readonly: true
    - codebase-pattern-finder - agent for finding code patterns
      - name: codebase-pattern-finder
      - description: "Finds patterns and idioms in the codebase"
      - model: composer-1.5
      - readonly: true
    - codebase-research-locator - agent for research and locating code
      - name: codebase-research-locator
      - description: "Researches and locates code"
      - model: composer-1.5
      - readonly: true
    - codebase-research-analyzer - agent for research and analysis
      - name: codebase-research-analyzer
      - description: "Researches and analyzes code"
      - model: composer-1.5
      - readonly: true
    - web-search-researcher - agent for web research
      - name: web-search-researcher
      - description: "Performs web research and searches"
      - model: composer-1.5
      - readonly: true
1. Rule Types in Cursor:
   - **Always Apply**: Apply to every chat session (set `alwaysApply: true`)
   - **Apply Intelligently**: When Agent decides it's relevant based on description
   - **Apply to Specific Files**: When file matches a specified pattern (use `globs`)
   - **Apply Manually**: When @-mentioned in chat (e.g., `@codebase-analyzer`)

   Configure the appropriate type for each agent based on its purpose.

1. For simple agent instructions, you can also use AGENTS.md files as an alternative to `.cursor/rules/`:
   - Place `AGENTS.md` in project root or subdirectories
   - Uses plain markdown without frontmatter
   - Nested AGENTS.md files in subdirectories are automatically applied
   - Example:

        ```markdown
        # Project Instructions

        ## Code Style
        - Use TypeScript for all new files
        - Prefer functional components
        ```

1. Let the user know that the installation is complete and they can now use the SUPER-RPI commands. Ask them if they need an example of how to use the commands.

## Important Notes

- Cursor uses markdown files with YAML frontmatter for Rules
- File extensions can be `.md` or `.mdc` (`.mdc` is preferred for rules with frontmatter)
- Rules are stored in `.cursor/rules/` directory (project-scoped)
- Rules can reference files using `@filename.ts` syntax
- Use `/create-rule` in chat to have the agent create rules automatically
- Rules do NOT impact Cursor Tab or Inline Edit (Cmd/Ctrl+K), only Agent (Chat)
- Team Rules (Team/Enterprise plans) take precedence over Project Rules

## Rule Precedence

Rules are applied in this order: **Team Rules → Project Rules → User Rules**
All applicable rules are merged; earlier sources take precedence when guidance conflicts.
