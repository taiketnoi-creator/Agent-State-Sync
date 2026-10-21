# Hướng dẫn cài đặt Agent Javis trên máy mới

Tài liệu này dùng sau khi clone repository `Agent-Javis` trên máy Windows mới. Mục tiêu là khôi phục môi trường để đọc tài liệu, chạy agent và dựng video AI; không đưa credential hoặc file render nặng vào Git.

Ngày rà soát: 2026-10-13  
Repository: `https://github.com/taiketnoi-creator/Agent-Javis.git`  
Nhánh mặc định: `main`

## 1. Những gì nằm trong Git và những gì không

Git chứa source, Markdown, training, campaign brief, JSON/TypeScript/Python, asset nguồn nhỏ, font đã được cấp quyền và lockfile. Git không chứa token, session, database Codex, cache, `node_modules`, video render, voiceover sinh ra hoặc thư mục `out/`.

Skill Codex không tự xuất hiện chỉ vì clone project. Cài các skill cần thiết theo [skills-manifest.md](skills-manifest.md), vào thư mục `.codex/skills/` của user trên máy mới.

## 2. Phần mềm bắt buộc

| Thành phần | Dùng cho | Kiểm tra |
|---|---|---|
| Windows 10/11 64-bit | Môi trường đã được kiểm tra | `winver` |
| Git | Clone, pull, commit và đồng bộ | `git --version` |
| Python 3.11+ | Script tạo voice và tiện ích xử lý | `py --version` |
| Node.js LTS | Remotion/React video pipeline | `node --version` |
| pnpm hỗ trợ lockfile v9 | Cài dependency Remotion | `pnpm --version` |
| FFmpeg | Encode, mux, inspect và product-video-editor | `ffmpeg -version` |
| Codex Desktop/CLI | Chạy agent, skill và tool | Mở được project trong Codex |

Khuyến nghị cài bằng Windows Package Manager hoặc installer chính thức. Không chép thư mục `.codex` của máy cũ sang máy mới vì trong đó có credential, session và database riêng.

## 3. Clone project

Mở PowerShell:

```powershell
Set-Location 'D:\Phiên bản Ai agent'
git clone https://github.com/taiketnoi-creator/Agent-Javis.git
Set-Location '.\Agent-Javis'
git switch main
git pull --ff-only
```

Nếu thư mục đã tồn tại:

```powershell
Set-Location 'D:\Phiên bản Ai agent\Agent-Javis'
git status
git pull --ff-only
```

Không chạy `git reset --hard` để xử lý khác biệt khi chưa xác định file nào thuộc về người dùng.

## 4. Cài skill Codex

Đọc [skills-manifest.md](skills-manifest.md). Skill tối thiểu cho workflow Page/Affiliate là `ai-affiliate-page-operator`.

Đích cài trên máy mới:

```text
C:\Users\<user>\.codex\skills\ai-affiliate-page-operator\
```

