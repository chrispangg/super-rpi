# Super RPI

**Super RPI** combines the best of [HumanLayer's RPI framework](https://github.com/humanlayer/humanlayer) with [Obra's Superpowers](https://github.com/obra/superpowers) to create a powerful, flexible, and opinionated framework for AI coding agents.

---

## What is RPI?

The **RPI framework** (from [HumanLayer](https://github.com/humanlayer/humanlayer)) stands for **Research → Plan → Implement**. It's a battle-tested methodology that enables AI agents to solve hard problems in complex codebases by:

- Using **sub-agents as compression functions** to reduce context bloating on the main agent
- Breaking complex tasks into manageable, verifiable steps
- Leveraging specialized agents for specific tasks (codebase analysis, file location, pattern finding)

---

## What are Superpowers?

[Obra's Superpowers](https://github.com/obra/superpowers) is a complete software development methodology built on composable **skills** - self-contained, reusable instructions that trigger automatically when needed. Key principles include:

- **Simplicity** - Just three core commands
- **Flexible system** - Heavy use of skills makes the system adaptable
- **Self-configuration** - Agents can configure themselves
- **Test-Driven Development** - RED-GREEN-REFACTOR cycle
- **Systematic over ad-hoc** - Process over guessing

---

## Why Super RPI?

This project was created to bridge the gap between these two excellent frameworks, giving you:

### 1. From HumanLayer's RPI Framework

- **Sub-agent compression** - Reduce context window bloat by delegating to specialized sub-agents
- **Battle-tested agents** - Three hand-crafted, proven sub-agents:
  - `codebase-analyzer` - Deep analysis of code implementation details
  - `codebase-locator` - Fast file and component discovery
  - `codebase-pattern-finder` - Identifies patterns and idioms across codebases

### 2. From Obra's Superpowers

- **Skill-based architecture** - Modular, reusable, composable instructions
- **Automatic skill invocation** - Skills trigger when relevant, no manual intervention
- **Self-configuring** - Leverages agent capabilities for setup and configuration
- **Multi-platform support** - Works across Claude Code, OpenCode, Cursor, and Codex

### 3. Opinionated Tools

- **grep** - Searchable code index over GitHub codebases for looking up library usage examples
- **deepwiki** - AI-written documentation lookup for understanding libraries internally
- **agent-browser** - Agent-native browser for web research and information gathering

---

## Philosophy

Super RPI follows these core principles:

1. **Context Engineering** - Keep the main agent's context lean by using sub-agents
2. **Systematic Workflows** - Follow defined processes (Research → Plan → Implement → Validate)
3. **Evidence Over Claims** - Verify before declaring success
4. **Test-Driven Development** - Write tests first, always
5. **Complexity Reduction** - Simplicity as the primary goal

---

## Installation Guide

Choose your AI coding platform and follow the instructions:

### Claude Code

Tell Claude:

```markdown
Fetch and follow instructions from https://raw.githubusercontent.com/chrispangg/super-rpi/refs/heads/main/.claude/INSTALL.md
```

### OpenCode

Tell OpenCode:

```markdown
Fetch and follow instructions from https://raw.githubusercontent.com/chrispangg/super-rpi/refs/heads/main/.opencode/INSTALL.md
```

### Cursor

Tell Cursor:

```markdown
Fetch and follow instructions from https://raw.githubusercontent.com/chrispangg/super-rpi/refs/heads/main/.cursor/INSTALL.md
```

### Codex

Tell Codex:

```markdown
Fetch and follow instructions from https://raw.githubusercontent.com/chrispangg/super-rpi/refs/heads/main/.codex/INSTALL.md
```

---

## The Agents

### Core Sub-Agents

| Agent | Purpose | Mode | Tools |
|-------|---------|------|-------|
| `codebase-analyzer` | Deep code analysis and implementation details | Read-only | No write/edit/bash |
| `codebase-locator` | Fast file and component discovery | Read-only | No write/edit/bash |
| `codebase-pattern-finder` | Find patterns and idioms in code | Read-only | No write/edit/bash |

### Research Sub-Agents

| Agent | Purpose | Mode | Tools |
|-------|---------|------|-------|
| `codebase-research-locator` | Research and locate code with bash access | Read-only | Bash enabled |
| `codebase-research-analyzer` | Research and analyze code with bash access | Read-only | Bash enabled |
| `web-search-researcher` | Web research and information gathering | Read-only | No bash |

---

## How to Use (The Basic Workflow)

Super RPI provides slash commands that automate the **Research → Plan → Implement** workflow. Simply run the commands and the framework handles the agents, skills, and orchestration.

### The RPI Workflow Commands

Run these commands in sequence to follow the full RPI methodology:

#### 1. Research the Codebase

```
/1_research-codebase <your research question>
```

Documents the codebase as-is and creates research artifacts for historical context.

**Example:**

```
/1_research-codebase Find all authentication-related files and understand how JWT tokens are validated
```

#### 2. Create a Plan

```
/2_create-plan
```

Interactively creates a detailed implementation plan through an iterative process with you.

#### 3. Define Test Cases

```
/3_define-test-cases
```

Generates comprehensive test cases based on the approved plan.

#### 4. Implement the Plan

```
/4_implement-plan
```

Executes the approved plan from `docs/tickets/TICKET-NAME/plan.md` using sub-agent-driven development.

#### 5. Validate Implementation

```
/5_validate-implementation
```

Verifies the implementation against test cases and acceptance criteria.

#### 6. Iterate (if needed)

```
/6_iterate-implementation
```

Refines the implementation based on validation feedback.

---

### Quick Start: One-Shot RPI

For smaller tasks, run the entire RPI workflow in one command:

```
/oneshot_rpi <ticket-number>
```

This runs all 6 steps automatically: research → plan → test cases → implement → validate → iterate.

---

### Additional Commands

#### Deep Debug

```
/deep_debug <problem description>
```

Systematic debugging for complex issues. Follows a 4-phase root cause analysis process.

#### Research Cloud

```
/research_cloud <query>
```

Performs external research using cloud-based tools and web search.

---

### Example Session

```
You: /1_research-codebase How does user authentication work in this codebase?

Agent: [Runs research, analyzes files, creates docs/tickets/.../research.md]

You: /2_create-plan

Agent: [Interactively designs solution with you, creates plan.md]

You: /4_implement-plan

Agent: [Executes plan using sub-agents, handles all implementation]

You: /5_validate-implementation

Agent: [Verifies everything works, runs tests]
```

That's it! The slash commands handle all the complexity - agent invocation, skill selection, and workflow orchestration.

---

## References

- [HumanLayer RPI Framework](https://github.com/humanlayer/humanlayer) - The original RPI framework
- [Obra's Superpowers](https://github.com/obra/superpowers) - Skill-based agent framework
- [12-Factor Agents](https://github.com/humanlayer/humanlayer) - Principles for reliable LLM applications
- [Advanced Context Engineering](https://humanlayer.dev) - Talk on solving hard problems with AI

---

## License

MIT License - See LICENSE file for details
