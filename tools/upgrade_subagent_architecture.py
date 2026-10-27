#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_subagent_architecture.py — Kiểm toán & Nâng cấp toàn diện cấu trúc 10 Agent (mama + 9 Subagent):
1. Chuẩn hóa YAML Frontmatter (`model: inherit` / `model: flash`, công cụ chuẩn Antigravity `read_file`, `write_file`, `edit_file`, `send_message`).
2. Đóng gói 9 Subagent chuyên biệt vào Plugin chuẩn `.agents/plugins/agent-javis/agents/*.md` và kích hoạt trực tiếp trên LanguageServer.
3. Khóa giao thức Single-Pass Execution & Role Identity Guard chống vòng lặp giữa Mama và Subagent.
4. Đồng bộ quy tắc lịch đăng trong `quan-ly-kenh.md` và `mama.md` khớp 100% với 8 Luật Cứng của CEO.
"""

import json
import os
import pathlib
import re
import shutil
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / ".agents" / "plugins" / "agent-javis"
AGENTS_DIR = PLUGIN_DIR / "agents"

SPECIALISTS = [
    "mkt",
    "content",
    "edit",
    "voice",
    "content-da-kenh",
    "quan-ly-kenh",
    "cham-soc-kenh",
    "hieu-suat",
    "bo-nao-thu-2",
]

SINGLE_PASS_RULE_BLOCK = """
## Giao thức Phản hồi Nhanh & Chống Vòng Lặp (`Single-Pass Subagent Protocol`)

- **Phân tách danh tính tuyệt đối:** Bạn là Subagent chuyên môn, **KHÔNG PHẢI `mama`**. Tuyệt đối không in lại `BÁO CÁO KHỞI ĐỘNG PHIÊN CỦA MAMA`, không hỏi lại `Confirmation Summary`, và không tự gọi dây chuyền sang Subagent khác.
- **Thực thi 1 mạch (`1-Turn Execution`):** Ngay khi nhận Task Packet từ `mama`, dùng các công cụ chuẩn (`read_file`, `write_file`, `edit_file`, `run_command`, MCP) để hoàn thành trọn vẹn đầu ra trong 1 lượt.
- **Bàn giao gọn nhẹ (`Zero-Waste Handoff`):** Ghi chi tiết vào file artifact được chỉ định hoặc SQLite, sau đó trả báo cáo nghiệm thu tóm tắt **10–15 dòng** (nêu rõ trạng thái `READY_FOR_REVIEW` / `BLOCKED`, đường dẫn file đầu ra, điểm tự chấm Rubric) về cho `mama` rồi **DỪNG NGAY LẬP TỨC** (không lặp lại tool call).
""".strip()


def fix_frontmatter_and_tools(md_text: str, is_mama: bool = False) -> str:
    # Normalize line endings to LF for clean regex processing
    txt = md_text.replace("\r\n", "\n")

    # 1. Fix model field in YAML frontmatter
    txt = re.sub(r"^model:\s*inherit\s*\(.*?\)\s*$", "model: inherit", txt, flags=re.M)
    txt = re.sub(r"^model:\s*flash\s*\(.*?\)\s*$", "model: flash", txt, flags=re.M)

    # 2. Fix tool names in frontmatter and body
    txt = txt.replace("- view_file", "- read_file")
    txt = txt.replace("- write_to_file", "- write_file")
    txt = txt.replace("- replace_file_content", "- edit_file")
    txt = txt.replace("`view_file`", "`read_file`")
    txt = txt.replace("`write_to_file`", "`write_file`")
    txt = txt.replace("`replace_file_content`", "`edit_file`")

    # 3. Ensure send_message is in specialist tools list so subagents can message mama
    if not is_mama:
        m = re.search(r"^---\n(.*?)\n---", txt, flags=re.S)
        if m:
            fm = m.group(1)
            if "- send_message" not in fm and "tools:" in fm:
                fm = fm.replace("tools:\n", "tools:\n  - send_message\n", 1)
                txt = f"---\n{fm}\n---" + txt[m.end():]

        # 4. Inject Single-Pass Subagent Protocol if not present
        if "Single-Pass Subagent Protocol" not in txt:
            # Insert right after the # Vai trò section
            role_match = re.search(r"(# Vai trò\n+.*?\n)(?=\n# )", txt, flags=re.S)
            if role_match:
                insert_pos = role_match.end(1)
                txt = txt[:insert_pos] + "\n\n" + SINGLE_PASS_RULE_BLOCK + "\n" + txt[insert_pos:]

    return txt


def upgrade_mama_md(txt: str) -> str:
    # Replace old rigid CEO INTAKE GATE with Dual-Speed Execution
    old_intake = """
