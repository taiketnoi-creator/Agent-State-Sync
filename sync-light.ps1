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
$dbPath = "C:\Users\guicci\.gemini\antigravity\scratch\ai-aff-video-system\data\aff_system.db"
$subagentDir = "D:\Phiên bản Ai agent\Subagent"

if ($RemoteUrl -ne "") {
    $existingRemote = git remote
    if ($existingRemote -contains "origin") {
        git remote set-url origin $RemoteUrl
    } else {
        git remote add origin $RemoteUrl
    }
    Write-Output "Đã cấu hình GitHub remote origin: $RemoteUrl"
}

if ($Mode -eq 'start') {
    $hasOrigin = (git remote) -contains "origin"
    if ($hasOrigin) {
        git pull --rebase origin main
    }
    Write-Output "=== ĐÃ ĐỒNG BỘ LỊCH SỬ MỚI NHẤT ==="
    Write-Output "Đọc PROJECT-BLUEPRINT.md và WORK-HISTORY.md để tiếp tục công việc ngay."
    exit 0
}

# Tự động tạo STATE-SNAPSHOT.md siêu nhẹ (< 5KB) ghi danh mục chiến dịch & tóm tắt DB mà không cần đẩy file .db
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$campaigns = @()
if (Test-Path "$subagentDir\campaigns") {
    $campaigns = Get-ChildItem -Path "$subagentDir\campaigns" -Directory | Select-Object -ExpandProperty Name
}

$dbSummary = "Chưa có dữ liệu"
if ((Test-Path $py) -and (Test-Path $dbPath)) {
    $pyCode = @"
import sqlite3, json, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect(r'$dbPath')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('SELECT id, name, niche, score, commission, status FROM products ORDER BY id DESC LIMIT 10')
prods = [dict(r) for r in cur.fetchall()]
cur.execute('SELECT id, title, status, platforms FROM video_jobs ORDER BY id DESC LIMIT 10')
jobs = [dict(r) for r in cur.fetchall()]
print(json.dumps({'products': prods, 'video_jobs': jobs}, ensure_ascii=False, indent=2))
"@
    $dbSummary = & $py -c $pyCode
}

$snapshotContent = @"
# Bản Chụp Trạng Thái Tự Động (Lightweight State Snapshot)

- **Cập nhật lần cuối:** `$timestamp`
- **Máy thực hiện:** `$env:COMPUTERNAME`

## 1. Các Thư Mục Chiến Dịch Hiện Có (`D:\Phiên bản Ai agent\Subagent\campaigns`)
$($campaigns | ForEach-Object { "- ``$_``" } | Out-String)

## 2. Tóm Tắt Dữ Liệu SQLite Local (Top 10 Mới Nhất - Không Cần Đẩy File `.db`)
``````json
$dbSummary
``````
"@

Set-Content -Path "$PSScriptRoot\STATE-SNAPSHOT.md" -Value $snapshotContent -Encoding UTF8

if ($Mode -eq 'snapshot') {
    Write-Output "Đã cập nhật STATE-SNAPSHOT.md thành công!"
    exit 0
}

git add -A
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Output "Không có thay đổi mới cần commit."
} else {
    git commit -m $Message
    Write-Output "Đã commit lịch sử công việc: $Message"
}

$hasOrigin = (git remote) -contains "origin"
if ($hasOrigin) {
    git push -u origin main
    Write-Output "Đã đẩy lịch sử siêu nhẹ lên GitHub thành công!"
} else {
    Write-Output "Chưa gắn link GitHub repo mới. Chạy lệnh: .\sync-light.ps1 -Mode finish -RemoteUrl 'https://github.com/<user>/<new-repo>.git'"
}
