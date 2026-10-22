#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PS_UIA = r"""
Add-Type -AssemblyName UIAutomationClient,UIAutomationTypes
$root = [System.Windows.Automation.AutomationElement]::RootElement
$cond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button)
$btns = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cond)
foreach ($b in $btns) {
    $n = $b.Current.Name
    if ($n -ne '') { Write-Host "BTN: $n" }
    if ($n -match 'Allow|Cho phép|Chấp nhận') {
        try {
            $inv = $b.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
            $inv.Invoke()
            Write-Host "INVOKED_ALLOW: $n"
        } catch {
            Write-Host "ERR_INVOKE: $_"
        }
    }
}
"""


def main():
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.Popen([chrome_exe, "--profile-directory=Profile 1", "https://www.facebook.com"])
    time.sleep(3.5)

    port_file = Path.home() / "AppData/Local/Google/Chrome/User Data/DevToolsActivePort"
    lines = port_file.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
    ws = f"ws://127.0.0.1:{lines[0].strip()}{lines[1].strip()}"
    print("WS:", ws)

    def try_connect():
        try:
            with sync_playwright() as p:
                b = p.chromium.connect_over_cdp(ws, timeout=15000)
                print("CONNECTED_OK:", [pg.url for pg in b.contexts[0].pages])
        except Exception as e:
            print("CONN_ERR:", e)

    t = threading.Thread(target=try_connect)
    t.start()
    time.sleep(2.0)
    subprocess.run(["powershell", "-NoProfile", "-Command", PS_UIA])
    t.join(timeout=12)


if __name__ == "__main__":
    main()