> **CEO INTAKE GATE — BẮT BUỘC HỎI LẠI TRƯỚC KHI ĐIỀU PHỐI:** Bạn luôn phải xác định mục tiêu, kết quả mong muốn, phạm vi, dữ liệu/asset còn thiếu, deadline, KPI và quyền được phép tác động bên ngoài. Không tự suy đoán các lựa chọn có thể làm đổi đáng kể chiến lược, ngân sách, pháp lý hoặc thương hiệu.

## Giao thức hỏi lại CEO

Trước khi gọi agent con, gửi một `Confirmation Summary` ngắn và hỏi các mục còn thiếu:

1. Mục tiêu chính là view, retention, CTR, đơn hàng, commission hay mục tiêu khác?
2. Tệp khách, sản phẩm/ngách, thị trường, nền tảng và mùa/sự kiện nào trong phạm vi?
3. Kết quả cần bàn giao gồm những artifact nào, số lượng bao nhiêu và deadline?
4. Ngân sách, giá trần, claim cấm, brand constraint hoặc compliance constraint nào?
5. Input/asset/link/dữ liệu nào đã có; phần nào cần agent nghiên cứu?
6. Trạng thái là `DRAFT_ONLY`, `READY_FOR_REVIEW` hay CEO đã cho phép `APPROVED_TO_PUBLISH`?
7. KPI, attribution window, điều kiện stop/scale và người duyệt cuối là ai?

Nếu brief đã trả lời đủ, vẫn hỏi một câu xác nhận: **“Tôi đã hiểu đúng mục tiêu, phạm vi, đầu ra và quyền hành động như trên; xác nhận để tôi mở Wave 1?”** Chỉ mở wave sau khi CEO xác nhận, trừ tác vụ chỉ đọc/nội bộ không có tác động bên ngoài.

> **BẠN LÀ BỘ NÃO ĐIỀU PHỐI:** Tuyệt đối không tự làm nội dung chi tiết. Nhiệm vụ của bạn là nhận lệnh CEO → Phân rã mục tiêu → Chỉ định rõ Subagent nào làm gì, đầu vào là gì, đầu ra yêu cầu là gì → Tổng hợp nghiệm thu cho CEO duyệt.
""".strip()

    new_intake = """
> **⚡ CƠ CHẾ PHÂN LUỒNG 2 TỐC ĐỘ (`DUAL-SPEED EXECUTION` — TRIỆT TIÊU VÒNG LẶP CHẬM TRỄ):**
> 1. **Luồng Nhanh (`FAST-TRACK — 1-Turn Direct / Single-Wave`):**
>    - Áp dụng cho **tác vụ vận hành hàng ngày, sửa lỗi nóng, kiểm tra hệ thống, dọn bài trùng, hoặc sản xuất lô ảnh/bài đăng theo khuôn mẫu đã khóa cứng** (như 8 Luật Cứng trong `.agents/GEMINI.md`): **TUYỆT ĐỐI KHÔNG** bắt CEO trả lời 7 câu `Confirmation Summary`, **KHÔNG** chia nhỏ thành 6 Wave tuần tự rườm rà. Thực thi ngay bằng script Python/MCP 0-token hoặc gọi **1 Wave Subagent song song duy nhất** để hoàn tất ngay trong 1 lượt!
> 2. **Luồng Chiến Dịch Mới (`FULL CAMPAIGN DAG — Multi-Wave`):**
>    - Chỉ áp dụng khi CEO yêu cầu lập chiến dịch mới hoàn toàn từ con số 0 và còn thiếu thông tin trọng yếu (chưa rõ sản phẩm, ngân sách, pháp lý).

## Giao thức hỏi lại CEO (Chỉ áp dụng cho Chiến dịch mới chưa rõ đầu vào)

Khi mở chiến dịch mới từ đầu và thiếu thông tin trọng yếu, gửi `Confirmation Summary` ngắn gọn (tối đa 3 câu hỏi cốt lõi còn thiếu trong 7 mục sau):

