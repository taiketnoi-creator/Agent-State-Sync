#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_daily_group_and_eod.py — Trạm Tự Động Hóa Tương Tác Hội Nhóm & Video Ngang/Dọc Cường Độ Cao.

QUY TẮC BẤT KHẢ XÂM PHẠM (CEO MANDATE — STRICT BAN):
1. TUYỆT ĐỐI NGHIÊM CẤM gọi `taskkill /F /IM chrome.exe` hoặc `Stop-Process -Name chrome` dưới mọi hình thức.
2. TUYỆT ĐỐI NGHIÊM CẤM đọc hay kết nối vào `AppData/Local/Google/Chrome/User Data` hoặc `DevToolsActivePort` trên Chrome chính của CEO.
3. TUYỆT ĐỐI NGHIÊM CẤM mở thêm cửa sổ trên `--profile-directory="Profile 59"` thuộc Chrome chính của CEO.
4. Mọi tương tác tự động bằng trình duyệt CHỈ ĐƯỢC PHÉP chạy trên thư mục Chrome Bot độc lập (`D:\\Phiên bản Ai agent\\Subagent\\.chrome-fb-bot`) qua cổng riêng `9222`. Nếu `.chrome-fb-bot` chưa mở hoặc chưa đăng nhập Facebook thì bỏ qua an toàn, tuyệt đối không đụng vào Chrome chính của CEO.
"""

import argparse
import datetime as dt
import json
import os
import pathlib
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
        "Công nhận chia sẻ này chuẩn thực chiến luôn bác ạ! Dùng 1 con AI đơn lẻ ôm đồm hết mọi việc rất dễ bị loạn ngữ cảnh. Giải pháp chuẩn nhất là thiết lập một Đội ngũ Subagent Cá nhân Toàn diện (1 Tổng quản + các Subagent Thư ký, Nghiên cứu, Nội dung, Tài chính) — bên mình vừa ghim trọn bộ Sơ đồ Kiến trúc & Nhận thiết kế Đội ngũ Subagent may đo 1:1 cho Cá nhân/Doanh nghiệp ngay trên tường Page, bác nào cần bấm vào tên Page mình xem nhé!",
        "Chuẩn luôn bác ơi! Với các chủ shop và SME, thay vì thuê thêm nhân sự làm các việc lặp lại, hiện nay có thể triển khai Phòng ban Subagent Doanh nghiệp (Marketing đa kênh, CSKH 24/7, Kế toán đối soát, Nhân sự SOP) phối hợp tự động. Bên mình có chia sẻ bộ Blueprint mẫu & Nhận xây dựng Đội ngũ Subagent trọn gói theo quy trình riêng ngay trên tường Page, anh em bấm vào tên Page mình tham khảo nha!",
        "Đúng chủ đề nhiều anh em đang tìm kiếm! Một Hệ sinh thái Subagent Cá nhân Toàn diện khi gắn thêm 'Bộ não thứ 2' (Memory Vault) sẽ nhớ 100% phong cách làm việc, lịch trình và quy tắc riêng của chủ nhân mà không bao giờ lặp lại lỗi cũ. Mình có ghim sẵn bản thiết kế mẫu kèm dịch vụ Setup Đội ngũ Subagent may đo ngay bài đầu tiên trên tường Page, bác nào cần bấm vào tên Page mình xem nha!",
        "Góc nhìn rất sát thực tế! Bí quyết để giải phóng 80% thời gian cho CEO và Freelancer không phải là học hàng trăm công cụ rời rạc, mà là sở hữu một Đội ngũ Subagent chuyên môn hóa có cổng kiểm duyệt chéo (Hard Gate). Bên mình đang tặng miễn phí Bộ Khung 10 Subagent (.MD) và nhận tư vấn xây dựng Đội ngũ Subagent riêng cho từng doanh nghiệp ngay trên tường Page, anh em bấm vào tên Page mình nhận nhé!",
        "Bài viết chất lượng quá! Bổ sung thêm cho anh em: khi xây dựng Đội ngũ Subagent cho Doanh nghiệp, quan trọng nhất là nối thẳng vào Zalo/Telegram của sếp để điều khiển bằng ngôn ngữ tự nhiên mọi lúc mọi nơi. Toàn bộ mô hình Phòng ban Subagent 24/7 này bên mình đã đóng gói sẵn và nhận triển khai trọn gói ngay trên tường Page, bác nào quan tâm bấm vào tên Page mình tham khảo nhé!",
        "Đồng ý 100% với tác giả! Từ quản lý lịch trình cá nhân, đọc báo cáo chuyên sâu, viết nội dung đa kênh cho tới vận hành quy trình doanh nghiệp đều có thể bàn giao cho Đội ngũ Subagent chuyên trách. Mình vừa cập nhật trọn bộ giải pháp Thiết kế & Bàn giao Đội ngũ Subagent Cá nhân / Doanh nghiệp Toàn diện ngay trên tường Page, bác nào muốn áp dụng thực tế cứ bấm vào tên Page mình xem chi tiết nha!"
    ],
    "phongtro": [
        "Xem mà đồng cảm thực sự! Phòng trọ nhỏ tầm 15–20m2 bí kíp của mình là gom gọn góc cửa bằng kệ giày khung thép chữ Z và dùng cây lau nhà tự vắt đứng độc lập góc 10cm để giải phóng diện tích sàn. Mình mới tổng hợp mấy món cứu cánh phòng trọ nhỏ gọn cực rẻ ngay trên tường Page, bạn nào đang dọn phòng bấm vào tên Page mình tham khảo nha!",
        "Phòng trọ kín gió hoặc thiếu ban công mỗi đợt mưa dầm 2–3 ngày quần áo phơi trong nhà hay bị mùi ẩm mốc ngai ngái. Mẹo cực hay là dùng túi sấy quần áo gấp gọn tích hợp tia UV khử khuẩn, sấy 45 phút khô cong thơm phức rồi gấp gọn bằng cuốn sổ — mình có ghim hình chi tiết ngay bài đầu tiên trên tường Page, bạn nào cần bấm vào tên Page mình xem nhé!",
        "Ở phòng trọ tầng cao nước yếu hoặc đường ống cũ hay có cặn vàng thì mọi người lắp thêm đầu vòi tăng áp xoay 720 độ có buồng lọc bông PP trong suốt nhé, nhìn lõi lọc chặn cặn bẩn thấy rõ luôn mà nước mạnh gấp 3 lần. Mình vừa lên bài review chi tiết món này ngay trên tường Page, bạn nào quan tâm bấm vào tên Page mình xem nha!",
        "Góc bàn phòng trọ hay đầu giường mà có ổ cắm nối dài chằng chịt dây sạc vừa bám bụi vừa sợ đổ nước vào thì cứ đặt gọn vào hộp nhựa ABS chống cháy nắp vân gỗ là sạch đẹp chuẩn Hàn Quốc ngay. Mình có tổng hợp list đồ dọn phòng trọ gọn đẹp giá hạt dẻ ngay trên tường Page, mọi người bấm vào tên Page mình xem thêm nhé!",
        "Khe hở dưới đáy cửa phòng trọ chính là đường cao tốc cho gián, bụi hành lang và hơi lạnh điều hòa thoát ra ngoài! Chỉ cần dán 1 thanh ron cao su 3 lớp chắn đáy cửa là vừa kín gió vừa cách âm hành lang cực tốt — mình vừa đăng hình thực tế ngay trên tường Page, bạn nào cần bấm vào tên Page mình tham khảo nha!",
        "Đi làm về muộn lúc 7h tối ngại nhất khoản dọn dẹp lỉnh kỉnh. Nguyên tắc của mình là ưu tiên các món gấp gọn đa năng không cần khoan đục tường để lúc chuyển trọ mang đi dễ dàng. Mình có ghim sẵn bộ sưu tập đồ gia dụng phòng trọ thông minh ngay trên tường Page, bạn nào đang decor lại phòng bấm vào tên Page mình xem nhé!"
    ],
    "ktx": [
        "Xem bài này nhớ cảnh KTX quá! Ở KTX tủ sắt cá nhân nhỏ xíu thì cứ dùng bộ túi nén hút chân không kèm bơm tay là thu gọn được 75% chỗ để chăn bông với áo khoác dày. Mình vừa tổng hợp trọn bộ đồ sinh tồn KTX siêu tiết kiệm diện tích ngay trên tường Page, đồng môn nào cần bấm vào tên Page mình xem nhé!",
        "Mùa thi cử thức đêm ôn bài ở KTX ngại nhất là bật đèn trần làm chói mắt 7 đứa bạn cùng phòng! Giải pháp chân ái là dùng đèn học LED chống cận ngàm kẹp thành giường tích điện, uốn cổ ngỗng chiếu đúng trang sách cực dịu mắt — mình có đăng chi tiết mẫu này ngay trên tường Page, bạn nào ở giường tầng bấm vào tên Page mình tham khảo nha!",
        "Nằm giường tầng 2 KTX ngại nhất mỗi lần muốn lấy chai nước, sạc dự phòng hay cất laptop lại phải trèo thang lên xuống. Ngoắc ngay 1 chiếc giỏ thép Carbon sơn tĩnh điện vào thành giường là mọi thứ nằm gọn trong tầm tay — trên tường Page mình có ghim sẵn hình thực tế món này, đồng môn nào cần bấm vào tên Page mình xem nhé!",
        "Ở phòng KTX đông người muốn có góc riêng tư để thay đồ, học bài hay ngủ sớm khi cả phòng vẫn bật đèn sáng trưng thì lắp bộ rèm che giường tầng vải cản sáng 90% kèm dây treo không khoan đục là chuẩn bài nhất! Mình vừa lên bài tổng hợp mẫu rèm KTX thoáng đẹp ngay trên tường Page, bạn nào cần bấm vào tên Page mình xem nha!",
        "Nằm giường tầng KTX lúc kéo rèm kín mà quạt trần không thổi tới thì hầm bí cực kỳ. Thủ sẵn 1 chiếc quạt tích điện ngàm kẹp lớn kẹp thẳng vào khung sắt đầu giường là gió mát rượi êm ru suốt đêm — mình có tổng hợp mấy món cứu nóng KTX giá sinh viên ngay trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Tân sinh viên hay học bài trên giường tầng nhớ sắm chiếc bàn học gấp gọn có khe dựng iPad và rãnh luồn dây sạc nhé, ngồi tựa lưng viết bài không bị gù lưng mỏi cổ chút nào. Toàn bộ list đồ dùng giường tầng KTX tiện nhất mình đã ghim sẵn trên tường Page, bạn nào cần bấm vào tên Page mình tham khảo nha!"
    ],
    "deadline": [
        "Dân văn phòng ngồi ghế xoay 8 tiếng mỗi ngày hay bị tê mỏi bắp chân và đau thắt lưng là do hai bàn chân bị hẫng! Đặt 1 chiếc ghế kê chân công thái học chỉnh 6 nấc có con lăn massage dưới gầm bàn là giữ đùi vuông góc 90 độ chuẩn chỉnh ngay — mình vừa lên bài chi tiết trên tường Page, bác nào hay đau lưng bấm vào tên Page mình xem nhé!",
        "Cày deadline ban đêm mà bật đèn bàn thường chiếu vào mặt màn hình tạo vệt lóa trắng xóa thì chỉ 1 tiếng là khô rát hai mắt! Đổi sang thanh đèn treo màn hình ScreenBar quang học bất đối xứng là sáng rực mặt bàn mà màn hình 0% chói lóa — mình có ghim hình thực tế ngay trên tường Page, anh em bấm vào tên Page mình tham khảo nha!",
        "Gõ bàn phím cơ và di chuột liên tục cả ngày khiến cạnh bàn cứng tỳ vào xương cổ tay đỏ ửng, lâu ngày rất dễ bị hội chứng ống cổ tay. Trang bị bộ đệm kê tay cao su non Memory Foam bọc vải Lycra mát mịn là êm cổ tay suốt 8 tiếng — mình vừa tổng hợp combo bảo vệ cổ tay trên tường Page, bác nào cần bấm vào tên Page mình xem nhé!",
        "Đặt laptop thẳng trên mặt bàn khiến cổ luôn phải cúi gập 45 độ, ngồi tới chiều là cứng đờ hai bả vai! Chỉ cần nâng màn hình lên ngang tầm mắt bằng giá đỡ laptop hợp kim nhôm CNC xoay 360 độ là hết hẳn đau mỏi vai gáy — trên tường Page mình có bài review chi tiết, anh em văn phòng bấm vào tên Page mình xem nha!",
        "Ghế xoay văn phòng thường để trống một khoảng hở ngay hõm thắt lưng nên ngồi tới 3h chiều là lưng cong hình chữ C. Lắp thêm chiếc gối tựa lưng cao su non ôm sát cột sống là ngồi làm việc cả ngày vẫn thẳng lưng nhẹ tênh — mình có ghim sẵn bộ phụ kiện công thái học văn phòng trên tường Page, mọi người bấm vào tên Page mình xem nhé!",
        "Bí quyết chạy deadline tập trung gấp đôi mà không bị xao nhãng bởi thông báo điện thoại là dùng đồng hồ Pomodoro lục giác cảm biến trọng lực: lật mặt 25 phút lên là tự đếm ngược vào việc ngay! Mình vừa tổng hợp các món decor bàn làm việc tăng hiệu suất trên tường Page, bác nào quan tâm bấm vào tên Page mình tham khảo nha!"
    ]
}

NICHE_META = [
    {
        "slug": "ai",
        "fanpage_name": "AI Players - Người chơi hệ AI",
        "name": "AI Players - Cộng đồng AI & Automation",
        "feeds": [
            {
                "mode": "post_group",
                "label": "Bài viết Hội nhóm AI mới & nhiều cmt",
                "url": "https://www.facebook.com/search/posts?q=AI%20Agent%20ChatGPT%20c%C3%B4ng%20vi%E1%BB%87c%20Vi%E1%BB%87t%20Nam",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Hội nhóm AI & Tự động hóa",
                "url": "https://www.facebook.com/search/videos?q=h%C6%B0%E1%BB%9Bng%20d%E1%BA%ABn%20AI%20ChatGPT%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%20h%C3%B3a%20c%C3%B4ng%20vi%E1%BB%87c",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) AI & Công nghệ",
                "url": "https://www.facebook.com/search/videos?q=m%E1%BA%B9o%20d%C3%B9ng%20AI%20ChatGPT%20reels",
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
                "label": "Bài viết Hội nhóm Decor/Dọn Phòng trọ sôi nổi",
                "url": "https://www.facebook.com/search/posts?q=c%E1%BA%A3i%20t%E1%BA%A1o%20d%E1%BB%8Dn%20ph%C3%B2ng%20tr%E1%BB%8D%20sinh%20vi%C3%AAn",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Cải tạo & Nấu ăn Phòng trọ",
                "url": "https://www.facebook.com/search/videos?q=c%E1%BA%A3i%20t%E1%BA%A1o%20decor%20ph%C3%B2ng%20tr%E1%BB%8D%20nh%E1%BB%8F",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) Đồ gia dụng Phòng trọ",
                "url": "https://www.facebook.com/search/videos?q=%C4%91%E1%BB%93%20d%C3%B9ng%20ph%C3%B2ng%20tr%E1%BB%8D%20sinh%20vi%C3%AAn%20reels",
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
                "label": "Bài viết Hội nhóm Ký túc xá ĐHQG sôi nổi",
                "url": "https://www.facebook.com/search/posts?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20gi%C6%B0%E1%BB%9Dng%20t%E1%BA%A7ng",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Đời sống & Đồ dùng KTX",
                "url": "https://www.facebook.com/search/videos?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20review",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) Ký túc xá & Tân sinh viên",
                "url": "https://www.facebook.com/search/videos?q=k%C3%BD%20t%C3%BAc%20x%C3%A1%20sinh%20vi%C3%AAn%20reels",
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
                "label": "Bài viết Hội nhóm Desk Setup & Văn phòng sôi nổi",
                "url": "https://www.facebook.com/search/posts?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20v%C4%83n%20ph%C3%B2ng%20desk%20setup",
            },
            {
                "mode": "video_horizontal",
                "label": "Video Ngang (16:9) Setup Góc Làm Việc & Công Thái Học",
                "url": "https://www.facebook.com/search/videos?q=setup%20g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20desk%20setup%20v%C4%83n%20ph%C3%B2ng",
            },
            {
                "mode": "video_vertical",
                "label": "Video Dọc / Reels (9:16) Phụ Kiện Bàn Làm Việc & Deadline",
                "url": "https://www.facebook.com/search/videos?q=g%C3%B3c%20l%C3%A0m%20vi%E1%BB%87c%20d%C3%A2n%20v%C4%83n%20ph%C3%B2ng%20reels",
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

    return {
        totalCandidates: candidates.length,
        likeCountRanked: likeRank,
        cmtCountRanked: cmtRank,
        topItems: topMeta
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

        # Đợi trang tải lại hoàn tất sau khi Switch Profile rồi xác minh dòng đầu tiên BẮT BUỘC là Fanpage mục tiêu
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
    except Exception as e:
        print(f'[SwitchError] {target_page_name}: {e}', flush=True)
    return False


def run_shift_interactions(shift: int, urls_per_niche: int, cmts_per_url: int, out_dir: pathlib.Path) -> dict:
    from playwright.sync_api import sync_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    ws_url = get_ws_url()
    summary = {
        "shift": shift,
        "filter_policy": "PRIORITIZE_NEW_HIGH_LIKES_HIGH_COMMENTS",
        "total_likes": 0,
        "total_comments": 0,
        "total_shares": 0,
        "total_groups_joined": 0,
        "total_videos_interacted": 0,
        "horizontal_videos_interacted": 0,
        "vertical_videos_interacted": 0,
        "details": [],
        "screenshots": [],
    }

    if not ws_url:
        summary["status"] = "ERROR_CANNOT_AUTOSTART_PORT_9222"
        return summary

    summary["status"] = "OK"
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, timeout=15000)
        ctx = browser.contexts[0]
        try:
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
            if "facebook.com" not in pg.url:
                pg.goto("https://www.facebook.com/", timeout=20000)
                time.sleep(2.0)
            has_login_input = pg.locator('input[name="email"], input[name="pass"]').count() > 0
            is_checkpoint = "checkpoint" in pg.url.lower() or "two_step_verification" in pg.url.lower()
            if has_login_input or is_checkpoint:
                alert_shot = out_dir / f"shift{shift}_alert_approval_needed.png"
                pg.screenshot(path=str(alert_shot))
                summary["status"] = "CHECKPOINT_APPROVAL_NEEDED" if is_checkpoint else "LOGIN_APPROVAL_NEEDED"
                summary["alert_photo"] = str(alert_shot)
                try:
                    from start_bot_chrome import stop_bot_chrome
                    summary["bot_chrome_auto_closed"] = stop_bot_chrome()
                except Exception:
                    pass
                return summary
        except Exception:
            pass

        for niche in NICHE_META:
            slug = niche["slug"]
            fanpage_name = niche["fanpage_name"]
            pool = COMMENTS_POOL[slug]

            # BẮT BUỘC CHUYỂN SANG ĐÚNG FANPAGE TRƯỚC KHI TƯƠNG TÁC (TUYỆT ĐỐI CẤM DÙNG TRANG CÁ NHÂN)
            if not ensure_fanpage_active(pg, fanpage_name):
                continue
            niche_likes = 0
            niche_cmts = 0
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

                    for _ in range(3):
                        pg.mouse.wheel(0, 750)
                        time.sleep(1.0)
                    pg.mouse.wheel(0, -1200)
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

                    max_likes_here = 4
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
                            time.sleep(0.45)
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
                    for rank_c in range(1, 6):
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

                            # CHỈ GÕ VÀO Ô BÌNH LUẬN CÓ NHÃN "dưới tên <Tên Fanpage>" — CẤM TUYỆT ĐỐI Ô CHAT MESSENGER HOẶC TRANG CÁ NHÂN
                            tb = pg.locator(
                                f'div[contenteditable="true"][role="textbox"][aria-label*="dưới tên {fanpage_name}"]'
                            ).first
                            if tb.is_visible(timeout=1800):
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

                                if f_mode == "video_horizontal" and niche_vid_horiz == 0:
                                    niche_vid_horiz += 1
                                    summary["horizontal_videos_interacted"] += 1
                                    summary["total_videos_interacted"] += 1
                                elif f_mode == "video_vertical" and niche_vid_vert == 0:
                                    niche_vid_vert += 1
                                    summary["vertical_videos_interacted"] += 1
                                    summary["total_videos_interacted"] += 1

                                shot_path = out_dir / f"highvol_{slug}_{f_mode}_{posted_here}.png"
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
                except Exception:
                    pass

            summary["details"].append(
                {
                    "slug": slug,
                    "name": niche["name"],
                    "likes": niche_likes,
                    "comments": niche_cmts,
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
    parser.add_argument("--shift", type=int, default=3, choices=[1, 2, 3])
    parser.add_argument(
        "--urls-per-niche",
        type=int,
        default=3,
        help="Số luồng mỗi ngách",
    )
    parser.add_argument("--cmts-per-url", type=int, default=2, help="Số bình luận trên mỗi luồng")
    parser.add_argument("--indices", type=str, default="0,1,2", help="Legacy compatibility flag")
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
                f"• Like: +{summary['total_likes']} | Bình luận: +{summary['total_comments']}",
                f"• Video đã xem & tương tác: +{summary['total_videos_interacted']} ({summary['horizontal_videos_interacted']} ngang, {summary['vertical_videos_interacted']} Reels)",
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
            "• Chưa ghi nhận tương tác mới trong ca này.",
        ]
        alert_text = "\n".join(alert_lines)
        cmd = [sys.executable, str(bridge), "--send", "8110826820", "--text", alert_text]
        if summary.get("alert_photo"):
            cmd += ["--photo", summary["alert_photo"]]
        subprocess.run(cmd, check=False)

    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
