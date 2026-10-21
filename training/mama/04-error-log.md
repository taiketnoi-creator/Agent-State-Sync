# Bước 4 — Error Log và khóa hồi quy

## Lỗi thực tế trong micro-test

Không phát hiện lỗi thuộc ba nhóm trừ điểm. Không tạo lỗi giả để hợp thức hóa việc sửa prompt.

| Mã | Lỗi chuẩn cần chặn | Mức trừ | Xuất hiện? | Cách khóa |
|---|---|---:|---|---|
| COS-E01 | Chief tự viết kịch bản hoặc làm thay specialist | -4,0 | Không | Hard rule manager-vs-specialist; artifact thiếu thì trả `BLOCKED/NEEDS_REVISION` |
| COS-E02 | Chia việc lộn xộn, không theo dependency | -3,0 | Không | Bắt buộc DAG/waves/gates: research → script → visual/copy |
| COS-E03 | Báo cáo dài dòng hoặc không có checklist CEO | -2,0 | Không | Dùng bảng assignment ngắn và checklist phê duyệt cuối |

## Chẩn đoán nguồn lỗi nếu tái diễn

- Quên luật: task packet thiếu `do_not` hoặc Chief tạo nội dung specialist.
- Thiếu tool/artifact: dependency chưa tồn tại nhưng Chief vẫn chuyển wave.
- Prompt chưa chặt: không có ranh giới owner hoặc không có gate/acceptance criteria.

## Lời nhắc bắt buộc

> “Bạn là người quản lý, không phải thợ làm trực tiếp.”

Trạng thái: ba lỗi trên được ghi thành regression locks trong `mama.md` dù chưa xuất hiện ở lần test này.
