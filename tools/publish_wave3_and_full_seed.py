#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_wave3_and_full_seed.py
1. Đăng bài Mở Màn Thu Phễu Wave 3 ("Tặng Kho Vũ Khí Hệ Thống Subagent AI" + Ảnh 3D Tech #1) lên Fanpage AI Players.
2. Ghim Pinned Comment #1 (hướng dẫn 3 bước + câu hỏi mở phân tệp).
3. Chạy trọn bộ 5 Bình luận Mồi Tương Tác Chéo (Cross-Page Seeding Pack) từ 3 Fanpage vệ tinh + Phản hồi tự nhiên của AI Players + Like chéo từ 4 Page.
4. Hoàn tất nốt 8 bài cũ trên AI Players để đạt 100% (26/26 bài) có thảo luận 2 chiều trên toàn bộ 4 Fanpage.
"""

import json
import mimetypes
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"
SUBAGENT_DIR = Path(__file__).resolve().parent.parent


def graph_post(endpoint: str, token: str, params: dict) -> dict:
    url = f"https://graph.facebook.com/v22.0/{endpoint}"
    payload = dict(params)
    payload["access_token"] = token
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        return {"error": err, "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def upload_photo_post(page_id: str, token: str, image_path: Path, caption: str) -> dict:
    url = f"https://graph.facebook.com/v22.0/{page_id}/photos"
    boundary = f"----AgentJavisBoundary{uuid.uuid4().hex}"
    body = bytearray()

    def add_field(name: str, value: str):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    add_field("access_token", token)
    add_field("message", caption)
    add_field("published", "true")

    mime_type = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"
    file_bytes = image_path.read_bytes()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="source"; filename="{image_path.name}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", errors="ignore"), "code": e.code}
    except Exception as e:
        return {"error": str(e)}


LAUNCH_CAPTION = """Dùng AI để làm việc nhanh hơn, nhưng ngày nào bạn cũng mất 45 phút chỉ để ngồi... gõ đi gõ lại và sửa lỗi hộ nó?

Lý do không phải vì bạn chưa biết mẹo "prompt thần thánh", mà vì bạn đang phạm phải sai lầm mà 90% người dùng AI mắc phải: Bắt 1 khung chat duy nhất đóng vai một nhân viên thời vụ ôm đồm tất cả mọi việc!

Vừa bắt nó đọc dữ liệu thô, vừa bắt nó chắt lọc ý chính, vừa bắt nó trau chuốt câu từ hành chính, rồi lại bắt nó tự kiểm tra tính logic. Kết quả là bộ nhớ AI bị nhiễu loạn:
- Báo cáo tuần thì viết chung chung, sáo rỗng, rơi rụng mất deadline và số liệu quan trọng.
- Kịch bản video ngắn 30 giây thì mở đầu bằng câu chào "Xin chào các bạn" lê thê làm rớt sạch người xem ở giây thứ 2, thoại dài tới 140 từ đọc muốn đứt hơi.
- Đau đầu nhất: Hôm nay dặn kỹ quy chuẩn công ty xong, ngày mai mở khung chat mới nó lại quên sạch sành sanh!

Đó là lý do các chuyên gia làm việc chuyên sâu hiện nay đã chuyển hẳn sang tư duy: "NGƯỜI CHƠI HỆ SUBAGENT".

Subagent là gì? Hiểu đơn giản, thay vì nói chuyện vu vơ với AI, bạn biến nó thành một "Tổ đội nhân sự AI chuyên biệt". Mỗi nhân sự chỉ giữ đúng 1 file mô tả công việc (.md) cố định, làm đúng 1 khâu trong dây chuyền và bàn giao kết quả cho khâu kế tiếp.

Hôm nay, AI Players gửi tặng bạn trọn bộ tài liệu thực chiến đóng gói sẵn để bạn nâng cấp cách dùng AI ngay tối nay:

🎁 KHO VŨ KHÍ KHỞI ĐỘNG SUBAGENT THỰC CHIẾN (BẢN V2026):
Bên trong đã chuẩn hóa sẵn 3 cụm công cụ copy-paste nạp vào máy tính là chạy:

1️⃣ BỘ 3 SUBAGENT VIDEO NGẮN 30 GIÂY:
- Subagent "Hook-Sniper 3s": Tự động xuất 5 phương án mở đầu giật khựng ngón tay lướt màn hình, cấm tuyệt đối câu chào hỏi rườm rà.
- Subagent "Script-Trimmer 85": Cầu dao gọt kịch bản tự động, ép toàn bộ lời thoại về đúng giới hạn an toàn 85 từ cho video 30 giây.
- Subagent "Subtitle-Splitter": Bộ quy tắc ngắt cụm phụ đề tiếng Việt 3–7 từ chuẩn mệnh đề, chấm dứt hoàn toàn cảnh rớt 1 chữ lẻ loi dưới đáy màn hình.

2️⃣ BỘ 3 TRỢ LÝ VĂN PHÒNG 5H CHIỀU:
- Trợ lý "Data Extractor": Quét sạch ghi chép họp, email hỗn độn và chỉ nhặt ra đúng dữ kiện có thật (Ai làm / Việc gì / Hạn nào / Con số nào).
- Trợ lý "Report Writer": Lắp dữ kiện vào khung báo cáo chuẩn mục tiêu - kết quả - vướng mắc, cấm dùng văn phong sáo rỗng.
- Trợ lý "Quality Verifier": Thanh tra độc lập đối chiếu báo cáo với dữ liệu gốc, bắt lỗi logic trước khi bạn bấm gửi sếp.

3️⃣ BỘ KHUNG GIAO VIỆC & THANH TRA CHẤT LƯỢNG:
- Phiếu giao việc Task Packet chuẩn 6 mục bắt buộc (Mục tiêu, Đầu vào, Tiêu chuẩn nghiệm thu, Điều cấm làm).
- Bảng Rubric chấm điểm 10 tiêu chí của Tổng biên tập khó tính Strict-Editor để đảm bảo không sản phẩm AI nào nộp ra bị gắn mác "văn mẫu ChatGPT".

Toàn bộ được viết bằng tiếng Việt rõ ràng, kèm hướng dẫn nạp file vào ChatGPT / Claude / Antigravity chỉ trong 3 phút.

👉 BẠN CHỈ CẦN BÌNH LUẬN DUY NHẤT TỪ KHÓA:
SUBAGENT

Hệ thống của AI Players sẽ gửi trọn bộ tài liệu và hướng dẫn mở khóa cho bạn ngay lập tức!"""

PINNED_COMMENT_TEXT = """📌 HƯỚNG DẪN 3 BƯỚC NHẬN VÀ SỬ DỤNG "KHO VŨ KHÍ KHỞI ĐỘNG SUBAGENT" TRONG 5 PHÚT:

1️⃣ Bình luận đúng từ khóa "SUBAGENT" ngay dưới bài viết này.
2️⃣ Tham gia trực tiếp Nhóm Zalo Cộng Đồng Bảo Mật của AI Players (đã bật chế độ ẨN 100% SỐ ĐIỆN THOẠI & chặn nhắn tin làm phiền) để tải trọn bộ 6 file cấu hình Subagent (.md) + Phiếu giao việc Task Packet:
🔗 Link vào nhóm nhận kho tài liệu: https://zalo.me/g/etllok798
🔑 Mật khẩu giải nén Lớp 2 (Passcode): AIPLAYERS2026 (Xem ngay tại Tin Ghim đầu nhóm Zalo)

💡 HỎI NHANH MỌI NGƯỜI: Bạn đang ứng dụng AI vào lĩnh vực nào nhiều nhất?
👉 Hãy comment "SUBAGENT + [Ngành của bạn]" (Ví dụ: SUBAGENT Văn phòng / SUBAGENT Làm video / SUBAGENT Marketing / SUBAGENT Chủ shop) để AI Players ưu tiên gửi thêm bộ ví dụ thực chiến đúng ngành cho bạn nhé! 👇"""


def main():
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    pages_by_id = {p["id"]: p for p in vault["pages"]}
    ai_page = pages_by_id["1022527194267367"]
    ktx_page = pages_by_id["1421270697727753"]
    dl_page = pages_by_id["1407231352464711"]
    pt_page = pages_by_id["1442323328956326"]
    ifn_page = pages_by_id.get("591875884001523")

    img_path = (
        SUBAGENT_DIR
        / "campaigns"
        / "2026-10-21"
        / "ai-players-subagent-course-funnel"
        / "images"
        / "3d_tech_01_subagent_core_station.jpg"
    )
    print(f">>> [BƯỚC 1] Đăng bài Mở Màn Thu Phễu Wave 3 kèm ảnh 3D High-Tech #1 ({img_path.name})...")
    pub_res = upload_photo_post(ai_page["id"], ai_page["access_token"], img_path, LAUNCH_CAPTION)
    print("  Result:", pub_res)
    post_id = pub_res.get("post_id") or pub_res.get("id")
    if not post_id:
        print("FAILED TO PUBLISH:", pub_res)
        return

    print(f">>> [BƯỚC 2] Đăng Pinned Comment #1 lên bài {post_id}...")
    pin_res = graph_post(f"{post_id}/comments", ai_page["access_token"], {"message": PINNED_COMMENT_TEXT})
    print("  Pinned Comment ID:", pin_res.get("id", pin_res))

    print(f">>> [BƯỚC 3] Thả Like chéo & Chạy 5 luồng Seeding Thảo Luận Chéo từ 3 Page vệ tinh trên bài {post_id}...")
    for sat in (dl_page, ktx_page, pt_page, ifn_page):
        if sat:
            graph_post(f"{post_id}/likes", sat["access_token"], {})

    seeding_threads = [
        (
            dl_page,
            "Trời ơi cứu tinh đây rồi! Tuần nào cũng đến 5h chiều thứ Sáu là ngồi toát mồ hôi hột vì con ChatGPT nó gom biên bản họp xong bịa thêm số liệu vào báo cáo. Cái bộ 3 Trợ lý Văn phòng nạp vào Claude Free dùng được luôn không admin ơi? Chứ deadline dí sát nút rồi!",
            "Dùng mượt trên cả Claude, ChatGPT bản miễn phí lẫn các trình duyệt AI bạn nhé! Bản chất file .md là bộ quy tắc phân vai độc lập, bạn chỉ cần copy nguyên văn nạp vào đầu cuộc trò chuyện là trợ lý tự vào nếp ngay. Bạn bấm vào link Zalo ở bình luận ghim đầu tiên (https://zalo.me/g/etllok798 - Passcode: AIPLAYERS2026) lấy trọn bộ nhé! 🚀",
        ),
        (
            ktx_page,
            "Cái Subagent Subtitle-Splitter ngắt chữ tiếng Việt chuẩn thật không ạ? Em làm Reels TikTok mà toàn bị cái CapCut nó ngắt kiểu dòng trên 'chiếc máy hút', dòng dưới rớt lại đúng chữ 'bụi', nhìn phèn không chịu được luôn á :(((",
            "Chuẩn bài luôn bạn ơi! Subtitle-Splitter được nạp sẵn từ điển bảo vệ cụm từ ghép tiếng Việt và giới hạn hiển thị từ 3 đến 7 từ/dòng theo đúng nhịp thở. Bạn sẽ không bao giờ thấy chữ rơi lẻ loi nữa đâu. Vào ngay bình luận ghim đầu tiên lấy bộ quy tắc về test thử lên clip tối nay nhé!",
        ),
        (
            pt_page,
            "Mới tập tành làm kênh Affiliate Shopee không biết viết kịch bản thì dùng bộ Video 30s này có bị khóa kênh hay bóp tương tác không ad? Sợ nhất AI viết ra mấy câu cam kết quá đà bị quét vi phạm chính sách ạ.",
            "Rất tỉnh táo bạn nhé! Đó là lý do trong Kho Vũ Khí có kèm thêm con Strict-Editor gác cổng. Nó có bộ lọc quét sạch từ cấm, từ ngữ tâng bốc sai sự thật trước khi xuất bản. Bạn cứ yên tâm lấy về dùng theo đúng cấu trúc 4 nhịp (Hook -> Pain -> Demo -> CTA) ở bình luận đầu tiên là vừa an toàn vừa giữ chân người xem cực tốt nhé!",
        ),
        (
            dl_page,
            "Đã tải được file Lớp 1 và lấy Passcode AIPLAYERS2026 trên tin ghim nhóm Zalo rồi nha page ơi, đọc cái Blueprint phân vai Quản đốc Mama với Thanh tra Verifier cuốn thực sự. Đang nạp thử 3 file .md văn phòng đây ạ!",
            "Tuyệt vời bạn ơi! Khi nạp file .md vào nhớ kèm theo Phiếu giao việc Task Packet 6 mục để Subagent khóa cứng đầu ra nhé. Tối nay 20h nhóm mở khung hỗ trợ kỹ thuật, có gì vướng cứ nhắn trong nhóm Admin giải đáp trực tiếp nha! ⚡",
        ),
        (
            ktx_page,
            "Cho em hỏi xíu là có cần biết lập trình hay biết code gì không ạ? Nhìn hệ thống 10 Subagent xịn quá mà em dân tay ngang hơi rén :D",
            "Hoàn toàn 0 dòng code bạn nhé! Toàn bộ file Subagent này là ngôn ngữ tiếng Việt đời thường được đóng gói theo dạng 'bản mô tả công việc'. Bạn chỉ việc sao chép và dán (Copy - Paste) vào khung chat là xong. Trải nghiệm thử 3 phút là thấy dễ bất ngờ luôn!",
        ),
    ]

    for sat_page, cmt_text, reply_text in seeding_threads:
        c = graph_post(f"{post_id}/comments", sat_page["access_token"], {"message": cmt_text})
        if "id" in c:
            cid = c["id"]
            graph_post(f"{cid}/likes", ai_page["access_token"], {})
            graph_post(f"{cid}/comments", ai_page["access_token"], {"message": reply_text})
            print(f"  + Seeded thread from {sat_page['name']}: {cid}")
        time.sleep(0.3)

    print(">>> [BƯỚC 4] Hoàn tất nốt 8 bài cũ trên AI Players để đạt 100% (26/26 bài) Active...")
    rem_items = [
        (
            "1022527194267367_122132331159248983",
            dl_page,
            "Tự động hóa khâu tổng hợp báo cáo tuần và nhắc lịch deadline cho team là việc mình muốn làm đầu tiên!",
            "Chuẩn luôn! Bắt đầu từ tác vụ lặp đi lặp lại mỗi ngày sẽ thấy hiệu quả tiết kiệm thời gian rõ rệt nhất.",
        ),
        (
            "1022527194267367_122132329413248983",
            ktx_page,
            "Đúng là giờ lên GitHub tìm workflow dựng sẵn nhanh hơn tự mày mò từ con số 0 gấp chục lần.",
            "Chính xác! Tận dụng các repo open-source đã kiểm chứng giúp rút ngắn 80% thời gian triển khai thực tế.",
        ),
        (
            "1022527194267367_122132329353248983",
            pt_page,
            "Tiêu chí số 2 (có ví dụ input/output thực tế) cực kỳ quan trọng để biết repo còn chạy tốt hay chỉ làm màu.",
            "Chuẩn bài! Cứ repo nào có sẵn thư mục examples/ và hướng dẫn chạy thử 3 bước rõ ràng là đáng để test ngay.",
        ),
        (
            "1022527194267367_122132329281248983",
            dl_page,
            "Nhiều repo vài chục nghìn sao mà ngừng cập nhật cả năm trời thì kéo về toàn lỗi thư viện.",
            "Đúng vậy! Kiểm tra lịch sử commit trong 30 ngày gần nhất và giấy phép MIT/Apache là bước bắt buộc trước khi đưa vào công việc.",
        ),
        (
            "1022527194267367_122132266383248983",
            ktx_page,
            "Xu hướng AI biết tự gọi công cụ (Tool Use) và tự kiểm tra kết quả đang thay đổi hoàn toàn cách làm việc luôn.",
            "Chuẩn xu hướng 2026! Khi AI được cấp quyền đọc/ghi file và gọi API theo quy trình kiểm soát, nó thực sự trở thành trợ lý vận hành đắc lực.",
        ),
        (
            "1022527194267367_122132266335248983",
            pt_page,
            "Mấy công cụ kéo thả trực quan kiểu Langflow với n8n giúp dân không chuyên code như tụi mình tiếp cận AI Agent dễ hơn hẳn.",
            "Đúng rồi bạn! Nhìn sơ đồ khối trực quan giúp mình kiểm soát luồng dữ liệu vào/ra rất dễ dàng mà không sợ rối code.",
        ),
        (
            "1022527194267367_122132266293248983",
            dl_page,
            "Chuẩn giao thức MCP đang trở thành cầu nối tiêu chuẩn giúp AI đọc trực tiếp Database và công cụ nội bộ luôn.",
            "Chính xác! Kết nối qua MCP giúp AI thao tác trực tiếp với SQLite, n8n và Fanpage mà không cần copy-paste thủ công nữa.",
        ),
        (
            "1022527194267367_122125951659248983",
            ktx_page,
            "Ai biết ứng dụng hệ thống AI và tự động hóa sớm thực sự đi nhanh hơn phần còn lại cả quãng dài!",
            "Cảm ơn bạn! Cùng theo dõi AI Players để cập nhật quy trình làm chủ tổ đội Subagent thực chiến mỗi ngày nhé!",
        ),
    ]
    for pid, gp, gcmt, hrep in rem_items:
        for sat in (dl_page, ktx_page, pt_page):
            graph_post(f"{pid}/likes", sat["access_token"], {})
        c = graph_post(f"{pid}/comments", gp["access_token"], {"message": gcmt})
        if "id" in c:
            cid = c["id"]
            graph_post(f"{cid}/likes", ai_page["access_token"], {})
            graph_post(f"{cid}/comments", ai_page["access_token"], {"message": hrep})
            print(f"  + Completed AI Players post {pid}")

    print("=== HOÀN TẤT XUẤT BẢN WAVE 3 & 100% TƯƠNG TÁC MẠNG LƯỚI ===")


if __name__ == "__main__":
    main()
