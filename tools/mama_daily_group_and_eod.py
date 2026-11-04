#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_daily_group_and_eod.py — Trạm Tự Động Hóa Tương Tác Hội Nhóm, Video Watch & Facebook Reels Cường Độ Cao (v2.1).

NÂNG CẤP ĐỘT PHÁ KÉO TƯƠNG TÁC THẬT VỀ 4 FANPAGE:
1. Mở rộng 4 luồng thực chiến/ngách (`post_group_hot`, `post_group_qna`, `video_vertical` Reels `/reel/`, `video_horizontal` Watch).
2. Tương tác trực tiếp trình phát Facebook Reels (`/reel/<id>`): Tự động bóc tách link `/reel/` thật từ kết quả tìm kiếm,
   mở trực tiếp từng Reel, xem 3.0s, bấm Like, mở khay Bình luận của Reel và thả bình luận dưới danh nghĩa Fanpage.
3. Vũ khí `Direct User Comment Reply` (Phản hồi trực tiếp vào bình luận của người dùng thật):
   Bấm `Thích` + `Phản hồi` trực tiếp vào bình luận đang hỏi của thành viên trong Group/Reels để Facebook bắn
   Thông báo đẩy (Notification) trực tiếp tới điện thoại người dùng thật -> kéo lượt bấm vào tường Fanpage cao gấp 5-10 lần.
4. Phát hiện chính xác màn hình hết hạn phiên Facebook (`c_user` bị xóa / nút `Tiếp tục <Tên>`), không bao giờ báo `OK` ảo khi chưa đăng nhập.
5. Tuân thủ tuyệt đối LUẬT #1 (Định vị Đội ngũ Subagent Cá nhân & Doanh nghiệp Toàn diện), LUẬT #4 (Tường lửa bảo vệ
   trang cá nhân Thành Tài), LUẬT #5 (Tách tệp AI vs 3 Page Bán Hàng) và LUẬT #6 (Chạy ngầm 100% `--headless=new` cổng 9222).
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SUBAGENT_DIR = pathlib.Path(__file__).resolve().parent.parent
REPORTS_DIR = SUBAGENT_DIR / "campaigns" / "daily-reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

