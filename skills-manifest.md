# Skills manifest — Agent Javis

Danh sách skill bên ngoài mà project cần để tái tạo workflow trên máy khác. File này chỉ ghi nguồn cài và metadata; không chứa token, session, database hoặc bản sao toàn bộ thư mục `.codex`.

## Skill bắt buộc

| Tên skill | Dùng cho | Nguồn cài hiện tại | Phiên bản | Trạng thái kiểm tra | Thư mục cài trên máy đích |
|---|---|---|---|---|---|
| `ai-affiliate-page-operator` | Nghiên cứu niche/SKU, lập kế hoạch và vận hành Page AI Affiliate tại Việt Nam | Gói skill cục bộ Codex: `C:\Users\guicci\.codex\skills\ai-affiliate-page-operator\` | `UNVERSIONED` — package không có trường version; kiểm tra 2026-10-13 | Bắt buộc cho workflow Page/affiliate | `C:\Users\<user>\.codex\skills\ai-affiliate-page-operator\` |

### Tệp tham chiếu bắt buộc của skill

- `SKILL.md`
- `references/niche-product-research.md`

Các agent liên quan: `mama`, `mkt`, `content`, `edit`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`.

## Cách cài trên máy khác

1. Cài/đồng bộ package `ai-affiliate-page-operator` vào thư mục `.codex/skills/` của user trên máy mới.
2. Kiểm tra hai tệp `SKILL.md` và `references/niche-product-research.md` có mặt.
3. Đối chiếu skill với manifest này; nếu package có version hoặc nguồn Git chính thức, cập nhật cột `Phiên bản` và `Nguồn cài` trước khi dùng.
4. Mở project Agent-Javis và để agent đọc skill trước các task Page/affiliate.

## Quy tắc đồng bộ

- Không commit `C:\Users\<user>\.codex` toàn bộ vào project.
- Không đưa `auth.json`, `cap_sid`, token, cookie, session, SQLite, log hoặc cache vào Git.
- Nếu skill được nâng cấp, ghi version/ngày kiểm tra mới và rà lại các memory/training phụ thuộc nó.
- Nếu cần chia sẻ source skill tự phát triển, đặt source ở repository riêng có version/tag; manifest chỉ trỏ tới source đó.
