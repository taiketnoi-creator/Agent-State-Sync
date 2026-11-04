#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_subagent_agency_memory_and_rules.py — Khóa Cứng Định Vị Mới Của Page AI Players
vào Bộ Não Thứ 2 (bo-nao-thu-2), Mama (.agents/GEMINI.md), WORK-HISTORY.md và toàn bộ Subagent.
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent


def update_second_brain_index_and_manifest() -> None:
    # 1. Cập nhật INDEX.md của bo-nao-thu-2
    idx_path = SUBAGENT_DIR / "knowledge" / "bo-nao-thu-2" / "INDEX.md"
    idx_txt = idx_path.read_text(encoding="utf-8")
    new_row = (
        "| MEM-20261104-ai-players-subagent-agency-positioning | "
        "Mệnh lệnh CEO: Chuyển đổi 100% tuyến nội dung Page AI Players (cả Ảnh 1:1 & Video Reel 9:16) sang hướng Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Tạo Đội Ngũ Subagent May Đo Trọn Gói | "
        "decision | VALIDATED | ai-players, subagent-team, personal-subagent, enterprise-subagent, custom-agency-service, content-line, image-1x1, reel-9x16, ceo-mandate | "
        "CEO chỉ đạo trực tiếp — 2026-11-04 | `memories/MEM-20261104-ai-players-subagent-agency-positioning.md` |"
    )
    if "MEM-20261104-ai-players-subagent-agency-positioning" not in idx_txt:
        idx_txt = idx_txt.replace(
            "## Quy ước trạng thái",
            new_row + "\n\n## Quy ước trạng thái",
        )
        idx_path.write_text(idx_txt, encoding="utf-8")
        print("✅ Đã cập nhật knowledge/bo-nao-thu-2/INDEX.md")

    # 2. Cập nhật ACTIVE-RULES-MANIFEST.json của bo-nao-thu-2
    man_path = SUBAGENT_DIR / "knowledge" / "bo-nao-thu-2" / "ACTIVE-RULES-MANIFEST.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    man["version"] = "2.0.0"
    man["updated_at"] = "2026-11-04T09:20:00+07:00"

    rule_agency = {
        "rule_id": "RULE-AI-SUBAGENT-AGENCY-20261104",
        "name": "Tuyến Nội Dung Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Xây Dựng Đội Ngũ Subagent Trọn Gói (Page AI Players)",
        "memory_ref": "MEM-20261104-ai-players-subagent-agency-positioning",
        "description": "100% nội dung Hình ảnh 1:1 và Video Reel 9:16 trên Page AI Players phải xoay quanh 3 trụ cột: (1) Đội ngũ Subagent Cá nhân toàn diện, (2) Đội ngũ Subagent Doanh nghiệp chuyên môn hóa, và (3) Dịch vụ nhận tư vấn & xây dựng Đội ngũ Subagent may đo trọn gói cho khách hàng Cá nhân & Doanh nghiệp. Cấm đăng bài kiến thức AI/IT học thuật rời rạc chung chung.",
    }

    for agent_key in ["all", "content", "edit", "mkt", "content-da-kenh", "cham-soc-kenh", "quan-ly-kenh"]:
        rules_list = man["active_rules_by_agent"].setdefault(agent_key, [])
        if not any(r.get("rule_id") == "RULE-AI-SUBAGENT-AGENCY-20261104" for r in rules_list):
            rules_list.append(rule_agency)

    banned_list = man.setdefault("banned_stale_memories", [])
    if not any(b.get("pattern_id") == "BANNED-12" for b in banned_list):
        banned_list.append({
            "pattern_id": "BANNED-12",
            "keyword": "Nội dung AI/IT học thuật rời rạc chung chung trên Page AI Players (không gắn với Giải pháp & Dịch vụ Đội Ngũ Subagent Cá Nhân/Doanh Nghiệp)",
            "forbidden_elements": [
                "Giải thích thuật toán thuần học thuật (Prompt Caching, SLM 7B, Standard RAG, OCR) không gắn với Đội ngũ Subagent",
                "Chia sẻ tin tức AI chung chung không có CTA nhận xây dựng Đội ngũ Subagent cho Cá nhân & Doanh nghiệp"
            ],
            "reason": "CEO đã khóa cứng ngày 2026-11-04: Page AI Players chuyển 100% sang tuyến Subagent Cá nhân & Doanh nghiệp toàn diện, nhận tạo đội ngũ Subagent may đo trọn gói.",
            "replacement": "Mọi bài Ảnh 1:1 và Video Reel 9:16 trên AI Players phải minh họa sức mạnh của Đội ngũ Subagent Cá nhân/Doanh nghiệp và dẫn phễu Dịch vụ Xây dựng Đội ngũ Subagent trọn gói + Cộng đồng Zalo VIP."
        })

    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Đã cập nhật knowledge/bo-nao-thu-2/ACTIVE-RULES-MANIFEST.json")