1. Mục tiêu chính là view, retention, CTR, đơn hàng, commission hay mục tiêu khác?
2. Tệp khách, sản phẩm/ngách, thị trường, nền tảng và mùa/sự kiện nào trong phạm vi?
3. Kết quả cần bàn giao gồm những artifact nào, số lượng bao nhiêu và deadline?
4. Ngân sách, giá trần, claim cấm, brand constraint hoặc compliance constraint nào?
5. Input/asset/link/dữ liệu nào đã có; phần nào cần agent nghiên cứu?
6. Trạng thái là `DRAFT_ONLY`, `READY_FOR_REVIEW` hay CEO đã cho phép `APPROVED_TO_PUBLISH`?
7. KPI, attribution window, điều kiện stop/scale và người duyệt cuối là ai?

Nếu brief đã rõ hoặc thuộc **Luồng Nhanh (`FAST-TRACK`)**, tiến hành thực thi ngay lập tức mà không làm gián đoạn công việc của CEO.

> **BẠN LÀ BỘ NÃO ĐIỀU PHỐI THỰC CHIẾN:** Với chiến dịch lớn, hãy phân rã mục tiêu → Chỉ định rõ Subagent nào làm gì, đầu vào là gì, đầu ra yêu cầu là gì → Tổng hợp nghiệm thu cho CEO duyệt. Với tác vụ vận hành định kỳ/khẩn cấp đã có sẵn công cụ tự động trong `tools/`, xử lý dứt điểm ngay trong 1 lượt.
""".strip()

    if old_intake in txt:
        txt = txt.replace(old_intake, new_intake)

    old_batch = """
- **Phân tầng Model & Gọi Subagent theo lô (`Batch Subagent Invocation`):**
  + **Tầng Sáng tạo & Duyệt Gate (`Model="inherit"` — Gemini 4):** Áp dụng bắt buộc cho các Subagent phụ trách chất lượng ý tưởng, visual và phễu chuyển đổi: `mama`, `mkt`, `content`, `edit` (đảm bảo rubric $\\ge 9.0/10$).
  + **Tầng Hậu cần & Vận hành (`Model="flash"` — Gemini Flash):** Áp dụng cho các Subagent thừa hành, chuẩn hóa và phân phối: `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`.
  + **Gộp lệnh song song (`Batch Subagent Invocation`):** Truyền nhiều Subagent vào cùng một mảng `Subagents` trong 1 lần gọi `invoke_subagent` duy nhất (ví dụ sau khi có kịch bản, chạy song song `voice` + `content-da-kenh` + `cham-soc-kenh`) nhằm giảm tối đa số turns và tiết kiệm quota Gemini 4.
""".strip()

    new_batch = """
- **Phân tầng Model & Gọi Subagent song song (`Parallel Subagent Invocation`):**
  + **Tầng Sáng tạo & Duyệt Gate (`Model="inherit"` — Gemini 4):** Áp dụng bắt buộc cho các Subagent phụ trách chất lượng ý tưởng, visual và phễu chuyển đổi: `mama`, `mkt`, `content`, `edit` (đảm bảo rubric $\\ge 9.0/10$).
  + **Tầng Hậu cần & Vận hành (`Model="flash"` — Gemini Flash):** Áp dụng cho các Subagent thừa hành, chuẩn hóa và phân phối: `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`.
  + **Gọi song song đúng chuẩn Antigravity (`Parallel Tool Calls`):** Mỗi lệnh `invoke_subagent` truyền đúng 1 `TypeName` (`mkt`, `content`, `edit`, `voice`, `content-da-kenh`, `quan-ly-kenh`, `cham-soc-kenh`, `hieu-suat`, `bo-nao-thu-2`). Khi cần chạy song song nhiều Subagent trong cùng 1 Wave (ví dụ `voice` + `content-da-kenh` + `cham-soc-kenh`), phát **nhiều tool call `invoke_subagent` đồng thời trong cùng 1 lượt phản hồi** (tuyệt đối không truyền mảng `Subagents` không tồn tại trong schema).
""".strip()

    if old_batch in txt:
        txt = txt.replace(old_batch, new_batch)

    return txt


def upgrade_quan_ly_kenh_md(txt: str) -> str:
    old_sec = """
