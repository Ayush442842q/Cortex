# Scripts

Helper scripts for local maintainer workflows.

## Commit Five Tools

PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\commit_five_tools.ps1 `
  -Tools tools\tool_one.py,tools\tool_two.py,tools\tool_three.py,tools\tool_four.py,tools\tool_five.py `
  -SharedFiles README.md,tests\test_tool_loading.py
```

Bash:

```bash
./scripts/commit_five_tools.sh \
  tools/tool_one.py tools/tool_two.py tools/tool_three.py tools/tool_four.py tools/tool_five.py \
  --shared README.md tests/test_tool_loading.py
```

The scripts create one commit per tool. They stage only the current tool file plus optional shared files that have changes. They use your existing Git author configuration, so commits are made as you.

Add `-Push` in PowerShell or `--push` in Bash to push after all commits succeed.
