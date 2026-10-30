# Clean up all 4 stealth coinminer components with Administrator privileges
Write-Host "1. Dang tim va tat cac tien trinh dao coin gia mao Windows..." -ForegroundColor Cyan
Get-Process -Name "LockAppHost*", "MusNotification*", "UsoClient*", "SmartScreenHost*", "CompatTelRunner" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

$servicesPid = (Get-Process -Name 'services' -ErrorAction SilentlyContinue).Id
Get-CimInstance Win32_Process -Filter "Name='svchost.exe'" | Where-Object {
    $_.ParentProcessId -ne $servicesPid
} | ForEach-Object {
    Write-Host " -> Diet svchost.exe gia mao (PID: $($_.ProcessId))" -ForegroundColor Yellow
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

Write-Host "2. Dang xoa cac Scheduled Tasks va Services doc hai..." -ForegroundColor Cyan
schtasks /End /TN "\DeviceMetadataRetrieval_e122" 2>$null
schtasks /Delete /TN "\DeviceMetadataRetrieval_e122" /F 2>$null
schtasks /End /TN "\ScheduledDefragmentation_1f05" 2>$null
schtasks /Delete /TN "\ScheduledDefragmentation_1f05" /F 2>$null

Get-ScheduledTask | ForEach-Object {
    $t = $_
    foreach ($a in $t.Actions) {
        if ($a.Execute -match 'Network3F73|90D7B00F|B2A4528A|73BF5F50|SmartScreenHost27dac|UsoClient34ed49|MusNotificationce794c|LockAppHost14a02b') {
            Write-Host " -> Xoa Scheduled Task doc hai: $($t.TaskPath)$($t.TaskName)" -ForegroundColor Yellow
            Stop-ScheduledTask -InputObject $t -ErrorAction SilentlyContinue
            Unregister-ScheduledTask -InputObject $t -Confirm:$false -ErrorAction SilentlyContinue
        }
    }
}

Get-CimInstance Win32_Service | Where-Object {
    $_.PathName -match 'Network3F73|90D7B00F|B2A4528A|73BF5F50|SmartScreenHost27dac|UsoClient34ed49|MusNotificationce794c|LockAppHost14a02b'
} | ForEach-Object {
    Write-Host " -> Xoa Service doc hai: $($_.Name)" -ForegroundColor Yellow
    Stop-Service -Name $_.Name -Force -ErrorAction SilentlyContinue
    sc.exe delete $_.Name | Out-Null
}

Write-Host "3. Dang xoa va khoa cung (Immunize) 4 thu muc chua ma doc..." -ForegroundColor Cyan
$folders = @(
    'C:\ProgramData\Microsoft\Network\Diagnostics\73BF5F50',
    'C:\Users\guicci\AppData\Roaming\Network3F73',
    'C:\Users\guicci\AppData\Roaming\qivolab-tq4owh',
    'C:\Users\guicci\AppData\Local\Microsoft\Windows\Themes\90D7B00F',
    'C:\Users\guicci\AppData\Local\Microsoft\Windows\AppRepository\B2A4528A'
)
foreach ($f in $folders) {
    takeown /F $f /R /D Y >$null 2>&1
    icacls $f /reset /T >$null 2>&1
    Remove-Item -Path $f -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $f -Force -ErrorAction SilentlyContinue | Out-Null
    icacls $f /deny "Everyone:(OI)(CI)(F)" >$null 2>&1
    Write-Host " -> Da xoa & khoa cung: $f" -ForegroundColor Green
}

Write-Host "`n[HOAN TAT 100%] Da diet tan goc 4 o ma doc dao coin ngam!" -ForegroundColor Green
Start-Sleep -Seconds 3
