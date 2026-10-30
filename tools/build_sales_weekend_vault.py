#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sales_weekend_vault.py — Kết xuất & Lên lịch 9 Bài Ảnh Vuông 1:1 (Editorial Macro & 3-Detail Grid + Bold Typography)
Cho 3 Page Bán Hàng Affiliate (Phòng Trọ Hết Cứu, Ký Túc Xá Có Biến, Hội Deadline)
Khung giờ: 30/10 20:00, 31/10 11:45, 31/10 20:00.
"""

import argparse
import datetime as dt
import json
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
VAULT_DIR = SUBAGENT_DIR / "campaigns" / "2026-10-30" / "sales-weekend-vault"
RAW_DIR = VAULT_DIR / "raw"
FINAL_DIR = VAULT_DIR / "images"
QA_GRID_PATH = VAULT_DIR / "sales_weekend_9_qa_grid.jpg"
MANIFEST_PATH = VAULT_DIR / "manifest.json"


def build_shopee_link(keyword: str, sub_id: str) -> str:
    origin = f"https://shopee.vn/search?keyword={urllib.parse.quote(keyword)}"
    return f"https://s.shopee.vn/an_redir?origin_link={urllib.parse.quote(origin, safe='')}&affiliate_id={AFF_ID}&sub_id={sub_id}"


SALES_ITEMS_SPEC = [
    # ------------------------------------------------------------------
    # 1. PHÒNG TRỌ HẾT CỨU (1442323328956326) — Accent Cam Đỏ #EA580C
    # ------------------------------------------------------------------
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-DRYER-UV-3010",
        "slot_dt": "2026-10-30 20:00",
        "raw_file": "phongtro_01_may_say_quan_ao_raw.png",
        "out_file": "phongtro_01_may_say_quan_ao_bold.jpg",
        "accent_hex": "#FF3D00",
        "accent_dark_hex": "#9A1B00",
        "page_badge": "CỨU CÁNH MÙA MƯA",
        "title_line1": "MÁY SẤY QUẦN ÁO",
        "title_highlight": "GẤP GỌN KHỬ KHUẨN UV",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("SƯỞI GỐM PTC", ""),
            ("ĐÈN UV KHỬ MÙI", ""),
            ("GẤP GỌN BỎ TỦ", ""),
        ],
        "shopee_kw": "may say quan ao mini gap gon khu khuan uv",
        "sub_id": "phongtro-3010-dryeruv-pin-img",
        "caption": (
            "Phòng trọ không có ban công hoặc nằm tầng thấp thiếu nắng: Mỗi lần mưa dầm 2–3 ngày là quần áo phơi trong phòng ẩm sì, bốc mùi hôi ngai ngái mặc vào cực kỳ ngứa ngáy!\n\n"
            "Sắm ngay 1 em Máy Sấy Quần Áo Mini Gấp Gọn Khử Khuẩn UV này treo ngay góc phòng trọ là quần áo khô cong thơm tho bất chấp thời tiết:\n"
            "✨ Thanh nhiệt gốm PTC tỏa hơi ấm đối lưu 360°: Sấy khô nhanh áo sơ mi, đồ lót, tất vớ chỉ từ 30–60 phút mà không làm co rút sợi vải.\n"
            "✨ Tích hợp đèn tia UV khử khuẩn: Loại bỏ hoàn toàn mùi ẩm mốc đặc trưng của phòng trọ kín gió.\n"
            "✨ Dùng xong gập phẳng lại nhỏ gọn đúng bằng cuốn sổ dày, cất gọn vào ngăn kéo không tốn diện tích.\n\n"
            "💬 Phòng trọ của bạn hiện đang phơi đồ ngoài hành lang chung hay phơi luôn trong phòng? Bình luận chia sẻ bên dưới nhé, chỗ mua máy sấy gấp gọn chính hãng mình ghim ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-FAUCET-720-3110",
        "slot_dt": "2026-10-31 11:45",
        "raw_file": "phongtro_02_voi_tang_ap_loc_nuoc_raw.png",
        "out_file": "phongtro_02_voi_tang_ap_loc_nuoc_bold.jpg",
        "accent_hex": "#0066FF",
        "accent_dark_hex": "#003D99",
        "page_badge": "NƯỚC MẠNH GẤP 3",
        "title_line1": "ĐẦU VÒI TĂNG ÁP",
        "title_highlight": "XOAY 720° LỌC CẶN",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("KHỚP XOAY 720°", ""),
            ("LÕI LỌC CẶN BẨN", ""),
            ("TĂNG ÁP X3 LẦN", ""),
        ],
        "shopee_kw": "dau voi nuoc tang ap xoay 720 co loi loc pp",
        "sub_id": "phongtro-3110-faucet720-pin-img",
        "caption": (
            "Ở phòng trọ tầng cao nước chảy yếu xìu như mèo đái, đã thế đường ống cũ lâu năm lại hay lẫn cặn vàng gỉ sét dùng đánh răng rửa mặt mỗi sáng cực kỳ xót da!\n\n"
            "Chỉ cần vặn thêm Đầu Vòi Nước Tăng Áp Xoay 720° Kèm Lõi Lọc Cặn PP này vào vòi bồn rửa mặt / bồn rửa bát là thấy ngay sự khác biệt:\n"
            "✨ Mặt phun Inox đục lỗ vi điểm Laser: Gom áp lực nước bắn ra mạnh gấp 3 lần nhưng tia nước cực mịn không bị bắn tung tóe ướt áo.\n"
            "✨ Lõi bông PP mật độ cao nằm trong khoang trong suốt: Chỉ sau 1 tuần nhìn vào thấy lõi chuyển màu vàng nâu là biết nó đã chặn lại bao nhiêu cặn bẩn giúp bạn.\n"
            "✨ Khớp cầu kép xoay 720°: Ngửa vòi lên trên để súc miệng, rửa mặt trực tiếp hoặc xoay tráng sạch mọi góc bồn rửa.\n\n"
            "💬 Nước ở khu trọ bạn đang ở chảy mạnh hay yếu? Xem ngay link đầu vòi lọc cặn kèm 5 lõi thay thế giá siêu rẻ ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1442323328956326",
        "page_name": "Phòng Trọ Hết Cứu",
        "sku_code": "PT-SHOERACK-Z5-3110",
        "slot_dt": "2026-10-31 20:00",
        "raw_file": "phongtro_03_ke_giay_5_tang_raw.png",
        "out_file": "phongtro_03_ke_giay_5_tang_bold.jpg",
        "accent_hex": "#00A859",
        "accent_dark_hex": "#006633",
        "page_badge": "GỌN GÓC CỬA PHÒNG",
        "title_line1": "KỆ GIÀY 5 TẦNG",
        "title_highlight": "KHUNG CHỮ Z SIÊU BỀN",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("KHUNG CHỮ Z CHẮC", ""),
            ("VẢI CHỐNG THẤM", ""),
            ("ĐỰNG 15 ĐÔI GIÀY", ""),
        ],
        "shopee_kw": "ke de giay dep 5 tang chu z khung thep",
        "sub_id": "phongtro-3110-shoerackz-pin-img",
        "caption": (
            "Bước vào cửa phòng trọ mà giày thể thao, dép đi trong nhà, giày đi làm xếp tràn lan hết cả lối đi thì nhìn căn phòng chật chội đi một nửa!\n\n"
            "Chỉ tốn đúng 1 góc hẹp 25cm ngay sau cánh cửa với chiếc Kệ Để Giày 5 Tầng Khung Thép Chữ Z này là gom gọn gàng cả chục đôi giày:\n"
            "✨ Kết cấu khung chữ Z đối xứng chịu lực cực khỏe: Chất đầy giày thể thao, bốt cổ cao từ tầng 1 đến tầng 5 vẫn đứng vững chãi không rung lắc.\n"
            "✨ Mặt tầng bằng vải không dệt phủ màng chống thấm: Đi mưa về đặt giày ướt lên không bị rỏ nước bẩn xuống đôi giày ở tầng dưới.\n"
            "✨ Tháo lắp trong 5 phút không cần tua-vít, lúc chuyển trọ tháo ra bỏ gọn vào túi cực tiện.\n\n"
            "💬 Hiện tại góc cửa phòng trọ của bạn có khoảng mấy đôi giày dép? Săn ngay kệ giày chữ Z giá hạt dẻ ở bình luận đầu tiên nha! 👇"
        ),
    },

    # ------------------------------------------------------------------
    # 2. KÝ TÚC XÁ CÓ BIẾN (1421270697727753)
    # ------------------------------------------------------------------
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-LAMP-CLIP-3010",
        "slot_dt": "2026-10-30 20:00",
        "raw_file": "ktx_01_den_hoc_kep_giuong_raw.png",
        "out_file": "ktx_01_den_hoc_kep_giuong_bold.jpg",
        "accent_hex": "#FF6B00",
        "accent_dark_hex": "#9A3412",
        "page_badge": "CÀY ĐÊM KHÔNG CHÓI",
        "title_line1": "ĐÈN HỌC CHỐNG CẬN",
        "title_highlight": "KẸP GIƯỜNG TẦNG KTX",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("KẸP CHẮC GIƯỜNG", ""),
            ("XOAY GẬP 360°", ""),
            ("PIN SẠC TYPE-C", ""),
        ],
        "shopee_kw": "den hoc led chong can kep ban giuong tang tich dien",
        "sub_id": "ktx-3010-lampclip-pin-img",
        "caption": (
            "Đêm ở KTX đúng 23h là cả phòng tắt đèn đi ngủ, muốn thức thêm 1–2 tiếng ôn bài chạy tiểu luận mà bật đèn trần thì ngại ảnh hưởng giấc ngủ của 7 đứa bạn cùng phòng!\n\n"
            "Giải pháp chuẩn nhất cho sinh viên giường tầng chính là em Đèn Học LED Chống Cận Kẹp Thành Giường Tích Điện này:\n"
            "✨ Ngàm kẹp lò xo lót đệm mút dày: Kẹp chặt vào thanh sắt đầu giường tầng 1 hay tầng 2 đều êm ru, không tốn 1cm mặt bàn.\n"
            "✨ Cổ ngỗng Silicon uốn cong 360° gom vùng sáng chiếu đúng vào trang vở và bàn phím laptop, hoàn toàn không hắt sáng sang giường bên cạnh.\n"
            "✨ Chạm cảm ứng đổi 3 màu ánh sáng (Trắng - Vàng - Trung tính) + Nhấn giữ tăng giảm độ sáng mượt mà, pin sạc Type-C dùng liên tục nhiều giờ.\n\n"
            "💬 Team KTX đang nằm giường tầng 1 hay tầng 2 điểm danh nào! Lấy ngay link đèn kẹp giường giá sinh viên ở bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-CURTAIN-BED-3110",
        "slot_dt": "2026-10-31 11:45",
        "raw_file": "ktx_02_rem_che_giuong_ktx_raw.png",
        "out_file": "ktx_02_rem_che_giuong_ktx_bold.jpg",
        "accent_hex": "#6D28D9",
        "accent_dark_hex": "#3B0764",
        "page_badge": "GÓC RIÊNG TƯ KTX",
        "title_line1": "RÈM CHE GIƯỜNG TẦNG",
        "title_highlight": "CẢN SÁNG 90% KÈM KHUNG",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("MÓC TRƯỢT ÊM", ""),
            ("VẢI DÀY 3 LỚP", ""),
            ("KÈM TÚI ĐỰNG ĐỒ", ""),
        ],
        "shopee_kw": "rem che giuong tang ktx can sang kem khung day treo",
        "sub_id": "ktx-3110-curtainbed-pin-img",
        "caption": (
            "Ở phòng KTX đông người bất tiện nhất là lúc muốn thay quần áo, gọi video về cho gia đình hoặc muốn ngủ sớm trong khi cả phòng vẫn đang bật đèn sáng trưng!\n\n"
            "Lắp ngay bộ Rèm Che Giường Tầng KTX Vải Polyester Cản Sáng 90% này là biến chiếc giường đơn thành căn phòng nhỏ riêng tư của riêng bạn:\n"
            "✨ Vải Polyester dệt 3 lớp dày dặn: Chắn tới 90% ánh đèn tuýp trần nhà và gió lùa trực tiếp từ quạt trần, giúp ngủ sâu giấc hơn hẳn.\n"
            "✨ Tặng kèm đầy đủ dây cáp/khung và móc treo hợp kim: Chỉ mất 5 phút tự buộc lên 4 góc giường KTX không cần khoan đục.\n"
            "✨ Không gian bên trong kín đáo, thẩm mỹ, tha hồ decor thêm dây đèn vàng ấm áp.\n\n"
            "💬 Bạn thích lắp rèm che 1 mặt trước hay che kín cả 3 mặt giường? Xem ngay bảng màu tối giản chuẩn KTX ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1421270697727753",
        "page_name": "Ký Túc Xá Có Biến",
        "sku_code": "KTX-CADDY-HANG-3110",
        "slot_dt": "2026-10-31 20:00",
        "raw_file": "ktx_03_gio_treo_dau_giuong_raw.png",
        "out_file": "ktx_03_gio_treo_dau_giuong_bold.jpg",
        "accent_hex": "#E11D48",
        "accent_dark_hex": "#881337",
        "page_badge": "TIỆN ÍCH GIƯỜNG TẦNG",
        "title_line1": "GIỎ TREO ĐẦU GIƯỜNG",
        "title_highlight": "THÉP CARBON CHỊU LỰC",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("MÓC ĐỆM CAO SU", ""),
            ("TREO TAI NGHE", ""),
            ("CHỊU TẢI 10KG", ""),
        ],
        "shopee_kw": "gio treo dau giuong tang ktx thep son tinh dien",
        "sub_id": "ktx-3110-caddyhang-pin-img",
        "caption": (
            "Nằm trên giường tầng 2 KTX ngại nhất là mỗi lần muốn cất laptop, lấy chai nước, hộp khăn giấy hay sạc dự phòng lại phải lọ mọ trèo thang lên xuống chục bận!\n\n"
            "Chỉ cần ngoắc chiếc Giỏ Treo Đầu Giường Tầng KTX Thép Carbon Sơn Tĩnh Điện này vào thanh chắn giường là mọi thứ đều nằm gọn ngay trong tầm với:\n"
            "✨ Khung thép Carbon hàn điểm chắc nịch: Đựng cùng lúc chiếc laptop 15.6 inch, 5 cuốn giáo trình dày và bình nước 1 lít vẫn không hề cong vênh.\n"
            "✨ Hai ngàm móc chữ U có bọc lớp cao su êm ái: Bám chặt vào thành giường sắt, lấy đồ không phát ra tiếng kêu lọc cọc ban đêm.\n"
            "✨ Tặng kèm hàng móc phụ bên hông để treo tai nghe chụp tai, chìa khóa tủ và túi vải nhỏ.\n\n"
            "💬 Trên giường KTX của bạn hiện đang để nhiều sách vở hay đồ ăn vặt hơn? Săn ngay giỏ treo thép dày giá sinh viên tại bình luận đầu tiên nhé! 👇"
        ),
    },

    # ------------------------------------------------------------------
    # 3. HỘI DEADLINE (1407231352464711)
    # ------------------------------------------------------------------
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-FOOT-REST-3010",
        "slot_dt": "2026-10-30 20:00",
        "raw_file": "deadline_01_ke_chan_cong_thai_hoc_raw.png",
        "out_file": "deadline_01_ke_chan_cong_thai_hoc_bold.jpg",
        "accent_hex": "#E11D48",
        "accent_dark_hex": "#881337",
        "page_badge": "CHỐNG MỎI LƯNG & CHÂN",
        "title_line1": "GHẾ KÊ CHÂN GẦM BÀN",
        "title_highlight": "CHỈNH 6 NẤC MASSAGE",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("CON LĂN MASSAGE", ""),
            ("CHỈNH 6 ĐỘ CAO", ""),
            ("ĐẾ CHỐNG TRƯỢT", ""),
        ],
        "shopee_kw": "ke chan cong thai hoc van phong massage 6 nac",
        "sub_id": "deadline-3010-footrest-pin-img",
        "caption": (
            "Dân văn phòng ngồi ghế cao suốt 8 tiếng mỗi ngày: Hai bàn chân bị lơ lửng hoặc phải co quắp dưới gầm ghế khiến máu huyết vùng bắp chân kém lưu thông, chiều về vừa tê chân vừa đau mỏi thắt lưng!\n\n"
            "Đặt ngay một chiếc Ghế Kê Chân Công Thái Học Chỉnh 6 Nấc Kèm Con Lăn Massage dưới gầm bàn làm việc là tư thế ngồi chuẩn chỉnh tức thì:\n"
            "✨ Nâng cao bàn chân giúp đùi và lưng tạo thành góc vuông 90° chuẩn công thái học, ép lưng tự động tựa sát vào thành ghế xoay.\n"
            "✨ Bề mặt hạt gai kết hợp trục con lăn ở giữa: Vừa gõ báo cáo vừa tháo giày lăn nhẹ lòng bàn chân cực kỳ thư giãn và tỉnh táo.\n"
            "✨ Khung nhựa ABS dày dặn chỉnh được 6 mức độ cao & góc nghiêng, chân đế bọc đệm cao su bám chặt sàn gạch văn phòng.\n\n"
            "💬 Ngồi làm việc lâu bạn hay bị mỏi thắt lưng trước hay tê mỏi bắp chân trước? Xem ngay chỗ mua kê chân công thái học tại bình luận đầu tiên nhé! 👇"
        ),
    },
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-SCREEN-BAR-3110",
        "slot_dt": "2026-10-31 11:45",
        "raw_file": "deadline_02_den_treo_man_hinh_raw.png",
        "out_file": "deadline_02_den_treo_man_hinh_bold.jpg",
        "accent_hex": "#0284C7",
        "accent_dark_hex": "#075985",
        "page_badge": "BẢO VỆ MẮT BAN ĐÊM",
        "title_line1": "ĐÈN TREO MÀN HÌNH",
        "title_highlight": "SCREENBAR CHỐNG CHÓI",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("GÁC NHẸ 1 GIÂY", ""),
            ("CẢM ỨNG 3 MÀU", ""),
            ("NGUỒN USB TYPE-C", ""),
        ],
        "shopee_kw": "den treo man hinh may tinh screenbar chong choi",
        "sub_id": "deadline-3110-screenbar-pin-img",
        "caption": (
            "Cày deadline ban đêm với chiếc đèn bàn thông thường: Ánh đèn chiếu thẳng vào mặt gương màn hình tạo ra vệt lóa trắng xóa, nhìn chỉ 1 tiếng là nhức mỏi và khô rát hai mắt!\n\n"
            "Nâng cấp góc làm việc lên chuẩn chuyên nghiệp với Thanh Đèn Treo Màn Hình ScreenBar Quang Học Bất Đối Xứng:\n"
            "✨ Thiết kế đường truyền sáng bất đối xứng 45°: Chỉ chiếu sáng rực rỡ khu vực bàn phím và sổ tay trên mặt bàn, hoàn toàn không hắt một tia sáng nào lên màn hình máy tính.\n"
            "✨ Ngàm đối trọng thông minh gác nhẹ lên cạnh trên màn hình trong 1 giây, giải phóng 100% diện tích mặt bàn.\n"
            "✨ Thân đèn hợp kim nhôm đen nhám sang trọng, chạm cảm ứng đổi 3 mức nhiệt độ màu (2900K – 4000K – 6000K) bảo vệ thị lực tối đa.\n\n"
            "💬 Ban đêm ngồi làm việc bạn thường thích bật ánh sáng Vàng ấm hay Trắng dịu? Săn ngay đèn ScreenBar chính hãng ở bình luận đầu tiên nha! 👇"
        ),
    },
    {
        "page_id": "1407231352464711",
        "page_name": "Hội Deadline",
        "sku_code": "DL-WRIST-PAD-3110",
        "slot_dt": "2026-10-31 20:00",
        "raw_file": "deadline_03_dem_ke_tay_memory_foam_raw.png",
        "out_file": "deadline_03_dem_ke_tay_memory_foam_bold.jpg",
        "accent_hex": "#FF4500",
        "accent_dark_hex": "#9A1B00",
        "page_badge": "ÊM CỔ TAY SUỐT 8 GIỜ",
        "title_line1": "BỘ ĐỆM KÊ CỔ TAY",
        "title_highlight": "CAO SU NON MEMORY FOAM",
        "spec_pills": [],
        "macro_points": [],
        "detail_items": [
            ("CAO SU NON ĐẶC", ""),
            ("NÂNG ĐỠ CỔ TAY", ""),
            ("ĐẾ PU BÁM BÀN", ""),
        ],
        "shopee_kw": "bo dem ke tay ban phim va chuot cao su non memory foam",
        "sub_id": "deadline-3110-wristpad-pin-img",
        "caption": (
            "Gõ bàn phím cơ và di chuột liên tục cả ngày: Cạnh bàn cứng tỳ trực tiếp vào xương cổ tay làm vùng da cổ tay đỏ ửng, lâu ngày dễ dẫn đến hội chứng ống cổ tay cực kỳ khó chịu!\n\n"
            "Trang bị ngay Bộ Đệm Kê Tay Bàn Phím & Lót Chuột Cao Su Non Memory Foam này để bảo vệ đôi tay chạy deadline mỗi ngày:\n"
            "✨ Lõi 100% Cao su non Memory Foam tỷ trọng cao: Êm ái nâng cổ tay lên đúng độ cao ngang với mặt bàn phím, giúp cổ tay luôn duỗi thẳng tự nhiên.\n"
            "✨ Bề mặt bọc vải Lycra lụa thoáng khí: Mát mịn, di cổ tay mượt mà không bị rít hay bí mồ hôi vào mùa nóng.\n"
            "✨ Mặt đáy phủ lớp PU chống trượt bám chặt vào mặt bàn như giác hút, gõ phím nhanh đến mấy đệm vẫn nằm im cố định.\n\n"
            "💬 Hiện tại bạn đang dùng bàn phím cơ cao hay bàn phím văn phòng mỏng? Xem ngay combo đệm kê tay Phím + Chuột giá ưu đãi ở bình luận đầu tiên nhé! 👇"
        ),
    },
]


def build_qa_grid_9(image_paths: list[Path], out_grid: Path) -> None:
    cols, rows = 3, 3
    cell = 420
    canvas = Image.new("RGB", (cols * cell, rows * cell), (18, 22, 30))
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
    now_ts = int(time.time())

    # Tự động xóa bản hẹn giờ cũ (nếu có) trước khi đẩy bản thiết kế mới lên
    legacy_cluttered_posts = [
        ("1442323328956326", "122108772873514839"),
        ("1442323328956326", "122108773083514839"),
        ("1442323328956326", "122108773251514839"),
        ("1421270697727753", "122112234267511096"),
        ("1421270697727753", "122112234429511096"),
        ("1421270697727753", "122112234669511096"),
        ("1407231352464711", "122115488817502096"),
        ("1407231352464711", "122115488913502096"),
        ("1407231352464711", "122115489033502096"),
    ]
    if MANIFEST_PATH.exists():
        try:
            old_items = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            for old_it in old_items:
                if old_it.get("page_id") and old_it.get("post_id"):
                    legacy_cluttered_posts.append((old_it["page_id"], old_it["post_id"]))
        except Exception:
            pass

    seen_del = set()
    for old_pid, old_post_id in legacy_cluttered_posts:
        if old_post_id in seen_del or old_pid not in pages:
            continue
        seen_del.add(old_post_id)
        try:
            tok = pages[old_pid]["access_token"]
            del_r = requests.delete(
                f"https://graph.facebook.com/v22.0/{old_post_id}",
                params={"access_token": tok},
                timeout=30,
            )
            print(f"🗑️ Đã xóa bài rối chữ cũ {old_post_id}: {del_r.json()}", flush=True)
        except Exception as e:
            print(f"⚠️ Bỏ qua xóa {old_post_id}: {e}", flush=True)

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

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    rendered_paths = []
    manifest_items = []

    for idx, spec in enumerate(SALES_ITEMS_SPEC, 1):
        raw_p = RAW_DIR / spec["raw_file"]
        if not raw_p.exists():
            raise FileNotFoundError(f"Chưa có ảnh raw: {raw_p}")
        out_jpg = FINAL_DIR / spec["out_file"]
        uri, bg_col = clean_photo_zones_to_data_uri(raw_p)
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
        print(f"  ✔ [{idx:02d}/09] Đã kết xuất ảnh Bold Typography: {out_jpg.name}", flush=True)

    build_qa_grid_9(rendered_paths, QA_GRID_PATH)
    print(f"🖼️ Đã tạo bảng QA Grid 9 ảnh bán hàng tại: {QA_GRID_PATH}", flush=True)

    if args.publish:
        manifest_items = publish_and_schedule_sales_9(manifest_items)

    MANIFEST_PATH.write_text(json.dumps(manifest_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 Đã lưu Manifest tại: {MANIFEST_PATH}", flush=True)


if __name__ == "__main__":
    main()
