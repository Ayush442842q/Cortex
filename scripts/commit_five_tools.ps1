[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string[]]$Tools,

    [string[]]$SharedFiles = @("README.md", "tests/test_tool_loading.py"),

    [switch]$Push,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if ($DryRun) {
        Write-Host "DRY RUN: git $($Args -join ' ')"
        return
    }
    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed"
    }
}

function Get-ToolName {
    param([string]$Path)
    $name = [System.IO.Path]::GetFileNameWithoutExtension($Path)
    return ($name -replace "_tool$", "" -replace "_", "-")
}

function Test-ChangedPath {
    param([string]$Path)
    $status = & git status --porcelain -- $Path
    return -not [string]::IsNullOrWhiteSpace($status)
}

$repoRoot = (& git rev-parse --show-toplevel 2>$null).Trim()
if (-not $repoRoot) {
    throw "Not inside a Git repository."
}
Set-Location $repoRoot

$Tools = @($Tools | ForEach-Object { $_ -split "," } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object { $_.Trim() })
$SharedFiles = @($SharedFiles | ForEach-Object { $_ -split "," } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object { $_.Trim() })

$branch = (& git branch --show-current).Trim()
if (-not $branch) {
    throw "Could not determine current branch."
}

$unmerged = & git diff --name-only --diff-filter=U
if ($unmerged) {
    throw "Unmerged files exist. Resolve conflicts before running this script."
}

if ($Tools.Count -ne 5) {
    throw "Pass exactly five tool files. Received $($Tools.Count)."
}

$normalizedTools = @()
foreach ($tool in $Tools) {
    $full = Resolve-Path -LiteralPath $tool -ErrorAction Stop
    $relative = Resolve-Path -LiteralPath $full -Relative
    $relative = $relative.TrimStart(".", "\", "/") -replace "\\", "/"
    if (-not ($relative.StartsWith("tools/") -and $relative.EndsWith(".py"))) {
        throw "Tool path must be a Python file under tools/: $tool"
    }
    $normalizedTools += $relative
}

Write-Host "Branch: $branch"
Write-Host "Preparing one commit per tool:"
$normalizedTools | ForEach-Object { Write-Host "  $_" }

foreach ($tool in $normalizedTools) {
    $pathsToStage = @($tool)
    foreach ($shared in $SharedFiles) {
        if ((Test-Path -LiteralPath $shared) -and (Test-ChangedPath $shared)) {
            $pathsToStage += ($shared -replace "\\", "/")
        }
    }

    $changed = $false
    foreach ($path in $pathsToStage) {
        if (Test-ChangedPath $path) {
            $changed = $true
            break
        }
    }

    if (-not $changed) {
        Write-Host "Skipping ${tool}: no changes to commit."
        continue
    }

    Invoke-Git reset --quiet
    Invoke-Git add -- $pathsToStage

    $toolName = Get-ToolName $tool
    $message = "Add $toolName tool"

    Write-Host "Committing: $message"
    Invoke-Git commit -m $message
}

Invoke-Git reset --quiet

if ($Push) {
    Write-Host "Pushing branch: $branch"
    Invoke-Git push -u origin $branch
}

Write-Host "Done."
