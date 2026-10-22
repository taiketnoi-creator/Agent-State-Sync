# MEM-20261022-audience-cluster-firewall-ai-vs-sales-pages — Tường Lửa Tệp Khán Giả: Tách Biệt Tuyệt Đối Giữa Page AI Players Và 3 Page Bán Hàng Affiliate

- **ID:** `MEM-20261022-audience-cluster-firewall-ai-vs-sales-pages`
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Ngày chốt:** `2026-10-22`
- **Nguồn:** Chỉ đạo trực tiếp của CEO (`"page ai và 3 page bán hàng không cần tương tác chéo nhau vì không cùng tệp"`)
- **Phạm vi áp dụng:** `cham-soc-kenh`, `quan-ly-kenh`, `mama`, và toàn bộ kịch bản Seeding / Tương tác chéo Fanpage (`tools/fb_*.py`).

---

## 1. Quy Tắc Cốt Lõi (Hard Gate)

1. **Cấm tuyệt đối tương tác chéo (Comment / Reply chéo) giữa `AI Players - Người chơi hệ AI` (`1022527194267367`) và 3 Page Bán Hàng Affiliate (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`):**
   - **Lý do thuật toán & tệp khách hàng:**
     + `AI Players` phục vụ tệp **Công nghệ / AI Agent / Tự động hóa / Chủ doanh nghiệp & Dân văn phòng nâng cao**.
     + 3 Page bán hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) phục vụ tệp **Tiêu dùng đời sống / Sinh viên / Người thuê trọ / Gia dụng & Phụ kiện bàn làm việc (< 300.000đ)**.
     + Việc để các Page bán đồ phòng trọ/KTX sang bình luận chuyện Multi-Agent trên `AI Players` (hoặc ngược lại) làm nhiễu đồ thị phân phối tệp khán giả (Facebook Andromeda Audience Graph) và thiếu tự nhiên với người đọc thật.

2. **Phân tách 2 Cụm Tương Tác Độc Lập:**
   - **Cụm 1 — Hệ Sinh Thái Công Nghệ & AI (`AI Players - Người chơi hệ AI`):**
     + Chỉ tự đăng **Author Pinned Comment / Chuỗi bình luận kiến thức chuyên sâu (Self-Thread)** của chính Page `AI Players` và phản hồi 100% bình luận của khách hàng thật (hoặc chỉ tương tác với các Page thuộc ngách Công nghệ/AI/Doanh nghiệp như `IFN` nếu cần).
     + Đi seeding bên ngoài chỉ tập trung vào các **Hội nhóm AI, Automation, Vibe Coding, Hiệu suất làm việc**.
   - **Cụm 2 — Hệ Sinh Thái 3 Page Bán Hàng Cùng Tệp Đời Sống Trẻ (`Phòng Trọ Hết Cứu` $\leftrightarrow$ `Ký Túc Xá Có Biến` $\leftrightarrow$ `Hội Deadline`):**
     + Được phép tương tác chéo (Comment / Reply / Like 2 chiều) **trong nội bộ 3 Page bán hàng này với nhau** vì cùng tệp khách hàng trẻ (Sinh viên KTX $\rightarrow$ Người thuê trọ $\rightarrow$ Dân văn phòng trẻ).
     + Tuyệt đối không kéo `AI Players` vào bình luận dưới bài bán hàng của 3 Page này.
