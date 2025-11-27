# Contributing Guide

## 1. Introduction

This document describes the standardized development workflow for this project, which is based on collaboration with specialized LLM agents (modes). The goal is to efficiently manage complex tasks by breaking them down into clear, manageable steps and delegating them to the most suitable agent.

## 2. Development Workflow

The workflow is divided into five phases and is controlled by an `Orchestrator` mode.

### Phase 1: Task Analysis (Orchestrator)

Every new requirement or complex feature is first analyzed by the `Orchestrator`. The `Orchestrator` breaks down the requirement into a series of logical and independent subtasks. The result of this phase is a detailed TODO list that serves as a guide for the entire implementation.

### Phase 2: Delegation to Specialists (Orchestrator)

After creating the TODO list, the `Orchestrator` delegates each individual subtask to a specialized mode. The choice of mode depends on the nature of the task (e.g., `architect` for planning, `code` for implementation, `debug` for troubleshooting).

Delegation is done using the `new_task` tool. It is crucial that the instructions for each subtask are clear, precise, and isolated to give the specialist mode a clear objective.

### Phase 3: Implementation (Specialist Mode)

The assigned specialist mode autonomously executes the task assigned to it. It focuses exclusively on the requirements defined in the task. After successful completion, the mode reports the result back to the `Orchestrator` using the `attempt_completion` tool.

### Phase 4: Review and Integration (Orchestrator)

The `Orchestrator` receives the result from the specialist mode and reviews it. If the task was completed successfully, the `Orchestrator` updates the status in the TODO list (e.g., from "in progress" to "done") and initiates the next subtask from the list by delegating it to the appropriate specialist. This cycle is repeated until all tasks in the TODO list are completed.

### Phase 5: Feature Documentation (Orchestrator)

After a feature is successfully implemented and reviewed, the Orchestrator's final task is to update the `CHANGELOG.md` file. This update must be included in the same commit as the feature code itself. This ensures that the feature documentation and the code are always in sync.

## 3. Principles for LLM Collaboration

To ensure effective and efficient collaboration, the following principles should be observed:

*   **Clarity:** Formulate every requirement and every task as clearly, specifically, and unambiguously as possible. Vague instructions lead to unpredictable results.
*   **Iterative Approach:** Proceed in small, verifiable steps. Do not try to solve complex problems in a single large step. Smaller, incremental changes are easier to review and correct.
*   **Feedback:** If a specialist mode does not perform a task as expected, provide specific and constructive feedback. Describe exactly what was wrong and what the expected result looks like. This helps the model learn from mistakes and improve the next iteration.

## Versioning Strategy

This project follows Semantic Versioning (SemVer). The version format is `MAJOR.MINOR.PATCH`.

*   **MAJOR** version for incompatible API changes.
*   **MINOR** version for adding functionality in a backward-compatible manner.
*   **PATCH** version for backward-compatible bug fixes.