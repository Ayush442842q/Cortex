#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/commit_five_tools.sh TOOL1 TOOL2 TOOL3 TOOL4 TOOL5 [--shared FILE ...] [--push] [--dry-run]

Creates one commit per tool file. Each commit stages only that tool plus changed shared files.
EOF
}

tools=()
shared=("README.md" "tests/test_tool_loading.py")
push=false
dry_run=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --shared)
      shift
      shared=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        shared+=("$1")
        shift
      done
      ;;
    --push)
      push=true
      shift
      ;;
    --dry-run)
      dry_run=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      tools+=("$1")
      shift
      ;;
  esac
done

if [[ ${#tools[@]} -ne 5 ]]; then
  echo "Error: pass exactly five tool files. Received ${#tools[@]}." >&2
  usage
  exit 1
fi

git_cmd() {
  if [[ "$dry_run" == true ]]; then
    printf 'DRY RUN: git'
    printf ' %q' "$@"
    printf '\n'
  else
    git "$@"
  fi
}

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

branch="$(git branch --show-current)"
if [[ -z "$branch" ]]; then
  echo "Error: could not determine current branch." >&2
  exit 1
fi

if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  echo "Error: unmerged files exist. Resolve conflicts before running this script." >&2
  exit 1
fi

normalize_path() {
  python -c "import os, sys; print(os.path.relpath(sys.argv[1]).replace(os.sep, '/'))" "$1"
}

tool_name() {
  local base
  base="$(basename "$1" .py)"
  base="${base%_tool}"
  echo "${base//_/-}"
}

changed_path() {
  [[ -n "$(git status --porcelain -- "$1")" ]]
}

normalized_tools=()
for tool in "${tools[@]}"; do
  if [[ ! -f "$tool" ]]; then
    echo "Error: tool file not found: $tool" >&2
    exit 1
  fi
  rel="$(normalize_path "$tool")"
  if [[ "$rel" != tools/*.py ]]; then
    echo "Error: tool path must be a Python file under tools/: $tool" >&2
    exit 1
  fi
  normalized_tools+=("$rel")
done

echo "Branch: $branch"
echo "Preparing one commit per tool:"
printf '  %s\n' "${normalized_tools[@]}"

for tool in "${normalized_tools[@]}"; do
  paths_to_stage=("$tool")
  for shared_file in "${shared[@]}"; do
    if [[ -e "$shared_file" ]] && changed_path "$shared_file"; then
      paths_to_stage+=("$(normalize_path "$shared_file")")
    fi
  done

  changed=false
  for path in "${paths_to_stage[@]}"; do
    if changed_path "$path"; then
      changed=true
      break
    fi
  done

  if [[ "$changed" == false ]]; then
    echo "Skipping $tool: no changes to commit."
    continue
  fi

  git_cmd reset --quiet
  git_cmd add -- "${paths_to_stage[@]}"

  message="Add $(tool_name "$tool") tool"
  echo "Committing: $message"
  git_cmd commit -m "$message"
done

git_cmd reset --quiet

if [[ "$push" == true ]]; then
  echo "Pushing branch: $branch"
  git_cmd push -u origin "$branch"
fi

echo "Done."
