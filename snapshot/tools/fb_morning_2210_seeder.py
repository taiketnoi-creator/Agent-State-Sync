#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fb_morning_2210_seeder.py — Thực thi Ca Sáng (Đã khóa Tường Lửa Tệp Khán Giả theo chỉ đạo CEO):
1. Cụm 1 (AI Players - Người chơi hệ AI):
   - Quét và trả lời 100% bình luận khách hàng thật còn tồn đọng (replies=0).
   - Tự đăng Author Deep-Dive Comment (Self-Thread kiến thức) của chính Page AI Players.
   - TUYỆT ĐỐI KHÔNG dùng 3 Page bán hàng sang bình luận tại AI Players.
2. Cụm 2 (3 Page Bán Hàng Affiliate cùng tệp: Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline):
   - Chỉ tương tác chéo 2 chiều trong nội bộ 3 Page bán hàng với nhau (TUYỆT ĐỐI KHÔNG dùng AI Players đi bình luận dạo ở 3 Page bán hàng).
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VAULT_PATH = Path.home() / ".codex" / "mcp" / "facebook-mcp-server" / "pages_vault.json"

AI_ID = "1022527194267367"
SALES_IDS = ["1442323328956326", "1421270697727753", "1407231352464711"]


def graph_post(endpoint: str, token: str, params: dict) -> dict:
    url = f"https://graph.facebook.com/v22.0/{endpoint}"
    payload = dict(params)
    payload["access_token"] = token
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        return {"error": err, "code": e.code}
    except Exception as e:
        return {"error": str(e)}


def graph_get(endpoint: str, token: str, params: dict = None) -> dict:
    q = dict(params or {})
    q["access_token"] = token
    url = f"https://graph.facebook.com/v22.0/{endpoint}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))


