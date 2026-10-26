param(
    [ValidateSet('start', 'finish', 'snapshot')]
    [string]$Mode = 'snapshot',
    [string]$Message = "Cap nhat lich su cong viec & trang thai du an ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))",
    [string]$RemoteUrl = ""
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Continue'
Set-Location $PSScriptRoot

$pyCandidates = @(
    "python",
    "C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Users\guicci\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe"
)
$py = "python"
foreach ($cand in $pyCandidates) {
    if ($cand -eq "python") {
        if (Get-Command python -ErrorAction SilentlyContinue) {
            $py = "python"
            break
        }
    } elseif (Test-Path $cand) {
        $py = $cand
        break
    }
}

if ($RemoteUrl -ne "") {
    $existingRemote = git remote
    if ($existingRemote -contains "origin") {
        git remote set-url origin $RemoteUrl
    } else {
        git remote add origin $RemoteUrl
    }
    Write-Output "Configured GitHub remote origin: $RemoteUrl"
}

$hasOrigin = (git remote) -contains "origin"

if ($Mode -eq 'start') {
    if ($hasOrigin) {
        git pull --rebase --autostash origin main
    }
    & $py "$PSScriptRoot\generate_snapshot.py" --direction pull
    Write-Output "=== SYNCED LATEST PROJECT HISTORY (GIT -> SUBAGENT) ==="
    exit 0
}

if ($Mode -eq 'snapshot') {
    & $py "$PSScriptRoot\generate_snapshot.py" --direction auto
    exit 0
}

# Mode = finish:
# 1. Push workspace changes from Subagent -> Agent-State-Sync
& $py "$PSScriptRoot\generate_snapshot.py" --direction push

# 2. Commit local changes first so rebase is clean
git add -A
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m $Message
    Write-Output "Committed work history: $Message"
} else {
    Write-Output "No new local changes to commit before pull."
}

# 3. Pull --rebase from remote to integrate any commits from the other PC
if ($hasOrigin) {
    git pull --rebase --autostash origin main
    # Mirror any newly pulled remote files back to Subagent
    & $py "$PSScriptRoot\generate_snapshot.py" --direction pull
    git add -A
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        git commit -m "$Message (merged)"
    }
    git push -u origin main
    Write-Output "Pushed lightweight history to GitHub successfully!"
} else {
    Write-Output "No GitHub remote URL set yet."
}
