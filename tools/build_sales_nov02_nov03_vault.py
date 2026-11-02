#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sales_nov02_nov03_vault.py — Kết xuất & Lên lịch 9 Bài Ảnh Vuông 1:1 (Minimal Pop-Bold Typography)
Cho 3 Page Bán Hàng Affiliate (Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline)
Khung giờ: 02/11 11:45, 02/11 20:00, 03/11 11:45.
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
from zero_repost_gate import record_published_content, verify_zero_clone_images

VN_TZ = dt.timezone(dt.timedelta(hours=7))
AFF_ID = "17395830088"
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-11-02" / "sales-nov02-nov03-vault"
RAW_DIR = VAULT_DIR / "raw"
FINAL_DIR = VAULT_DIR / "images"
QA_GRID_PATH = VAULT_DIR / "sales_nov02_nov03_9_qa_grid.jpg"
MANIFEST_PATH = VAULT_DIR / "manifest.json"

ARTIFACT_DIR = Path(r"C:\Users\guicci\.gemini\antigravity\brain\1b0d78de-0eaf-4a05-a2d4-462df1e13063")

RAW_SOURCE_MAP = {
    "phongtro_04_cay_lau_nha_tu_vat_raw.png": ARTIFACT_DIR / "phongtro_04_cay_lau_nha_tu_vat_raw_png_1793583907268.jpg",
    "phongtro_05_hop_o_cam_chong_chay_raw.png": ARTIFACT_DIR / "phongtro_05_hop_o_cam_chong_chay_raw_1793583937313.jpg",
    "phongtro_06_ron_dan_chan_cua_raw.png": ARTIFACT_DIR / "phongtro_06_ron_dan_chan_cua_raw_1793583969951.jpg",
    "ktx_04_quat_tich_dien_kep_giuong_raw.png": ARTIFACT_DIR / "ktx_04_quat_tich_dien_kep_giuong_raw_1793583991908.jpg",
    "ktx_05_tui_hut_chan_khong_chan_goi_raw.png": ARTIFACT_DIR / "ktx_05_tui_hut_chan_khong_chan_goi_raw_1793584013993.jpg",
    "ktx_06_ban_hoc_gap_gon_khe_ipad_raw.png": ARTIFACT_DIR / "ktx_06_ban_hoc_gap_gon_khe_ipad_raw_1793584035641.jpg",
    "deadline_04_gia_do_laptop_nhom_cnc_raw.png": ARTIFACT_DIR / "deadline_04_gia_do_laptop_nhom_cnc_raw_1793584063984.jpg",
    "deadline_05_goi_tua_lung_cao_su_non_raw.png": ARTIFACT_DIR / "deadline_05_goi_tua_lung_cao_su_non_raw_1793584095779.jpg",
    "deadline_06_dong_ho_pomodoro_xoay_raw.png": ARTIFACT_DIR / "deadline_06_dong_ho_pomodoro_xoay_raw_v2_1793584153639.jpg",
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
        "sku_code": "PT-MOP-360-0211",
        "slot_dt": "2026-11-02 11:45",
        "raw_file": "phongtro_04_cay_lau_nha_tu_vat_raw.png",
        "out_file": "phongtro_04_cay_lau_nha_tu_vat_bold.jpg",
        "accent_hex": "#FF3D00",
        "accent_dark_hex": "#9A1B00",
        "page_badge": "SẠCH BÓNG SÀN TRỌ",
        "title_line1": "CÂY LAU NHÀ TỰ VẮT",
        "title_highlight": "XOAY 360° ĐỨNG ĐỘC LẬP",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("GẠT VẮT KÉP KHÔ", ""),
            ("LUỒN GẦM GIƯỜNG", ""),
            ("ĐỨNG GỌN GÓC 10CM", ""),
        ],
        "shopee_kw": "cay lau nha tu vat thong minh xoay 360 dung doc lap",
        "sub_id": "phongtro-0211-mop360-pin-img",
        "caption": (
            "Phòng trọ nhỏ mà phải bê thêm cái thùng vắt nước lau nhà to đùng thì choán hết cả nhà vệ sinh, mỗi lần cúi người vắt giẻ bằng tay lại vừa mỏi lưng vừa ướt bẩn!\n\n"
            "Đổi ngay sang chiếc Cây Lau Nhà Tự Vắt Thông Minh Xoay 360° Đứng Độc Lập này là lau xong cả phòng trọ chỉ trong 5 phút:\n"
            "✨ Thanh gạt vắt trợ lực kép: Kéo nhẹ 1 đường là ép sạch 95% nước bẩn và tóc rụng trên bông lau mà tay không hề chạm nước.\n"
            "✨ Đầu lau dẹp siêu mỏng xoay 360°: Luồn thẳng vào gầm giường, gầm tủ lạnh và khe hẹp sát chân tường dễ dàng.\n"
            "✨ Lau xong dựng đứng tự cân bằng ngay góc phòng 10cm, bông sợi Microfiber khô thoáng không gây mùi ẩm.\n\n"
            "💬 Hiện tại ở phòng trọ bạn đang dùng cây lau nhà thùng xoay hay cây lau tự vắt gọn nhẹ? Xem ngay link cây lau nhà kèm 3 miếng bông thay thế giá hời ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-CABLE-BOX-0211",
        "slot_dt": "2026-11-02 20:00",
        "raw_file": "phongtro_05_hop_o_cam_chong_chay_raw.png",
        "out_file": "phongtro_05_hop_o_cam_chong_chay_bold.jpg",
        "accent_hex": "#00A859",
        "accent_dark_hex": "#006633",
        "page_badge": "GỌN DÂY AN TOÀN",
        "title_line1": "HỘP ĐỰNG Ổ CẮM ĐIỆN",
        "title_highlight": "CHỐNG CHÁY NẮP VÂN GỖ",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("NHỰA ABS CHỐNG CHÁY", ""),
            ("KHE Đỡ ĐIỆN THOẠI", ""),
            ("KHE TẢN NHIỆT ĐÁY", ""),
        ],
        "shopee_kw": "hop dung o cam dien giau day chong chay nap van go",
        "sub_id": "phongtro-0211-cablebox-pin-img",
        "caption": (
            "Góc bàn phòng trọ hay đầu giường luôn có một ổ cắm nối dài chằng chịt dây sạc laptop, sạc điện thoại, dây quạt... vừa bám đầy bụi bẩn vừa nguy hiểm mỗi khi vô tình làm đổ cốc nước!\n\n"
            "Đặt toàn bộ ổ điện vào chiếc Hộp Đựng Ổ Cắm Điện Giấu Dây Nhựa ABS Chống Cháy Nắp Vân Gỗ này là góc phòng gọn đẹp chuẩn Hàn Quốc ngay:\n"
            "✨ Thân nhựa ABS dày dặn chịu nhiệt cao, che kín toàn bộ ổ cắm khỏi bụi bẩn và tia nước bắn.\n"
            "✨ Mặt nắp vân gỗ sang trọng tích hợp rãnh luồn cáp sạc để đặt điện thoại, iPad lên trên sạc cực gọn.\n"
            "✨ Đáy hộp thiết kế các khe thoáng đối lưu tản nhiệt, cắm sạc cả ngày vẫn mát rượi.\n\n"
            "💬 Ổ cắm điện ở phòng trọ bạn hiện đang đặt dưới sàn nhà hay để trên mặt bàn? Săn ngay hộp giấu dây cỡ lớn ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-DOOR-SEAL-0311",
        "slot_dt": "2026-11-03 11:45",
        "raw_file": "phongtro_06_ron_dan_chan_cua_raw.png",
        "out_file": "phongtro_06_ron_dan_chan_cua_bold.jpg",
        "accent_hex": "#0066FF",
        "accent_dark_hex": "#003D99",
        "page_badge": "CHẶN GIÁN & BỤI",
        "title_line1": "RON DÁN CHÂN CỬA",
        "title_highlight": "SILICONE 3 LỚP CÁCH ÂM",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("CHẶN GIÁN BÒ VÀO", ""),
            ("KEO 3M SIÊU DÍNH", ""),
            ("GIỮ LẠNH ĐIỀU HÒA", ""),
        ],
        "shopee_kw": "ron dan chan cua silicone 3 lop cach am chan con trung",
        "sub_id": "phongtro-0311-doorseal-pin-img",
        "caption": (
            "Khe hở dưới đáy cửa phòng trọ chính là 'đường cao tốc' để gián, kiến ba khoang, bụi hành lang bò vào phòng ban đêm, lại còn làm thất thoát hơi lạnh điều hòa tốn bộn tiền điện!\n\n"
            "Chỉ mất đúng 2 phút bóc dán cuộn Ron Dán Chân Cửa Silicone 3 Lớp Cách Âm Chắn Côn Trùng này là bịt kín hoàn toàn khe cửa:\n"
            "✨ Cấu trúc 3 khoang rỗng tiêu âm & 3 lưỡi quét sát mặt sàn: Chặn đứng 100% gián, côn trùng, bụi mịn và giảm tiếng bước chân ngoài hành lang.\n"
            "✨ Lớp keo Acrylic 3M bám dính cực chắc trên cả cửa gỗ, cửa nhôm kính và cửa sắt mà khi bóc ra không để lại vết keo.\n"
            "✨ Chất liệu Silicone dẻo dai mở đóng cửa êm ru, không gây xước gạch men.\n\n"
            "💬 Cửa phòng trọ của bạn hiện là cửa gỗ hay cửa sắt/nhôm kính? Lấy ngay cuộn ron 1m giá chỉ vài chục cành tại bình luận đầu tiên nhé! 👇"
        ),
    },

    # ------------------------------------------------------------------
    # 2. KÝ TÚC XÁ CÓ BIẾN (1421270697727753)
    # ------------------------------------------------------------------
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-CLIP-FAN-0211",
        "slot_dt": "2026-11-02 11:45",
        "raw_file": "ktx_04_quat_tich_dien_kep_giuong_raw.png",
        "out_file": "ktx_04_quat_tich_dien_kep_giuong_bold.jpg",
        "accent_hex": "#6D28D9",
        "accent_dark_hex": "#4C1D95",
        "page_badge": "MÁT LẠNH GIƯỜNG TẦNG",
        "title_line1": "QUẠT KẸP GIƯỜNG KTX",
        "title_highlight": "PIN 10000MAH XOAY 720°",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("KẸP CHẶT THÀNH SẮT", ""),
            ("XOAY 720° ĐA HƯỚNG", ""),
            ("MÀN HÌNH LED PIN", ""),
        ],
        "shopee_kw": "quat tich dien kep ban giuong tang ktx 10000mah xoay 720",
        "sub_id": "ktx-0211-clipfan-pin-img",
        "caption": (
            "Nằm giường tầng KTX (nhất là lúc kéo rèm che kín hoặc góc giường khuất quạt trần) hầm hập bí bách không ngủ nổi, mà đặt quạt cây thì không có chỗ để!\n\n"
            "Vật bất ly thân của sinh viên KTX chính là chiếc Quạt Tích Điện Kẹp Thành Giường Pin 10000mAh Xoay 720° này:\n"
            "✨ Ngàm kẹp lò xo bản rộng lót cao su: Kẹp cứng cáp vào thanh sắt đầu giường tầng 1 hay tầng 2 đều không rung lắc.\n"
            "✨ Động cơ không chổi than 5 cánh chạy siêu êm (< 25dB): Gió mát rượi suốt đêm mà hoàn toàn không phát tiếng ồn làm phiền bạn cùng phòng.\n"
            "✨ Màn hình LED báo % pin trực quan, xoay trục kép 720° chỉnh hướng gió chuẩn xác, lồng quạt tháo rời rửa sạch trong 10 giây.\n\n"
            "💬 Giường KTX của bạn nằm ngay dưới quạt trần hay nằm ở góc khuất gió? Xem ngay link quạt kẹp giường pin trâu giá sinh viên ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-VAC-BAG-0211",
        "slot_dt": "2026-11-02 20:00",
        "raw_file": "ktx_05_tui_hut_chan_khong_chan_goi_raw.png",
        "out_file": "ktx_05_tui_hut_chan_khong_chan_goi_bold.jpg",
        "accent_hex": "#0284C7",
        "accent_dark_hex": "#0369A1",
        "page_badge": "RỘNG GẤP 4 TỦ ĐỒ",
        "title_line1": "TÚI HÚT CHÂN KHÔNG",
        "title_highlight": "NÉN MỎNG 80% CHĂN ÁO",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("NÉN MỎNG 80% TỦ", ""),
            ("KÈM BƠM TAY NHANH", ""),
            ("CHỐNG ẨM MỐC KÍN", ""),
        ],
        "shopee_kw": "bo tui hut chan khong dung chan men quan ao kem bom",
        "sub_id": "ktx-0211-vacbag-pin-img",
        "caption": (
            "Tủ cá nhân ở KTX chỉ bé bằng một ngăn nhỏ, mới cất 1 chiếc chăn bông mùa đông với vài chiếc áo khoác phao là đã chật cứng không còn chỗ treo đồ đi học!\n\n"
            "Giải cứu ngay chiếc tủ KTX với Bộ Túi Hút Chân Không Đựng Chăn Mền Quần Áo Kèm Bơm Tay Chuyên Dụng:\n"
            "✨ Nén xẹp 80% thể tích chỉ sau 30 giây hút khí: Chiếc chăn bông dày cộp lập tức mỏng dính như tờ bìa, giúp tủ đồ rộng gấp 4 lần.\n"
            "✨ Màng nhựa PA+PE 5 lớp dẻo dai kết hợp khóa Zip kép đổi màu & van chống trào ngược: Giữ chân không kín khít suốt nhiều tháng, chống ẩm mốc và côn trùng tuyệt đối.\n"
            "✨ Tặng kèm bơm hút cầm tay nhỏ gọn, lúc dọn phòng về nghỉ lễ nhét gọn cả tủ đồ vào đúng 1 chiếc vali.\n\n"
            "💬 Trong tủ đồ KTX của bạn hiện tại thứ gì đang chiếm nhiều diện tích nhất? Săn ngay combo 8 túi đủ size kèm bơm ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-BED-DESK-0311",
        "slot_dt": "2026-11-03 11:45",
        "raw_file": "ktx_06_ban_hoc_gap_gon_khe_ipad_raw.png",
        "out_file": "ktx_06_ban_hoc_gap_gon_khe_ipad_bold.jpg",
        "accent_hex": "#E11D48",
        "accent_dark_hex": "#9F1239",
        "page_badge": "GÓC HỌC TRÊN GIƯỜNG",
        "title_line1": "BÀN HỌC GẤP GỌN KTX",
        "title_highlight": "MẶT GỖ CÓ KHE ĐỠ IPAD",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("KHE DỰNG IPAD/SÁCH", ""),
            ("CHÂN THÉP CHỮ W", ""),
            ("GẬP MỎNG CẤT KHE", ""),
        ],
        "shopee_kw": "ban hoc gap gon tren giuong ktx co khe de ipad",
        "sub_id": "ktx-0311-beddesk-pin-img",
        "caption": (
            "Ngồi trên giường KTX mà đặt laptop trực tiếp lên đùi hay lên chăn gối vừa làm máy nóng ran bít khe tản nhiệt, vừa phải cúi gập cổ mỏi nhừ cả vai gáy!\n\n"
            "Sắm ngay một chiếc Bàn Học Gấp Gọn Trên Giường Mặt Gỗ MDF Chống Thấm Có Khe Đựng iPad & Cốc Nước chuẩn sinh viên:\n"
            "✨ Cạnh bàn uốn cong công thái học ôm sát người ngồi, mặt bàn rộng rãi để vừa cả laptop 15.6 inch, chuột rời và sổ ghi chép.\n"
            "✨ Tích hợp rãnh sâu dựng đứng iPad/điện thoại để vừa xem bài giảng vừa ghi chép, kèm hốc giữ bình nước chống đổ ra nệm.\n"
            "✨ Chân thép chữ W bọc mút chống trượt cực vững, dùng xong gập phẳng dày chỉ 4.5cm nhét gọn vào khe nệm đầu giường.\n\n"
            "💬 Ở KTX bạn thường ngồi học trên giường hay xuống bàn sinh hoạt chung nhiều hơn? Xem ngay link bàn gấp gỗ dày giá sinh viên tại bình luận đầu tiên nha! 👇"
        ),
    },

    # ------------------------------------------------------------------
    # 3. HỘI DEADLINE (1407231352464711)
    # ------------------------------------------------------------------
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-LAPTOP-STAND-0211",
        "slot_dt": "2026-11-02 11:45",
        "raw_file": "deadline_04_gia_do_laptop_nhom_cnc_raw.png",
        "out_file": "deadline_04_gia_do_laptop_nhom_cnc_bold.jpg",
        "accent_hex": "#FF6B00",
        "accent_dark_hex": "#B45309",
        "page_badge": "CHỐNG GÙ CỔ VAI GÁY",
        "title_line1": "GIÁ ĐỠ LAPTOP NHÔM",
        "title_highlight": "CNC 7 NẤC TẢN NHIỆT",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("CHỈNH 7 NẤC ĐỘ CAO", ""),
            ("THOÁNG KHÍ MÁT MÁY", ""),
            ("GẬP GỌN BỎ TÚI", ""),
        ],
        "shopee_kw": "gia do laptop hop kim nhom cnc chinh 7 nac tan nhiet",
        "sub_id": "deadline-0211-laptopstand-pin-img",
        "caption": (
            "Đặt laptop thẳng trên mặt bàn văn phòng khiến bạn luôn phải cúi đầu 45° suốt 8 tiếng: Chiều về đốt sống cổ căng cứng, vai gáy mỏi nhừ còn đáy laptop thì nóng hầm hập làm máy giật lag!\n\n"
            "Nâng tầm mắt chuẩn công thái học ngay với Giá Đỡ Laptop Hợp Kim Nhôm CNC Nguyên Khối Chỉnh 7 Nấc:\n"
            "✨ Nâng màn hình laptop lên ngang tầm mắt với 7 nấc chỉnh góc nghiêng linh hoạt, giúp cột sống cổ và lưng tự động giữ thẳng.\n"
            "✨ Khung hợp kim nhôm Anodized cắt vát kim cương chịu lực tới 20kg, đệm cao su dày chống trượt và chống trầy xước máy tuyệt đối.\n"
            "✨ Thiết kế rỗng đáy hoàn toàn giúp luồng gió lưu thông 360° hạ nhiệt CPU nhanh chóng; gập lại nhỏ gọn như thanh thước bỏ vừa túi chống sốc.\n\n"
            "💬 Hiện tại laptop của bạn đang đặt thẳng trên mặt bàn hay đã có giá đỡ nâng cao? Săn ngay giá đỡ nhôm CNC kèm túi nhung ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-LUMBAR-PAD-0211",
        "slot_dt": "2026-11-02 20:00",
        "raw_file": "deadline_05_goi_tua_lung_cao_su_non_raw.png",
        "out_file": "deadline_05_goi_tua_lung_cao_su_non_bold.jpg",
        "accent_hex": "#0066FF",
        "accent_dark_hex": "#1E3A8A",
        "page_badge": "ÊM LƯNG 8 TIẾNG",
        "title_line1": "GỐI TỰA LƯNG GHẾ",
        "title_highlight": "CAO SU NON ÔM CỘT SỐNG",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("ĐỠ CONG THẮT LƯNG", ""),
            ("CAO SU NON ĐÀN HỒI", ""),
            ("VẢI LƯỚI 3D THOÁNG", ""),
        ],
        "shopee_kw": "goi tua lung ghe van phong cao su non memory foam cong thai hoc",
        "sub_id": "deadline-0211-lumbarpad-pin-img",
        "caption": (
            "Ghế xoay văn phòng thông thường luôn để lại một khoảng trống hẫng ngay vùng thắt lưng: Càng ngồi chạy deadline về chiều lưng càng trượt dài cong chữ C, đứng dậy là ê ẩm cả vùng eo!\n\n"
            "Lấp đầy khoảng trống cột sống ngay lập tức với Gối Tựa Lưng Ghế Văn Phòng Cao Su Non Memory Foam Công Thái Học:\n"
            "✨ Thiết kế 2 cánh ôm sát kết hợp đường cong chữ S nâng đỡ trọn vẹn 5 đốt sống thắt lưng, giảm tới 70% áp lực dồn xuống hông khi ngồi lâu.\n"
            "✨ Ruột gối 100% Cao su non Memory Foam đàn hồi chậm: Ôm khít theo dáng lưng từng người và không bao giờ bị xẹp lún sau thời gian dài sử dụng.\n"
            "✨ Vỏ áo gối bằng vải lưới tổ ong 3D thoáng khí có khóa kéo tháo giặt dễ dàng, kèm 2 dây đai khóa cài cố định chắc chắn vào mọi loại ghế.\n\n"
            "💬 Ngồi ghế văn phòng hiện tại bạn hay bị đau mỏi vùng thắt lưng dưới hay vùng bả vai trên? Xem ngay gối tựa lưng Memory Foam chính hãng ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-POMODORO-HEX-0311",
        "slot_dt": "2026-11-03 11:45",
        "raw_file": "deadline_06_dong_ho_pomodoro_xoay_raw.png",
        "out_file": "deadline_06_dong_ho_pomodoro_xoay_bold.jpg",
        "accent_hex": "#E11D48",
        "accent_dark_hex": "#881337",
        "page_badge": "X3 ĐỘ TẬP TRUNG",
        "title_line1": "ĐỒNG HỒ POMODORO",
        "title_highlight": "CẢM BIẾN XOAY LỤC GIÁC",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("LẬT MẶT ĐẾM NGAY", ""),
            ("BÁO RUNG KHÔNG ỒN", ""),
            ("SẠC TYPE-C BỀN BỈ", ""),
        ],
        "shopee_kw": "dong ho bam gio pomodoro cam bien xoay luc giac",
        "sub_id": "deadline-0311-pomodorohex-pin-img",
        "caption": (
            "Định cầm điện thoại lên bật hẹn giờ Pomodoro 25 phút để tập trung làm việc, nhưng vừa mở màn hình lại thấy thông báo tin nhắn thế là cuốn vào lướt mạng mất đứt nửa tiếng!\n\n"
            "Tách biệt hoàn toàn khỏi sự xao nhãng của điện thoại với chiếc Đồng Hồ Pomodoro Cảm Biến Trọng Lực Xoay Lục Giác đặt ngay trên bàn làm việc:\n"
            "✨ Tích hợp cảm biến trọng lực thông minh: Chỉ cần lật mặt số 5 – 15 – 25 – 30 – 45 – 60 phút lên trên là đồng hồ tự động đếm ngược tức thì không cần bấm nút.\n"
            "✨ Chế độ Báo Rung / Nháy Đèn yên tĩnh: Nhắc nhở hết phiên làm việc chuẩn xác mà không phát ra tiếng chuông làm ảnh hưởng đồng nghiệp xung quanh.\n"
            "✨ Màn hình LED sắc nét trên nền đen nhám sang trọng, sạc pin qua cổng USB Type-C dùng bền bỉ hàng tháng trời.\n\n"
            "💬 Mỗi phiên tập trung sâu (Deep Work) của bạn thường kéo dài 25 phút hay 45–60 phút? Săn ngay đồng hồ Pomodoro lục giác ở bình luận đầu tiên nhé! 👇"
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
