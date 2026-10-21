param(
    [int]$Shift = 3,
    [string]$Indices = "0,1,2",
    [int]$ReplyTask = 0
)

$subagentDir = "f:\Ai Agent Setup\SubAgent\Subagent"
$pyScript = "$subagentDir\tools\mama_daily_group_and_eod.py"

Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes

$argList = "`"$pyScript`" --shift $Shift --indices `"$Indices`" --send-telegram"
if ($ReplyTask -gt 0) {
    $argList += " --reply-task $ReplyTask"
}

$proc = Start-Process -FilePath "python" -ArgumentList $argList -WorkingDirectory $subagentDir -WindowStyle Hidden -PassThru

# Auto-Allow Chrome Remote Debugging prompt in Session 6
for ($i = 0; $i -lt 6; $i++) {
    Start-Sleep -Milliseconds 1000
    try {
        $root = [System.Windows.Automation.AutomationElement]::RootElement
        $cond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button)
        $buttons = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cond)
        foreach ($btn in $buttons) {
            $name = $btn.Current.Name
            if ($name -and ($name -match "^Cho ph" -or $name -eq "Allow")) {
                try {
                    $inv = $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
                    $inv.Invoke()
                } catch {}
            }
        }
    } catch {}
}
