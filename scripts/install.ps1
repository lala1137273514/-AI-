param(
    [ValidateSet("copy", "link")]
    [string]$Mode = "copy",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Join-RepoPath {
    param([string]$RelativePath)
    return Join-Path $RepoRoot $RelativePath
}

function Backup-Path {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backup = "$Path.bak_$timestamp"
    Move-Item -LiteralPath $Path -Destination $backup
    return $backup
}

function Install-Path {
    param(
        [string]$Source,
        [string]$Target,
        [ValidateSet("file", "directory")]
        [string]$Kind
    )

    $sourcePath = Join-RepoPath $Source
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        throw "Missing source: $Source"
    }

    $parent = Split-Path -Parent $Target
    New-Item -ItemType Directory -Force -Path $parent | Out-Null

    if ((Test-Path -LiteralPath $Target) -and -not $Force) {
        Write-Host "Skip existing: $Target"
        return
    }

    if (Test-Path -LiteralPath $Target) {
        $backup = Backup-Path $Target
        Write-Host "Backed up: $backup"
    }

    if ($Mode -eq "link") {
        $itemType = if ($Kind -eq "directory") { "SymbolicLink" } else { "SymbolicLink" }
        New-Item -ItemType $itemType -Path $Target -Target $sourcePath | Out-Null
        Write-Host "Linked: $Target"
        return
    }

    if ($Kind -eq "directory") {
        Copy-Item -LiteralPath $sourcePath -Destination $Target -Recurse -Force
    } else {
        Copy-Item -LiteralPath $sourcePath -Destination $Target -Force
    }
    Write-Host "Installed: $Target"
}

Install-Path "codex/AGENTS.md" (Join-Path $HOME ".codex/AGENTS.md") "file"
Install-Path "claude/CLAUDE.md" (Join-Path $HOME ".claude/CLAUDE.md") "file"
Install-Path "shared/skills/cc-persona" (Join-Path $HOME ".codex/skills/cc-persona") "directory"

# Examples are copied as examples only. Real credentials stay local.
Install-Path "codex/config.example.toml" (Join-Path $HOME ".codex/config.shared.example.toml") "file"
Install-Path "claude/settings.example.json" (Join-Path $HOME ".claude/settings.example.json") "file"
