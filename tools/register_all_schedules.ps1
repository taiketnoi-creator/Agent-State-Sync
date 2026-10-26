# ==============================================================================
# register_all_schedules.ps1 — Đăng ký tự động toàn bộ Lịch Chạy Ngầm Khi Mở Máy
# & 7 Mốc Thời Gian Vận Hành/Báo Cáo Hàng Ngày trên mọi máy (Máy Văn Phòng & Máy Nhà)
# ==============================================================================
$ErrorActionPreference = "Continue"

$subagentDir = Split-Path -Parent $PSScriptRoot
$engineScript = Join-Path $subagentDir "tools\mama_auto_scheduler_engine.py"
$botChromeScript = Join-Path $subagentDir "tools\start_bot_chrome.py"

$pyExe = "C:\Users\guicci\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
if (-not (Test-Path $pyExe)) {
    $pyExe = "python"
}

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$tasks = @(
    @{
        Name = "AgentJavis_0900_BootAndMorningReport"
        Time = "09:00"
        Mode = "boot-or-9am"
        Desc = "Mốc 09:00 sáng: Tự động bật Chrome Bot 9222, nạp lịch đăng 4 Page (11:45 & 20:00), gắn Pinned Comment #1, dọn kho 7 ngày & xuất Báo cáo 9h sáng"
    },
    @{
        Name = "AgentJavis_1145_MiddayPublishAndCare"
        Time = "11:45"
        Mode = "midday-1145"
        Desc = "Mốc 11:45 Trưa: Nghiệm thu bài đăng giờ vàng trưa trên 4 Page, gắn Pinned Comment #1 & tương tác nội bộ cụm 3 Page bán hàng"
    },
    @{
        Name = "AgentJavis_1200_Shift1GroupAndReport"
        Time = "12:00"
        Mode = "shift1-1200"
        Desc = "Mốc 12:00 Trưa: Tự động bật Chrome Bot 9222, Tương tác Hội nhóm 4 ngách Ca 1 & gửi Báo cáo Nghiệm thu Ca Trưa"
    },
    @{
        Name = "AgentJavis_1730_Shift2CareAndReport"
        Time = "17:30"
        Mode = "shift2-1730"
        Desc = "Mốc 17:30 Chiều: Tự động bật Chrome Bot 9222, chăm sóc bình luận & Tương tác Hội nhóm Ca 2 + Báo cáo Ca Chiều"
    },
    @{
        Name = "AgentJavis_2000_EveningPublishAndCare"
        Time = "20:00"
        Mode = "evening-2000"
        Desc = "Mốc 20:00 Tối: Nghiệm thu bài đăng giờ vàng tối trên 4 Page, gắn Pinned Comment #1 & tương tác nội bộ cụm 3 Page bán hàng"
    },
    @{
        Name = "AgentJavis_2030_Shift3GroupAndReport"
        Time = "20:30"
        Mode = "shift3-2030"
        Desc = "Mốc 20:30 Tối: Tự động bật Chrome Bot 9222, Tương tác Hội nhóm 4 ngách Ca 3 (Giờ Vàng Buổi Tối) & gửi Báo cáo Nghiệm thu Ca Tối"
    },
    @{
        Name = "AgentJavis_2130_EODSummaryReport"
        Time = "21:30"
        Mode = "eod-2130"
        Desc = "Mốc 21:30 Tối: Xuất Báo cáo Tổng kết Cuối ngày (EOD Report) đối chiếu KPI toàn hệ thống"
    }
)

foreach ($t in $tasks) {
    $action = New-ScheduledTaskAction -Execute $pyExe -Argument "`"$engineScript`" --mode $($t.Mode)" -WorkingDirectory $subagentDir
    if ($t.Mode -eq "boot-or-9am") {
        $trigger = @(
            (New-ScheduledTaskTrigger -Daily -At $t.Time),
            (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME)
        )
    } else {
        $trigger = New-ScheduledTaskTrigger -Daily -At $t.Time
    }
    Register-ScheduledTask -TaskName $t.Name -Action $action -Trigger $trigger -Settings $settings -Description $t.Desc -Force | Out-Null
    Write-Host "✅ Đã đăng ký Task: $($t.Name) (Mốc: $($t.Time) | StartWhenAvailable: True)" -ForegroundColor Green
}

# Tạo thêm Startup Script chạy ngầm ngay giây đầu tiên khi mở máy: tự bật Chrome Bot 9222 + chạy boot-or-9am
$startupDir = [Environment]::GetFolderPath("Startup")
$vbsPath = Join-Path $startupDir "AgentJavis_AutoBoot_OnStartup.vbs"
$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "$subagentDir"
WshShell.Run """$pyExe"" ""$botChromeScript""", 0, False
WshShell.Run """$pyExe"" ""$engineScript"" --mode boot-or-9am", 0, False
"@
Set-Content -Path $vbsPath -Value $vbsContent -Encoding Unicode
Write-Host "✅ Đã cài đặt Auto-Boot (Chrome Bot 9222 + Scheduler) ngay khi bật máy tại: $vbsPath" -ForegroundColor Cyan
