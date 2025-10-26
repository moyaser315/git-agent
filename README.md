# Git AI Agent

## Project Description

This project is an experimental, terminal-based AI Agent built in Python. Its primary goal is to demonstrate Function Calling (Tool Use) capabilities in a practical, real-world development scenario.

The agent is designed to manage complex Git workflows, with a specific and advanced focus on automatic conflict detection and resolution during branch merging. By exposing Git commands as discrete functions, we allow the LLM to autonomously determine the necessary steps to fulfill user requests, from simple commits to complex merge conflict fixes.

## Core Goals

- Function Chaining: Enable the LLM to execute a sequence of functions to complete multi-step tasks (e.g., checkout -> merge -> commit).

- Conflict Detection: Accurately identify when a git merge operation results in a conflict.

- LLM-Driven Resolution: Use the LLM's reasoning ability to read conflicted file content (with markers), generate the resolved code, and apply the fix.

- State Management: Leverage functions to read the repository's current status (git status, git diff) and provide this context back to the LLM for informed decision-making.

## To-Do List

The project is structured into three phases

### Phase 1: Context and Saving Changes **DONE**

Focus: Environment setup and non-destructive state retrieval.

- [x] Setup Environment
- [x] Agent Loop 
- [x] git config
- [x] git status
- [x] git diff
- [x] git stash
- [x] git add
- [x] git commit

## Phase 2: Branching 

Focus: Executing the merge trigger and handling pre-merge state.

- [ ] git branch
- [ ] git checkout
- [ ] git fetch
- [ ] git merge 
- [ ] Refine LLM Planning:

Phase 3: Conflict Resolution (The Core Goal)

Focus: Reading, resolving, and confirming conflicts within the agent loop.

- [ ] get conflicted files
- [x] read file content
- [x] write file content
- [ ] add resolved
- [ ] git revert
- [ ] git reset
- [ ] Program the agent's full conflict resolution sequence (Read -> LLM Resolve -> Write -> Add -> Commit).