# Agent Rules

## Roles

- Claude Code acts as prompt engineer and planner.
- Codex acts as developer and reviewer.
- The user is the controller and final approver.

## Development Rules

- Read this file before making changes.
- Keep changes scoped to the approved task.
- Do not revert user changes unless explicitly requested.
- Inspect project scripts before choosing test/build commands.
- Report verification results clearly.

## Handoff

Tasks live in .ai/tasks/.
Codex run logs live in .ai/codex-runs/.
Reviews live in .ai/reviews/.
