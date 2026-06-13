param(
    [switch]$SkipCcPersona
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$CodexHome = Join-Path $HOME ".codex"
$ClaudeHome = Join-Path $HOME ".claude"

function Copy-RequiredFile {
    param(
        [string]$Source,
        [string]$Target
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Missing required source: $Source"
    }

    $targetPath = Join-Path $RepoRoot $Target
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetPath) | Out-Null
    Copy-Item -LiteralPath $Source -Destination $targetPath -Force
    Write-Host "Exported: $Target"
}

Copy-RequiredFile (Join-Path $CodexHome "AGENTS.md") "codex/AGENTS.md"
Copy-RequiredFile (Join-Path $ClaudeHome "CLAUDE.md") "claude/CLAUDE.md"

if (-not $SkipCcPersona) {
    $skillSource = Join-Path $CodexHome "skills/cc-persona"
    $skillTarget = Join-Path $RepoRoot "shared/skills/cc-persona"
    New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $skillTarget "references") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $skillTarget "scripts") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $skillTarget "tests") | Out-Null

    $rootFiles = @("README.md", "SKILL.md", "cc-core.md", "config.json", "lessons.md")
    foreach ($file in $rootFiles) {
        Copy-RequiredFile (Join-Path $skillSource $file) "shared/skills/cc-persona/$file"
    }

    Get-ChildItem -LiteralPath (Join-Path $skillSource "references") -Filter "*.md" -File |
        ForEach-Object { Copy-RequiredFile $_.FullName "shared/skills/cc-persona/references/$($_.Name)" }

    Get-ChildItem -LiteralPath (Join-Path $skillSource "scripts") -Filter "*.py" -File |
        ForEach-Object { Copy-RequiredFile $_.FullName "shared/skills/cc-persona/scripts/$($_.Name)" }

    Get-ChildItem -LiteralPath (Join-Path $skillSource "tests") -Filter "*.py" -File |
        ForEach-Object { Copy-RequiredFile $_.FullName "shared/skills/cc-persona/tests/$($_.Name)" }
}

& (Join-Path $PSScriptRoot "check-secrets.ps1")
