# Dead Code

## Priority: HIGH

## Description

Code that is never executed or used. This includes unreachable branches, unused variables, unused imports, unused functions, and commented-out code.

## Patterns to Check

### Unused imports
```python
# Bad: imported but never used
import os
from typing import Optional, List, Dict  # Only List is used

def get_items() -> List[str]:
    return ["a", "b"]
```

### Unreachable code after return
```python
def process(data):
    if not data:
        return None
        logger.info("No data")  # Never executes
```

### Commented-out code
```python
def calculate(x, y):
    # old_result = x * y + some_offset
    # if old_result > threshold:
    #     return old_result
    return x * y
```

### Unused variables
```javascript
const result = await fetchData();
const parsed = JSON.parse(result);
const filtered = parsed.filter(item => item.active);
// Only 'filtered' is used, but all three are assigned
return filtered.map(item => item.name);
```

## What to Do

- Remove unused imports
- Remove unreachable code after return/raise/throw
- Delete commented-out code (it's in git history if needed)
- Remove variables that are assigned but never read
- Flag unused function parameters (but don't auto-remove, they may be required by an interface)