- **Tự động hóa Lên lịch & Đăng bài qua MCP `facebook-page`:**
  + Khi đã có lệnh `APPROVED_TO_PUBLISH`:
    * Lên lịch bài viết: Gọi MCP `facebook-page:schedule_post` với thời gian phát hành rơi đúng vào 2 khung giờ vàng: **11h45 trưa** hoặc **20h00 tối** (Asia/Ho_Chi_Minh).
    * Đăng ngay: Gọi MCP `facebook-page:post_to_facebook` (đối với video/status/link) hoặc `facebook-page:post_image_to_facebook` (đối với bài ảnh/carousel).
    * Kiểm tra lịch đã lên: Gọi MCP `facebook-page:get_scheduled_posts` để xác thực lịch đăng và đảm bảo tuân thủ nghiêm ngặt giới hạn **tối đa 2 video/ngày/kênh**.
    * Lấy thông tin kênh: Gọi MCP `facebook-page:get_page_info`.
""".strip()

    new_sec = """
- **Tự động hóa Lên lịch & Đăng bài qua MCP `facebook-page` & Cổng Chặn `zero_repost_gate.py`:**
  + **Bắt buộc kiểm tra chống đăng lặp (`tools/zero_repost_gate.py`):** Mọi bài đăng/ảnh/video trước khi xuất bản hoặc hẹn giờ đều phải đi qua `verify_fresh_content()` (kiểm tra SHA-256, tên file, dấu vân tay nội dung và đối chiếu trực tiếp trên Meta Graph API), cấm tuyệt đối đăng lặp lại nội dung cũ.
  + Khi đã có lệnh `APPROVED_TO_PUBLISH`, áp dụng đúng định mức cho từng nhóm Page theo **Luật #1 & Luật #3 của CEO**:
    * **Nhóm A — Page `AI Players - Người chơi hệ AI` (`1022527194267367`):** Định mức **9 bài/ngày** gồm **6 bài Ảnh vuông `1:1` (`1080×1080`)** (`08:30, 10:15, 13:30, 15:15, 18:15, 21:15`) + **3 Video Reels Remotion** (`11:45, 16:30, 20:00`), 100% có `Pinned Comment #1` dẫn phễu.
    * **Nhóm B — 3 Page Bán Hàng Affiliate (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`):** **Đóng băng tuyệt đối Video Bán Hàng**; chỉ đăng **2 bài Ảnh vuông `1:1`/page/ngày** (`Editorial Macro & 3-Detail Grid`) vào 2 khung giờ vàng cố định: **11h45 trưa** và **20h00 tối** (Asia/Ho_Chi_Minh), 100% có `Pinned Comment #1` gắn link Shopee Affiliate (`SHOPEE_AFFILIATE_ID=17395830088`).
    * Kiểm tra lịch đã lên: Gọi MCP `facebook-page:get_scheduled_posts` để xác thực lịch đăng đúng định mức của từng Page.
    * Lấy thông tin kênh: Gọi MCP `facebook-page:get_page_info`.
""".strip()

    if old_sec in txt:
        txt = txt.replace(old_sec, new_sec)

    old_step2 = """
## Bước 2 — Lập Content Calendar

- **CHỈ ĐĂNG ĐÚNG 2 KHUNG GIỜ VÀNG CỐ ĐỊNH: 11h45 trưa và 20h00 tối** (Asia/Ho_Chi_Minh), nằm trong các cửa sổ 11:30–13:30 và 19:30–22:30.
- **TUYỆT ĐỐI KHÔNG đăng quá 2 video/ngày trên cùng một kênh.**
- Ghép đúng video version, title, caption, hashtag, disclosure và link routing.
- Facebook Reels: không đặt URL trong caption; **MỌI VIDEO KHI LÊN LỊCH PHẢI ĐI KÈM MẪU PINNED COMMENT CHỨA LINK SHOPEE** sau khi publish được duyệt.
- YouTube Shorts: ưu tiên link trong description/bio; chỉ dùng comment khi policy/connector cho phép và có approval.
""".strip()

    new_step2 = """
## Bước 2 — Lập Content Calendar

- **Định mức & Khung giờ chuẩn theo từng nhóm Fanpage (Asia/Ho_Chi_Minh):**
  + **3 Page Bán Hàng (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`):** Chỉ đăng **2 bài Ảnh vuông `1:1`/ngày/kênh** vào đúng **11:45 trưa và 20:00 tối** (đóng băng video bán hàng cho đến khi CEO mở băng).
  + **Page `AI Players - Người chơi hệ AI`:** Đăng **9 bài/ngày** (**6 bài Ảnh `1:1`** lúc `08:30, 10:15, 13:30, 15:15, 18:15, 21:15` + **3 Video Reels** lúc `11:45, 16:30, 20:00`).
- Ghép đúng asset version, title, caption, hashtag, disclosure và link routing; kiểm tra qua `zero_repost_gate.py`.
- Trên Facebook: không đặt URL trong caption; **100% BÀI ĐĂNG/VIDEO KHI LÊN LỊCH PHẢI ĐI KÈM PINNED COMMENT #1** (chứa link Shopee Affiliate đối với 3 Page Bán Hàng, hoặc link/keyword dẫn phễu đối với Page `AI Players`).
- YouTube Shorts: ưu tiên link trong description/bio; chỉ dùng comment khi policy/connector cho phép và có approval.
""".strip()

    if old_step2 in txt:
        txt = txt.replace(old_step2, new_step2)

    return txt


def main():
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    plugin_manifest = {
        "name": "agent-javis",
        "displayName": "Agent-Javis 9 Subagents Team",
        "description": "Đội 9 Subagent chuyên biệt E-commerce & Affiliate AI dưới quyền điều phối của Mama (Chief of Staff).",
        "version": "3.1.0",
    }
    (PLUGIN_DIR / "plugin.json").write_text(
        json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # 1. Process mama.md
    mama_path = ROOT / "mama.md"
    mama_txt = mama_path.read_text(encoding="utf-8")
    mama_txt = fix_frontmatter_and_tools(mama_txt, is_mama=True)
    mama_txt = upgrade_mama_md(mama_txt)
    mama_path.write_text(mama_txt, encoding="utf-8")
    print("✅ Updated mama.md")

    # 2. Process 9 specialists and copy into .agents/plugins/agent-javis/agents/
    for name in SPECIALISTS:
        sp_path = ROOT / f"{name}.md"
        txt = sp_path.read_text(encoding="utf-8")
        txt = fix_frontmatter_and_tools(txt, is_mama=False)
        if name == "quan-ly-kenh":
            txt = upgrade_quan_ly_kenh_md(txt)
        sp_path.write_text(txt, encoding="utf-8")
        (AGENTS_DIR / f"{name}.md").write_text(txt, encoding="utf-8")
        print(f"✅ Updated & registered {name}.md -> .agents/plugins/agent-javis/agents/{name}.md")

    # 3. Also copy sync-light.ps1 and on_stop_sync.py from Agent-State-Sync to Subagent so there are no stale paths
    sync_repo = ROOT.parent / "Agent-State-Sync"
    if (sync_repo / "sync-light.ps1").exists():
        shutil.copy2(sync_repo / "sync-light.ps1", ROOT / "sync-light.ps1")
        print("✅ Synced clean sync-light.ps1 to Subagent/")

    # 4. Enable plugin in LanguageServer and verify all 9 agents parse cleanly
    addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS", "")
    token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN", "")
    if addr and token:
        # Enable agent-javis plugin live
        req_en = urllib.request.Request(
            f"http://{addr}/exa.language_server_pb.LanguageServerService/JetboxWriteState",
            data=json.dumps({"userConfig": {"plugins": {"agent-javis": {"enabled": True}}}}).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-codeium-csrf-token": token},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req_en, timeout=5) as _:
                pass
        except Exception as e:
            print("⚠️ JetboxWriteState warning:", e)

        req_ls = urllib.request.Request(
            f"http://{addr}/exa.language_server_pb.LanguageServerService/GetAllPlugins",
            data=json.dumps({"workspaceUris": ["file:///f:/Ai%20Agent%20Setup/SubAgent/Subagent"]}).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-codeium-csrf-token": token},
            method="POST",
        )
        with urllib.request.urlopen(req_ls, timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
            for p in data.get("plugins", []):
                if p.get("name") == "agent-javis":
                    agents = p.get("agents", [])
                    print(f"\n🎯 Antigravity LanguageServer Discovery: {len(agents)}/9 Subagents ACTIVE!")
                    for a in agents:
                        ag = a.get("agent", {})
                        tools_list = [t.get("name") for t in ag.get("config", {}).get("agentConfig", {}).get("mixinConfig", {}).get("tools", [])]
                        print(f"   - {ag.get('name'):16s} | Tier: {ag.get('modelTier'):18s} | Tools ({len(tools_list)}): {', '.join(tools_list[:6])}...")


if __name__ == "__main__":
    main()
