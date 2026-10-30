# ==============================================================================
# register_all_schedules.ps1 — Đăng ký tự động toàn bộ Lịch Chạy Ngầm Khi Mở Máy
# & 7 Mốc Thời Gian Vận Hành/Báo Cáo Hàng Ngày trên mọi máy (Máy Văn Phòng & Máy Nhà)
# QUY TẮC:
# - KHÔNG tự mở Chrome khi bật máy (đã xóa start_bot_chrome.py khỏi Startup VBS).
# - 3 Ca tương tác trình duyệt (12:00, 17:30, 20:30) chạy ngầm 100% (--headless=new)
#   đúng giờ định sẵn, KHÔNG chạy bù khi bật máy muộn và tự đóng ngay sau ca.
# ==============================================================================
$ErrorActionPreference = "Continue"

$subagentDir = Split-Path -Parent $PSScriptRoot
$engineScript = Join-Path $subagentDir "tools\mama_auto_scheduler_engine.py"

$pyExe = "C:\Users\guicci\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
if (-not (Test-Path $pyExe)) {
    $pyExe = "python"
}

$settingsCatchUp = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$settingsStrictTime = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

$tasks = @(
    @{
        Name = "AgentJavis_0900_BootAndMorningReport"
        Time = "09:00"
        Mode = "boot-or-9am"
        CatchUp = $true
        Desc = "Mốc 09:00 sáng: Kiểm tra lịch đăng 4 Page qua Graph API, gắn Pinned Comment #1 & xuất Báo cáo 9h sáng (KHÔNG mở Chrome)"
    },
    @{
        Name = "AgentJavis_1145_MiddayPublishAndCare"
        Time = "11:45"
        Mode = "midday-1145"
        CatchUp = $true
        Desc = "Mốc 11:45 Trưa: Nghiệm thu bài đăng giờ vàng trưa trên 4 Page & gắn Pinned Comment #1 qua Graph API"
    },
    @{
        Name = "AgentJavis_1200_Shift1GroupAndReport"
        Time = "12:00"
        Mode = "shift1-1200"
        CatchUp = $false
        Desc = "Mốc 12:00 Trưa: Chạy ngầm 100% (--headless=new) Chrome Bot 9222, Tương tác Hội nhóm Ca 1 rồi tự đóng trình duyệt"
    },
    @{
        Name = "AgentJavis_1730_Shift2CareAndReport"
        Time = "17:30"
        Mode = "shift2-1730"
        CatchUp = $false
        Desc = "Mốc 17:30 Chiều: Chạy ngầm 100% (--headless=new) Chrome Bot 9222, Tương tác Hội nhóm Ca 2 rồi tự đóng trình duyệt"
    },
    @{
        Name = "AgentJavis_2000_EveningPublishAndCare"
        Time = "20:00"
        Mode = "evening-2000"
        CatchUp = $true
        Desc = "Mốc 20:00 Tối: Nghiệm thu bài đăng giờ vàng tối trên 4 Page & gắn Pinned Comment #1 qua Graph API"
    },
    @{
        Name = "AgentJavis_2030_Shift3GroupAndReport"
        Time = "20:30"
        Mode = "shift3-2030"
        CatchUp = $false
        Desc = "Mốc 20:30 Tối: Chạy ngầm 100% (--headless=new) Chrome Bot 9222, Tương tác Hội nhóm Ca 3 rồi tự đóng trình duyệt"
    },
    @{
        Name = "AgentJavis_2130_EODSummaryReport"
        Time = "21:30"
        Mode = "eod-2130"
        CatchUp = $true
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
    $taskSettings = if ($t.CatchUp) { $settingsCatchUp } else { $settingsStrictTime }
    Register-ScheduledTask -TaskName $t.Name -Action $action -Trigger $trigger -Settings $taskSettings -Description $t.Desc -Force | Out-Null
    Write-Host "✅ Đã đăng ký Task: $($t.Name) (Mốc: $($t.Time) | CatchUp: $($t.CatchUp))" -ForegroundColor Green
}

# Gỡ bỏ các Task cũ lỗi thời nếu còn tồn tại trên máy
foreach ($oldTask in @("AgentJavis_ClickAllowCDP", "MamaSession6")) {
    if (Get-ScheduledTask -TaskName $oldTask -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $oldTask -Confirm:$false -ErrorAction SilentlyContinue
        Write-Host "🗑️ Đã gỡ bỏ Scheduled Task cũ: $oldTask" -ForegroundColor Yellow
    }
}

# Cập nhật Startup Script khi mở máy: CHỈ chạy ngầm đồng bộ Git & kiểm tra Graph API (TUYỆT ĐỐI KHÔNG tự mở Chrome!)
$startupDir = [Environment]::GetFolderPath("Startup")
$vbsPath = Join-Path $startupDir "AgentJavis_AutoBoot_OnStartup.vbs"
$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "$subagentDir"
WshShell.Run """$pyExe"" ""$engineScript"" --mode boot-or-9am", 0, False
"@
Set-Content -Path $vbsPath -Value $vbsContent -Encoding Unicode
Write-Host "✅ Đã cập nhật Auto-Boot (Đã TẮT hoàn toàn việc tự mở Chrome khi bật máy) tại: $vbsPath" -ForegroundColor Cyan