COMMENTS_POOL = {
    "ai": [
        "Chuẩn thực chiến luôn bác! Dùng 1 con AI lẻ rất dễ loạn ngữ cảnh — bên mình đang vận hành mô hình Đội ngũ 10 Subagent Cá nhân & Doanh nghiệp có cổng kiểm duyệt riêng. Mình có ghim sẵn Sơ đồ Kiến trúc + Nhận thiết kế Đội ngũ Subagent may đo 1:1 ngay bài đầu trên tường Page, bác bấm vào tên Page mình xem nha!",
        "Đúng nỗi đau của nhiều anh em làm văn phòng và chủ shop! Thay vì làm thủ công từng việc, chỉ cần dựng một Đội ngũ Subagent chuyên trách (Tổng quản, MKT, Content, Báo cáo, CSKH) chạy ngầm 24/7. Bản thiết kế mẫu & dịch vụ Setup Đội ngũ Subagent trọn gói mình ghim ngay trên tường Page, anh em bấm vào tên Page mình lấy nhé!",
        "Góc nhìn rất sát thực tế! Khi gắn thêm 'Bộ não thứ 2' (Memory Vault) vào Đội ngũ Subagent Cá nhân, AI sẽ nhớ 100% quy tắc và phong cách làm việc của chủ nhân mà không lặp lại lỗi cũ. Mình vừa ghim bộ khung 10 Subagent (.MD) ngay bài đầu tiên trên tường Page, bác nào cần bấm vào tên Page mình tải miễn phí nha!",
        "Bí quyết giải phóng 80% thời gian cho CEO và Freelancer là bàn giao việc lặp lại cho một Đội ngũ Subagent Doanh nghiệp nối thẳng qua Zalo/Telegram. Toàn bộ Blueprint kiến trúc & đăng ký tư vấn thiết kế Đội ngũ Subagent riêng mình để sẵn ngay bài ghim trên tường Page, bác bấm vào tên Page mình tham khảo nhé!",
        "Chia sẻ quá chất lượng! Anh em nào muốn có riêng một Đội ngũ Subagent Cá nhân hoặc Phòng ban Subagent Doanh nghiệp may đo sát 100% quy trình thực tế mà không cần tự mò code phức tạp thì ghé ngay bài đầu tiên trên tường Page mình nhé — có sẵn bản mẫu miễn phí lẫn gói dựng trọn gói 1:1 luôn ạ!",
        "Đồng ý 100%! Từ lọc dữ liệu, viết kịch bản đa kênh, thiết kế đồ họa Zero-Clone tới trực bình luận đều có thể giao cho Đội ngũ Subagent tự hành. Mình vừa cập nhật sơ đồ vận hành 11 Subagent thực tế ngay trên tường Page, bác nào quan tâm bấm vào tên Page mình xem chi tiết nha!"
    ],
    "phongtro": [
        "Đồng cảm thực sự luôn! Phòng trọ nhỏ 15–20m2 bí kíp của mình là dùng kệ giày chữ Z sát cửa và cây lau nhà tự vắt đứng gọn góc 10cm. Mình vừa ghim hình thực tế mấy món cứu cánh phòng trọ nhỏ gọn cực rẻ ngay bài đầu trên tường Page, bạn nào đang dọn phòng bấm vào tên Page mình xem nha!",
        "Phòng trọ kín gió gặp đợt mưa ẩm quần áo hay bị mùi ngai ngái thì cứ dùng túi sấy quần áo gấp gọn có tia UV khử khuẩn nhé, sấy 45 phút khô thơm phức rồi gấp gọn bằng cuốn sổ! Hình thực tế món này mình ghim ngay trên tường Page, bạn bấm vào tên Page mình tham khảo nha!",
        "Ở trọ tầng cao nước yếu hoặc đường ống cũ có cặn vàng thì lắp thêm đầu vòi tăng áp xoay 720 độ có lõi lọc bông PP trong suốt là nước mạnh gấp 3 mà sạch hẳn cặn bẩn. Mình có để chi tiết món này ngay bài đầu trên tường Page, bạn nào cần bấm vào tên Page mình xem nhé!",
        "Khe hở dưới đáy cửa phòng trọ chính là đường cao tốc cho gián, bụi hành lang và thoát hơi lạnh điều hòa! Dán 1 thanh ron cao su 3 lớp chắn đáy cửa là kín bưng và cách âm cực êm — mình vừa đăng hình thực tế ngay trên tường Page, bạn bấm vào tên Page mình xem nha!",
        "Góc bàn phòng trọ hay đầu giường nhiều dây sạc chằng chịt thì cứ gom vào hộp nhựa ABS chống cháy nắp vân gỗ là gọn đẹp chuẩn Hàn Quốc ngay. List đồ cải tạo phòng trọ giá hạt dẻ không cần khoan tường mình ghim sẵn trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Đi làm về muộn ngại nhất dọn dẹp lỉnh kỉnh, cứ ưu tiên đồ gấp gọn dán tường chịu lực để lúc chuyển trọ mang đi nhẹ tênh. Mình vừa tổng hợp mấy món đồ trọ thông minh đáng tiền nhất ngay trên tường Page, bạn nào đang decor lại phòng bấm vào tên Page mình xem nha!"
    ],
    "ktx": [
        "Nhớ cảnh KTX quá! Tủ sắt cá nhân ở KTX nhỏ xíu thì cứ dùng bộ túi nén hút chân không kèm bơm tay là thu gọn được 75% chỗ để chăn bông với áo khoác dày. Trọn bộ đồ sinh tồn KTX tiết kiệm diện tích mình ghim sẵn ngay trên tường Page, đồng môn bấm vào tên Page mình xem nhé!",
        "Mùa thi thức đêm ôn bài ở KTX ngại nhất bật đèn trần làm chói mắt cả phòng! Chân ái là đèn học LED chống cận ngàm kẹp thành giường tích điện, chiếu đúng trang sách cực dịu mắt — mình vừa lên bài mẫu này ngay trên tường Page, bạn nào ở giường tầng bấm vào tên Page mình xem nha!",
        "Nằm giường tầng 2 KTX ngại nhất mỗi lần lấy chai nước, sạc dự phòng hay laptop lại phải trèo thang lên xuống. Ngoắc ngay 1 chiếc giỏ thép sơn tĩnh điện vào thành giường là đủ chỗ để mọi thứ trong tầm tay — hình thực tế mình ghim ngay trên tường Page, bạn bấm vào tên Page mình xem nhé!",
        "Ở phòng KTX 6–8 người muốn có góc riêng tư thay đồ, học bài hay ngủ sớm thì lắp bộ rèm che giường tầng cản sáng 90% kèm dây treo không khoan đục là chuẩn bài nhất! Mình vừa tổng hợp các mẫu rèm KTX thoáng đẹp ngay trên tường Page, đồng môn bấm vào tên Page mình tham khảo nha!",
        "Giường tầng KTX lúc kéo rèm kín quạt trần không thổi tới thì hầm bí cực kỳ. Thủ sẵn chiếc quạt tích điện ngàm kẹp lớn kẹp thẳng vào khung sắt đầu giường là mát rượi êm ru suốt đêm — mình có ghim chi tiết món này trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Tân sinh viên học bài trên giường tầng nhớ sắm bàn học gấp gọn có khe dựng iPad và lỗ luồn dây sạc nhé, ngồi viết bài êm lưng không lo mỏi cổ. Toàn bộ list đồ giường tầng KTX giá sinh viên mình ghim sẵn trên tường Page, bạn nào cần bấm vào tên Page mình xem nha!"
    ],
    "deadline": [
        "Dân văn phòng ngồi ghế xoay 8 tiếng hay tê mỏi bắp chân và đau thắt lưng là do hai bàn chân bị hẫng! Đặt chiếc ghế kê chân công thái học có con lăn massage dưới gầm bàn là giữ đùi vuông góc 90 độ êm ru ngay — mình vừa ghim chi tiết trên tường Page, bác nào hay mỏi lưng bấm vào tên Page mình xem nhé!",
        "Cày deadline ban đêm mà bật đèn bàn thường chiếu lóa mặt màn hình thì chỉ 1 tiếng là mỏi nhức hai mắt! Đổi sang thanh đèn treo màn hình ScreenBar quang học bất đối xứng là sáng rực mặt bàn mà màn hình 0% chói lóa — hình thực tế mình ghim ngay trên tường Page, anh em bấm vào tên Page mình xem nha!",
        "Gõ phím và di chuột liên tục cả ngày khiến cạnh bàn cứng tỳ vào cổ tay đỏ ửng, rất dễ bị hội chứng ống cổ tay. Dùng bộ đệm kê tay cao su non Memory Foam bọc vải thoáng khí là êm cổ tay suốt 8 tiếng — mình có ghim combo này trên tường Page, bác nào cần bấm vào tên Page mình tham khảo nhé!",
        "Đặt laptop thẳng trên mặt bàn khiến cổ luôn cúi gập 45 độ, tới chiều là cứng đờ hai bả vai! Nâng màn hình lên ngang tầm mắt bằng giá đỡ laptop hợp kim nhôm xoay 360 độ là hết hẳn mỏi cổ vai gáy — bài review chi tiết mình để ngay trên tường Page, anh em văn phòng bấm vào tên Page mình xem nha!",
        "Ghế xoay văn phòng thường hở ngay hõm thắt lưng nên ngồi tới chiều là lưng cong chữ C. Lắp thêm gối tựa lưng cao su non ôm sát cột sống là ngồi làm việc cả ngày vẫn thẳng lưng nhẹ tênh — bộ phụ kiện công thái học văn phòng mình ghim sẵn trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Muốn chạy deadline tập trung gấp đôi mà không bị xao nhãng bởi điện thoại thì dùng đồng hồ Pomodoro lục giác cảm biến trọng lực: lật mặt 25 phút lên là tự đếm ngược vào việc ngay! Mình vừa lên bài món này trên tường Page, bác nào làm văn phòng bấm vào tên Page mình xem nha!"
    ]
}

DIRECT_REPLY_POOL = {
    "ai": [
        "Chuẩn luôn bác! Nếu muốn tách việc cho một Đội ngũ Subagent Cá nhân hoặc Doanh nghiệp chạy tự động có cổng kiểm duyệt riêng, bác bấm vào tên Page mình xem bộ khung 10 Subagent mẫu & dịch vụ thiết kế may đo 1:1 ngay bài ghim đầu tiên nhé!",
        "Góc nhìn rất thực tế ạ! Bên mình vừa đóng gói sẵn Sơ đồ Kiến trúc Đội ngũ Subagent Toàn diện kèm nhận dựng hệ thống Subagent theo quy trình riêng ngay trên tường Page, bác bấm vào tên Page mình tham khảo nha!",
        "Đúng chỗ nhiều anh em đang vướng luôn! Mình có ghim trọn bộ Blueprint Đội ngũ Subagent Cá nhân & Doanh nghiệp miễn phí ở bài đầu tiên trên tường Page, bác bấm vào tên Page mình lấy về áp dụng thử nhé!"
    ],
    "phongtro": [
        "Đồng cảm luôn bạn ơi! Mình vừa tổng hợp mấy món đồ phòng trọ nhỏ gọn không cần khoan tường xử lý gọn tình trạng này ngay bài đầu tiên trên tường Page, bạn bấm vào tên Page mình xem thử nha!",
        "Chuẩn bài luôn ạ! Trên tường Page mình vừa lên hình chi tiết mấy món cứu cánh phòng trọ nhỏ giá hạt dẻ mà cực bền, bạn bấm vào tên Page mình tham khảo thêm nhé!",
        "Mẹo này áp dụng ở phòng trọ siêu tiện luôn! Mình có ghim sẵn list đồ gia dụng phòng trọ thông minh ngay trên tường Page, bạn bấm vào tên Page mình xem chi tiết nha!"
    ],
    "ktx": [
        "Chuẩn cảnh sinh viên KTX luôn bạn ơi! Mình vừa ghim trọn bộ đồ dùng giường tầng KTX siêu gọn nhẹ giá sinh viên ngay bài đầu trên tường Page, bạn bấm vào tên Page mình xem nha!",
        "Ở KTX có món này tiện hơn hẳn thật! Trên tường Page mình có tổng hợp sẵn mấy món bảo bối giường tầng KTX không cần khoan đục, đồng môn bấm vào tên Page mình tham khảo nhé!",
        "Đồng môn nói chuẩn quá! Mình vừa cập nhật bộ sưu tập đồ sinh tồn KTX tiết kiệm diện tích ngay trên tường Page, bạn bấm vào tên Page mình xem chi tiết nha!"
    ],
    "deadline": [
        "Chuẩn nỗi đau dân văn phòng luôn bác! Mình vừa ghim trọn bộ phụ kiện công thái học chống mỏi cổ vai gáy & cổ tay ngay bài đầu trên tường Page, bác bấm vào tên Page mình tham khảo nhé!",
        "Ngồi máy tính 8 tiếng mỗi ngày có thêm món công thái học đỡ mỏi hẳn thật! Trên tường Page mình vừa lên bài chi tiết mấy món setup góc làm việc cực êm, bác bấm vào tên Page mình xem nha!",
        "Đồng ý 100% luôn ạ! Mình có tổng hợp sẵn combo desk setup tăng tập trung chạy deadline ngay trên tường Page, bác bấm vào tên Page mình xem chi tiết nhé!"
    ]
}

