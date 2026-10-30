@echo off
chcp 65001 >nul
title AI Office - Van phong ao 3D Agent-Javis
cd /d "%~dp0"
set "PATH=C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs;%APPDATA%\npm;%PATH%"
where node >nul 2>nul || (echo Chua cai Node.js. & pause & exit /b 1)
if not exist "node_modules\three" (
  echo Dang cai dat thu vien 3D lan dau...
  call npm install --no-audit --no-fund
)
start "" cmd /c "timeout /t 2 >nul & start http://localhost:4800"
node --experimental-transform-types src/server.ts
if %errorlevel%==3 (timeout /t 6 >nul & exit /b 0)
:lai
echo.
echo [%date% %time%] May chu van phong da dung. Tu mo lai sau 5 giay...
echo (Muon tat han: dong cua so nay. Xem loi trong data\server.log)
timeout /t 5 >nul
node --experimental-transform-types src/server.ts
if %errorlevel%==3 (timeout /t 6 >nul & exit /b 0)
goto lai
