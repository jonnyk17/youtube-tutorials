# Outdated Dependencies

## Priority: HIGH

## Description

Dependencies that are significantly behind the latest version. Major version bumps often include security fixes, performance improvements, and breaking changes that get harder to migrate the longer you wait.

## What to Flag

- **Major version behind**: Package is 2+ major versions behind latest (e.g., using v3 when v5 is out)
- **Unmaintained**: No releases in 12+ months and the package has known alternatives
- **Deprecated**: Package explicitly marked as deprecated by maintainers

## What NOT to Flag

- Minor or patch version differences (these are routine)
- Packages pinned to a specific version with a documented reason
- Packages where the latest version has known instability

## How to Check

```bash
# Node.js
npm outdated
bun outdated

# Python
pip list --outdated
uv pip list --outdated
```