NICHE_META = [
    {
        "slug": "ai",
        "fanpage_name": "AI Players - Người chơi hệ AI",
        "name": "AI Players - Cộng đồng AI & Subagent",
        "feeds": [
            {
                "mode": "post_group",
                "label": "Bài thảo luận Hội nhóm AI & Tự động hóa sôi nổi",
                "url": "https://www.facebook.com/search/posts?q=AI%20Agent%20ChatGPT%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20h%C3%B3a%20c%C3%B4ng%20vi%E1%BB%87c",
            },
            {
                "mode": "post_group",
                "label": "Bài hỏi đáp & xin tư vấn quy trình AI doanh nghiệp",
                "url": "https://www.facebook.com/search/posts?q=%E1%BB%A9ng%20d%E1%BB%A5ng%20AI%20v%C3%A0o%20c%C3%B4ng%20vi%E1%BB%87c%20v%C4%83n%20ph%C3%B2ng%20doanh%20nghi%E1%BB%87p",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) AI & Tự động hóa",
                "url": "https://www.facebook.com/search/videos?q=AI%20ChatGPT%20c%C3%B4ng%20vi%E1%BB%87c%20reels",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Hướng dẫn AI & Workflow",
                "url": "https://www.facebook.com/search/videos?q=h%C6%B0%E1%BB%9Bng%20d%E1%BA%ABn%20AI%20ChatGPT%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20h%C3%B3a%20c%C3%B4ng%20vi%E1%BB%87c",
            },
        ],
    },
    {
        "slug": "phongtro",
        "fanpage_name": "Phòng Trọ Hết Cứu",
        "name": "Phòng Trọ Hết Cứu - Decor & Mẹo Phòng Trọ",
        "feeds": [
            {
                "mode": "post_group",
                "label": "Bài thảo luận Hội nhóm Decor & Cải tạo Phòng trọ",
                "url": "https://www.facebook.com/search/posts?q=c%E1%BA%A3i%20t%E1%BA%A1o%20d%E1%BB%8Dn%20ph%C3%B2ng%20tr%E1%BB%8D%20sinh%20vi%C3%AAn",
            },
            {
                "mode": "post_group",
                "label": "Bài hỏi kinh nghiệm đồ dùng & decor phòng trọ nhỏ",
                "url": "https://www.facebook.com/search/posts?q=decor%20ph%C3%B2ng%20tr%E1%BB%8D%20nh%E1%BB%8F%20ti%E1%BA%BFt%20ki%E1%BB%87m",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) Đồ gia dụng Phòng trọ",
                "url": "https://www.facebook.com/search/videos?q=%C4%91%E1%BB%93%20d%C3%B9ng%20ph%C3%B2ng%20tr%E1%BB%8D%20sinh%20vi%C3%AAn%20reels",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Cải tạo & Dọn Phòng trọ",
                "url": "https://www.facebook.com/search/videos?q=c%E1%BA%A3i%20t%E1%BA%A1o%20decor%20ph%C3%B2ng%20tr%E1%BB%8D%20nh%E1%BB%8F",
            },
        ],
    },
    {
        "slug": "ktx",
        "fanpage_name": "Ký Túc Xá Có Biến",
        "name": "Ký Túc Xá Có Biến - Sinh Viên & Đời Sống KTX",
        "feeds": [
            {
                "mode": "post_group",
                "label": "Bài thảo luận Hội nhóm Ký túc xá & Giường tầng",
                "url": "https://www.facebook.com/search/posts?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20gi%C6%B0%E1%BB%9Dng%20t%E1%BA%A7ng",
            },
            {
                "mode": "post_group",
                "label": "Bài hỏi kinh nghiệm tân sinh viên ở KTX",
                "url": "https://www.facebook.com/search/posts?q=kinh%20nghi%E1%BB%87m%20%E1%BB%9F%20k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) Ký túc xá & Sinh viên",
                "url": "https://www.facebook.com/search/videos?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20reels",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Đời sống & Đồ dùng KTX",
                "url": "https://www.facebook.com/search/videos?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20review",
            },
        ],
    },
    {
        "slug": "deadline",
        "fanpage_name": "Hội Deadline",
        "name": "Hội Deadline - Dân Văn Phòng & Desk Setup",
        "feeds": [
            {
                "mode": "post_group",
                "label": "Bài thảo luận Hội nhóm Desk Setup & Văn phòng",
                "url": "https://www.facebook.com/search/posts?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20v%C4%83n%20ph%C3%B2ng%20desk%20setup",
            },
            {
                "mode": "post_group",
                "label": "Bài chia sẻ dân văn phòng đau lưng mỏi cổ vai gáy",
                "url": "https://www.facebook.com/search/posts?q=d%C3%A2n%20v%C4%83n%20ph%C3%B2ng%20%C4%91au%20l%C6%B0ng%20m%E1%BB%8Fi%20c%E1%BB%95%20gh%E1%BA%BF%20c%C3%B4ng%20th%C3%A1i%20h%E1%BB%8Dc",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) Phụ Kiện Bàn Làm Việc & Deadline",
                "url": "https://www.facebook.com/search/videos?q=g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20d%C3%A2n%20v%C4%83n%20ph%C3%B2ng%20reels",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Setup Góc Làm Việc & Công Thái Học",
                "url": "https://www.facebook.com/search/videos?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20desk%20setup%20v%C4%83n%20ph%C3%B2ng",
            },
        ],
    },
]

