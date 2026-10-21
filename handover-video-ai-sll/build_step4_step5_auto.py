import os
import subprocess
import shutil

CAMP_DIR = r"f:\Ai Agent Setup\SubAgent\Subagent\campaigns\2026-10-21\quat-cam-tay-imi-5000mah"
KF_DIR = os.path.join(CAMP_DIR, "keyframes_v1")
RAW_SCENES_DIR = os.path.join(CAMP_DIR, "raw_scenes")
OVL_DIR = os.path.join(CAMP_DIR, "overlays")
OUT_DIR = os.path.join(CAMP_DIR, "outputs")
ART_DIR = r"C:\Users\Admin\.gemini\antigravity\brain\bbac4450-95dd-406a-9d31-4dce666ddac3"

BRAND_KIT = r"f:\Ai Agent Setup\SubAgent\Subagent\templates\remotion-cuongit-template\public\brand-kit"
BGM_PATH = os.path.join(BRAND_KIT, "bgm", "1.The Violins.mp3")
SFX_HOOK = os.path.join(BRAND_KIT, "sfx", "discord-notification.mp3")
SFX_TRUST = os.path.join(BRAND_KIT, "sfx", "apple-pay-sound.mp3")
VO_PATH = os.path.join(CAMP_DIR, "voiceover_v1.mp3")

for d in [RAW_SCENES_DIR, OVL_DIR, OUT_DIR]:
    os.makedirs(d, exist_ok=True)

# 1. Generate transparent 1080x1920 PNG overlays via PowerShell System.Drawing
ps_overlay_script = rf'''
Add-Type -AssemblyName System.Drawing

function New-Canvas {{
    $bmp = New-Object System.Drawing.Bitmap(1080, 1920, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.Color]::Transparent)
    return @($bmp, $g)
}}

# A. OVERLAY 1: HOOK "CHÚ Ý!" (0.0s - 2.6s)
$res = New-Canvas
$bmp = $res[0]; $g = $res[1]
$path = New-Object System.Drawing.Drawing2D.GraphicsPath
$rect = New-Object System.Drawing.Rectangle(190, 140, 700, 155)
$path.AddArc($rect.X, $rect.Y, 60, 60, 180, 90)
$path.AddArc($rect.Right - 60, $rect.Y, 60, 60, 270, 90)
$path.AddArc($rect.Right - 60, $rect.Bottom - 60, 60, 60, 0, 90)
$path.AddArc($rect.X, $rect.Bottom - 60, 60, 60, 90, 90)
$path.CloseFigure()

$shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(160, 0, 0, 0))
$g.FillRectangle($shadowBrush, 205, 155, 700, 155)

$gradBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, [System.Drawing.Color]::FromArgb(255, 235, 30, 30), [System.Drawing.Color]::FromArgb(255, 180, 0, 0), 45)
$g.FillPath($gradBrush, $path)
$penYellow = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 230, 0), 8)
$g.DrawPath($penYellow, $path)

$sf = New-Object System.Drawing.StringFormat
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center
$fontHook = New-Object System.Drawing.Font("Segoe UI", 64, [System.Drawing.FontStyle]::Bold)
$whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 245, 100))
$g.DrawString("CHÚ Ý!", $fontHook, $whiteBrush, (New-Object System.Drawing.RectangleF(190, 140, 700, 155)), $sf)

$bmp.Save("{OVL_DIR}\overlay_hook_chu_y.png", [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

# B. OVERLAY 2: TOP-RIGHT LOGO "iMI TURBO 120" (17.5s - 39.9s)
$res = New-Canvas
$bmp = $res[0]; $g = $res[1]
$rectLogo = New-Object System.Drawing.Rectangle(730, 80, 290, 86)
$bgLogo = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(175, 15, 23, 42))
$penLogo = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(220, 96, 165, 250), 3)
$g.FillRectangle($bgLogo, $rectLogo)
$g.DrawRectangle($penLogo, $rectLogo)
$fontLogo = New-Object System.Drawing.Font("Segoe UI", 28, [System.Drawing.FontStyle]::Bold)
$cyanBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$g.DrawString("iMI • 120 SPEED", $fontLogo, $cyanBrush, (New-Object System.Drawing.RectangleF(730, 80, 290, 86)), $sf)
$bmp.Save("{OVL_DIR}\overlay_logo_imi.png", [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

# C. OVERLAY 3: 3D GOLD SHIELD WARRANTY (28.0s - 33.5s)
$res = New-Canvas
$bmp = $res[0]; $g = $res[1]
$rectShield = New-Object System.Drawing.Rectangle(540, 620, 490, 320)
$shadowShield = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(180, 0, 0, 0))
$g.FillRectangle($shadowShield, 555, 635, 490, 320)

$gradGold = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rectShield, [System.Drawing.Color]::FromArgb(245, 30, 41, 59), [System.Drawing.Color]::FromArgb(245, 15, 23, 42), 90)
$g.FillRectangle($gradGold, $rectShield)
$penGold = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 250, 204, 21), 7)
$g.DrawRectangle($penGold, $rectShield)

$goldBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 250, 204, 21))
$whiteText = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$fontTitle = New-Object System.Drawing.Font("Segoe UI", 32, [System.Drawing.FontStyle]::Bold)
$fontSub = New-Object System.Drawing.Font("Segoe UI", 26, [System.Drawing.FontStyle]::Bold)

$g.DrawString("CHÍNH HÃNG iMI", $fontTitle, $goldBrush, (New-Object System.Drawing.RectangleF(540, 645, 490, 70)), $sf)
$g.DrawString("PIN TRÂU 5000mAh", $fontSub, $whiteText, (New-Object System.Drawing.RectangleF(540, 735, 490, 70)), $sf)
$g.DrawString("BẢO HÀNH UY TÍN", $fontSub, $goldBrush, (New-Object System.Drawing.RectangleF(540, 815, 490, 70)), $sf)

$bmp.Save("{OVL_DIR}\overlay_shield_warranty.png", [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output "Generated 3 PNG overlays successfully."
'''

