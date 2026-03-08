---
name: deep-debugging
description: Use when you need to deep-debug an issue by understanding the problem, investigating across codebase and environment, drilling into root cause, and producing an investigation report
---

# Deep Debugging

You are performing a deep, systematic investigation to find the root cause of a bug or unexpected behaviour. You spread wide first — gathering evidence from codebase, logs, database, and environment — then narrow in to a concrete root cause.

**Announce at start:** "I'm using the deep-debugging skill to investigate this issue."

The user's problem description or context is provided when this skill is invoked.

## Guiding Philosophy

- **Wide first, narrow second**: Cast a broad net across all possible evidence sources, then converge on the most likely cause
- **Evidence over hypothesis**: Never guess. Every claim must be backed by a log line, a code path, a query result, or a git diff
- **Parallel agents**: Spawn multiple investigation agents concurrently to maximise coverage and minimise time
- **No file editing**: This skill is pure investigation — you do not fix anything

---

## Phase 1: Understand the Problem

### Step 1: Read all provided context files

If the user mentions any files (ticket, plan, notes), read them **fully** — never use limit/offset.

### Step 2: Gather problem definition

Use `AskUserQuestion` to collect what you don't yet know. Ask only what is necessary — at minimum confirm:

1. **What is the expected behaviour?** What should have happened?
2. **What is the actual behaviour?** What happened instead? (error message, wrong output, silence)
3. **Which environment?** Local (Docker), staging, or production? *(default: local if not specified)*
4. **When did this start?** After a specific commit, deploy, or config change?
5. **Any context files?** Ticket number, plan path, or log excerpts to read first?

### Step 3: Quick git state check

Run these in parallel:

```bash
git branch --show-current
git log --oneline -10
git status --short
git diff --stat HEAD~1
```

Record: current branch, last 10 commits, any uncommitted changes, and what changed most recently.

### Step 4: Synthesise your understanding

Before spawning any agents, document your mental model:

- **Component(s) involved**: Which pipeline, function, service, or UI feature?
- **Expected vs actual**: Precise description
- **Hypothesis space**: What are the 3-5 most plausible causes? (code bug, bad data, config mismatch, environment issue, race condition, missing resource)
- **Environment target**: Local / staging / production — determines where to look

Use `TodoWrite` to create investigation tasks, one per hypothesis or evidence source.

---

## Phase 2: Wide Investigation (Parallel Agents)

Spawn agents concurrently based on the environment and symptom. The goal is to gather evidence from all likely sources simultaneously.

### Always spawn (regardless of environment)

**Agent A — Codebase location sweep** (`codebase-locator`):
> Find all files related to [component/feature]. Include: entry points, service files, activity files, models, config, and tests.

**Agent B — Code path trace** (`codebase-analyzer`):
> Trace the execution path for [specific operation that is failing]. Follow from the entry point through to where the failure would occur. Document all relevant file:line references.

**Agent C — Pattern comparison** (`codebase-pattern-finder`):
> Find examples of [the operation or pattern in question] working correctly elsewhere in the codebase. Show concrete code examples with file:line references.

---

### If environment is **local** (Docker)

**Agent D — Container logs and health** (`environment-debugger`):
> Investigate local Docker environment for [component]. Check: container health (`docker compose ps`), recent logs from `azure-functions` and `postgres` containers (last 200 lines), any crash loops or errors matching [symptom keywords].

**Agent E — Database state** (`environment-debugger`):
> Query the local PostgreSQL database (`ai_call_insight`) for state related to [component/job/record]. Check relevant tables for unexpected status values, missing rows, or anomalous timestamps. Include row counts.

**Agent F — Azurite / Durable Function state** (`environment-debugger`) *(only if ADAM job or Durable Function related)*:
> Inspect Azurite blob storage for task hub state related to [orchestrator/job ID]. List containers, check for stuck or failed orchestration instances.

---

### If environment is **staging** or **production**

Determine the correct values:

- Staging: app=`func-aiinsight-stg-1`, rg=`RG-AiPltfrm-AUE-AIInsight-STG`
- Production: app=`func-aiinsight-prd-1`, rg=`RG-AiPltfrm-AUE-AIInsight-PRD`

**Agent D — Azure Function logs** (`environment-debugger`):
> Query App Insights / Log Analytics for [function app name] in [resource group]. Find all errors, warnings, and exceptions in the last 2 hours related to [symptom]. Include exact log lines with timestamps.

**Agent E — Database state** (`environment-debugger`):
> Connect to the [staging/production] PostgreSQL database and query tables related to [component/job]. Check for unexpected statuses, missing records, or anomalous timestamps. Include row counts and recent entries.

