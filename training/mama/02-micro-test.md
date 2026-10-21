# Bước 2 — Micro-test

## Đề bài CEO

> “Tuần này tôi muốn ra một chiến dịch video AI bán đồ gia dụng mini tiện ích mùa mưa cho sinh viên trên FB Reels và YouTube Shorts. Hãy lập kế hoạch và phân bổ việc cho các Subagent.”

## Kế hoạch điều phối

Mục tiêu chuẩn hóa: tạo một campaign package dạng draft cho sinh viên Việt Nam trong bối cảnh mùa mưa, gồm shortlist sản phẩm đã xác minh, kịch bản, production pack và copy cho Facebook Reels/YouTube Shorts. Không publish, không chi tiền và không tự điền dữ liệu chưa xác minh.

| Wave/Gate | Owner | Input | Output | Acceptance criteria | Do not |
|---|---|---|---|---|---|
| Wave 1 | `mkt` | Brand guideline; tệp sinh viên; mùa mưa; Shopee; nhóm gia dụng mini | Shortlist có evidence, version và trạng thái | Đúng whitelist/khung giá/shop; Before/After 3–5s; insight khách Việt; facts có nguồn | Không viết script/caption; không bịa giá, shop, hoa hồng |
| Gate 1 | Chief of Staff | Shortlist + evidence | `APPROVED / NEEDS_REVISION / BLOCKED` | Khóa sản phẩm, pain point, facts và claim được phép | Không tự nghiên cứu hoặc thêm sản phẩm |
| Wave 2 | `content` | Artifact Gate 1 đã duyệt; brand voice; nền tảng | Content master/kịch bản có version | Hook → Pain → Demo → CTA; ≤35s; claim bám facts | Không đổi sản phẩm/giá; không tạo motion prompt |
| Gate 2 | Chief of Staff | Kịch bản + claim map | Quyết định duyệt | Kịch bản đúng brand, đủ input sản xuất | Không tự viết lại nội dung chi tiết |
| Wave 3A | `edit` | Kịch bản Gate 2; asset/facts đã duyệt | Storyboard + motion prompt + QA pack | Prompt tiếng Anh, timeline giây, rigid lock, không deepfake | Không viết publish copy; không generate/publish hàng loạt |
| Wave 3B | `content-da-kenh` | Kịch bản Gate 2; product facts; quy chuẩn link | Gói FB Reels + YouTube Shorts | FB không URL caption; YT điều hướng mô tả/bio; không claim quá đà | Không sửa facts/kịch bản; không đăng |
| Final Gate | Chief of Staff | Toàn bộ artifact có version | CEO-ready approval summary | Khớp product/claim/CTA/asset ID; nêu trạng thái và blocker | Không publish, chi tiền hoặc thay link production |

Wave 3A và 3B chỉ chạy song song sau khi Gate 2 đạt vì cả hai cùng phụ thuộc vào kịch bản đã duyệt.

## Checklist CEO duyệt

- [ ] Shortlist và bằng chứng sản phẩm đạt chuẩn.
- [ ] Kịch bản/claim đúng thương hiệu.
- [ ] Visual không vi phạm bản quyền/deepfake.
- [ ] Copy và vị trí link đúng từng nền tảng.
- [ ] Cho phép chuyển từ draft sang sản xuất/xuất bản hay yêu cầu sửa.

Trạng thái: `READY_FOR_SCORING`.
