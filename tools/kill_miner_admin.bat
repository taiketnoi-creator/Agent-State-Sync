@echo off
chcp 65001 >nul
:: Tu dong yeu cau quyen Administrator (UAC) de tat tien trinh gia svchost.exe (PID 10924) dang ngon 800% CPU
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo =====================================================================
echo   DANG TAT TIEN TRINH DAO COIN AN (svchost.exe PID 10924 - 800%% CPU)
echo =====================================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "d:\Phiên bản Ai agent\Subagent\tools\kill_miner_admin.ps1"
echo.
echo [HOAN TAT] CPU da duoc giai phong 100%%! Cua so nay se tu dong sau 3 giay...
timeout /t 3 >nul