Sau khi cài, kiểm tra hai file:

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\ai-affiliate-page-operator\SKILL.md"
Test-Path "$env:USERPROFILE\.codex\skills\ai-affiliate-page-operator\references\niche-product-research.md"
```

Nếu skill là package nội bộ chưa có nguồn tải tự động, lấy source skill từ kho backup/repository được cấp quyền; không lấy `auth.json`, `cap_sid`, cookie, session hoặc toàn bộ `.codex`.

## 5. Tạo môi trường Python cho voice

Script Remotion voice hiện dùng `gTTS` và `imageio-ffmpeg`. Tạo virtual environment riêng trong project hoặc ngoài project; nếu tạo trong project, thư mục `.venv/` phải được ignore.

```powershell
Set-Location 'D:\Phiên bản Ai agent\Agent-Javis'
py -3.11 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install gTTS imageio-ffmpeg
```

Kiểm tra:

```powershell
python -c "from gtts import gTTS; import imageio_ffmpeg; print('Python voice dependencies: OK')"
```

`gTTS` cần mạng khi tạo voice. Trước khi dùng thương mại phải kiểm tra điều khoản hiện hành và ghi provider/license trong audio manifest. Không clone giọng người thật.

## 6. Cài dependency Remotion

Project video mẫu nằm tại:

```text
campaigns/2026-10-12/ai-players-personal-brand/video-test-01/remotion-video-slide/
```

Sau khi cài Node.js LTS và pnpm hỗ trợ lockfile v9:

```powershell
Set-Location 'D:\Phiên bản Ai agent\Agent-Javis\campaigns\2026-10-12\ai-players-personal-brand\video-test-01\remotion-video-slide'
pnpm install --frozen-lockfile
pnpm exec remotion --version
```

Nếu `pnpm` chưa có, cài qua Corepack hoặc trình quản lý package được đội duyệt, sau đó chạy lại `pnpm install --frozen-lockfile`. Không commit `node_modules/`, pnpm store hoặc `out/`.

Render thử chỉ tạo output cục bộ:

```powershell
pnpm run render
```

Output video phải nằm trong `out/` hoặc thư mục render cục bộ; không đưa MP4/MOV lên Git.

## 7. FFmpeg và công cụ video

Kiểm tra FFmpeg hệ thống:

```powershell
ffmpeg -version
ffprobe -version
```

FFmpeg dùng cho mux voice, encode, kiểm tra metadata và workflow `product-video-editor`. `imageio-ffmpeg` trong virtual environment chỉ hỗ trợ một số script Python, không thay thế việc kiểm tra FFmpeg hệ thống cho toàn pipeline.

CapCut Desktop hoặc phần mềm dựng thủ công là tùy chọn, chỉ cần khi task yêu cầu bàn giao CapCut/EDL. Remotion + FFmpeg là pipeline mặc định cho video slide trong repository.

## 8. Voice và hình ảnh

- Voice: dùng TTS được phép sử dụng như provider đã được ghi trong manifest; không đưa API key vào Markdown/Git.
- Hình ảnh AI: dùng skill/image tool đã cài trong Codex hoặc nguồn asset có quyền. Ảnh AI chỉ là minh họa nếu chưa có bằng chứng sản phẩm; phải gắn nhãn `Minh họa bằng AI` khi có nguy cơ bị hiểu là cảnh thật.
- Font và asset nguồn của video slide đã nằm trong `assets/` hoặc thư mục project. Kiểm tra license trước khi phân phối thương mại.
- Nhạc/SFX phải có license hoặc được đánh dấu `NEEDS_LICENSE`; không tải nhạc không rõ quyền sử dụng.

## 9. Kết nối ngoài và secrets

Không đặt token/password trong file Markdown, Git hoặc prompt. Tạo secrets bằng secret manager/environment của runtime trên từng máy mới.

Các kết nối chỉ cần khi task thực sự yêu cầu:

- Facebook/Meta: Page ID và quyền tối thiểu cho draft/publish/comment.
- YouTube: channel/OAuth scope tối thiểu.
- Shopee Affiliate: tài khoản/link route/UTM và disclosure.
- Browser/connector: đăng nhập riêng trên máy mới; không sao chép cookie/session.

Mặc định toàn đội chạy `DRAFT_ONLY`. Chỉ publish sau dry-run và CEO approval.

## 10. Smoke test sau cài đặt

Chạy lần lượt:

```powershell
Set-Location 'D:\Phiên bản Ai agent\Agent-Javis'
git status
py --version
python -c "import gtts, imageio_ffmpeg; print('Python: OK')"
node --version
pnpm --version
ffmpeg -version
Test-Path '.\knowledge\brand_guidelines.md'
Test-Path '.\campaigns\2026-10-12\ai-players-personal-brand\page-brief.md'
```

Sau đó vào thư mục Remotion và chạy `pnpm install --frozen-lockfile`, `pnpm exec remotion --version`, rồi mới render preview. Kiểm tra preview ở đầu–giữa–cuối, voice, caption, safe zone và metadata trước khi bàn giao.

## 11. Checklist nghiệm thu máy mới

- [ ] Clone đúng repository và nhánh `main`.
- [ ] Git, Python, Node.js LTS, pnpm và FFmpeg hoạt động.
- [ ] Skill trong `skills-manifest.md` đã cài đúng user.
- [ ] Virtual environment Python có `gTTS` và `imageio-ffmpeg`.
- [ ] Remotion cài dependency bằng lockfile, không lỗi `pnpm install --frozen-lockfile`.
- [ ] Font/asset nguồn đọc được; license đã được ghi nhận.
- [ ] Chạy được smoke test và render preview cục bộ.
- [ ] Không có credential, session, database, `node_modules`, cache hoặc output render trong Git.
- [ ] Agent chạy dry-run ở `DRAFT_ONLY` trước khi kết nối nền tảng thật.
