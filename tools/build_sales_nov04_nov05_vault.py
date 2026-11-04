#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sales_nov04_nov05_vault.py — Kết xuất & Lên lịch 9 Bài Ảnh Vuông 1:1 (Minimal Pop-Bold Typography)
Cho 3 Page Bán Hàng Affiliate (Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline)
Khung giờ: 04/11 11:45, 04/11 20:00, 05/11 11:45.
"""

import argparse
import datetime as dt
import json
import shutil
import sys
import time
import urllib.parse
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SUBAGENT_DIR / "tools"))

from render_vid_style_card import render_html_to_image
from render_sales_bold_editorial import clean_photo_zones_to_data_uri, build_bold_sales_card_html
from zero_repost_gate import record_published_content

VN_TZ = dt.timezone(dt.timedelta(hours=7))
AFF_ID = "17395830088"
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-11-04" / "sales-nov04-nov05-vault"
RAW_DIR = VAULT_DIR / "raw"
FINAL_DIR = VAULT_DIR / "images"
QA_GRID_PATH = VAULT_DIR / "sales_nov04_nov05_9_qa_grid.jpg"
MANIFEST_PATH = VAULT_DIR / "manifest.json"

ARTIFACT_DIR = Path(r"C:\Users\guicci\.gemini\antigravity\brain\1b0d78de-0eaf-4a05-a2d4-462df1e13063")

RAW_SOURCE_MAP = {
    "phongtro_07_ke_goc_nha_tam_dan_tuong_raw.png": ARTIFACT_DIR / "phongtro_07_ke_goc_nha_tam_dan_tuong_raw_1793758443189.jpg",
    "phongtro_08_may_bat_muoi_quang_xuc_tac_raw.png": ARTIFACT_DIR / "phongtro_08_may_bat_muoi_quang_xuc_tac_raw_1793758461391.jpg",
    "phongtro_09_thung_rac_cam_ung_thong_minh_raw.png": ARTIFACT_DIR / "phongtro_09_thung_rac_cam_ung_thong_minh_raw_1793758480476.jpg",
    "ktx_07_o_cam_thap_tich_hop_usb_c_raw.png": ARTIFACT_DIR / "ktx_07_o_cam_thap_tich_hop_usb_c_raw_1793758523623.jpg",
    "ktx_08_noi_lau_mini_2_tang_chong_dinh_raw.png": ARTIFACT_DIR / "ktx_08_noi_lau_mini_2_tang_chong_dinh_raw_1793758544911.jpg",
    "ktx_09_hop_dung_my_pham_chong_bui_raw.png": ARTIFACT_DIR / "ktx_09_hop_dung_my_pham_chong_bui_raw_1793758565728.jpg",
    "deadline_07_chuot_doc_cong_thai_hoc_raw.png": ARTIFACT_DIR / "deadline_07_chuot_doc_cong_thai_hoc_raw_1793758587374.jpg",
    "deadline_08_ly_giu_nhiet_inox_316_co_ong_hut_raw.png": ARTIFACT_DIR / "deadline_08_ly_giu_nhiet_inox_316_co_ong_hut_raw_1793758636869.jpg",
    "deadline_09_ban_phim_co_low_profile_khong_day_raw.png": ARTIFACT_DIR / "deadline_09_ban_phim_co_low_profile_khong_day_raw_1793758743999.jpg",
}


def build_shopee_link(keyword: str, sub_id: str) -> str:
    origin = f"https://shopee.vn/search?keyword={urllib.parse.quote(keyword)}"
    return f"https://s.shopee.vn/an_redir?origin_link={urllib.parse.quote(origin, safe='')}&affiliate_id={AFF_ID}&sub_id={sub_id}"


SALES_ITEMS_SPEC = [
    # ------------------------------------------------------------------
    # 1. PHÒNG TRỌ HẾT CỨU (1442323328956326)
    # ------------------------------------------------------------------
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-SHOWER-CADDY-0411",
        "slot_dt": "2026-11-04 11:45",
        "raw_file": "phongtro_07_ke_goc_nha_tam_dan_tuong_raw.png",
        "out_file": "phongtro_07_ke_goc_nha_tam_dan_tuong_bold.jpg",
        "accent_hex": "#0066FF",
        "accent_dark_hex": "#003D99",
        "page_badge": "GỌN NHÀ TẮM TRỌ",
        "title_line1": "KỆ GÓC NHÀ TẮM",
        "title_highlight": "INOX 304 DÁN TƯỜNG",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("KEO DÁN CHỊU 15KG", ""),
            ("RÃNH THOÁT NƯỚC", ""),
            ("MÓC TREO ĐA NĂNG", ""),
        ],
        "shopee_kw": "ke goc nha tam inox 304 dan tuong khong khoan",
        "sub_id": "phongtro-0411-showercaddy-pin-img",
        "caption": (
            "Nhà tắm phòng trọ đã nhỏ mà chai dầu gội, sữa tắm, sữa rửa mặt cứ phải xếp dưới sàn gạch ướt nhẹp, vừa trơn trượt vừa đóng cặn vàng ố dưới đáy chai!\n\n"
            "Không cần khoan đục tường làm mất tiền cọc chủ trọ, chỉ cần dán chiếc Kệ Góc Nhà Tắm Inox 304 Dán Tường Siêu Dính này vào góc gạch men là gọn sạch tức thì:\n"
            "✨ Miếng dán Acrylic bản rộng chịu tải tới 15kg: Đặt 6–8 chai dầu gội sữa tắm cỡ lớn vẫn bám chặt cứng, chống nước nóng hoàn toàn.\n"
            "✨ Chất liệu Inox 304 dày dặn chống gỉ sét 100%, đáy kệ khoét rãnh thoát nước nhanh khô thoáng.\n"
            "✨ Kèm dãy móc treo bông tắm, dao cạo râu và khăn mặt cực kỳ tiện lợi.\n\n"
            "💬 Hiện tại chai dầu gội sữa tắm ở phòng trọ bạn đang để trên kệ hay xếp dưới sàn nhà tắm? Xem ngay link kệ góc Inox 304 giá chỉ vài chục cành tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-MOSQUITO-LAMP-0411",
        "slot_dt": "2026-11-04 20:00",
        "raw_file": "phongtro_08_may_bat_muoi_quang_xuc_tac_raw.png",
        "out_file": "phongtro_08_may_bat_muoi_quang_xuc_tac_bold.jpg",
        "accent_hex": "#7C3AED",
        "accent_dark_hex": "#4C1D95",
        "page_badge": "NGỦ NGON KHÔNG MUỖI",
        "title_line1": "ĐÈN BẮT MUỖI UV",
        "title_highlight": "HÚT XOÁY LỐC ÊM RU",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("ÁNH SÁNG TÍM 365NM", ""),
            ("QUẠT HÚT XOÁY 360°", ""),
            ("KHAY ĐỰNG THÁO RỜI", ""),
        ],
        "shopee_kw": "den bat muoi thong minh quang xuc tac hut xoay loc",
        "sub_id": "phongtro-0411-mosquitolamp-pin-img",
        "caption": (
            "Phòng trọ tầng trệt hay gần cây cối cứ tối tắt đèn chuẩn bị ngủ là tiếng muỗi vo ve bên tai, xịt thuốc muỗi thì nồng nặc khó thở mà mắc màn thì bí bách!\n\n"
            "Chỉ cần cắm chiếc Đèn Bắt Muỗi Quang Xúc Tác Hút Xoáy Lốc 360° này ở góc phòng trước khi đi ngủ 1 tiếng là ngủ ngon một mạch tới sáng:\n"
            "✨ Vòng ánh sáng tím bước sóng 365nm kết hợp nhiệt lượng mô phỏng hơi người thu hút muỗi từ mọi góc phòng.\n"
            "✨ Quạt hút lốc xoáy 7 cánh cuốn chặt muỗi xuống lồng giam chống thoát bên dưới mà không gây tiếng nổ tanh tách giật mình.\n"
            "✨ Độ ồn dưới 25dB êm như tiếng lá rơi, vừa làm đèn ngủ dịu mắt vừa bảo vệ sức khỏe không hóa chất.\n\n"
            "💬 Phòng trọ của bạn hiện đang dùng vợt muỗi, nhang muỗi hay đèn bắt muỗi tự động? Săn ngay đèn bắt muỗi chính hãng tại bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-SMART-TRASH-0511",
        "slot_dt": "2026-11-05 11:45",
        "raw_file": "phongtro_09_thung_rac_cam_ung_thong_minh_raw.png",
        "out_file": "phongtro_09_thung_rac_cam_ung_thong_minh_bold.jpg",
        "accent_hex": "#FF3D00",
        "accent_dark_hex": "#9A1B00",
        "page_badge": "KHÓA MÙI SẠCH SẼ",
        "title_line1": "THÙNG RÁC CẢM ỨNG",
        "title_highlight": "MỞ NẮP TỰ ĐỘNG 0.3S",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("CẢM BIẾN VẪY TAY", ""),
            ("TỰ RÚT DÂY TÚI RÁC", ""),
            ("CHỐNG NƯỚC IPX5", ""),
        ],
        "shopee_kw": "thung rac thong minh cam ung tu dong dong mo nap",
        "sub_id": "phongtro-0511-smarttrash-pin-img",
        "caption": (
            "Phòng trọ khép kín nấu ăn ngay trong phòng mà dùng sọt rác không nắp thì mùi thức ăn thừa bốc lên khắp phòng và kéo ruồi gián tới ngay!\n\n"
            "Nâng cấp góc bếp và nhà vệ sinh phòng trọ với chiếc Thùng Rác Thông Minh Cảm Ứng Tự Động Mở Nắp 0.3 Giây này:\n"
            "✨ Cảm biến hồng ngoại thông minh: Chỉ cần đưa tay hoặc chạm nhẹ đầu gối cách 25cm là nắp tự bật mở trong 0.3s, sau 5 giây tự động đóng kín khóa chặt 100% mùi hôi.\n"
            "✨ Thiết kế vòng kẹp giấu viền túi rác gọn gàng cùng cơ chế rút dây buộc kín miệng túi mà tay không chạm bẩn.\n"
            "✨ Chuẩn chống nước IPX5 đặt thoải mái cả trong nhà tắm ẩm ướt lẫn cạnh bồn rửa bát.\n\n"
            "💬 Ở phòng trọ bạn đang dùng thùng rác đạp chân hay sọt rác hở nắp? Xem ngay ưu đãi thùng rác cảm ứng 16L tại bình luận đầu tiên nhé! 👇"
        ),
    },

    # ------------------------------------------------------------------
    # 2. KÝ TÚC XÁ CÓ BIẾN (1421270697727753)
    # ------------------------------------------------------------------
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-TOWER-SOCKET-0411",
        "slot_dt": "2026-11-04 11:45",
        "raw_file": "ktx_07_o_cam_thap_tich_hop_usb_c_raw.png",
        "out_file": "ktx_07_o_cam_thap_tich_hop_usb_c_bold.jpg",
        "accent_hex": "#0284C7",
        "accent_dark_hex": "#0369A1",
        "page_badge": "TRẠM ĐIỆN BÀN HỌC",
        "title_line1": "Ổ CẮM THÁP ĐA NĂNG",
        "title_highlight": "8 LỖ + CỔNG SẠC USB-C",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("SẠC NHANH TYPE-C", ""),
            ("CÔNG TẮC TỪNG TẦNG", ""),
            ("TỰ NGẮT CHỐNG QUÁ TẢI", ""),
        ],
        "shopee_kw": "o cam dien hinh thap da nang co cong usb type c chong qua tai",
        "sub_id": "ktx-0411-towersocket-pin-img",
        "caption": (
            "Cả phòng KTX 6–8 người mà chỉ có 2 ổ điện trên tường, mỗi lần cắm sạc laptop, điện thoại, quạt kẹp giường là phải tranh nhau từng lỗ cắm!\n\n"
            "Đặt ngay chiếc Ổ Cắm Điện Hình Tháp Đa Năng Tích Hợp Cổng USB & Type-C này ở giữa bàn học là cả nhóm cắm thoải mái không vướng víu:\n"
            "✨ Thiết kế trụ đứng 4 mặt thông minh: Các củ sạc to bản cắm xoay 4 hướng không bao giờ bị cấn đè lên nhau như ổ cắm dài truyền thống.\n"
            "✨ Tích hợp sẵn cụm cổng USB-A và Type-C sạc nhanh trực tiếp cho điện thoại, tai nghe mà không cần củ sạc rời.\n"
            "✨ Trang bị rơ-le tự ngắt khi quá tải 2500W và công tắc riêng cho từng tầng cực kỳ an toàn trong KTX.\n\n"
            "💬 Bàn học KTX của bạn hiện đang phải nối mấy chiếc ổ cắm điện mới đủ dùng? Săn ngay ổ cắm tháp chống cháy tại bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-MINI-HOTPOT-0411",
        "slot_dt": "2026-11-04 20:00",
        "raw_file": "ktx_08_noi_lau_mini_2_tang_chong_dinh_raw.png",
        "out_file": "ktx_08_noi_lau_mini_2_tang_chong_dinh_bold.jpg",
        "accent_hex": "#EA580C",
        "accent_dark_hex": "#9A3412",
        "page_badge": "CỨU ĐÓI ĐÊM KHUYA",
        "title_line1": "NỒI LẨU ĐIỆN MINI",
        "title_highlight": "2 TẦNG HẤP LUỘC KTX",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("LÒNG GỐM CHỐNG DÍNH", ""),
            ("CÔNG SUẤT 600W KTX", ""),
            ("VỪA NẤU VỪA HẤP", ""),
        ],
        "shopee_kw": "noi lau dien mini da nang 2 tang chong dinh cho sinh vien",
        "sub_id": "ktx-0411-minihotpot-pin-img",
        "caption": (
            "Đêm ôn thi đói bụng mà chỉ úp mì tôm nước sôi hoài cũng ngán, muốn nấu nồi mì trứng xúc xích hay hấp bánh bao nóng hổi mà sợ công suất cao làm nhảy át KTX!\n\n"
            "Chân ái của sinh viên nội trú chính là chiếc Nồi Lẩu Điện Mini Đa Năng 2 Tầng Kèm Xửng Hấp Inox này:\n"
            "✨ Hai nấc nhiệt 300W – 600W chuẩn an toàn điện KTX: Sôi nhanh trong 3 phút mà hoàn toàn không lo sập nguồn phòng.\n"
            "✨ Tầng dưới nấu mì, nấu lẩu, chiên trứng; tầng trên hấp bánh bao, há cảo, ngô khoai cùng lúc tiết kiệm gấp đôi thời gian.\n"
            "✨ Lòng nồi phủ men gốm Ceramic chống dính cao cấp, ăn xong chỉ cần lấy khăn giấy lau nhẹ rồi tráng nước là sạch bong.\n\n"
            "💬 Món tủ đêm khuya của phòng KTX bạn là mì tôm trứng hay lẩu viên thả? Xem ngay link nồi 2 tầng giá sinh viên dưới bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-COSMETIC-BOX-0511",
        "slot_dt": "2026-11-05 11:45",
        "raw_file": "ktx_09_hop_dung_my_pham_chong_bui_raw.png",
        "out_file": "ktx_09_hop_dung_my_pham_chong_bui_bold.jpg",
        "accent_hex": "#DB2777",
        "accent_dark_hex": "#9D174D",
        "page_badge": "GÓC BÀN XINH XỈU",
        "title_line1": "TỦ ĐỰNG MỸ PHẨM",
        "title_highlight": "NẮP VÒM CHỐNG BỤI",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("NẮP TRONG CHỐNG BỤI", ""),
            ("ĐỰNG CHAI CAO 22CM", ""),
            ("NGĂN KÉO PHÂN TẦNG", ""),
        ],
        "shopee_kw": "ke dung my pham co nap day chong bui cao cap",
        "sub_id": "ktx-0511-cosmeticbox-pin-img",
        "caption": (
            "Bàn học KTX chỉ rộng đúng 60cm, vừa để sách vở vừa bày lọ tẩy trang, kem chống nắng, son môi, cọ trang điểm là mỗi lần lấy vở học lại quệt đổ hết cả bàn!\n\n"
            "Gom gọn toàn bộ đồ skincare và makeup vào chiếc Tủ Đựng Mỹ Phẩm Nắp Vòm Chống Bụi Cao Cấp này là bàn học rộng thoáng gấp 3 lần:\n"
            "✨ Tầng trên nắp vòm mở 2 chiều cao ráo: Đựng vừa mọi chai nước tẩy trang, toner, xịt khoáng cỡ lớn tới 500ml mà không bám một hạt bụi.\n"
            "✨ Hai ngăn kéo phân tầng bên dưới cất gọn mặt nạ giấy, bảng phấn mắt, thỏi son và bông tẩy trang ngăn nắp.\n"
            "✨ Có quai xách chắc chắn, cuối tuần hay nghỉ hè mang đồ về quê cực kỳ gọn nhẹ.\n\n"
            "💬 Hiện tại đồ skincare trên bàn KTX của bạn đang xếp trong khay mở hay hộp có nắp đậy? Săn ngay tủ đựng mỹ phẩm màu kem xinh xỉu ở bình luận đầu tiên nha! 👇"
        ),
    },

    # ------------------------------------------------------------------
    # 3. HỘI DEADLINE (1407231352464711)
    # ------------------------------------------------------------------
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-VERT-MOUSE-0411",
        "slot_dt": "2026-11-04 11:45",
        "raw_file": "deadline_07_chuot_doc_cong_thai_hoc_raw.png",
        "out_file": "deadline_07_chuot_doc_cong_thai_hoc_bold.jpg",
        "accent_hex": "#2563EB",
        "accent_dark_hex": "#1E3A8A",
        "page_badge": "HẾT TÊ CỔ TAY",
        "title_line1": "CHUỘT DỌC KHÔNG DÂY",
        "title_highlight": "NGHIÊNG 57° ÊM CỔ TAY",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("GÓC CẦM TỰ NHIÊN 57°", ""),
            ("CLICK SILENT KHÔNG ỒN", ""),
            ("BLUETOOTH + USB 2.4G", ""),
        ],
        "shopee_kw": "chuot doc cong thai hoc khong day silent bluetooth",
        "sub_id": "deadline-0411-vertmouse-pin-img",
        "caption": (
            "Cầm chuột phẳng truyền thống làm việc liên tục 8–10 tiếng mỗi ngày khiến xương cẳng tay bị vặn chéo, lâu ngày dẫn đến tê buốt ngón tay và hội chứng ống cổ tay!\n\n"
            "Bảo vệ đôi tay chạy deadline mỗi ngày với chiếc Chuột Dọc Công Thái Học Không Dây Góc Nghiêng 57° này:\n"
            "✨ Góc nghiêng 57° chuẩn giải phẫu học: Đặt bàn tay ở tư thế 'bắt tay' tự nhiên nhất, giải phóng hoàn toàn áp lực đè lên dây thần kinh cổ tay.\n"
            "✨ Switch bấm Silent giảm 95% tiếng click: Làm việc đêm khuya hay trong văn phòng yên tĩnh đều êm ru, tích hợp sẵn nút Back/Forward ngay ngón cái.\n"
            "✨ Kết nối kép Bluetooth 5.0 + đầu thu USB 2.4G, pin sạc Type-C dùng liền 1 tháng mới phải sạc lại.\n\n"
            "💬 Cuối ngày làm việc cổ tay phải của bạn có hay bị mỏi hoặc tê nhẹ không? Trải nghiệm ngay chuột dọc công thái học tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-TUMBLER-316-0411",
        "slot_dt": "2026-11-04 20:00",
        "raw_file": "deadline_08_ly_giu_nhiet_inox_316_co_ong_hut_raw.png",
        "out_file": "deadline_08_ly_giu_nhiet_inox_316_co_ong_hut_bold.jpg",
        "accent_hex": "#0D9488",
        "accent_dark_hex": "#115E59",
        "page_badge": "ĐÁ LẠNH CẢ NGÀY",
        "title_line1": "LY GIỮ NHIỆT 900ML",
        "title_highlight": "INOX 316 GIỮ ĐÁ 24 GIỜ",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("LÕI INOX 316 Y TẾ", ""),
            ("KHÔNG ĐỌNG MỒ HÔI", ""),
            ("NẮP KÍN CHỐNG TRÀN", ""),
        ],
        "shopee_kw": "ly giu nhiet inox 316 900ml co quai xach ong hut",
        "sub_id": "deadline-0411-tumbler316-pin-img",
        "caption": (
            "Mua ly cà phê đá để trên bàn làm việc mới được 30 phút đã tan hết đá nhạt thếch, lại còn chảy nước mồ hôi ướt đẫm cả bàn phím và sổ tay!\n\n"
            "Giữ trọn vị cà phê mát lạnh tỉnh táo từ 8h sáng đến 8h tối với chiếc Ly Giữ Nhiệt 900ml Lõi Inox 316 Kèm Ống Hút & Quai Xách này:\n"
            "✨ Lõi thép không gỉ Inox 316 chuẩn y tế kết hợp thành bình cách nhiệt chân không 5 lớp: Giữ đá lạnh nguyên viên suốt 24 giờ và giữ nóng 12 giờ.\n"
            "✨ Bề mặt sơn tĩnh điện nhám mịn tuyệt đối không đọng một giọt mồ hôi nào ra mặt bàn laptop.\n"
            "✨ Nắp xoay gioăng Silicone chống tràn 360° tích hợp 2 chế độ uống (hút qua ống hút hoặc uống trực tiếp).\n\n"
            "💬 Khi ngồi chạy deadline bạn hay uống cà phê đá, trà đậm hay nước lọc? Săn ngay ly giữ nhiệt Inox 316 cỡ đại 900ml ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-LOWPROFILE-KB-0511",
        "slot_dt": "2026-11-05 11:45",
        "raw_file": "deadline_09_ban_phim_co_low_profile_khong_day_raw.png",
        "out_file": "deadline_09_ban_phim_co_low_profile_khong_day_bold.jpg",
        "accent_hex": "#E11D48",
        "accent_dark_hex": "#881337",
        "page_badge": "GÕ NHANH ÊM TAY",
        "title_line1": "BÀN PHÍM CƠ SIÊU MỎNG",
        "title_highlight": "LOW-PROFILE 3 CHẾ ĐỘ",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("SWITCH THẤP ĐỠ MỎI", ""),
            ("KẾT NỐI 3 THIẾT BỊ", ""),
            ("KHUNG NHÔM SIÊU MỎNG", ""),
        ],
        "shopee_kw": "ban phim co low profile khong day bluetooth 3 mode",
        "sub_id": "deadline-0511-lowprofilekb-pin-img",
        "caption": (
            "Gõ bàn phím laptop cả ngày thì nông tay và nóng máy, còn dùng bàn phím cơ dày cộp thì phải ngửa cổ tay lên cao gây mỏi nhức khớp cổ tay!\n\n"
            "Sự kết hợp hoàn hảo cho dân văn phòng và coder chạy deadline chính là chiếc Bàn Phím Cơ Không Dây Siêu Mỏng Low-Profile 3 Mode này:\n"
            "✨ Hành trình phím cơ Low-Profile ngắn hơn 40% so với phím cơ truyền thống: Phản hồi xúc giác đầm tay, gõ nhanh gấp rưỡi mà không cần kê tay vẫn không mỏi.\n"
            "✨ Khung hợp kim nhôm CNC mỏng nhẹ chỉ 14mm, bỏ gọn vào balo mang đi họp hay ra quán cà phê cực sang.\n"
            "✨ Chuyển đổi tức thì giữa 3 thiết bị (Laptop Windows, MacBook, iPad) chỉ bằng 1 tổ hợp phím Fn + 1/2/3.\n\n"
            "💬 Hiện tại bạn đang gõ trực tiếp trên phím laptop hay dùng bàn phím rời? Xem ngay link bàn phím cơ Low-Profile giá ưu đãi tại bình luận đầu tiên nhé! 👇"
        ),
    },
]


def stage_raw_files() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for dst_name, src_path in RAW_SOURCE_MAP.items():
        dst_path = RAW_DIR / dst_name
        if src_path.exists():
            shutil.copy2(src_path, dst_path)


def build_qa_grid_9(image_paths: list[Path], out_grid: Path) -> None:
    cols, rows = 3, 3
    cell = 360
    canvas = Image.new("RGB", (cols * cell, rows * cell), (15, 23, 42))
    for idx, p in enumerate(image_paths[:9]):
        with Image.open(p) as im:
            thumb = im.convert("RGB").resize((cell - 10, cell - 10), Image.Resampling.LANCZOS)
            x = (idx % cols) * cell + 5
            y = (idx // cols) * cell + 5
            canvas.paste(thumb, (x, y))
    canvas.save(out_grid, format="JPEG", quality=93, optimize=True)


def publish_and_schedule_sales_9(manifest_items: list[dict]) -> list[dict]:
    import requests
    from mama_auto_scheduler_engine import load_vault, graph_post

    pages = load_vault()
    now_ts = int(dt.datetime.now(VN_TZ).timestamp())

    for item in manifest_items:
        pid = item["page_id"]
        tok = pages[pid]["access_token"]
        img_path = Path(item["image_path"])
        dt_obj = dt.datetime.strptime(item["slot_dt"], "%Y-%m-%d %H:%M").replace(tzinfo=VN_TZ)
        sched_ts = int(dt_obj.timestamp())
        if sched_ts <= now_ts + 900:
            sched_ts = 0

        data = {"caption": item["caption"], "access_token": tok}
        if sched_ts > 0:
            data["published"] = "false"
            data["scheduled_publish_time"] = str(sched_ts)
        else:
            data["published"] = "true"

        with open(img_path, "rb") as f:
            r = requests.post(
                f"https://graph.facebook.com/v22.0/{pid}/photos",
                data=data,
                files={"source": (img_path.name, f, "image/jpeg")},
                timeout=90,
            )
        res = r.json()
        post_id = res.get("post_id") or res.get("id", "")
        cmt_id = ""
        if post_id:
            record_published_content(
                page_id=pid,
                media_path=img_path,
                caption=item["caption"],
                post_id=str(post_id),
            )
            c_res = graph_post(f"{post_id}/comments", tok, {"message": item["pinned_cmt"]})
            cmt_id = c_res.get("id", "")
            item["status"] = "LIVE_PUBLISHED" if sched_ts == 0 else "SCHEDULED"
            item["post_id"] = post_id
            item["comment_id"] = cmt_id
            print(f"✅ [{item['page_name']} | {item['sku_code']}] {item['status']} ({item['slot_dt']}) -> post_id={post_id} | cmt_id={cmt_id}", flush=True)
        else:
            item["status"] = "ERROR"
            item["error"] = res
            print(f"❌ [{item['sku_code']}] Lỗi: {res}", flush=True)
        time.sleep(1.2)
    return manifest_items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Đăng/Hẹn giờ 9 bài lên 3 Page Bán Hàng")
    args = parser.parse_args()

    stage_raw_files()
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    for idx, spec in enumerate(SALES_ITEMS_SPEC, 1):
        raw_p = RAW_DIR / spec["raw_file"]
        if not raw_p.exists():
            raise FileNotFoundError(f"Chưa có ảnh raw: {raw_p}")
        out_jpg = FINAL_DIR / spec["out_file"]
        uri, bg_col = clean_photo_zones_to_data_uri(raw_p, erase_legacy_text=False)
        html = build_bold_sales_card_html(
            bg_data_uri=uri,
            bg_css_color=bg_col,
            page_badge=spec["page_badge"],
            title_line1=spec["title_line1"],
            title_highlight=spec["title_highlight"],
            spec_pills=spec["spec_pills"],
            macro_points=spec["macro_points"],
            detail_items=spec["detail_items"],
            accent_hex=spec["accent_hex"],
            accent_dark_hex=spec["accent_dark_hex"],
            secondary_hex="#0F172A",
        )
        render_html_to_image(html, out_jpg, width=1080, height=1080)
        rendered_paths.append(out_jpg)

        shopee_url = build_shopee_link(spec["shopee_kw"], spec["sub_id"])
        pinned_cmt = (
            f"🛒 LINK CHÍNH HÃNG {spec['title_line1']} {spec['title_highlight']} GIÁ ƯU ĐÃI:\n"
            f"👉 Xem chi tiết & săn deal trên Shopee tại đây: {shopee_url}\n\n"
            f"ℹ️ [Affiliate Disclosure: Chia sẻ có thể mang lại khoản hoa hồng nhỏ giúp duy trì Page mà không làm thay đổi giá mua của bạn!]"
        )
        manifest_items.append({
            "index": idx,
            "page_id": spec["page_id"],
            "page_name": spec["page_name"],
            "sku_code": spec["sku_code"],
            "slot_dt": spec["slot_dt"],
            "image_path": str(out_jpg),
            "shopee_url": shopee_url,
            "caption": spec["caption"],
            "pinned_cmt": pinned_cmt,
        })
        print(f"  ✔ [{idx:02d}/09] Đã kết xuất ảnh Minimal Pop-Bold Typography: {out_jpg.name}", flush=True)

    build_qa_grid_9(rendered_paths, QA_GRID_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 9 ảnh bán hàng tại: {QA_GRID_PATH}", flush=True)

    if args.publish:
        manifest_items = publish_and_schedule_sales_9(manifest_items)

    MANIFEST_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_PATH}", flush=True)


if __name__ == "__main__":
    main()
