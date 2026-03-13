---
name: code-simplifier
description: Reviews code for unnecessary complexity, dead code, duplication, and over-engineering. Suggests concrete simplifications while preserving functionality. Use after writing code, passing tests, or when code works but feels complex.
---

# Code Simplifier

Identifies opportunities to simplify code without changing behavior. The goal is clarity and maintainability, not cleverness.

## When to Apply

- After writing or modifying code
- After all tests pass
- When code works but feels harder to read than it should be
- During refactoring passes
- When onboarding someone to a codebase

## What It Checks

| Priority | Category | Rules |
|----------|----------|-------|
| HIGH | Dead Code | Unreachable branches, unused variables, unused imports, unused functions |
| HIGH | Duplication | Copy-paste code, repeated patterns that should be extracted |
| MEDIUM | Complexity | Deep nesting, long functions, complex conditionals |
| MEDIUM | Over-engineering | Unnecessary abstractions, premature generalization, design patterns used where a simple function would do |
| LOW | Readability | Overly clever code, unclear naming, missing early returns |

## How to Use

```
Simplify the code I just wrote
```

```
Find dead code across the codebase
```

```
Can this function be simplified?
```

## Philosophy

Three similar lines of code is better than a premature abstraction. Only suggest extraction when there are 3+ copies or the duplication will clearly grow. Preserve the author's intent. Simplify the implementation, not the design.

## Rules

Read individual rule files in `rules/` for detailed checks with examples.
