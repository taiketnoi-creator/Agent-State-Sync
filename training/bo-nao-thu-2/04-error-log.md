# Bước 4 — Error Log & Khóa Hồi Quy Cho Bộ Não Thứ 2

## Danh Mục Lỗi Thường Gặp & Cơ Chế Khóa Hồi Quy

Tài liệu này tổng hợp 4 nhóm sai lầm phổ biến nhất khi vận hành quản trị tri thức dài hạn và các quy tắc khóa cứng (Regression Locks) để ngăn ngừa tuyệt đối.

---

### 1. MEM-E01: Lưu log thô quá dài gây tràn bộ nhớ ngữ cảnh (Context Bloat)

- **Biểu hiện**: Sao chép nguyên văn thông báo lỗi của n8n, stack trace Python, payload JSON hàng trăm dòng hoặc nhật ký trò chuyện dông dài vào file `MEM-*.md`.
- **Hậu quả**: Khi Mama hoặc các specialist khác đọc tri thức, các file ký ức này làm phình to context window, tiêu tốn quota token đắt đỏ của model chính (Gemini 4/GPT) mà không mang lại giá trị tương xứng.
- **Cơ chế khóa cứng (Regression Lock)**:
  + Áp dụng trần dung lượng: Mỗi file `MEM-*.md` không vượt quá **50 dòng** và dung lượng không quá **3KB**.
  + Nếu có log kỹ thuật dài cần lưu trữ, đẩy vào `scratch/` hoặc bảng SQLite, trong file memory chỉ ghi tóm tắt bản chất lỗi và 1 dòng tham chiếu đường dẫn.

---

### 2. MEM-E02: Quên cập nhật chỉ mục `INDEX.md` (Broken Index / Phantom Memory)

- **Biểu hiện**: Tạo file `MEM-YYYYMMDD-slug.md` trong thư mục `memories/` nhưng không cập nhật dòng mới vào bảng chỉ mục `knowledge/bo-nao-thu-2/INDEX.md`.
- **Hậu quả**: Ký ức bị "mồ côi" (phantom memory). Mama và các Subagent chỉ đọc `INDEX.md` để tra cứu nhanh, nếu không có trong index thì tri thức coi như bị lãng quên và không bao giờ được tái sử dụng.
- **Cơ chế khóa cứng (Regression Lock)**:
  + Quy tắc nguyên tử (Atomicity Rule): Thao tác ghi nhớ chỉ được coi là hoàn tất (`DONE`) khi và chỉ khi cả 2 việc được thực hiện đồng thời:
    1. Ghi file `knowledge/bo-nao-thu-2/memories/MEM-*.md`.
    2. Cập nhật bảng tổng hợp `knowledge/bo-nao-thu-2/INDEX.md`.

---

### 3. MEM-E03: Đánh nhãn `VALIDATED` cho giả thuyết/ý tưởng chưa kiểm chứng (Premature Validation)

- **Biểu hiện**: Nghe CEO hoặc một specialist đưa ra một nhận định ("video đăng 2h sáng view sẽ cao", "giảm giá 10% sẽ tăng gấp đôi đơn") liền gắn trạng thái `VALIDATED` và `confidence: high`.
- **Hậu quả**: Các Subagent khác (như `mkt`, `quan-ly-kenh`) khi truy vấn sẽ tưởng đây là sự thật đã được chứng minh và áp dụng sai lệch vào sản xuất thực tế, gây sụt giảm hiệu suất kênh.
- **Cơ chế khóa cứng (Regression Lock)**:
  + Quy tắc phòng thủ mặc định: Mọi nhận định, ý tưởng, giả định chưa có số liệu đối soát (analytics report, đơn hàng Shopee thực tế, hoặc A/B test có ý nghĩa thống kê) **BẮT BUỘC** gắn trạng thái `UNVERIFIED` và `confidence: low`.
  + Chỉ chuyển sang `VALIDATED` khi có bằng chứng số liệu cụ thể hoặc phê duyệt chính thức bằng văn bản từ CEO.

---

### 4. MEM-E04: Để lọt Secret / Token / API Key / PII vào kho tri thức (Credential Leakage)

- **Biểu hiện**: Lưu trữ nguyên vẹn API key Shopee, webhook URL có auth token, pass database hoặc số điện thoại khách hàng vào kho tri thức.
- **Hậu quả**: Rủi ro an ninh mạng nghiêm trọng. Khi kho tài liệu được đồng bộ qua Git hoặc đọc bởi các agent, credential có thể bị lộ ra ngoài.
- **Cơ chế khóa cứng (Regression Lock)**:
  + Bắt buộc chạy kiểm tra lọc chuỗi nhạy cảm: Quét các từ khóa `key`, `token`, `secret`, `password`, `Bearer`, `http...token=`.
  + Tự động thay thế ngay lập tức bằng placeholder an toàn: `[REDACTED_API_KEY]`, `[REDACTED_TOKEN]`, `[REDACTED_SECRET]`.
  + Cảnh báo CEO lập tức đổi credential nếu phát hiện lọt qua tin nhắn chat.

---

## Lời Nhắc Bắt Buộc (System Motto)

> *"Bộ não thứ 2 là thủ thư tri thức, không phải thùng rác chứa dữ liệu thô.  
> Ký ức phải ngắn gọn, chính xác, bảo mật và luôn sẵn sàng để hành động."*
