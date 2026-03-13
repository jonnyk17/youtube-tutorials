# Over-Engineering

## Priority: MEDIUM

## Description

Abstractions, patterns, and infrastructure that add complexity without proportional value. Common in AI-generated code, which tends to create elaborate class hierarchies and configuration layers for simple problems.

## Patterns to Check

### Factory pattern for one implementation
```python
# Over-engineered
class NotificationFactory:
    @staticmethod
    def create(type: str) -> Notification:
        if type == "email":
            return EmailNotification()
        raise ValueError(f"Unknown type: {type}")

# Only EmailNotification exists. The factory adds nothing.
```

```python
# Simple
notification = EmailNotification()
```

### Abstract base class with one child
```python
# Over-engineered
class BaseRepository(ABC):
    @abstractmethod
    async def get(self, id): ...
    @abstractmethod
    async def create(self, data): ...
    @abstractmethod
    async def delete(self, id): ...

class UserRepository(BaseRepository):
    async def get(self, id): ...
    async def create(self, data): ...
    async def delete(self, id): ...

# Only one repository exists. The ABC adds nothing.
```

### Configuration layer for hardcoded values
```python
# Over-engineered
class Config:
    MAX_RETRIES = 3
    TIMEOUT = 30
    BATCH_SIZE = 100

# These never change and are only used in one place each
```

## What to Check

- Factory/strategy/builder patterns with only one implementation
- Abstract base classes with a single concrete subclass
- Configuration objects where values never change
- Wrapper classes that just delegate to the wrapped object
- Generic type parameters used in only one place
- "Manager" or "Handler" classes that could be plain functions
