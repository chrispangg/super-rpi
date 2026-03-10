# Super RPI

Inspiration from Humanlayers's RPI framework + Obra's Superpowers.

Why did I create this?

1. The best elemets from Humanlayers' RPI framework:
    - Using sub-agents as compression functions to reduce context bloating on the main agent.
    - Three hand crafted sub-agents that are battle tested and work well. i.e. codebase-analyzer, codebase-locator, codebase-pattern-finder.
2. The best elements from Obra's Superpowers:
    - Simplicity - just three commands
    - Flexible system - heavy use of skills to make the system flexible and adaptable. i.e. agents can invoke skills outside of commands
    - Self-configuration - leverage agents to self configure
3. Opiniated tools for your agents:
    - grep - searchable code index over github codebases - great for looking up examples of code usage for opensource libraries.
    - deepwiki - look up AI written documentation for opensource libraries. Great for understanding how a library works internally and how to use it.
    - agent-browser - agent-native browser to browse the web and search for information

## Installation Guide

### Claude Code

Tell Claude:

```markdown
Fetch and follow instructions from https://raw.githubusercontent.com/chrispangg/super-rpi/refs/heads/main/.claude/INSTALL.md
```