def update_gemini_md_and_work_history() -> None:
    gem_path = SUBAGENT_DIR / ".agents" / "GEMINI.md"
    gem_txt = gem_path.read_text(encoding="utf-8")

    old_rule1_header = "1. **LUẬT #1 — Định Mức & Quy Chuẩn Ảnh Bài Đăng Độc Bản `Zero-Clone` Page `AI Players - Người chơi hệ AI` (`1022527194267367`):**"
    new_rule1_block = (
        "1. **LUẬT #1 — Định Vị Tuyến Nội Dung `Subagent Cá Nhân & Doanh Nghiệp Toàn Diện` + Quy Chuẩn Độc Bản `Zero-Clone` Page `AI Players - Người chơi hệ AI` (`1022527194267367`):**\n"
        "   - **TUYẾN NỘI DUNG CỐT LÕI ĐÃ KHÓA CỨNG NGÀY 04/11/2026 (`MEM-20261104-ai-players-subagent-agency-positioning`):**\n"
        "     + **100% cả Hình Ảnh (`1:1`) và Video Reels (`9:16`) trên Page `AI Players`** bắt buộc đi theo hướng **Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Tư Vấn, Thiết Kế & Xây Dựng Đội Ngũ Subagent May Đo Trọn Gói Cho Khách Hàng Cá Nhân & Doanh Nghiệp**.\n"
        "     + **CẤM TUYỆT ĐỐI (`BANNED-12`)** đăng các bài kiến thức AI/IT học thuật rời rạc chung chung không gắn với giải pháp Đội ngũ Subagent!\n"
        "     + Mọi bài đăng phải có CTA kép dẫn xuống `Pinned Comment #1`: **(1) Đặt lịch Tư vấn & Xây dựng Đội ngũ Subagent riêng cho Cá nhân/Doanh nghiệp** và **(2) Tham gia Nhóm Zalo Cộng Đồng VIP (`https://zalo.me/g/fzxvbf259`) để nhận bộ khung mẫu**."
    )
    if "MEM-20261104-ai-players-subagent-agency-positioning" not in gem_txt and old_rule1_header in gem_txt:
        gem_txt = gem_txt.replace(old_rule1_header, new_rule1_block, 1)

    # Cập nhật Mục 5 trong .agents/GEMINI.md
    if "## 5. SỔ TAY NHIỆM VỤ ĐANG THỰC THI" in gem_txt:
        head, _ = gem_txt.split("## 5. SỔ TAY NHIỆM VỤ ĐANG THỰC THI", 1)
        sec5 = """## 5. SỔ TAY NHIỆM VỤ ĐANG THỰC THI & CHỜ HOÀN TẤT (`ACTIVE TASKS — CẤM BỎ DỞ`)

*(Cập nhật đồng bộ 2 máy lúc `2026-11-04 09:25` — `mama` phải chủ động theo sát và hoàn tất dứt điểm từng việc dưới đây)*

1. **`[IN_PROGRESS]` (Ưu tiên #1 — Mệnh Lệnh Mới Của CEO 04/11) Chuyển Đổi 100% Tuyến Nội Dung Page `AI Players` (Cả Ảnh `1:1` & Video Reels `9:16`) Sang Hướng `Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Tạo Đội Ngũ Subagent Trọn Gói`:**
   - **Đã khóa cứng vào Bộ Não Thứ 2 (`MEM-20261104-ai-players-subagent-agency-positioning` & `ACTIVE-RULES-MANIFEST.json` v2.0.0)**: Cấm đăng bài kiến thức AI học thuật rời rạc; 100% Ảnh 1:1 (`6 bài/ngày`) và Video Reels 9:16 (`3 bài/ngày`) xoay quanh **Subagent Cá nhân toàn diện, Đội ngũ Subagent Doanh nghiệp, và Dịch vụ Nhận tạo Đội ngũ Subagent may đo 1:1**.
   - Thay thế toàn bộ hàng đợi hẹn giờ cũ trên `AI Players` (`04/11 – 06/11`) bằng lô **Ảnh Độc Bản `Zero-Clone` & Video Reels 9:16 chuẩn tuyến Subagent Cá nhân & Doanh nghiệp** kèm `Pinned Comment #1` nhận đặt làm Đội ngũ Subagent riêng.

2. **`[IN_PROGRESS]` (Ưu tiên #2) Sản Xuất & Nạp Kho Ảnh Vuông `1:1` Chuẩn `Minimal Pop-Bold Typography` Cho 3 Page Bán Hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`):**
   - Duy trì đều đặn 2 bài/page/ngày (`11:45` & `20:00`, chuẩn `Minimal Pop-Bold Typography`: ít chữ, chữ chính siêu dày `Black 900`, màu sắc bắt mắt + Pinned Comment #1 gắn link Shopee Affiliate `SHOPEE_AFFILIATE_ID=17395830088` + Bình luận phá băng #2).

3. **`[IN_PROGRESS]` (Ưu tiên #3) Vận Hành 3 Ca Tương Tác Hội Nhóm (`12:00`, `17:30`, `20:30`) Công Thức `80% Giá Trị + 20% Kéo Về Tường Fanpage` + Auto-Reply Bình Luận Khách:**
   - Chạy ngầm 100% (`--headless=new`), đồng bộ Cookie 2 máy (`guicci` & `Admin-PC`), riêng ngách `ai` điều hướng thẳng khách hàng cá nhân & chủ doanh nghiệp về dịch vụ xây dựng Đội ngũ Subagent trên tường Page `AI Players`.

4. **`[OPEN]` (Ưu tiên #4 — Đào Tạo Video AI Bán Hàng SLL Đạt Chuẩn Vàng Trước Khi Mở Băng):**
   - Hoàn thiện quy trình sản xuất Video AI Bán Hàng SLL đạt chuẩn Vàng trình CEO nghiệm thu (trong thời gian này 3 Page Bán Hàng giữ nguyên 100% chỉ đăng Ảnh vuông 1:1).
"""
        gem_txt = head + sec5
    gem_path.write_text(gem_txt, encoding="utf-8")
    print("✅ Đã cập nhật .agents/GEMINI.md")

    # Cập nhật WORK-HISTORY.md để mama_boot_check.py hiển thị đúng trên cả 2 máy
    wh_path = SUBAGENT_DIR / "WORK-HISTORY.md"
    if wh_path.exists():
        wh_txt = wh_path.read_text(encoding="utf-8")
        new_task_line = (
            "- [IN_PROGRESS] **(Ưu tiên #1 — Chốt 04/11) Chuyển Đổi 100% Tuyến Nội Dung Page `AI Players` (Ảnh `1:1` & Video Reel `9:16`) Sang Hướng `Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Tạo Đội Ngũ Subagent May Đo`:** "
            "Đã khóa vào Bộ Não Thứ 2 (`MEM-20261104-ai-players-subagent-agency-positioning`), xóa các bài AI học thuật rời rạc và nạp kho Ảnh + Video Reel định vị Dịch vụ Xây dựng Đội ngũ Subagent Cá nhân & Doanh nghiệp.\n"
        )
        if "MEM-20261104-ai-players-subagent-agency-positioning" not in wh_txt:
            wh_txt = wh_txt.replace(
                "- [IN_PROGRESS] **(Ưu tiên #1)",
                new_task_line + "- [DONE] **(Hạng mục trước)",
                1,
            )
            wh_path.write_text(wh_txt, encoding="utf-8")
            print("✅ Đã cập nhật WORK-HISTORY.md")


