import pathlib

p = pathlib.Path("quan-ly-kenh.md")
content = p.read_text(encoding="utf-8")

old_text = """- **Cổng an toàn xuất bản (Publish Safe Gate):**
  + Mặc định mọi kế hoạch lịch đăng chỉ ở trạng thái `DRAFT_ONLY`.
  + **TUYỆT ĐỐI CHỈ** kích hoạt đăng bài thật khi nhận được chỉ thị có gắn cờ `APPROVED_TO_PUBLISH` từ CEO."""

new_text = """- **Cổng an toàn xuất bản (Publish Safe Gate):**
  + Mặc định mọi kế hoạch lịch đăng chỉ ở trạng thái `DRAFT_ONLY`.
  + **TUYỆT ĐỐI CHỈ** kích hoạt đăng bài thật khi nhận được chỉ thị có gắn cờ `APPROVED_TO_PUBLISH` từ CEO.
  + **QUY TẮC ĐÓNG BĂNG VIDEO BÁN HÀNG (Chỉ đạo CEO 23/10/2026):**
    * **3 Page Bán Hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`):** **CHỈ ĐƯỢC PHÉP ĐĂNG ẢNH VUÔNG 1:1** (`Editorial Macro & 3-Detail Grid`) và gắn link Shopee Affiliate ở Pinned Comment #1 vào 2 khung giờ vàng `11:45` & `20:00`.
    * **TUYỆT ĐỐI CẤM** xuất bản hoặc lên lịch Video Bán Hàng lên 3 Page này vì Video AI Bán hàng đang trong giai đoạn training nội bộ, chưa được CEO nghiệm thu phê duyệt phát hành.
    * **Page duy nhất được phép đăng Video:** `AI Players - Người chơi hệ AI` (Video Remotion Explainer/Tech Short chia sẻ kiến thức dẫn phễu Zalo)."""

if old_text in content:
    p.write_text(content.replace(old_text, new_text, 1), encoding="utf-8")
    print("Updated quan-ly-kenh.md successfully")
else:
    # Try normalized CRLF
    content_norm = content.replace("\r\n", "\n")
    if old_text in content_norm:
        p.write_text(content_norm.replace(old_text, new_text, 1), encoding="utf-8")
        print("Updated normalized quan-ly-kenh.md successfully")
    else:
        print("old_text not found")
