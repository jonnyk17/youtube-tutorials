# Unused Dependencies

## Priority: MEDIUM

## Description

Dependencies listed in package.json or pyproject.toml that are not imported anywhere in the codebase. They bloat install time, increase attack surface, and create confusion.

## How to Check

### JavaScript
```bash
npx depcheck
```

Or manually: search the codebase for imports of each dependency.

### Python
Search for `import package_name` or `from package_name` for each dependency in pyproject.toml.

## What to Flag

- Packages in `dependencies` (not devDependencies) with zero imports
- Packages that were likely part of a removed feature

## What NOT to Flag

- CLI tools that are called via scripts (e.g., `eslint`, `pytest`, `prisma`)
- Babel/PostCSS/webpack plugins loaded via config files
- Type packages (`@types/*`) used only by the type checker
- Packages referenced in configuration files rather than imports
