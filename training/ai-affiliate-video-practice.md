# Training thực chiến: Video Affiliate tạo bằng AI

Tài liệu này là chương trình chung cho đội Agent Javis, được chuẩn hóa từ training thực chiến do CEO cung cấp ngày 2026-10-12. Mục tiêu là tạo video affiliate minh bạch, dựa trên nhu cầu mua thật và không biến minh hoạ AI thành bằng chứng sản phẩm.

## Nguyên tắc không được vi phạm

- Chỉ dùng AI để tạo bối cảnh, câu chuyện và minh hoạ; claim sản phẩm phải có nguồn listing, tài liệu hãng hoặc kiểm thử thật.
- Không giả trải nghiệm cá nhân/khách hàng, review, testimonial hoặc before/after là kết quả thật.
- Không dùng người thật, người nổi tiếng, clone giọng, logo/bao bì giả hoặc claim y tế, giảm cân, tài chính, cam kết tuyệt đối.
- Cảnh AI biến đổi hoặc trông như thật cần disclosure `Minh hoạ bằng AI`; nội dung có link/giỏ hàng cần disclosure `Có thể nhận hoa hồng affiliate` theo vị trí phù hợp nền tảng.
- Mọi thông tin biến động như giá, voucher, tồn kho và shop phải có nguồn/ngày chốt hoặc hướng người xem kiểm tra hiện tại.

## Chuỗi artifact bắt buộc cho mỗi video

1. Product brief đã kiểm chứng.
2. Claim ledger: claim, nguồn, ngày chốt, trạng thái `VERIFIED | UNVERIFIED | BANNED`.
3. Script có hook, tình huống, lợi ích có nguồn, giới hạn, CTA và disclosure.
4. Shot list, prompt theo shot và asset manifest.
5. Video dọc, subtitle, caption và mapping asset → SKU → link version.
6. Phiếu compliance `ĐẠT`.
7. Số liệu 24h/72h và quyết định vòng test kế tiếp.

## Product brief và ngưỡng test

Chấm 1–5 cho: nhu cầu thật, khả năng minh hoạ không bịa kết quả, khác biệt một câu, độ tin cậy listing/shop và ít nhất 10 góc nội dung. Chỉ `TEST` SKU từ **18/25**. Brief ghi SKU/link/ngày chốt, buyer/problem, 3 lợi ích có nguồn, 2 giới hạn, review xấu phổ biến, 10 góc video và claim cấm/chưa đủ bằng chứng.

## Công thức video 20–35 giây

`Hook (0–2s) → tình huống (2–7s) → minh hoạ cách giải quyết (7–20s) → giới hạn/bằng chứng (20–28s) → một CTA (28–35s)`.

Mỗi video chỉ test **một biến chính**: hook, format hoặc CTA. CTA phải dẫn người xem kiểm tra đúng SKU, review và giá hiện tại.

## Prompt và asset manifest

Không dùng một prompt dài cho cả video. Chia 4–6 shot, một hành động/shot, thường 1–3 giây/shot. Brief trước prompt gồm Product thật, Audience, Single problem, Verified benefit/claim ID, disclosure, visual style và forbidden list.

Manifest tối thiểu: `video_id`, `SKU`, `script_id`, `shot_id`, `prompt_version`, `model/tool`, `reference_asset_id + quyền dùng`, `output_asset_id`, `claim_ids`, `disclosure_overlay/timecode`, `approval_status`, `regenerate_reason`.

## Vòng test 7 ngày

| Ngày | Thao tác |
|---:|---|
| 1 | 3 SKU, product brief và 10 góc/SKU |
| 2 | 3 script/SKU, duyệt claim/compliance |
| 3–4 | 2 biến thể/SKU, giữ một biến test |
| 5 | Ghi objection/câu hỏi |
| 6 | Tạo comment-reply hoặc creative phản hồi đã duyệt |
| 7 | Báo cáo `KEEP / ITERATE / STOP` |

Funnel cần đo: `views → 3s/hold → retention/completion → click → valid orders → valid commission`. Đơn hủy, từ chối nhận hoặc hoàn không phải đơn thành công. View thấp ưu tiên hook/shot đầu; view tốt nhưng click thấp kiểm lợi ích/CTA/link; click có nhưng đơn thấp kiểm listing, giá, ship, review, tồn kho và mapping SKU trước khi đổ lỗi cho creative. Lỗi compliance hoặc hoàn/hủy tăng bất thường phải pause SKU để audit.