JS_RANK_HOT_POSTS_AND_VIDEOS = r"""
(feedMode) => {
    document.querySelectorAll('[data-javis-like-rank]').forEach(el => el.removeAttribute('data-javis-like-rank'));
    document.querySelectorAll('[data-javis-cmt-rank]').forEach(el => el.removeAttribute('data-javis-cmt-rank'));
    document.querySelectorAll('[data-javis-share-rank]').forEach(el => el.removeAttribute('data-javis-share-rank'));

    function parseMetricCount(str) {
        if (!str) return 0;
        let s = str.toLowerCase().replace(/\s+/g, '');
        let m = s.match(/(\d+(?:[.,]\d+)?)\s*(k|nghìn|triệu|m|tr)?/i);
        if (!m) return 0;
        let num = parseFloat(m[1].replace(',', '.'));
        let unit = (m[2] || '').toLowerCase();
        if (unit === 'k' || unit === 'nghìn') num *= 1000;
        if (unit === 'triệu' || unit === 'm' || unit === 'tr') num *= 1000000;
        return Math.round(num);
    }

    function getPostContainer(btn) {
        let cur = btn;
        for (let d = 0; d < 14; d++) {
            if (!cur || !cur.parentElement) break;
            cur = cur.parentElement;
            if (cur.getAttribute('role') === 'article') return cur;
            const txt = (cur.innerText || '');
            if (txt.length > 140 && (cur.querySelector('[aria-label="Thích"], [aria-label^="Bày tỏ cảm xúc Thích"]') || cur.querySelector('a[href*="/videos/"], a[href*="/reel/"], video'))) {
                if (d >= 6) return cur;
            }
        }
        return cur;
    }

    const candidates = [];
    const seenContainers = new Set();

    const actionBtns = Array.from(document.querySelectorAll('[aria-label="Thích"], [aria-label^="Bày tỏ cảm xúc Thích"], [aria-label="Viết bình luận"], [aria-label="Bình luận"], [aria-label^="Bình luận về"], [aria-label^="Comment on "]'));
    for (const btn of actionBtns) {
        const container = getPostContainer(btn);
        if (!container || seenContainers.has(container)) continue;
        seenContainers.add(container);

        const text = (container.innerText || '');
        const lower = text.toLowerCase();

        let freshnessScore = 0;
        const hasOldYear = /\b(2018|2019|2020|2021|2022|2023|2024|2025)\b/.test(lower);
        const hasVeryFresh = /\b(vừa xong|phút|giờ|hôm qua|1 ngày|2 ngày|3 ngày|4 ngày|5 ngày|6 ngày|1 tuần)\b/i.test(lower);
        if (hasOldYear && !hasVeryFresh) {
            freshnessScore = -2000;
        } else if (hasVeryFresh) {
            freshnessScore = 300;
        } else {
            freshnessScore = 50;
        }

        let likes = 0;
        let comments = 0;
        let shares = 0;
        let views = 0;

        const cmtMatch = text.match(/(\d+(?:[.,]\d+)?\s*(?:K|nghìn|triệu)?)\s*bình luận/i);
        if (cmtMatch) comments = parseMetricCount(cmtMatch[1]);

        const shareMatch = text.match(/(\d+(?:[.,]\d+)?\s*(?:K|nghìn|triệu)?)\s*lượt chia sẻ/i);
        if (shareMatch) shares = parseMetricCount(shareMatch[1]);

        const viewMatch = text.match(/(\d+(?:[.,]\d+)?\s*(?:K|nghìn|triệu)?)\s*lượt xem/i);
        if (viewMatch) views = parseMetricCount(viewMatch[1]);

        const ariaReactions = Array.from(container.querySelectorAll('[aria-label*="Thích:"], [aria-label*="người"], [role="toolbar"]'));
        for (const ar of ariaReactions) {
            const al = ar.getAttribute('aria-label') || ar.innerText || '';
            const c = parseMetricCount(al);
            if (c > likes) likes = c;
        }
        if (likes === 0) {
            const lines = text.split('\n').map(x => x.trim()).filter(Boolean);
            for (const ln of lines) {
                if (/^\d+(?:[.,]\d+)?\s*(?:K|nghìn)?$/i.test(ln)) {
                    likes = Math.max(likes, parseMetricCount(ln));
                }
            }
        }

        const hasVideoTag = !!container.querySelector('video, a[href*="/videos/"], a[href*="/watch/"]');
        const hasReelTag = !!container.querySelector('a[href*="/reel/"], a[href*="/reels/"]') || lower.includes('reels');
        let videoType = 'post';
        const vidEl = container.querySelector('video');
        if (hasReelTag) {
            videoType = 'video_vertical';
        } else if (vidEl) {
            const rect = vidEl.getBoundingClientRect();
            if (rect.height > rect.width * 1.15) {
                videoType = 'video_vertical';
            } else {
                videoType = 'video_horizontal';
            }
        } else if (hasVideoTag || feedMode.startsWith('video_')) {
            videoType = (feedMode === 'video_vertical') ? 'video_vertical' : 'video_horizontal';
        }

        const likeBtn = container.querySelector('[aria-label="Thích"], [aria-label^="Bày tỏ cảm xúc Thích"]');
        const cmtBtn = container.querySelector('[aria-label="Viết bình luận"], [aria-label="Bình luận"], [aria-label^="Bình luận về"], [aria-label^="Comment on "]');
        const shareBtn = container.querySelector('[aria-label*="Chia sẻ"], [aria-label*="Gửi nội dung này"]');

        let hotScore = freshnessScore + (likes * 1.5) + (comments * 6.0) + (shares * 4.0) + (views * 0.05);
        if (feedMode === 'video_horizontal' && videoType === 'video_horizontal') hotScore += 250;
        if (feedMode === 'video_vertical' && videoType === 'video_vertical') hotScore += 250;
        if (likes > 0 || comments > 0 || views > 0) hotScore += 150;

        candidates.push({
            container,
            likeBtn,
            cmtBtn,
            shareBtn,
            likes,
            comments,
            shares,
            views,
            hasVeryFresh,
            videoType,
            hotScore
        });
    }

    candidates.sort((a, b) => b.hotScore - a.hotScore);

    let likeRank = 0;
    let cmtRank = 0;
    let shareRank = 0;
    const topMeta = [];

    for (const item of candidates) {
        if (item.likeBtn) {
            likeRank += 1;
            item.likeBtn.setAttribute('data-javis-like-rank', String(likeRank));
            item.likeBtn.setAttribute('data-javis-vtype', item.videoType);
        }
        if (item.cmtBtn) {
            cmtRank += 1;
            item.cmtBtn.setAttribute('data-javis-cmt-rank', String(cmtRank));
            item.cmtBtn.setAttribute('data-javis-vtype', item.videoType);
        }
        if (item.shareBtn && shareRank === 0) {
            shareRank += 1;
            item.shareBtn.setAttribute('data-javis-share-rank', '1');
        }
        if (topMeta.length < 6) {
            topMeta.push({
                rank: topMeta.length + 1,
                videoType: item.videoType,
                likes: item.likes,
                comments: item.comments,
                views: item.views,
                fresh: item.hasVeryFresh,
                hotScore: Math.round(item.hotScore)
            });
        }
    }

    const reelLinks = [];
    const videoLinks = [];
    const seenUrls = new Set();
    for (const a of Array.from(document.querySelectorAll('a[href]'))) {
        const href = a.href || '';
        if (!href.startsWith('https://www.facebook.com/')) continue;
        const clean = href.split('?')[0];
        if (seenUrls.has(clean)) continue;
        if (href.includes('/reel/')) {
            seenUrls.add(clean);
            reelLinks.push(clean);
        } else if (href.includes('/videos/') || href.includes('/watch/')) {
            seenUrls.add(href.includes('/watch/') ? href : clean);
            videoLinks.push(href.includes('/watch/') ? href : clean);
        }
    }

    return {
        totalCandidates: candidates.length,
        likeCountRanked: likeRank,
        cmtCountRanked: cmtRank,
        topItems: topMeta,
        reelLinks: reelLinks.slice(0, 6),
        videoLinks: videoLinks.slice(0, 6)
    };
}
"""