# Chỉ tương tác chéo nội bộ trong Cụm 3 Page Bán Hàng Cùng Tệp
SALES_CLUSTER_DIALOGUES = [
    # === 1. PHÒNG TRỌ HẾT CỨU (3 bài chủ lực) ===
    {
        "post_id": "1442323328956326_122102747385514839",
        "host_id": "1442323328956326",
        "guest_id": "1421270697727753",  # Ký Túc Xá Có Biến
        "guest_cmt": "Sáng nay nấu đồ ăn sáng trong góc bếp trọ kín gió mới thấy giá trị của con quạt cầm tay phản lực này, bật mức 50 đặt cạnh bếp là thổi bay hơi nóng hầm hập luôn!",
        "host_reply": "Chuẩn bài luôn bạn ơi! 🌬️ Quạt iMI có đế đứng vững trên bàn bếp cộng thêm màn hình LED báo chính xác từng % pin nên vừa nấu ăn vừa bật quạt cực kỳ tiện. Link chính hãng kèm ưu đãi mình ghim ngay ở bình luận đầu tiên nha!",
    },
    {
        "post_id": "1442323328956326_122102743245514839",
        "host_id": "1442323328956326",
        "guest_id": "1407231352464711",  # Hội Deadline (Cùng tệp đời sống trẻ)
        "guest_cmt": "Điểm ăn tiền nhất của dòng quạt phản lực iMI này là sạc chung cáp Type-C với điện thoại và sạc dự phòng, đi làm hay ở trọ mất điện đều chủ động được nguồn pin.",
        "host_reply": "Đúng chuẩn luôn ạ! 🔋 Viên pin 5000mAh dùng cổng sạc Type-C phổ biến giúp anh em ở trọ yên tâm ngủ ngon cả những đêm khu trọ bảo trì điện đột xuất. Cả nhà xem chi tiết ở bình luận ghim đầu tiên nhé!",
    },
    {
        "post_id": "1442323328956326_122101744053514839",
        "host_id": "1442323328956326",
        "guest_id": "1421270697727753",  # Ký Túc Xá Có Biến
        "guest_cmt": "Bộ bào cắt rau củ đa năng này lúc rửa các lưỡi dao có nhanh không shop? Mình sợ nhất mấy món đồ bếp dùng thì nhanh mà lúc cọ rửa lại lâu.",
        "host_reply": "Rửa siêu nhanh chỉ mất 30 giây thôi bạn ơi! 🥕 Bộ sản phẩm có kèm lược gạt vụn rau củ chuyên dụng, bạn chỉ cần xả dưới vòi nước mạnh là sạch bong mà không cần chạm tay vào lưỡi dao. Xem ngay link Shopee ở bình luận đầu tiên nha!",
    },

    # === 2. KÝ TÚC XÁ CÓ BIẾN (3 bài chủ lực) ===
    {
        "post_id": "1421270697727753_122107644243511096",
        "host_id": "1421270697727753",
        "guest_id": "1407231352464711",  # Hội Deadline (Cùng tệp đời sống trẻ)
        "guest_cmt": "Thiết kế vỏ nhám chống bám vân tay của mẫu quạt iMI này hợp với sinh viên và dân văn phòng thật, bỏ chung vào ngăn balo với sách vở, chìa khóa cả ngày cũng không sợ trầy xước.",
        "host_reply": "Chuẩn luôn bác ơi! 🎒 Kích thước nhỏ gọn bằng chiếc điện thoại mà luồng gió phản lực thổi gom mát lạnh ngay tức thì khi đi bộ chuyển tiết giữa trưa. Các đồng môn bấm vào link ở bình luận đầu tiên để săn giá ưu đãi sinh viên nhé!",
    },
    {
        "post_id": "1421270697727753_122107638801511096",
        "host_id": "1421270697727753",
        "guest_id": "1442323328956326",  # Phòng Trọ Hết Cứu
        "guest_cmt": "Mình thích nhất tính năng nhấn giữ nút cộng trừ để tăng giảm mượt từ mức 1 lên 120, vào phòng tự học cần yên tĩnh thì chỉnh mức 20-30 là gió thoang thoảng siêu êm!",
        "host_reply": "Đúng điểm đáng tiền nhất của con quạt iMI 120 cấp gió luôn bạn! ❄️ Tinh chỉnh mượt mà theo đúng không gian học tập từ sân trường nắng gắt vào tới thư viện yên tĩnh. Link chuẩn mình ghim ngay dưới bình luận #1 nha!",
    },
    {
        "post_id": "1421270697727753_122106524439511096",
        "host_id": "1421270697727753",
        "guest_id": "1442323328956326",  # Phòng Trọ Hết Cứu
        "guest_cmt": "Túi hút chân không PA+PE này dùng sang học kỳ sau mở ra lấy đồ rồi hút lại lần nữa vẫn giữ nguyên độ kín hơi chứ shop?",
        "host_reply": "Tái sử dụng thoải mái nhiều năm luôn bạn nhé! 🧺 Chất liệu nhựa PA+PE dẻo dai kết hợp khóa zip 2 rãnh và van khóa khí 1 chiều bằng silicon cực kín, mỗi mùa đổi thời tiết cứ lấy ra dùng lại như mới. Xem ngay ở bình luận đầu tiên nha!",
    },

    # === 3. HỘI DEADLINE (3 bài chủ lực) ===
    {
        "post_id": "1407231352464711_122111929659502096",
        "host_id": "1407231352464711",
        "guest_id": "1442323328956326",  # Phòng Trọ Hết Cứu (Cùng tệp đời sống trẻ)
        "guest_cmt": "Sáng đi làm gửi xe dưới hầm nóng hầm hập, lên tới bàn làm việc bật con quạt iMI mức 80 trong 2 phút là ráo sạch mồ hôi, bắt đầu vào việc tỉnh táo hẳn!",
        "host_reply": "Chuẩn bài cứu tinh mỗi sáng đi làm luôn bác ơi! 💼 Vừa làm quạt cầm tay lúc di chuyển, lên tới công ty lại đặt đứng trên bàn làm việc như một món phụ kiện công nghệ sang xịn. Link tham khảo mình ghim ở bình luận đầu tiên nhé!",
    },
    {
        "post_id": "1407231352464711_122111928543502096",
        "host_id": "1407231352464711",
        "guest_id": "1421270697727753",  # Ký Túc Xá Có Biến
        "guest_cmt": "Pin 5000mAh của quạt này nếu chỉ bật mức gió nhẹ 25-30 trên bàn làm việc buổi trưa thì mấy ngày mới phải cắm sạc lại 1 lần vậy ad?",
        "host_reply": "Nếu mỗi buổi nghỉ trưa văn phòng bạn bật mức gió dịu 25–30 trong khoảng 1–2 tiếng thì dùng vô tư cả tuần (5–6 ngày) mới cần cắm sạc lại qua cáp Type-C máy tính nhé! 🔋 Bạn xem chi tiết ưu đãi ở bình luận ghim đầu tiên nha!",
    },
    {
        "post_id": "1407231352464711_122110435863502096",
        "host_id": "1407231352464711",
        "guest_id": "1442323328956326",  # Phòng Trọ Hết Cứu
        "guest_cmt": "Từ ngày kê laptop lên giá đỡ nhôm ngang tầm mắt và dồn bàn phím rời ra phía trước theo hướng dẫn của Page, ngồi làm việc cả buổi sáng đỡ hẳn tật rướn cổ về phía màn hình!",
        "host_reply": "Chúc mừng bạn đã nâng cấp góc làm việc chuẩn công thái học nha! 🖥️✨ Chỉ cần thay đổi góc nhìn màn hình thêm 15–20cm chiều cao là giảm tải ngay áp lực cho đốt sống cổ. Chúc bạn một ngày chạy deadline mượt mà nhé!",
    },
]


