# SUPER-RPI Installation Guide

## Steps

1. make sure claude code cli is installed
2. ask if user want to install this in local-scoped, project-scoped or user-scoped.
3. <<instructions for each scope>>
4. clone this repo and place it in the scoped directory
5. update the settings.json file in the existing .claude folder to align with the content in the repo's .claude directory(don't replace user's existing settings.json content if they already have a settings.json file) - explain to them `bypassPermissions` is required for the commands to work properly
6. Then move the rest of the agents, commands, skills folders to the scoped .claude directory
7. Because agents and commands are generic by default so they can be adaptable for each harness, we will need to modify the metadata for the following agents to align them with claude code. Here's an example of how metadata should look like:
        ```markdown
        ---
        name: codebase-analyzer
        description: Analyzes codebase implementation details. Call the codebase-analyzer agent when you need to find detailed information about specific components. As always, the more detailed your request prompt, the better! :)
        tools: Read, Grep, Glob, LS
        model: sonnet
        color: orange
        ```
    Now apply this metadata to the following agents:
    - codebase-analyzer - add tools: Read, Grep, Glob, LS, model: sonnet
    - codebase-locator - add tools: Grep, Glob, LS, model: haiku, color: orange
    - codebase-pattern-finder - add tools: Grep, Glob, Read, LS, model: sonnet, color: red
    - codebase-research-locator - add tools: Read, Grep, Glob, LS, Bash, model: haiku, color: green
    - codebase-research-analyzer - add tools: Read, Grep, Glob, LS, Bash, model: haiku, color: blue
    - web-search-researcher - add tools: WebSearch, WebFetch, TodoWrite, Read, Grep, Glob, LS, Skill(deepwiki), Skill(grep), Skill(agent-browser), model: sonnet, color: yellow
