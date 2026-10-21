# Micro-test — lịch 1 tuần, 10 video

## Đề bài

Lập lịch phát hành 1 tuần (10 video) cho Facebook Reels và YouTube Shorts về sản phẩm tiện ích mini Shopee, kèm checklist kỹ thuật trước khi public.

## Phân bổ

Mỗi kênh nhận 5 video trong tuần, dùng các slot 11:45 và 20:00. Không kênh nào vượt 2 video/ngày; tổng cộng 10 slot hợp lệ.

| Ngày | Giờ | Nền tảng | Tên video | Asset ID/status | Link route | Pinned comment status |
|---|---:|---|---|---|---|---|
| Thứ 2 | 11:45 | Facebook Reels | Máy cạo lông xù: Before/After | V001 / READY_FOR_REVIEW | FB caption không URL; comment ghim Shopee | DRAFT_READY `[SHOPEE_AFFILIATE_LINK]` |
| Thứ 2 | 20:00 | YouTube Shorts | Giá đỡ điện thoại xoay 360° | V002 / READY_FOR_REVIEW | Description/bio | N/A; không spam comment |
| Thứ 3 | 11:45 | Facebook Reels | Đèn kẹp bàn học: góc tối thành sáng | V003 / READY_FOR_REVIEW | FB comment ghim Shopee | DRAFT_READY `[SHOPEE_AFFILIATE_LINK]` |
| Thứ 3 | 20:00 | YouTube Shorts | Quạt tích điện mini: cứu nóng ký túc xá | V004 / READY_FOR_REVIEW | Description/bio | N/A; không spam comment |
| Thứ 4 | 11:45 | Facebook Reels | Ống luồn dây: bàn học gọn trong 5 giây | V005 / READY_FOR_REVIEW | FB comment ghim Shopee | DRAFT_READY `[SHOPEE_AFFILIATE_LINK]` |
| Thứ 4 | 20:00 | YouTube Shorts | Máy hút bụi mini: vụn snack biến mất | V006 / READY_FOR_REVIEW | Description/bio | N/A; không spam comment |
| Thứ 5 | 11:45 | Facebook Reels | Kê tay công thái học: đỡ mỏi khi gõ | V007 / READY_FOR_REVIEW | FB comment ghim Shopee | DRAFT_READY `[SHOPEE_AFFILIATE_LINK]` |
| Thứ 5 | 20:00 | YouTube Shorts | Túi nén chân không: vali rộng hơn | V008 / READY_FOR_REVIEW | Description/bio | N/A; không spam comment |
| Thứ 6 | 11:45 | Facebook Reels | Ô gấp ngược: vào lớp không nhỏ nước | V009 / READY_FOR_REVIEW | FB comment ghim Shopee | DRAFT_READY `[SHOPEE_AFFILIATE_LINK]` |
| Thứ 6 | 20:00 | YouTube Shorts | Khay làm đá thông minh: đá ra không vỡ | V010 / READY_FOR_REVIEW | Description/bio | N/A; không spam comment |

## Checklist 5 bước

1. Asset/technical: đúng version, 9:16, duration, subtitle, thumbnail, render.
2. Audio/copyright: voice/SFX QA, nhạc có license/thư viện nền tảng, không deepfake.
3. Copy/link/disclosure: đúng route FB/YT, disclosure, không URL FB caption, link version/placeholder rõ.
4. Approval: chỉ public khi `APPROVED_TO_PUBLISH`; thiếu thì `READY_FOR_APPROVAL`.
5. Post-publish/rollback: ops log, timestamp, owner, rollback note, kiểm tra pinned/link sau đăng.

Status: `DRAFT_ONLY`; không có hành động bên ngoài.