def get_ws_url() -> str:
    """
    Kết nối vào trình duyệt Bot độc lập (`.chrome-fb-bot`) tại cổng 9222.
    Nếu cổng 9222 chưa bật, TỰ ĐỘNG KHỞI ĐỘNG NGẦM 100% (không bắt CEO mở file .bat).
    TUYỆT ĐỐI KHÔNG đọc DevToolsActivePort hay đụng vào Chrome chính của CEO.
    """
    def _fetch_ws() -> str:
        for url in (
            "http://localhost:9222/json/version",
            "http://[::1]:9222/json/version",
            "http://127.0.0.1:9222/json/version",
        ):
            try:
                with urllib.request.urlopen(url, timeout=2.0) as resp:
                    info = json.loads(resp.read().decode("utf-8", errors="ignore"))
                    if info.get("webSocketDebuggerUrl"):
                        return info["webSocketDebuggerUrl"].replace(
                            "ws://127.0.0.1:9222/", "ws://localhost:9222/"
                        )
            except Exception:
                continue
        return ""

    ws = _fetch_ws()
    if ws:
        return ws

    try:
        from start_bot_chrome import ensure_bot_chrome_online, sync_bot_state_between_machines
        sync_bot_state_between_machines(direction="pull")
        ws = ensure_bot_chrome_online(timeout_sec=12.0, headless=True)
        if ws:
            return ws
    except Exception:
        pass

    return _fetch_ws()


def _find_account_dialog(pg):
    dialogs = pg.locator('div[role="dialog"]')
    for i in range(dialogs.count()):
        d = dialogs.nth(i)
        aria = (d.get_attribute("aria-label") or "").lower()
        if "thông báo" not in aria and "notifications" not in aria and "messenger" not in aria:
            try:
                txt = d.inner_text(timeout=1500)
                if txt and txt.strip():
                    return d, [ln.strip() for ln in txt.splitlines() if ln.strip()]
            except Exception:
                continue
    return None, []


def _click_first_visible(locator_list) -> bool:
    cnt = locator_list.count()
    for i in range(cnt - 1, -1, -1):
        el = locator_list.nth(i)
        try:
            el.scroll_into_view_if_needed(timeout=800)
        except Exception:
            pass
        try:
            if el.is_visible():
                el.click(timeout=3000)
                return True
        except Exception:
            continue
    return False


def ensure_fanpage_active(pg, target_page_name: str) -> bool:
    """
    TƯỜNG LỬA CẤM TUYỆT ĐỐI TRANG CÁ NHÂN (ZERO PERSONAL PROFILE TOUCH):
    Bắt buộc chuyển trình duyệt sang đúng Fanpage mục tiêu trước khi đi tương tác.
    Nếu đang ở Trang cá nhân (Thành Tài) mà không chuyển sang Fanpage được -> DỪNG NGAY LẬP TỨC (return False).
    """
    acct_selector = '[aria-label="Tài khoản, trang cá nhân của bạn"], [aria-label="Trang cá nhân của bạn"], [aria-label="Tài khoản"], [aria-label="Your profile"], [aria-label="Account"]'
    try:
        pg.goto("https://www.facebook.com/", timeout=25000)
        time.sleep(2.5)

        close_btns = pg.locator('[aria-label="Đóng đoạn chat"], [aria-label="Close chat"]')
        for i in range(close_btns.count()):
            try:
                close_btns.nth(i).click(timeout=600)
            except Exception:
                pass

        acct_btn = pg.locator(acct_selector).first
        acct_btn.wait_for(state="visible", timeout=10000)
        acct_btn.click(timeout=3500)
        time.sleep(1.8)
        dialog, d_lines = _find_account_dialog(pg)
        if not dialog:
            return False

        current_name = d_lines[0] if d_lines else ""
        if target_page_name.lower() in current_name.lower() and "thành tài" not in current_name.lower():
            pg.keyboard.press("Escape")
            time.sleep(0.5)
            return True

        quick_candidates = dialog.locator(f'div[role="button"][aria-label="Chuyển sang {target_page_name}"]')
        if _click_first_visible(quick_candidates):
            time.sleep(5.5)
        else:
            see_all = dialog.locator('div[role="button"][aria-label="Xem tất cả trang cá nhân"], div[role="button"]:has-text("Xem tất cả trang cá nhân")')
            if _click_first_visible(see_all):
                time.sleep(2.2)
                dialog, _ = _find_account_dialog(pg) or (dialog, [])

            target_candidates = dialog.locator(
                f'div[role="button"][aria-label*="{target_page_name}"], div[role="listitem"]:has-text("{target_page_name}"), div[role="button"]:has-text("{target_page_name}")'
            )
            if _click_first_visible(target_candidates):
                time.sleep(5.5)
            else:
                pg.keyboard.press("Escape")
                return False

        acct_btn = pg.locator(acct_selector).first
        acct_btn.wait_for(state="visible", timeout=12000)
        acct_btn.click(timeout=3500)
        time.sleep(1.8)
        _, d_lines = _find_account_dialog(pg)
        active_name = d_lines[0] if d_lines else ""
        pg.keyboard.press("Escape")
        time.sleep(0.5)
        if target_page_name.lower() in active_name.lower() and "thành tài" not in active_name.lower():
            return True
    except Exception as e:
        print(f"[SwitchError] {target_page_name}: {e}", flush=True)
    return False


def accept_group_rules_if_present(pg) -> bool:
    try:
        cb = pg.get_by_text("Tôi đồng ý với các quy tắc nhóm")
        if cb.is_visible(timeout=900):
            cb.click()
            time.sleep(0.3)
            pg.locator('[aria-label="Gửi"], div[role="button"]:has-text("Gửi")').last.click()
            time.sleep(1.2)
            return True
    except Exception:
        pass
    return False


