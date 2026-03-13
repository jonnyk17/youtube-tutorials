# Command Injection

## Priority: CRITICAL

## Description

Command injection occurs when user input is passed to shell commands. Attackers can execute arbitrary system commands.

## Vulnerable

```python
import os
import subprocess

# os.system with user input
os.system(f"ping {hostname}")

# subprocess with shell=True and user input
subprocess.run(f"convert {filename} output.png", shell=True)

# eval/exec with user input
eval(user_expression)
```

```javascript
const { exec } = require("child_process");

// exec with user input
exec(`ffmpeg -i ${inputFile} output.mp4`);
```

## Fixed

```python
# subprocess with argument list (no shell)
subprocess.run(["ping", hostname])
subprocess.run(["convert", filename, "output.png"])
```

```javascript
const { execFile } = require("child_process");

// execFile with argument array
execFile("ffmpeg", ["-i", inputFile, "output.mp4"]);
```

## What to Check

- `os.system()`, `os.popen()` with any variable input
- `subprocess.run()` or `subprocess.Popen()` with `shell=True` and variable input
- `exec()`, `eval()` with user-controlled data
- Node.js `child_process.exec()` with template literals containing variables
- Any shell command string built with string concatenation or formatting
