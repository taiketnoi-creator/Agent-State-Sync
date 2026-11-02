param(
    [int]$Shift = 3,
    [string]$Indices = "0,1,2",
    [int]$ReplyTask = 0
)

$subagentDir = Split-Path -Parent $PSScriptRoot
$pyScript = Join-Path $subagentDir "tools\mama_daily_group_and_eod.py"
$pyExe = "C:\Users\guicci\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
if (-not (Test-Path $pyExe)) {
    $pyExe = "python"
}

$argList = "`"$pyScript`" --shift $Shift --indices `"$Indices`" --send-telegram"
if ($ReplyTask -gt 0) {
    $argList += " --reply-task $ReplyTask"
}

Start-Process -FilePath $pyExe -ArgumentList $argList -WorkingDirectory $subagentDir -WindowStyle Hidden