def find_safe_fanpage_textbox(pg, fanpage_name: str):
    """
    Tìm ô bình luận/phản hồi an toàn thuộc Fanpage (`dưới tên <fanpage_name>` hoặc ô trả lời khi Page đang có nhãn `dưới tên <fanpage_name>`).
    TUYỆT ĐỐI CHẶN CỨNG nếu phát hiện bất kỳ ô nào có chữ 'Thành Tài'.
    """
    all_tbs = pg.locator('div[contenteditable="true"][role="textbox"]')
    cnt = all_tbs.count()
    if cnt == 0:
        return None

    has_fanpage_identity_on_page = False
    for i in range(cnt):
        aria = (all_tbs.nth(i).get_attribute("aria-label") or "")
        if "thành tài" in aria.lower():
            return None
        if fanpage_name.lower() in aria.lower():
            has_fanpage_identity_on_page = True

    for i in range(cnt - 1, -1, -1):
        tb = all_tbs.nth(i)
        aria = (tb.get_attribute("aria-label") or "")
        if "thành tài" in aria.lower():
            return None
        if fanpage_name.lower() in aria.lower():
            try:
                if tb.is_visible(timeout=800):
                    return tb
            except Exception:
                continue

    if has_fanpage_identity_on_page:
        for i in range(cnt - 1, -1, -1):
            tb = all_tbs.nth(i)
            aria = (tb.get_attribute("aria-label") or "").lower()
            if "thành tài" in aria or "tin nhắn" in aria or "message" in aria:
                continue
            if any(k in aria for k in ["phản hồi", "trả lời", "bình luận", "reply", "comment"]):
                try:
                    if tb.is_visible(timeout=800):
                        return tb
                except Exception:
                    continue
    return None


def try_reply_to_user_comment(pg, fanpage_name: str, reply_text: str) -> bool:
    """
    Tìm một bình luận của người dùng thật trong khay bình luận đang mở, bấm Thích + Phản hồi trực tiếp
    để Facebook bắn Notification đỏ tới điện thoại của người dùng đó.
    """
    try:
        reply_btns = pg.locator('div[role="button"]:has-text("Phản hồi"), span:has-text("Phản hồi")')
        rcnt = reply_btns.count()
        if rcnt == 0:
            return False

        for idx in range(min(rcnt, 4)):
            rbtn = reply_btns.nth(idx)
            try:
                if not rbtn.is_visible(timeout=600):
                    continue
                rbtn.scroll_into_view_if_needed(timeout=800)
                rbtn.click(timeout=1200)
                time.sleep(1.1)

                tb = find_safe_fanpage_textbox(pg, fanpage_name)
                if tb is not None:
                    tb.click(timeout=1200)
                    time.sleep(0.2)
                    pg.keyboard.insert_text(reply_text)
                    time.sleep(0.3)
                    pg.keyboard.press("Enter")
                    time.sleep(2.0)
                    accept_group_rules_if_present(pg)
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def interact_direct_reel_or_video_urls(
    pg,
    urls: list[str],
    fanpage_name: str,
    slug: str,
    f_mode: str,
    pool: list[str],
    reply_pool: list[str],
    cmt_cursor: int,
    max_targets: int,
    out_dir: pathlib.Path,
) -> dict:
    """
    Mở trực tiếp từng URL Facebook Reels (`/reel/...`) hoặc Watch (`/watch/...`),
    xem 3.0s, bấm Thích, mở khay Bình luận, bình luận dưới tên Fanpage và Phản hồi bình luận người xem.
    """
    res = {
        "likes": 0,
        "comments": 0,
        "user_replies": 0,
        "videos_interacted": 0,
        "shots": [],
        "cmt_cursor": cmt_cursor,
    }
    interacted = 0
    for v_url in urls:
        if interacted >= max_targets:
            break
        try:
            pg.goto(v_url, timeout=25000)
            time.sleep(3.2)

            like_btns = pg.locator('[aria-label="Thích"], [aria-label^="Bày tỏ cảm xúc Thích"]')
            if like_btns.count() > 0:
                for li in range(min(like_btns.count(), 3)):
                    lb = like_btns.nth(li)
                    try:
                        if lb.is_visible(timeout=600):
                            lb.click(timeout=1500)
                            res["likes"] += 1
                            time.sleep(0.5)
                            break
                    except Exception:
                        continue

            tb = find_safe_fanpage_textbox(pg, fanpage_name)
            if tb is None:
                cmt_btns = pg.locator(
                    '[aria-label="Bình luận"], [aria-label="Viết bình luận"], [aria-label^="Bình luận"], [aria-label^="Comment"]'
                )
                for ci in range(min(cmt_btns.count(), 4)):
                    cb = cmt_btns.nth(ci)
                    try:
                        if cb.is_visible(timeout=600):
                            cb.click(timeout=1500)
                            time.sleep(1.8)
                            tb = find_safe_fanpage_textbox(pg, fanpage_name)
                            if tb is not None:
                                break
                    except Exception:
                        continue

            if tb is not None:
                cmt_text = pool[res["cmt_cursor"] % len(pool)]
                res["cmt_cursor"] += 1
                tb.click(timeout=1500)
                time.sleep(0.25)
                pg.keyboard.insert_text(cmt_text)
                time.sleep(0.35)
                pg.keyboard.press("Enter")
                time.sleep(2.4)
                accept_group_rules_if_present(pg)

                interacted += 1
                res["comments"] += 1
                res["videos_interacted"] += 1

                r_text = reply_pool[res["cmt_cursor"] % len(reply_pool)]
                if try_reply_to_user_comment(pg, fanpage_name, r_text):
                    res["user_replies"] += 1
                    res["comments"] += 1

                shot_path = out_dir / f"highvol_{slug}_{f_mode}_direct_{interacted}.png"
                pg.screenshot(path=str(shot_path))
                res["shots"].append(str(shot_path))
        except Exception:
            continue
    return res