def update_specialist_agents_and_tools() -> None:
    agency_note = (
        "\n\n# Định Vị Cốt Lõi Của Page AI Players (Khóa Cứng Ngày 04/11/2026 — `MEM-20261104-ai-players-subagent-agency-positioning`)\n"
        "- **Tuyến nội dung duy nhất cho Page `AI Players - Người chơi hệ AI` (`1022527194267367`):** Cả Hình ảnh vuông `1:1` và Video Reels `9:16` đều phải xoay quanh **Hệ Sinh Thái Subagent Cá Nhân & Doanh Nghiệp Toàn Diện — Nhận Tư Vấn, Thiết Kế & Xây Dựng Đội Ngũ Subagent May Đo Trọn Gói Cho Khách Hàng Cá Nhân & Doanh Nghiệp**.\n"
        "- **Cấm tuyệt đối (`BANNED-12`):** Không làm bài kiến thức AI/IT học thuật rời rạc chung chung. Mọi bài đều phải dẫn về giải pháp Đội ngũ Subagent toàn diện và CTA đặt làm Đội ngũ Subagent riêng / tham gia Nhóm Zalo VIP tại Bình luận đầu tiên (#1).\n"
    )
    for rel in [
        "content.md",
        "edit.md",
        "content-da-kenh.md",
        "cham-soc-kenh.md",
        ".agents/plugins/agent-javis/agents/content.md",
        ".agents/plugins/agent-javis/agents/edit.md",
        ".agents/plugins/agent-javis/agents/content-da-kenh.md",
        ".agents/plugins/agent-javis/agents/cham-soc-kenh.md",
    ]:
        p = SUBAGENT_DIR / rel
        if p.exists():
            t = p.read_text(encoding="utf-8")
            if "MEM-20261104-ai-players-subagent-agency-positioning" not in t:
                p.write_text(t.rstrip() + agency_note, encoding="utf-8")
                print(f"✅ Đã cập nhật quy chuẩn Subagent Agency vào {rel}")


if __name__ == "__main__":
    update_second_brain_index_and_manifest()
    update_gemini_md_and_work_history()
    update_specialist_agents_and_tools()
