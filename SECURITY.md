# Security Policy

## Reporting a Vulnerability

Please do not open a public issue for sensitive security reports. Email the maintainer or use a private GitHub security advisory if available.

Include:

- affected tool or module
- steps to reproduce
- expected impact
- suggested fix, if you have one

## Security Model

Cortex is a local agent that can run tools with real side effects. Treat it like any other program with local shell and filesystem access.

Current high-risk capabilities include:

- shell command execution
- file creation, deletion, moving, and copying
- Git operations
- network requests
- SMTP email sending
- package installation by some tools
- process termination
- scheduled shell commands

Run Cortex only in trusted environments and avoid connecting it to untrusted prompts without additional sandboxing.
