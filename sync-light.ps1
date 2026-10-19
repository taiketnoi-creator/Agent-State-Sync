param(
    [ValidateSet('start', 'finish', 'snapshot')]
    [string]$Mode = 'snapshot',
    [string]$Message = "Cap nhat lich su cong viec & trang thai du an ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))",
    [string]$RemoteUrl = ""
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$py = "C:\Users\guicci\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe"

if ($RemoteUrl -ne "") {
    $existingRemote = git remote
    if ($existingRemote -contains "origin") {
        git remote set-url origin $RemoteUrl
    } else {
        git remote add origin $RemoteUrl
    }
    Write-Output "Configured GitHub remote origin: $RemoteUrl"
}

if ($Mode -eq 'start') {
    $hasOrigin = (git remote) -contains "origin"
    if ($hasOrigin) {
        git pull --rebase origin main
    }
    Write-Output "=== SYNCED LATEST PROJECT HISTORY ==="
    Write-Output "Read PROJECT-BLUEPRINT.md and WORK-HISTORY.md to continue immediately."
    exit 0
}

& $py "$PSScriptRoot\generate_snapshot.py"

if ($Mode -eq 'snapshot') {
    exit 0
}

git add -A
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Output "No new changes to commit."
} else {
    git commit -m $Message
    Write-Output "Committed work history: $Message"
}

$hasOrigin = (git remote) -contains "origin"
if ($hasOrigin) {
    git push -u origin main
    Write-Output "Pushed lightweight history to GitHub successfully!"
} else {
    Write-Output "No GitHub remote URL set yet. Run: .\sync-light.ps1 -Mode finish -RemoteUrl 'https://github.com/<user>/<new-repo>.git'"
}
