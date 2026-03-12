# SUPER-RPI Installation Guide for OpenCode

## Steps

1. make sure opencode cli is installed
1. ask if user (using the question tool) want to install this in project-scoped or user-scoped.
1. **Choose your installation scope:**
   - **User-scoped** (`~/.config/opencode/`): Available across all your projects. Create `~/.config/opencode/` directory.
   - **Project-scoped** (`.opencode/` in repo): Shared with all collaborators. Create `.opencode/` in project root.
1. clone this repo (<https://github.com/chrispangg/super-rpi.git>) and place it in the scoped directory
1. update the opencode.json file in the existing .opencode folder to align with the content in the repo's .opencode directory (don't replace user's existing opencode.json content if they already have one) - explain to them `permission` settings may need to be configured for the commands to work properly
1. Then move the rest of the agents, commands, skills folders to the scoped directory:
   - For user-scoped: `~/.config/opencode/agents/`, `~/.config/opencode/commands/`, `~/.config/opencode/skills/`
   - For project-scoped: `.opencode/agents/`, `.opencode/commands/`, `.opencode/skills/`
   Create these directories if they don't exist.
1. Because agents and commands are generic by default so they can be adaptable for each harness, we will need to modify the metadata for the following agents to align them with opencode. OpenCode uses YAML frontmatter in markdown files for agent configuration. Here's an example of how metadata should look like:
        ```markdown
        ---
        description: Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components. As always, the more detailed your request prompt, the better!
        mode: subagent
        model: kimi-k2.5
        tools:
          write: false
          edit: false
          bash: false
        color: orange
        ---
        ```
    Now apply this metadata to the following agents:
    - codebase-analyzer - read-only agent for analyzing code details
      - mode: subagent
      - tools: write: false, edit: false, bash: false
      - color: orange
      - model: kimi-k2.5
    - codebase-locator - fast read-only agent for finding files
      - mode: subagent
      - tools: write: false, edit: false, bash: false
      - color: orange
      - model: kimi-k2.5
    - codebase-pattern-finder - agent for finding code patterns
      - mode: subagent
      - tools: write: false, edit: false, bash: false
      - color: red
      - model: kimi-k2.5
    - codebase-research-locator - agent for research and locating code
      - mode: subagent
      - tools: write: false, edit: false, bash: true
      - color: green
      - model: kimi-k2.5
    - codebase-research-analyzer - agent for research and analysis
      - mode: subagent
      - tools: write: false, edit: false, bash: true
      - color: blue
      - model: kimi-k2.5
    - web-search-researcher - agent for web research
      - mode: subagent
      - tools: write: false, edit: false, bash: false
      - color: yellow
      - model: kimi-k2.5
1. For commands, OpenCode also uses YAML frontmatter in markdown files. The metadata format should look like:
        ```markdown
        ---
        description: Description of what the command does
        agent: build
        model: kimi-k2.5
        ---
        ```
   The content after the frontmatter becomes the command template/prompt. Commands are placed in the `commands/` directory.
1. Let the user know that the installation is complete and they can now use the SUPER-RPI commands. Ask them if they need an example of how to use the commands.