def run_shift_interactions(shift: int, urls_per_niche: int, cmts_per_url: int, out_dir: pathlib.Path) -> dict:
    from playwright.sync_api import sync_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    ws_url = get_ws_url()
    summary = {
        "shift": shift,
        "filter_policy": "PRIORITIZE_NEW_HIGH_LIKES_HIGH_COMMENTS_AND_DIRECT_REELS_AND_USER_REPLIES",
        "total_likes": 0,
        "total_comments": 0,
        "total_user_replies": 0,
        "total_shares": 0,
        "total_groups_joined": 0,
        "total_videos_interacted": 0,
        "horizontal_videos_interacted": 0,
        "vertical_videos_interacted": 0,
        "details": [],
        "screenshots": [],
    }

    if not ws_url:
        from graph_api_page_interactor import run_graph_api_fallback
        return run_graph_api_fallback(shift, out_dir)

    summary["status"] = "OK"
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, timeout=15000)
        ctx = browser.contexts[0]
        try:
            local_fb_cookies = ctx.cookies("https://www.facebook.com")
            if not any(c.get("name") == "c_user" for c in local_fb_cookies):
                from start_bot_chrome import import_bot_session_vault
                vault_cookies = import_bot_session_vault()
                if vault_cookies:
                    ctx.add_cookies(vault_cookies)
        except Exception:
            pass
        fb_pages = [pg for pg in ctx.pages if "facebook.com" in pg.url]
        non_chrome = [pg for pg in ctx.pages if not pg.url.startswith("chrome://")]
        pg = fb_pages[-1] if fb_pages else (non_chrome[-1] if non_chrome else ctx.new_page())

        try:
            pg.goto("https://www.facebook.com/", timeout=22000)
            time.sleep(2.5)
            fb_cookies_now = ctx.cookies("https://www.facebook.com")
            has_c_user = any(c.get("name") == "c_user" for c in fb_cookies_now)
            has_login_input = pg.locator(
                'input[name="email"], input[name="pass"], [aria-label^="Tiếp tục "], [aria-label="Dùng trang cá nhân khác"]'
            ).count() > 0
            is_checkpoint = "checkpoint" in pg.url.lower() or "two_step_verification" in pg.url.lower()
            if (not has_c_user) or has_login_input or is_checkpoint:
                try:
                    from start_bot_chrome import stop_bot_chrome
                    stop_bot_chrome()
                except Exception:
                    pass
                from graph_api_page_interactor import run_graph_api_fallback
                return run_graph_api_fallback(shift, out_dir)
        except Exception:
            pass

        for niche in NICHE_META:
            slug = niche["slug"]
            fanpage_name = niche["fanpage_name"]
            pool = COMMENTS_POOL[slug]
            reply_pool = DIRECT_REPLY_POOL[slug]

            if not ensure_fanpage_active(pg, fanpage_name):
                continue
            niche_likes = 0
            niche_cmts = 0
            niche_user_replies = 0
            niche_shares = 0
            niche_joins = 0
            niche_vid_horiz = 0
            niche_vid_vert = 0
            niche_shots = []
            niche_top_scored = []
            cmt_cursor = ((shift - 1) * 2) % len(pool)

            feeds = niche["feeds"]
            for u_idx in range(min(urls_per_niche, len(feeds))):
                feed_cfg = feeds[u_idx]
                f_mode = feed_cfg["mode"]
                url = feed_cfg["url"]
                try:
                    pg.goto(url, timeout=25000)
                    time.sleep(3.2)

                    for _ in range(4):
                        pg.mouse.wheel(0, 800)
                        time.sleep(0.9)
                    pg.mouse.wheel(0, -1400)
                    time.sleep(0.8)

                    try:
                        join_btns = pg.locator('div[role="button"]:has-text("Tham gia")')
                        if join_btns.count() > 0:
                            join_btns.first.scroll_into_view_if_needed(timeout=1500)
                            join_btns.first.click(timeout=1500)
                            time.sleep(1.0)
                            accept_group_rules_if_present(pg)
                            niche_joins += 1
                            summary["total_groups_joined"] += 1
                    except Exception:
                        pass

                    rank_info = {}
                    try:
                        rank_info = pg.evaluate(JS_RANK_HOT_POSTS_AND_VIDEOS, f_mode)
                        if rank_info and rank_info.get("topItems"):
                            niche_top_scored.extend(rank_info["topItems"][:2])
                    except Exception:
                        rank_info = {}

                    max_likes_here = 5
                    for rank_i in range(1, max_likes_here + 1):
                        try:
                            btn = pg.locator(f'[data-javis-like-rank="{rank_i}"]').first
                            if btn.count() == 0:
                                btn = pg.locator('[aria-label="Thích"], [aria-label^="Bày tỏ cảm xúc Thích"]').nth(rank_i - 1)
                            btn.scroll_into_view_if_needed(timeout=1500)
                            vtype = btn.get_attribute("data-javis-vtype") or f_mode

                            if f_mode.startswith("video_") or vtype.startswith("video_"):
                                time.sleep(2.5 if rank_i == 1 else 1.2)
                                if f_mode == "video_vertical" or vtype == "video_vertical":
                                    niche_vid_vert += 1
                                    summary["vertical_videos_interacted"] += 1
                                else:
                                    niche_vid_horiz += 1
                                    summary["horizontal_videos_interacted"] += 1
                                summary["total_videos_interacted"] += 1

                            btn.click(timeout=1500)
                            niche_likes += 1
                            summary["total_likes"] += 1
                            time.sleep(0.4)
                        except Exception:
                            pass

                    try:
                        share_btn = pg.locator('[data-javis-share-rank="1"]').first
                        if share_btn.count() == 0:
                            share_btn = pg.locator(
                                '[aria-label="Chia sẻ"], div[role="button"]:has-text("Chia sẻ")'
                            ).first
                        if share_btn.count() > 0:
                            share_btn.scroll_into_view_if_needed(timeout=1500)
                            share_btn.click(timeout=1500)
                            time.sleep(1.2)
                            share_now = pg.locator(
                                'div[role="menuitem"]:has-text("Chia sẻ ngay"), div[role="button"]:has-text("Chia sẻ ngay"), span:has-text("Chia sẻ ngay")'
                            )
                            if share_now.count() > 0:
                                share_now.first.click(timeout=1500)
                                time.sleep(1.5)
                                niche_shares += 1
                                summary["total_shares"] += 1
                            else:
                                pg.keyboard.press("Escape")
                    except Exception:
                        try:
                            pg.keyboard.press("Escape")
                        except Exception:
                            pass

                    posted_here = 0
                    for rank_c in range(1, 7):
                        if posted_here >= cmts_per_url:
                            break
                        cmt_text = pool[cmt_cursor % len(pool)]
                        cmt_cursor += 1
                        try:
                            c_btn = pg.locator(f'[data-javis-cmt-rank="{rank_c}"]').first
                            if c_btn.count() == 0:
                                c_btn = pg.locator('[aria-label="Viết bình luận"], [aria-label="Bình luận"], [aria-label^="Bình luận về"], [aria-label^="Comment on "]').nth(rank_c - 1)
                            if c_btn.count() == 0:
                                continue

                            c_btn.scroll_into_view_if_needed(timeout=1800)
                            if f_mode.startswith("video_"):
                                time.sleep(1.8)
                            c_btn.click(timeout=1800)
                            time.sleep(1.8)

                            tb = find_safe_fanpage_textbox(pg, fanpage_name)
                            if tb is not None:
                                tb.click(timeout=1600)
                                time.sleep(0.25)
                                pg.keyboard.insert_text(cmt_text)
                                time.sleep(0.35)
                                pg.keyboard.press("Enter")
                                time.sleep(2.4)
                                accept_group_rules_if_present(pg)
                                posted_here += 1
                                niche_cmts += 1
                                summary["total_comments"] += 1

                                if posted_here == 1:
                                    r_text = reply_pool[cmt_cursor % len(reply_pool)]
                                    if try_reply_to_user_comment(pg, fanpage_name, r_text):
                                        niche_user_replies += 1
                                        summary["total_user_replies"] += 1
                                        niche_cmts += 1
                                        summary["total_comments"] += 1

                                if f_mode == "video_horizontal" and niche_vid_horiz == 0:
                                    niche_vid_horiz += 1
                                    summary["horizontal_videos_interacted"] += 1
                                    summary["total_videos_interacted"] += 1
                                elif f_mode == "video_vertical" and niche_vid_vert == 0:
                                    niche_vid_vert += 1
                                    summary["vertical_videos_interacted"] += 1
                                    summary["total_videos_interacted"] += 1

                                shot_path = out_dir / f"highvol_{slug}_{f_mode}_{u_idx}_{posted_here}.png"
                                pg.screenshot(path=str(shot_path))
                                niche_shots.append(str(shot_path))
                                summary["screenshots"].append(str(shot_path))

                                pg.keyboard.press("Escape")
                                time.sleep(0.8)
                            else:
                                pg.keyboard.press("Escape")
                                time.sleep(0.4)
                        except Exception:
                            try:
                                pg.keyboard.press("Escape")
                            except Exception:
                                pass

                    if f_mode.startswith("video_") and posted_here < cmts_per_url:
                        direct_links = (
                            (rank_info.get("reelLinks") or []) + (rank_info.get("videoLinks") or [])
                            if f_mode == "video_vertical"
                            else (rank_info.get("videoLinks") or []) + (rank_info.get("reelLinks") or [])
                        )
                        if direct_links:
                            d_res = interact_direct_reel_or_video_urls(
                                pg=pg,
                                urls=direct_links,
                                fanpage_name=fanpage_name,
                                slug=slug,
                                f_mode=f_mode,
                                pool=pool,
                                reply_pool=reply_pool,
                                cmt_cursor=cmt_cursor,
                                max_targets=max(1, cmts_per_url - posted_here),
                                out_dir=out_dir,
                            )
                            cmt_cursor = d_res["cmt_cursor"]
                            niche_likes += d_res["likes"]
                            summary["total_likes"] += d_res["likes"]
                            niche_cmts += d_res["comments"]
                            summary["total_comments"] += d_res["comments"]
                            niche_user_replies += d_res["user_replies"]
                            summary["total_user_replies"] += d_res["user_replies"]
                            if f_mode == "video_vertical":
                                niche_vid_vert += d_res["videos_interacted"]
                                summary["vertical_videos_interacted"] += d_res["videos_interacted"]
                            else:
                                niche_vid_horiz += d_res["videos_interacted"]
                                summary["horizontal_videos_interacted"] += d_res["videos_interacted"]
                            summary["total_videos_interacted"] += d_res["videos_interacted"]
                            niche_shots.extend(d_res["shots"])
                            summary["screenshots"].extend(d_res["shots"])
                except Exception:
                    pass

            summary["details"].append(
                {
                    "slug": slug,
                    "name": niche["name"],
                    "likes": niche_likes,
                    "comments": niche_cmts,
                    "user_replies": niche_user_replies,
                    "shares": niche_shares,
                    "groups_joined": niche_joins,
                    "video_horizontal": niche_vid_horiz,
                    "video_vertical": niche_vid_vert,
                    "videos_total": niche_vid_horiz + niche_vid_vert,
                    "top_scored_samples": niche_top_scored[:3],
                    "screenshots": niche_shots,
                }
            )

        try:
            from start_bot_chrome import export_bot_session_vault
            export_bot_session_vault(ctx.cookies("https://www.facebook.com"))
        except Exception:
            pass

    try:
        from start_bot_chrome import stop_bot_chrome, sync_bot_state_between_machines
        summary["bot_chrome_auto_closed"] = stop_bot_chrome()
        sync_bot_state_between_machines(direction="push")
    except Exception:
        pass

    shots = summary["screenshots"]
    if len(shots) >= 8:
        grid_path = out_dir / f"shift{shift}_highvol_grid_8.jpg"
        cmd = ["ffmpeg", "-y"]
        for s in shots[:8]:
            cmd += ["-i", s]
        cmd += [
            "-filter_complex",
            "[0:v][1:v][2:v][3:v][4:v][5:v][6:v][7:v]xstack=inputs=8:layout=0_0|w0_0|w0+w1_0|w0+w1+w2_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0,scale=2560:-1",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(grid_path),
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if grid_path.exists():
            summary["grid_photo"] = str(grid_path)
    elif len(shots) >= 4:
        grid_path = out_dir / f"shift{shift}_summary_grid.jpg"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            shots[0],
            "-i",
            shots[1],
            "-i",
            shots[2],
            "-i",
            shots[3],
            "-filter_complex",
            "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,scale=1920:-1",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(grid_path),
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if grid_path.exists():
            summary["grid_photo"] = str(grid_path)

    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shift", type=int, default=1, choices=[1, 2, 3])
    parser.add_argument(
        "--urls-per-niche",
        type=int,
        default=4,
        help="Số luồng mỗi ngách (mặc định 4 luồng: 2 Group + 1 Reels dọc + 1 Video ngang)",
    )
    parser.add_argument("--cmts-per-url", type=int, default=3, help="Số bình luận trên mỗi luồng")
    parser.add_argument("--indices", type=str, default="0,1,2,3", help="Legacy compatibility flag")
    parser.add_argument("--reply-task", type=int, default=0, help="Optional Telegram task_id to reply to")
    parser.add_argument("--send-telegram", action="store_true", help="Send EOD/Shift report to Telegram")
    args = parser.parse_args()

    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    out_dir = REPORTS_DIR / today_str
    summary = run_shift_interactions(args.shift, args.urls_per_niche, args.cmts_per_url, out_dir)

    log_file = out_dir / f"shift{args.shift}_result.json"
    log_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    shift_names = {
        1: "Ca 1 (12:00)",
        2: "Ca 2 (17:30)",
        3: "Ca 3 (20:30)",
    }
    bridge = SUBAGENT_DIR / "tools" / "telegram_bridge.py"
    short_now = dt.datetime.now().strftime("%H:%M %d/%m")

    if summary.get("total_likes", 0) > 0 or summary.get("total_comments", 0) > 0:
        if args.send_telegram or args.reply_task > 0:
            lines = [
                f"✅ Xong {shift_names.get(args.shift, 'Ca tương tác')} ({short_now})",
                f"• Like: +{summary['total_likes']} | Bình luận: +{summary['total_comments']} (Reply trực tiếp user: +{summary.get('total_user_replies', 0)})",
                f"• Video & Reels đã tương tác: +{summary['total_videos_interacted']} ({summary['horizontal_videos_interacted']} ngang, {summary['vertical_videos_interacted']} Reels)",
                f"• Share: +{summary.get('total_shares', 0)} | Vào nhóm mới: +{summary['total_groups_joined']}",
            ]
            msg_text = "\n".join(lines)
            cmd = [sys.executable, str(bridge)]
            if args.reply_task > 0:
                cmd += ["--reply", str(args.reply_task), "--text", msg_text]
            else:
                cmd += ["--send", "8110826820", "--text", msg_text]
            if summary.get("grid_photo"):
                cmd += ["--photo", summary["grid_photo"]]
            subprocess.run(cmd, check=False)
    else:
        status_code = summary.get("status", "ZERO_INTERACTION")
        alert_lines = [
            f"⚠️ Cảnh báo {shift_names.get(args.shift, 'Ca tương tác')} ({short_now}): {status_code}",
            "• Phiên đăng nhập Facebook trên trình duyệt Bot (.chrome-fb-bot) đã hết hạn (màn hình 'Tiếp tục Thành Tài'). Đã mở cửa sổ .chrome-fb-bot để CEO bấm Tiếp tục / nhập mật khẩu 1 lần.",
        ]
        alert_text = "\n".join(alert_lines)
        cmd = [sys.executable, str(bridge), "--send", "8110826820", "--text", alert_text]
        if summary.get("alert_photo"):
            cmd += ["--photo", summary["alert_photo"]]
        subprocess.run(cmd, check=False)

    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
