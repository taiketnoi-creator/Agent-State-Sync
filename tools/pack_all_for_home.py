#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pack_all_for_home.py — Đóng gói toàn bộ Hệ thống 10 Subagent + MCP + SQLite DB + Token (.env)
thành 1 file .zip duy nhất tại `D:\Phiên bản Ai agent\Full-Agent-Backup-Home.zip`,
kèm script 1-click khôi phục tự động trên máy ở nhà.
"""

import os
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(r"D:\Phiên bản Ai agent")
SUBAGENT_DIR = ROOT_DIR / "Subagent"
STATE_SYNC_DIR = ROOT_DIR / "Agent-State-Sync"
HOME_DIR = Path.home()

OUTPUT_ZIP = ROOT_DIR / "Full-Agent-Backup-Home.zip"

EXCLUDE_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".remotion",
    ".next",
    "dist",
    ".git",  # Git history đã có trên GitHub, bỏ .git nặng 145MB để file nén nhẹ và nhanh
}

RESTORE_PS1 = r"""# ==============================================================================
# SCRIPT KHÔI PHỤC TỰ ĐỘNG HỆ THỐNG AGENT-JAVIS TRÊN MÁY Ở NHÀ (1-CLICK RESTORE)
# ==============================================================================
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$BackupRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$CBackup = Join-Path $BackupRoot "_C_Drive_Backup"
$UserHome = $env:USERPROFILE

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "🚀 ĐANG KHÔI PHỤC HỆ THỐNG 10 SUBAGENT + MCP + DB TRÊN MÁY NÀY..." -ForegroundColor Cyan
Write-Host "   Thư mục giải nén : $BackupRoot"
Write-Host "   User Profile đích: $UserHome"
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Khôi phục Facebook Page MCP Server + .env (Token FB, Vbee) + pages_vault.json (5 Fanpage)
$TargetFbMcp = Join-Path $UserHome ".codex\mcp\facebook-mcp-server"
New-Item -ItemType Directory -Force -Path $TargetFbMcp | Out-Null
Copy-Item -Path (Join-Path $CBackup "facebook-mcp-server\*") -Destination $TargetFbMcp -Recurse -Force
Write-Host "✅ [1/4] Đã khôi phục Facebook MCP Server + Kho 5 Fanpage + Token (.env) vào: $TargetFbMcp" -ForegroundColor Green

# 2. Khôi phục AI Affiliate Video System + SQLite Database (aff_system.db)
$TargetAffSys = Join-Path $UserHome ".gemini\antigravity\scratch\ai-aff-video-system"
New-Item -ItemType Directory -Force -Path $TargetAffSys | Out-Null
Copy-Item -Path (Join-Path $CBackup "ai-aff-video-system\*") -Destination $TargetAffSys -Recurse -Force
Write-Host "✅ [2/4] Đã khôi phục SQLite Database (aff_system.db) & n8n-SQLite MCP vào: $TargetAffSys" -ForegroundColor Green

