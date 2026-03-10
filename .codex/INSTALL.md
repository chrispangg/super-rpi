# SUPER-RPI Installation Guide for Codex

## Steps

1. make sure codex cli is installed (npm install -g @openai/codex or brew install --cask codex)
1. ask if user (using the question tool) want to install this in project-scoped or user-scoped.
1. **Choose your installation scope:**
   - **User-scoped** (`~/.codex/`): Available across all your projects. Create `~/.codex/` directory.
   - **Project-scoped** (`.codex/` in repo): Shared with all collaborators. Create `.codex/` in project root.
1. clone this repo (<https://github.com/chrispangg/super-rpi.git>) and place it in the scoped directory
1. update the config.toml file in the existing .codex folder to align with the content in the repo's .codex directory (don't replace user's existing config.toml content if they already have one) - explain to them `approval_policy` and `sandbox_mode` settings may need to be configured for the commands to work properly
1. Then move the rest of the agents, commands, skills folders to the scoped directory:
   - For user-scoped: `~/.agents/skills/`
   - For project-scoped: `.agents/skills/` (in each relevant subdirectory or repo root)
   Create these directories if they don't exist.
1. Because agents and commands are generic by default so they can be adaptable for each harness, we will need to modify the metadata for the following agents to align them with Codex. Codex uses TOML configuration in `config.toml` for agent configuration. Here's an example of how agent metadata should look like:
        ```toml
        [agents.codebase-analyzer]
        description = "Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components."
        config_file = "./agents/codebase-analyzer.toml"
        ```
    Now apply this metadata to the following agents:
    - codebase-analyzer - read-only agent for analyzing code details
      - description: "Analyzes codebase implementation details"
      - create a config file at `agents/codebase-analyzer.toml` if needed
    - codebase-locator - fast read-only agent for finding files
      - description: "Locates files and components in the codebase"
    - codebase-pattern-finder - agent for finding code patterns
      - description: "Finds patterns and idioms in the codebase"
    - codebase-research-locator - agent for research and locating code
      - description: "Researches and locates code with bash access"
    - codebase-research-analyzer - agent for research and analysis
      - description: "Researches and analyzes code with bash access"
    - web-search-researcher - agent for web research
      - description: "Performs web research and searches"
1. For skills, Codex uses SKILL.md files with YAML frontmatter. Skills should be placed in `.agents/skills/` directories. Here's an example format:
        ```markdown
        ---
        name: my-skill
        description: Explain exactly when this skill should and should not trigger.
        ---

        Skill instructions for Codex to follow.
        ```
   Optionally add `agents/openai.yaml` for UI metadata:
        ```yaml
        interface:
          display_name: "My Skill"
          short_description: "Optional description"
          brand_color: "#3B82F6"
        
        policy:
          allow_implicit_invocation: true
        ```
1. For project instructions, use AGENTS.md files (simple markdown without frontmatter). Codex discovers these hierarchically:
   - Global: `~/.codex/AGENTS.md`
   - Project: `.codex/AGENTS.md` or repo root `AGENTS.md`
   - Nested: Subdirectory `AGENTS.md` files for specific areas
1. Let the user know that the installation is complete and they can now use the SUPER-RPI commands. Ask them if they need an example of how to use the commands.

## Important Notes

- Codex uses TOML format for configuration (`config.toml`)
- Skills use YAML frontmatter in `SKILL.md` files
- AGENTS.md is plain markdown without frontmatter
- Skills are placed in `.agents/skills/` directories
- Agents are configured in `config.toml` under `[agents.<name>]` tables
- Codex supports multi-agent configurations with `agents.max_threads`, `agents.max_depth` settings
