import tempfile, subprocess, os
from pathlib import Path
from PIL import Image

browser = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
with tempfile.TemporaryDirectory() as tmpdir:
    html_file = Path(tmpdir) / 'test.html'
    raw_png = Path(tmpdir) / 'test.png'
    user_data_dir = Path(tmpdir) / 'chrome_user_data'
    html_file.write_text('<!DOCTYPE html><html><body style="background:#0b0c0e;color:#CCFF00;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;"><h1>TEST RENDER OK</h1></body></html>', encoding='utf-8')
    cmd = [
        browser,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--user-data-dir={user_data_dir}',
        '--window-size=1080,1080',
        f'--screenshot={raw_png}',
        str(html_file)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('Return code:', res.returncode)
    print('File exists:', raw_png.exists())
    if raw_png.exists():
        with Image.open(raw_png) as im:
            print('Image size:', im.size)