**Agent F — Durable Function task hub** (`environment-debugger`) *(only if ADAM job or Durable Function related)*:
> Use `az storage` to inspect the Durable Function task hub in [storage account]. List orchestration instances, check for stuck PENDING/RUNNING instances, and trace any failed instances related to [job ID or time window].

**Agent G — Function app health** (`environment-debugger`):
> Check the health and recent deployment status of [function app name] using `az functionapp`. Report: running state, last modified time, any deployment errors.

---

### Wait for ALL agents to complete before proceeding

Synthesise findings:

- What evidence was found? List each piece with its source agent
- What came back clean / empty? (negative findings matter)
- Which hypothesis from Phase 1 now looks most likely?
- Is there one clear signal, or do we need to drill deeper?

---

## Phase 2.5: Drill Deep (Conditional — Do This When Evidence Points to a Specific Cause)

If Phase 2 produced a strong signal, validate it by cross-referencing codebase and environment evidence.

**Spawn targeted follow-up agents:**

**Agent — Code validation** (`codebase-analyzer`):
> Given this finding: [specific log line / error / stack trace from Phase 2], trace exactly which lines of code in [file:line] would produce this behaviour. Confirm or rule out [hypothesis].

**Agent — Targeted environment re-query** (`environment-debugger`):
> Re-query [specific log source / database table / task hub] with tighter filters: [specific job ID / timestamp range / error type]. Return the exact sequence of events leading up to [failure point].

Cross-reference:

- Does the code path match the log evidence?
- Does the database state confirm the code reached or did not reach a specific point?
- Is the error reproducible from the evidence, or is it intermittent?

---

## Phase 3: Write Investigation Report

Once you have sufficient evidence (or have exhausted the available signals), write the report.

### Report location

```
docs/investigation/YYYY-MM-DD-{slug}.md
```

Where `{slug}` is a 2-4 word kebab-case shorthand for the issue (e.g., `job-stuck-pending`, `transcript-parse-null`, `auth-token-expired`).

Get the date: `date '+%Y-%m-%d'`

Create the `docs/investigation/` directory if it does not exist.

### Report structure

```markdown
---
date: <YYYY-MM-DD HH:MM:SS TZ>
investigator: Claude (deep-debugging)
git_commit: <hash>
branch: <branch>
environment: <local | staging | production>
component: <component or feature investigated>
status: <root-cause-identified | inconclusive | hypothesis>
---

# Investigation Report: [Short Title]

## What's Wrong

[One clear, concrete statement of the observed issue based on evidence — not a hypothesis]

## Evidence Found

### From Logs
**Source**: [docker compose logs / App Insights / Log Analytics]
**Time window**: [e.g., last 2 hours]

- `[timestamp]` — `[exact error/warning line]`
- `[timestamp]` — `[related trace]`

### From Database
```sql
-- Query used
SELECT ...
```

**Finding**: [Factual statement about what the data shows]

### From Codebase

- `src/path/to/file.py:123` — [what this line does that is relevant]
- `src/path/to/other.py:456` — [relevant code behaviour]

### From Task Hub / Blob Storage

*(If applicable)*

- [Finding from orchestration state]

### From Git

- Recent commits touching relevant files:
  - `abc1234` — [commit message] — [why relevant]

## Root Cause

[Most likely explanation based on ALL evidence combined. Be precise: name the file, function, condition, or data state that is the proximate cause. Distinguish between confirmed root cause and strong hypothesis.]

**Confidence**: [High / Medium / Low — and why]

## Next Steps

1. **Immediate action**:

   ```bash
   [Specific command or code change to try first]
   ```

2. **If that doesn't resolve it**:
   - [Alternative action]
   - [Service to restart / config to check]

3. **To verify the fix**:
   - [How to confirm the issue is resolved]

## Out of Reach

The following could not be investigated from this context:

- [Browser console errors — check F12 in browser]
- [Internal MCP state / external service internals]
- [Anything requiring human access or UI interaction]

---
*Would you like me to drill deeper into any specific area?*

```

---

## After Writing the Report

1. Present a concise summary to the user — 3-5 bullet points of the key findings
2. State the root cause (or top hypothesis if inconclusive) explicitly
3. Point the user to the report file path
4. Ask if they want to investigate any area further

---

## Important Notes

- **Always read mentioned files fully** — no limit/offset
- **Parallel agents are non-negotiable** — never investigate sequentially when agents can run concurrently
- **Negative findings matter** — "logs were clean" or "table had expected values" rules out hypotheses
- **Quote evidence verbatim** — never paraphrase error messages or log lines
- **No code editing** — this skill investigates only; implementation happens using the implementing-plans skill
- **Environment default is local** — if the user does not specify, assume Docker
- **Phase 2.5 is conditional** — only run drill-down if Phase 2 produced a clear signal worth validating
