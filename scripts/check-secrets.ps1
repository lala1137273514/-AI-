$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

$blockedNames = @(
    "auth.json",
    ".credentials.json",
    "credentials.json",
    "settings.json",
    "settings.local.json",
    "history.jsonl",
    "session_index.jsonl",
    "state.json",
    "user_profile.json",
    "raw_memories.md"
)

$blockedSuffixes = @(
    ".sqlite",
    ".sqlite-shm",
    ".sqlite-wal",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".tar.gz",
    ".pyc"
)

$blockedDirs = @(
    ".git",
    "sessions",
    "archived_sessions",
    "cache",
    "tmp",
    ".tmp",
    "logs",
    "log",
    "telemetry",
    "paste-cache",
    "file-history",
    "shell-snapshots",
    "worktrees",
    "node_modules",
    "__pycache__",
    ".omx",
    "tmp-profile",
    ".lark-cli"
)

function Test-IsBlockedDir {
    param([string]$Path)

    $relative = Resolve-Path -LiteralPath $Path -Relative
    foreach ($dir in $blockedDirs) {
        if ($relative -match "(^|[\\/])$([regex]::Escape($dir))([\\/]|$)") {
            return $true
        }
    }
    return $false
}

$files = Get-ChildItem -LiteralPath $RepoRoot -Recurse -Force -File |
    Where-Object { -not (Test-IsBlockedDir $_.DirectoryName) }

$badFiles = @()
foreach ($file in $files) {
    if ($blockedNames -contains $file.Name) {
        if ($file.Name -ne "settings.example.json") {
            $badFiles += $file.FullName
            continue
        }
    }

    foreach ($suffix in $blockedSuffixes) {
        if ($file.Name.EndsWith($suffix, [StringComparison]::OrdinalIgnoreCase)) {
            $badFiles += $file.FullName
            break
        }
    }
}

if ($badFiles.Count -gt 0) {
    Write-Error ("Blocked sensitive/runtime files:`n" + ($badFiles -join "`n"))
}

$secretPatterns = [ordered]@{
    "Private key" = "-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"
    "Generic sk token" = "\bsk-[A-Za-z0-9][A-Za-z0-9_\-]{16,}\b"
    "GitHub token" = "\bgh[pousr]_[A-Za-z0-9_]{20,}\b"
    "Anthropic token style" = "\bsk-ant-[A-Za-z0-9_\-]{20,}\b"
    "Supabase publishable token" = "\bsb_publishable_[A-Za-z0-9_\-]{20,}\b"
    "JWT" = "\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"
}

$hits = @()
foreach ($file in $files) {
    $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $text) {
        continue
    }

    foreach ($name in $secretPatterns.Keys) {
        if ($text -match $secretPatterns[$name]) {
            $hits += "$name`t$($file.FullName)"
        }
    }
}

if ($hits.Count -gt 0) {
    Write-Error ("Potential secrets found:`n" + ($hits -join "`n"))
}

Write-Host "Secret check passed."
