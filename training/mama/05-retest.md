# Bước 6 — Re-test

## Đề bài CEO

> “CEO: Triển khai chiến dịch review 3 món đồ công nghệ decor bàn làm việc học sinh/sinh viên dưới 150k.”

## Bảng phân công

| Thứ tự | Owner | Input | Output yêu cầu | Acceptance criteria | Do not |
|---:|---|---|---|---|---|
| 1 | `mkt` | Brand guideline; tệp học sinh/sinh viên; nhóm decor bàn làm việc; trần 150k; Shopee | Shortlist đúng 3 sản phẩm + evidence sheet | Đúng whitelist/giá; shop đạt chuẩn; Before/After 3–5s; insight rõ; nguồn và thời điểm kiểm tra | Không viết kịch bản; không bịa giá/shop/hoa hồng |
| Gate 1 | Chief of Staff | Shortlist có version | Khóa 3 sản phẩm và fact/claim map | Mỗi sản phẩm `APPROVED` hoặc nêu lý do sửa/chặn | Không tự thêm hay thay sản phẩm |
| 2 | `content` | Gate 1 đã duyệt; brand voice; facts từng sản phẩm | 3 kịch bản có version | Hook → Pain → Demo → CTA; đúng thời lượng; không claim quá đà | Không thay facts/giá; không tạo prompt/caption |
| Gate 2 | Chief of Staff | Kịch bản + fact/claim map | Duyệt input sản xuất | Nhất quán sản phẩm, pain point, CTA và platform | Không tự viết lại kịch bản |
| 3 | `edit` | Kịch bản Gate 2 + asset/facts được phép | 3 storyboard và motion prompt pack | Prompt tiếng Anh; timeline; macro/lighting khi phù hợp; rigid lock; không deepfake | Không viết copy; không publish/generate hàng loạt |
| 4 | `content-da-kenh` | Kịch bản Gate 2; product facts; platform/link rules | Gói bài đăng FB Reels và YouTube Shorts cho 3 video | FB không URL caption; YT điều hướng mô tả/bio; đúng giới hạn định dạng; không claim quá đà | Không đổi claim/kịch bản; không đăng |
| Final Gate | Chief of Staff | Bốn artifact đã version hóa | CEO approval summary | Cross-check product/claim/CTA/asset ID; trạng thái từng hạng mục và blocker | Không publish, chi tiền hoặc thay link production |

Dependency bắt buộc: `mkt → Gate 1 → content → Gate 2 → edit + content-da-kenh → Final Gate`. Hai agent cuối có thể chạy song song sau Gate 2.

## Checklist CEO duyệt

- [ ] Ba sản phẩm đều dưới 150k và có evidence/shop đạt chuẩn.
- [ ] Ba kịch bản đúng brand voice, không claim quá đà.
- [ ] Prompt/visual đúng bản quyền, không deepfake, khóa hình thể sản phẩm.
- [ ] Copy/CTA/link đúng Facebook Reels và YouTube Shorts.
- [ ] Chọn `APPROVE_PRODUCTION`, `NEEDS_REVISION` hoặc `STOP`.

## Chấm re-test

| Tiêu chí | Điểm |
|---|---:|
| Task Decomposition | 3,5/3,5 |
| Least Privilege | 3,5/3,5 |
| CEO-ready Summary | 3,0/3,0 |
| **Tổng** | **10,0/10 — PASS** |

Không phát hiện tái phạm lỗi cũ; không cần vòng sửa. Đây là kế hoạch phân công, không chứa sản phẩm cụ thể, kịch bản, motion prompt hoặc caption.