ps_file = os.path.join(CAMP_DIR, "make_overlays.ps1")
with open(ps_file, "w", encoding="utf-8-sig") as f:
    f.write(ps_overlay_script)

subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], check=True)

# 2. Generate 8 animated 9:16 video clips (Step 4 Motion Clips) matching exact voiceover beats
# Beats:
# Scene 1: 0.00 - 2.80s (2.80s)
# Scene 2: 2.80 - 7.40s (4.60s)
# Scene 3: 7.40 - 12.71s (5.31s)
# Scene 4: 12.71 - 17.49s (4.78s)
# Scene 5: 17.49 - 22.73s (5.24s)
# Scene 6: 22.73 - 28.09s (5.36s)
# Scene 7: 28.09 - 33.43s (5.34s)
# Scene 8: 33.43 - 39.92s (6.49s)

scenes_spec = [
    ("scene_01_hook.jpg", 2.80, "zoom_in"),
    ("scene_02_pain.jpg", 4.60, "zoom_out"),
    ("scene_03_hero_anchor.jpg", 5.31, "zoom_in"),
    ("scene_04_broll_hair_wind.jpg", 4.78, "pan_right"),
    ("scene_05_broll_macro_turbine.jpg", 5.24, "zoom_in"),
    ("scene_06_broll_finger_touch.jpg", 5.36, "zoom_out"),
    ("scene_07_broll_trust_hero.jpg", 5.34, "zoom_in"),
    ("scene_08_payoff_cta.jpg", 6.49, "zoom_in"),
]

clip_paths = []
for idx, (img_name, dur, motion) in enumerate(scenes_spec, 1):
    in_img = os.path.join(KF_DIR, img_name)
    out_clip = os.path.join(RAW_SCENES_DIR, f"scene_{idx:02d}.mp4")
    frames = int(round(dur * 30))
    if motion == "zoom_in":
        zp = f"zoompan=z='min(zoom+0.0012,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    elif motion == "zoom_out":
        zp = f"zoompan=z='if(eq(on,1),1.14,max(1.0,zoom-0.0010))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    else:
        zp = f"zoompan=z='1.10':x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", in_img,
        "-vf", f"scale=1200:2134,{zp},format=yuv420p",
        "-t", f"{dur:.2f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        out_clip
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clip_paths.append(out_clip)
    print(f"Rendered Step 4 motion clip {idx}/8: {out_clip} ({dur}s)")