def main():
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    pages_by_id = {p["id"]: p for p in vault.get("pages", [])}
    ai_page = pages_by_id[AI_ID]

    print("=== [CỤM 1 — AI PLAYERS] CHĂM SÓC BÌNH LUẬN KHÁCH HÀNG THẬT (KHÔNG SEEDING CHÉO TỪ 3 PAGE BÁN HÀNG) ===")
    p1_cmts = graph_get(
        "1022527194267367_122132884497248983/comments",
        ai_page["access_token"],
        {"fields": "id,from,message,comment_count", "limit": 15},
    ).get("data", [])
    for c in p1_cmts:
        fid = c.get("from", {}).get("id", "")
        if c.get("comment_count", 0) == 0 and fid not in ([AI_ID] + SALES_IDS):
            cid = c["id"]
            fname = c.get("from", {}).get("name", "bạn")
            graph_post(f"{cid}/likes", ai_page["access_token"], {})
            r = graph_post(
                f"{cid}/comments",
                ai_page["access_token"],
                {
                    "message": (
                        f"Chào {fname} nhé! 🚀 Cảm ơn bạn đã quan tâm tới kho mã nguồn Multi-Agent & RAG. "
                        f"Bạn lấy link GitHub chính thức ngay ở bình luận ghim đầu tiên và tham gia Nhóm Zalo Cộng Đồng Bảo Mật "
                        f"(https://zalo.me/g/etllok798 - Passcode: AIPLAYERS2026) để nhận trọn bộ Kho Vũ Khí 6 Subagent thực chiến tiếng Việt nha!"
                    )
                },
            )
            print(f"  + Đã trả lời khách hàng thật [{fname}] ({cid}): {r.get('id', r)}")

    print("\n=== [CỤM 2 — 3 PAGE BÁN HÀNG] TƯƠNG TÁC CHÉO NỘI BỘ 3 PAGE CÙNG TỆP ===")
    success_count = 0
    for item in SALES_CLUSTER_DIALOGUES:
        post_id = item["post_id"]
        host_page = pages_by_id[item["host_id"]]
        guest_page = pages_by_id[item["guest_id"]]

        # Cross-likes ONLY among the 3 Sales Pages
        for s_id in SALES_IDS:
            if s_id != item["host_id"] and s_id in pages_by_id:
                graph_post(f"{post_id}/likes", pages_by_id[s_id]["access_token"], {})

        c_res = graph_post(
            f"{post_id}/comments",
            guest_page["access_token"],
            {"message": item["guest_cmt"]},
        )
        if "id" in c_res:
            cid = c_res["id"]
            graph_post(f"{cid}/likes", host_page["access_token"], {})
            graph_post(f"{cid}/likes", guest_page["access_token"], {})
            r_res = graph_post(
                f"{cid}/comments",
                host_page["access_token"],
                {"message": item["host_reply"]},
            )
            success_count += 1
            print(f"  + [OK {success_count}/9] {host_page['name']} ({post_id}) <- {guest_page['name']} (cmt: {cid} | reply: {r_res.get('id', 'err')})")
        else:
            print(f"  ! [WARN] {post_id}: {c_res}")
        time.sleep(0.35)


if __name__ == "__main__":
    main()