# 3. Khôi phục & Tự động cập nhật đường dẫn User trong mcp_config.json và config.toml
$TargetGeminiConfigDir = Join-Path $UserHome ".gemini\config"
New-Item -ItemType Directory -Force -Path $TargetGeminiConfigDir | Out-Null
$McpCfgSrc = Join-Path $CBackup "gemini_config\mcp_config.json"
if (Test-Path $McpCfgSrc) {
    $rawJson = Get-Content $McpCfgSrc -Raw -Encoding UTF8
    $escapedHome = $UserHome.Replace("\", "\\")
    $updatedJson = $rawJson -replace "C:\\\\Users\\\\[^\\""]+", $escapedHome
    Set-Content -Path (Join-Path $TargetGeminiConfigDir "mcp_config.json") -Value $updatedJson -Encoding UTF8
    Write-Host "✅ [3/4] Đã cập nhật mcp_config.json khớp với User của máy nhà ($UserHome)" -ForegroundColor Green
}

$CodexCfgSrc = Join-Path $CBackup "codex\config.toml"
if (Test-Path $CodexCfgSrc) {
    $TargetCodexDir = Join-Path $UserHome ".codex"
    New-Item -ItemType Directory -Force -Path $TargetCodexDir | Out-Null
    $rawToml = Get-Content $CodexCfgSrc -Raw -Encoding UTF8
    $escapedHome = $UserHome.Replace("\", "\\")
    $updatedToml = $rawToml -replace "C:\\\\Users\\\\[^\\""']+", $escapedHome
    Set-Content -Path (Join-Path $TargetCodexDir "config.toml") -Value $updatedToml -Encoding UTF8
}

# 4. Tạo lại môi trường Python (.venv) cho facebook-mcp-server nếu chưa có
$FbVenvPython = Join-Path $TargetFbMcp ".venv\Scripts\python.exe"
if (-not (Test-Path $FbVenvPython)) {
    Write-Host "⏳ [4/4] Đang khởi tạo môi trường .venv cho facebook-mcp-server..." -ForegroundColor Yellow
    Push-Location $TargetFbMcp
    python -m venv .venv
    & ".\.venv\Scripts\pip.exe" install -r requirements.txt --quiet
    Pop-Location
    Write-Host "✅ [4/4] Đã cài đặt xong thư viện cho facebook-mcp-server!" -ForegroundColor Green
} else {
    Write-Host "✅ [4/4] Môi trường .venv của facebook-mcp-server đã sẵn sàng!" -ForegroundColor Green
}

# 5. Chạy Mama Boot Check kiểm tra ngay kết nối trên máy nhà
$BootCheckPy = Join-Path $BackupRoot "Subagent\tools\mama_boot_check.py"
if (Test-Path $BootCheckPy) {
    Write-Host "`n🔍 KẾT QUẢ KIỂM TRA HỆ THỐNG TRÊN MÁY NHÀ:" -ForegroundColor Cyan
    python $BootCheckPy
}

Write-Host "`n🎉 HOÀN TẤT! Mở Antigravity tại thư mục: $(Join-Path $BackupRoot 'Subagent')" -ForegroundColor Green
"""

RESTORE_BAT = """@echo off
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0restore_home_pc.ps1"
echo.
pause
"""

README_TXT = """====================================================================
HƯỚNG DẪN BUNG NÉN & CHẠY TRÊN MÁY Ở NHÀ (CHỈ MẤT 30 GIÂY)
====================================================================

1. Giải nén file `Full-Agent-Backup-Home.zip` này vào ổ đĩa trên máy ở nhà
   (Khuyên dùng đúng đường dẫn: `D:\\Phiên bản Ai agent\\`).

2. Nhấp đúp (Double-click) vào file:
   👉 `KHOI-PHUC-TREN-MAY-NHA.bat`
   Script sẽ tự động:
   - Chép kho 5 Fanpage (`pages_vault.json`) + file `.env` (Token Facebook & Vbee) vào `C:\\Users\\<Tên_Máy_Nhà>\\.codex\\mcp\\facebook-mcp-server`
   - Chép Database SQLite (`aff_system.db`) + MCP Server vào `C:\\Users\\<Tên_Máy_Nhà>\\.gemini\\antigravity\\scratch\\ai-aff-video-system`
   - Tự động sửa lại đường dẫn `C:\\Users\\...` trong `mcp_config.json` khớp với tên User của máy ở nhà.
   - Chạy kiểm tra kết nối `mama_boot_check.py`.

3. Mở phần mềm Antigravity -> Open Folder -> Chọn thư mục `Subagent`.
   (Nếu cần render video Remotion trên máy nhà, mở terminal trong `Subagent\\templates\\remotion-cuongit-template` chạy `npm install` 1 lần là xong).
====================================================================
"""


def add_folder_to_zip(zf: zipfile.ZipFile, src_dir: Path, arc_prefix: str):
    if not src_dir.exists():
        print(f"⚠️ Bỏ qua (không tồn tại): {src_dir}")
        return 0
    count = 0
    for root, dirs, files in os.walk(src_dir):
        # Lọc bỏ các thư mục nặng không cần thiết
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        root_path = Path(root)
        for file in files:
            if file.endswith(".pyc") or file.endswith(".pyo"):
                continue
            full_path = root_path / file
            rel_path = full_path.relative_to(src_dir)
            arcname = f"{arc_prefix}/{rel_path.as_posix()}"
            zf.write(full_path, arcname)
            count += 1
    return count


def main():
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    total_files = 0
    print(f"📦 Đang đóng gói vào: {OUTPUT_ZIP} ...")

    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        # 1. Đóng gói Subagent
        c1 = add_folder_to_zip(zf, SUBAGENT_DIR, "Subagent")
        print(f"  + Subagent/: {c1} files")
        total_files += c1

        # 2. Đóng gói Agent-State-Sync
        c2 = add_folder_to_zip(zf, STATE_SYNC_DIR, "Agent-State-Sync")
        print(f"  + Agent-State-Sync/: {c2} files")
        total_files += c2

        # 3. Đóng gói Facebook MCP Server (kèm .env và pages_vault.json)
        fb_mcp_dir = HOME_DIR / ".codex" / "mcp" / "facebook-mcp-server"
        c3 = add_folder_to_zip(zf, fb_mcp_dir, "_C_Drive_Backup/facebook-mcp-server")
        print(f"  + _C_Drive_Backup/facebook-mcp-server/: {c3} files (gồm cả .env & pages_vault.json)")
        total_files += c3

        # 4. Đóng gói AI Aff Video System (kèm SQLite aff_system.db)
        aff_sys_dir = HOME_DIR / ".gemini" / "antigravity" / "scratch" / "ai-aff-video-system"
        c4 = add_folder_to_zip(zf, aff_sys_dir, "_C_Drive_Backup/ai-aff-video-system")
        print(f"  + _C_Drive_Backup/ai-aff-video-system/: {c4} files (gồm cả aff_system.db)")
        total_files += c4

        # 5. Đóng gói các file cấu hình MCP
        cfg_files = [
            (HOME_DIR / ".gemini" / "config" / "mcp_config.json", "_C_Drive_Backup/gemini_config/mcp_config.json"),
            (HOME_DIR / ".gemini" / "antigravity" / "mcp_config.json", "_C_Drive_Backup/antigravity/mcp_config.json"),
            (HOME_DIR / ".codex" / "config.toml", "_C_Drive_Backup/codex/config.toml"),
        ]
        for src, arc in cfg_files:
            if src.exists():
                zf.write(src, arc)
                total_files += 1
                print(f"  + {arc}")

        # 6. Ghi kèm bộ script 1-click khôi phục trên máy nhà
        zf.writestr("restore_home_pc.ps1", RESTORE_PS1.encode("utf-8-sig"))
        zf.writestr("KHOI-PHUC-TREN-MAY-NHA.bat", RESTORE_BAT.encode("utf-8"))
        zf.writestr("HUONG-DAN-BUNG-NEN-MAY-NHA.txt", README_TXT.encode("utf-8"))
        total_files += 3

    size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"\n✅ ĐÓNG GÓI HOÀN TẤT!")
    print(f"   - Đường dẫn file Zip: {OUTPUT_ZIP}")
    print(f"   - Tổng số file     : {total_files} files")
    print(f"   - Dung lượng nén   : {size_mb:.2f} MB")


if __name__ == "__main__":
    main()
