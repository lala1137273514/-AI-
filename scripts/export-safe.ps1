param(
    [switch]$SkipCcPersona,
    [switch]$SkipMemories,
    [switch]$SkipAutomations,
    [switch]$SkipAgents,
    [switch]$SkipSkills
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

function Reset-RepoDirectory {
    param([string]$Target)

    $targetPath = Join-Path $RepoRoot $Target
    $repoFull = [System.IO.Path]::GetFullPath($RepoRoot)
    $targetFull = [System.IO.Path]::GetFullPath($targetPath)

    if (-not $targetFull.StartsWith($repoFull, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to reset outside repo: $targetFull"
    }

    if (Test-Path -LiteralPath $targetFull) {
        Remove-Item -LiteralPath $targetFull -Recurse -Force
    }

    New-Item -ItemType Directory -Force -Path $targetFull | Out-Null
    return $targetFull
}

function Copy-DirectoryFiltered {
    param(
        [string]$Source,
        [string]$Target
    )

    if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
        throw "Missing required source directory: $Source"
    }

    $targetPath = Join-Path $RepoRoot $Target
    New-Item -ItemType Directory -Force -Path $targetPath | Out-Null

    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        if ($_.Name -in @(".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".DS_Store")) {
            return
        }
        if ($_.Name -match "^(auth|credentials|settings\.local|state|history|session).*") {
            return
        }
        if ($_.Extension -in @(".pyc", ".sqlite", ".pem", ".key", ".p12", ".pfx")) {
            return
        }
        Copy-Item -LiteralPath $_.FullName -Destination $targetPath -Recurse -Force
    }

    $blockedDirectories = @(".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".omx", "tmp-profile", ".lark-cli", "runs", "extracted_results")
    Get-ChildItem -Recurse -Force -Directory -LiteralPath $targetPath |
        Where-Object { $blockedDirectories -contains $_.Name } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }

    Get-ChildItem -Recurse -Force -File -LiteralPath $targetPath |
        Where-Object { $_.Extension -eq ".pyc" } |
        ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force }
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

Copy-RequiredFile (Join-Path $CodexHome "rules/default.rules") "codex/rules/default.rules"

if (-not $SkipMemories) {
    Reset-RepoDirectory "shared/memories" | Out-Null
    Copy-RequiredFile (Join-Path $CodexHome "memories/MEMORY.md") "shared/memories/MEMORY.md"
    Copy-RequiredFile (Join-Path $CodexHome "memories/memory_summary.md") "shared/memories/memory_summary.md"

    New-Item -ItemType Directory -Force -Path (Join-Path $RepoRoot "shared/memories/rollout_summaries") | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $CodexHome "memories/rollout_summaries") -Filter "*.md" -File |
        ForEach-Object { Copy-RequiredFile $_.FullName "shared/memories/rollout_summaries/$($_.Name)" }

    Copy-DirectoryFiltered (Join-Path $CodexHome "memories/skills/feishu-retro-lark-cli-preflight") "shared/memories/skills/feishu-retro-lark-cli-preflight"
}

if (-not $SkipAutomations) {
    Reset-RepoDirectory "automations" | Out-Null
    foreach ($name in @("daily-feishu-retro", "morning-feishu-retro")) {
        $source = Join-Path $CodexHome "automations/$name"
        if (Test-Path -LiteralPath $source -PathType Container) {
            New-Item -ItemType Directory -Force -Path (Join-Path $RepoRoot "automations/$name") | Out-Null
            Copy-RequiredFile (Join-Path $source "automation.toml") "automations/$name/automation.example.toml"
            Copy-RequiredFile (Join-Path $source "memory.md") "automations/$name/memory.md"
        }
    }
}

if (-not $SkipAgents) {
    Reset-RepoDirectory "shared/agents/codex" | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $CodexHome "agents") -Filter "*.toml" -File |
        ForEach-Object { Copy-RequiredFile $_.FullName "shared/agents/codex/$($_.Name)" }

    Reset-RepoDirectory "shared/agents/claude" | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $ClaudeHome "agents") -Filter "*.md" -File |
        ForEach-Object { Copy-RequiredFile $_.FullName "shared/agents/claude/$($_.Name)" }
}

if (-not $SkipSkills) {
    Reset-RepoDirectory "shared/skills/lark" | Out-Null
    Get-ChildItem -Directory -Force -LiteralPath (Join-Path $ClaudeHome "skills") |
        Where-Object { $_.Name -like "lark-*" } |
        ForEach-Object { Copy-DirectoryFiltered $_.FullName "shared/skills/lark/$($_.Name)" }

    Reset-RepoDirectory "shared/skills/custom" | Out-Null
    $customSkillNames = @(
        "ai-coach",
        "humanizer",
        "loona-daily-review-v2",
        "loona-travel-flow",
        "shuorenhua",
        "travel-planner",
        "guizang-ppt-skill",
        "karpathy-guidelines",
        "prompt-eval",
        "skill-prompt-generator",
        "intelligent-prompt-generator",
        "art-master",
        "design-master",
        "product-master",
        "video-master",
        "prompt-analyzer",
        "prompt-extractor",
        "prompt-generator",
        "prompt-master",
        "prompt-xray",
        "universal-learner",
        "domain-classifier",
        "terminal-title"
    )

    foreach ($name in $customSkillNames) {
        $source = Join-Path $ClaudeHome "skills/$name"
        if (Test-Path -LiteralPath $source -PathType Container) {
            Copy-DirectoryFiltered $source "shared/skills/custom/$name"
        }
    }

    Copy-DirectoryFiltered (Join-Path $CodexHome "skills/feishu-retro-review") "shared/skills/custom/feishu-retro-review"
}

& (Join-Path $PSScriptRoot "check-secrets.ps1")
