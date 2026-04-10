# Legacy Code Refactoring

## Overview

Refactored `legacy_script.py` into a clean, production-ready `legacy_script_refactored.py`.

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| Architecture | Global variables, monolithic functions | Class-based, single responsibility |
| Credentials | Hardcoded (`"admin"`, `"12345"`) | Environment variables |
| File I/O | Manual `open()`/`close()` | Context managers (`with`) |
| Commands | Magic strings (`"add"`, `"show"`) | Enum (`Command`) |
| Types | None (dynamic) | Full type hints + dataclass |
| Error handling | None | Custom exceptions + try/except |
| Execution | Top-level code | `if __name__ == "__main__"` guard |
| Dead code | `calculate_something_else()` | Removed |
| Validation | None | Input validation added |

## Principles Applied

- **SOLID**: Clean separation of concerns (Repository, Authenticator, Manager)
- **DRY**: Enum for commands, single command execution logic
- **YAGNI**: Removed unused functions, no over-engineering

## Usage

```bash
export APP_USERNAME=admin
export APP_PASSWORD=your_password
python legacy_script_refactored.py
```