# 3. Create ASS subtitle file (1-line clauses, crisp Vietnamese typography in lower third)
ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Segoe UI,54,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,60,60,230,1
Style: Highlight,Segoe UI,56,&H0000FF87,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,60,60,230,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.10,0:00:02.80,Highlight,,0,0,0,,Ra đường trời nắng gắt mồ hôi chảy ròng ròng
Dialogue: 0,0:00:02.80,0:00:05.20,Default,,0,0,0,,dùng quạt nhựa kiểu cũ thì gió vừa yếu
Dialogue: 0,0:00:05.20,0:00:07.40,Default,,0,0,0,,lại vừa nhanh hết pin cực kỳ bất tiện!
Dialogue: 0,0:00:07.40,0:00:10.20,Highlight,,0,0,0,,Đổi ngay sang quạt cầm tay phản lực iMI
Dialogue: 0,0:00:10.20,0:00:12.71,Default,,0,0,0,,phiên bản 120 cấp độ gió này đi mọi người ơi!
Dialogue: 0,0:00:12.71,0:00:15.20,Default,,0,0,0,,Công nghệ lốc xoáy tuốc bin thổi gió cực mạnh
Dialogue: 0,0:00:15.20,0:00:17.49,Highlight,,0,0,0,,làm mát tức thì chỉ sau vài giây!
Dialogue: 0,0:00:17.49,0:00:20.20,Default,,0,0,0,,Điểm ăn tiền nhất là màn hình LED thông minh
Dialogue: 0,0:00:20.20,0:00:22.73,Highlight,,0,0,0,,báo rõ mức gió 120 và phần trăm pin
Dialogue: 0,0:00:22.73,0:00:25.40,Default,,0,0,0,,Nút bấm điều chỉnh mượt mà, vỏ ánh kim nhỏ gọn
Dialogue: 0,0:00:25.40,0:00:28.09,Default,,0,0,0,,bỏ túi xách mang đi đâu cũng sang!
Dialogue: 0,0:00:28.09,0:00:30.80,Highlight,,0,0,0,,Dung lượng pin lớn 5000mAh kèm sạc USB
Dialogue: 0,0:00:30.80,0:00:33.43,Default,,0,0,0,,dùng bền bỉ suốt cả ngày dài không lo hết pin
Dialogue: 0,0:00:33.43,0:00:36.42,Default,,0,0,0,,Đi học, đi làm hay du lịch đều mát rượi!
Dialogue: 0,0:00:36.42,0:00:39.90,Highlight,,0,0,0,,Bấm ngay giỏ hàng bên dưới săn giá ưu đãi nhé!
"""

ass_path = os.path.join(CAMP_DIR, "subtitles_v1.ass")
with open(ass_path, "w", encoding="utf-8-sig") as f:
    f.write(ass_content)

# 4. Concatenate the 8 clips
concat_list = os.path.join(CAMP_DIR, "concat_list.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for cp in clip_paths:
        f.write("file '" + cp.replace("\\", "/") + "'\n")

stitched_video = os.path.join(CAMP_DIR, "stitched_raw.mp4")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", stitched_video
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 5. Final Step 5 Commercial Assembly (Overlays + Subtitles + Master Voice + BGM + SFX)
final_output = os.path.join(OUT_DIR, "quat_cam_tay_imi_v1_commercial.mp4")
ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")

filter_complex = (
    "[0:v][1:v]overlay=0:0:enable='between(t,0.1,2.6)'[v1];"
    "[v1][2:v]overlay=0:0:enable='between(t,17.5,39.9)'[v2];"
    "[v2][3:v]overlay=0:0:enable='between(t,28.1,33.4)'[v3];"
    f"[v3]ass='{ass_escaped}'[vout];"
    "[4:a]volume=1.0[vo];"
    "[5:a]volume=0.14,afade=t=out:st=36:d=3.9[bgm];"
    "[6:a]adelay=150|150,volume=0.8[sfx1];"
    "[7:a]adelay=28100|28100,volume=0.9[sfx2];"
    "[vo][bgm][sfx1][sfx2]amix=inputs=4:duration=first:dropout_transition=2[aout]"
)

cmd_final = [
    "ffmpeg", "-y",
    "-i", stitched_video,
    "-i", os.path.join(OVL_DIR, "overlay_hook_chu_y.png"),
    "-i", os.path.join(OVL_DIR, "overlay_logo_imi.png"),
    "-i", os.path.join(OVL_DIR, "overlay_shield_warranty.png"),
    "-i", VO_PATH,
    "-i", BGM_PATH,
    "-i", SFX_HOOK,
    "-i", SFX_TRUST,
    "-filter_complex", filter_complex,
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    final_output
]
subprocess.run(cmd_final, check=True)
shutil.copy2(final_output, os.path.join(ART_DIR, "quat_cam_tay_imi_v1_commercial.mp4"))
print("SUCCESS! Final video saved to:", final_output)
