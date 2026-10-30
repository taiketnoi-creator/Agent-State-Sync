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
        "Công nhận xem chia sẻ này chuẩn thực tế luôn bác ạ. Nhiều anh em sợ xài AI Pro tốn tiền triệu mỗi tháng, nhưng thực ra nếu biết phân tầng công việc kết hợp lấy tài nguyên lẻ tại trạm tự động trên Telegram (gõ @KingToolShop_bot vào ô tìm kiếm Tele là thấy) thì chi phí chỉ bằng ly trà đá, vào bấm Start còn có sẵn mục nhận quà workflow 0đ trong 3 giây luôn.",
        "Đợt trước em làm content với chạy tự động hóa cũng hay mua acc lẻ trên mạng mà ức chế nhất vụ đêm hôm lỗi nick không ai bảo hành. Dạo này chuyển hẳn qua lấy trên trạm tự động @KingToolShop_bot ở Telegram, quét QR đúng 3 giây nó nhả tài khoản ngay trong đêm, lỗi bấm nút đổi mới 1-đổi-1 trong 30 giây nhàn hẳn!",
        "Bác nào đang tập làm AI Agent hay làm video ngắn mà muốn tiết kiệm chi phí tool (ChatGPT, Claude, Canva, CapCut...) thì cứ mở thanh tìm kiếm Telegram gõ @KingToolShop_bot nhé. Vào bấm nút Start là bot tự gửi tặng bộ Prompt + Workflow mẫu 0đ dùng thử ngay không cần chờ duyệt tay.",
        "Đúng chủ đề đang hot luôn! Mình đang dựng tổ đội 6 con Subagent chuyên biệt kết nối thẳng qua Telegram để giao việc từ xa, còn tài nguyên với tool phụ trợ thì lấy tự động bên @KingToolShop_bot trên Tele cho rẻ, tách riêng con viết bài và con kiểm duyệt giúp giảm hẳn lỗi ảo giác!",
        "Chuẩn bác ơi, giờ mà cứ trả nguyên giá 500k-1tr cho từng con AI lẻ thì đau ví lắm. Anh em làm thực chiến toàn lên Telegram tìm @KingToolShop_bot để lấy tài nguyên tự động 24/7, vừa có sẵn gói quà tân thủ 0đ khi bấm Start vừa được bảo hành tự động xuyên đêm.",
        "Nhiều bác sợ xài AI Agent tốn kém, nhưng thực ra nếu biết gom prompt với phân tầng model kết hợp lấy tài nguyên giá sỉ ở trạm bot @KingToolShop_bot trên Telegram thì mỗi tháng tốn chưa tới vài cốc trà đá đâu. Quan trọng là giải phóng được cái đầu sau giờ làm!",
    ],
    "phongtro": [
        "Xem mà đồng cảm thực sự! Phòng trọ nhỏ tầm 15-20m2 bí kíp của mình là sắm 1 chiếc máy hút bụi cầm tay không dây mini có đầu hút khe dẹt để hút sạch tóc rụng trên nệm với bụi bậu cửa sổ trong 2 phút, thêm bộ rổ bào cắt rau củ đa năng là tối đi làm về nấu canh nhanh gọn cực kỳ!",
        "Vụ mốc đen góc tường hay ẩm thấp mùa mưa như này xử lý bằng xịt cồn y tế 70 độ hoặc nước Javen pha loãng cực kỳ sạch nhé mọi người. Lau sạch xong dán lớp xốp cách nhiệt hoặc decal chống thấm lên là vừa đẹp vừa hết mùi hôi.",
        "Phòng trọ gác lửng hướng Tây buổi chiều hay lúc đứng nấu ăn nóng hầm hập thì bác cứ thủ sẵn 1 con quạt cầm tay phản lực 120 mức gió pin 5000mAh, vừa mát sâu vừa đề phòng những hôm khu trọ cúp điện đột xuất giữa đêm!",
        "Chủ nhà trọ khó tính cấm khoan đục tường thì bác nghía thử mấy dòng keo dán seal silicone hoặc miếng dán đinh vít chịu lực xem. Mình dán treo cái kệ gia vị với gương nặng 2kg cả năm nay chưa rớt miếng nào.",
        "Nguyên tắc dọn phòng trọ 15 phút mỗi chiều của mình: Mua 3 cái giỏ phân loại (1 đựng đồ giặt, 1 đựng đồ hay dùng, 1 đựng đồ linh tinh) kết hợp túi nén hút chân không cho chăn màn trái mùa là phòng lúc nào cũng thoáng rộng.",
        "Đi làm về muộn lúc 7h tối ngại nhất khoản ngồi thái cà rốt với khoai tây. Mình sắm bộ bào cắt rau củ đa năng kèm rổ xoay thoát nước, ấn nhẹ 30 giây là xong nồi canh, có cả cục nhựa bảo vệ ngón tay cực kỳ an toàn.",
    ],
    "ktx": [
        "Xem clip/bài này nhớ cảnh KTX quá! Ở KTX tủ đồ nhỏ thì cứ dùng bộ túi nén hút chân không kèm bơm tay mini là gọn được 75% chỗ để chăn áo mùa đông. Còn nằm giường tầng 2 kéo rèm kín hơi bí thì kẹp thêm chiếc quạt tích điện xoay 360 độ vào thành giường là mát êm ru tới sáng luôn!",
        "Mùa thi cử thức đêm cày bài ở KTX khổ nhất là vụ bật đèn làm chói mắt đứa đối diện. Mình xài cái đèn kẹp đầu giường có cổ uốn dẻo, chỉnh luồng sáng chiếu thẳng vô cuốn vở thôi, bạn bè vẫn ngủ ngon lành mà mình thì học bài tẹt ga.",
        "Mùa nắng đi bộ từ giảng đường về KTX hay ngồi hội trường đông người thì chiếc quạt cầm tay phản lực 120 cấp gió có màn hình LED báo pin đúng là vật bất ly thân trong balo luôn các đồng môn ạ!",
        "Ban công KTX phơi đồ chung dễ thất lạc với gió thổi bay mất tiêu. Mẹo là mua chùm móc kẹp inox tròn kết hợp dây phơi chống trượt, móc nguyên chùm vớ với áo mỏng lên vừa tiết kiệm diện tích vừa không lo bay mất.",
        "Tầm 12h trưa hay đêm muộn ở KTX phòng 6-8 người khó tránh khỏi tiếng ồn. Ngoài việc thống nhất nội quy giờ giấc chung thì thủ sẵn cặp nút bịt tai cách âm với rèm che giường tầng là có ngay không gian riêng tư yên tĩnh.",
        "Tân sinh viên mới vào KTX nhớ sắm ngay 1 ổ cắm điện nối dài có công tắc riêng từng lỗ và dây dài 3m nhé, leo lên giường tầng 2 vừa cắm sạc laptop vừa cắm quạt kẹp đầu giường tiện hơn rất nhiều!",
    ],
    "deadline": [
        "Đang chạy slide hay dựng video gấp lúc 1-2h sáng mà vướng bản quyền Canva/CapCut hay hết lượt ChatGPT thì tụt mood thực sự. Mẹo cho anh em hay cày đêm là lưu sẵn con bot @KingToolShop_bot trên Telegram (gõ tên này vào ô tìm kiếm Tele là thấy), quét QR 3 giây nó tự nhả tài khoản xuyên đêm kèm bảo hành 1-đổi-1 tự động luôn.",
        "Kinh nghiệm xương máu cho anh em dân văn phòng với sinh viên hay cày đồ án đêm: nhất định phải lưu sẵn trạm tài nguyên tự động @KingToolShop_bot trên Telegram. Nửa đêm cần gấp Canva, CapCut, Office hay AI chỉ cần bấm vào là bot tự trả nick trong 3 giây, bấm Start lần đầu còn được tặng sẵn quà 0đ nữa!",
        "Xem góc làm việc mê quá! Anh em hay ngồi cày deadline ban đêm ngoài việc kê laptop lên giá đỡ nhôm xoay 360 độ với đèn screenbar cho đỡ mỏi mắt, thì nhớ lưu thêm con bot @KingToolShop_bot trên Telegram để cần công cụ làm việc lúc 2h sáng là lấy tự động trong 3 giây khỏi chờ chủ shop ngủ dậy nhé!",
        "Nhiều người hay nhầm giữa quản lý thời gian với quản lý năng lượng. Việc máy móc lặp lại cứ giao cho AI với bộ mẫu tự động xử lý (anh em có thể lên Telegram gõ @KingToolShop_bot bấm Start để lấy bộ template + prompt miễn phí), tiết kiệm được cả tiếng đồng hồ mỗi tối đấy!",
        "Trưa văn phòng tắt điều hòa tổng thì thủ sẵn quạt phản lực mini trên bàn, còn tối về chạy báo cáo/slide gấp thì cứ thủ sẵn trạm @KingToolShop_bot trên Telegram. Cần tài nguyên thiết kế hay AI lúc mấy giờ đêm nó cũng tự nhả trong 3 giây, có bảo hành tự động 1-đổi-1 cực yên tâm.",
        "Góc làm việc tại nhà (WFH) muốn cày việc đêm mượt thì ánh sáng đèn kẹp màn hình quyết định 50%, 50% còn lại là bộ công cụ AI/Canva/CapCut không bị gián đoạn giữa chừng. Bác nào hay thức khuya cứ gõ @KingToolShop_bot trên Telegram lưu sẵn, nửa đêm cần gì bấm 3 giây là có liền!",
    ],
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
            if (txt.length > 140 && (cur.querySelector('[aria-label="Thích"]') || cur.querySelector('a[href*="/videos/"], a[href*="/reel/"], video'))) {
                if (d >= 6) return cur;
            }
        }
        return cur;
    }

    const candidates = [];
    const seenContainers = new Set();

    const actionBtns = Array.from(document.querySelectorAll('[aria-label="Thích"], [aria-label="Viết bình luận"], [aria-label="Bình luận"]'));
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

        const likeBtn = container.querySelector('[aria-label="Thích"]');
        const cmtBtn = container.querySelector('[aria-label="Viết bình luận"], [aria-label="Bình luận"]');
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
        try:
            with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=2.0) as resp:
                info = json.loads(resp.read().decode("utf-8", errors="ignore"))
                if info.get("webSocketDebuggerUrl"):
                    return info["webSocketDebuggerUrl"]
        except Exception:
            pass
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


def ensure_fanpage_active(pg, target_page_name: str) -> bool:
    """
    TƯỜNG LỬA CẤM TUYỆT ĐỐI TRANG CÁ NHÂN (ZERO PERSONAL PROFILE TOUCH):
    Bắt buộc chuyển trình duyệt sang đúng Fanpage mục tiêu trước khi đi tương tác.
    Nếu đang ở Trang cá nhân (Thành Tài) mà không chuyển sang Fanpage được -> DỪNG NGAY LẬP TỨC (return False).
    """
    try:
        pg.goto("https://www.facebook.com/", timeout=25000)
        time.sleep(2.5)

        # Đóng mọi popup chat Messenger nếu có
        close_btns = pg.locator('[aria-label="Đóng đoạn chat"], [aria-label="Close chat"]')
        for i in range(close_btns.count()):
            try:
                close_btns.nth(i).click(timeout=600)
            except Exception:
                pass

        acct_btn = pg.locator('[aria-label="Trang cá nhân của bạn"], [aria-label="Tài khoản"], [aria-label="Your profile"], [aria-label="Account"]').first
        if acct_btn.count() == 0:
            return False

        acct_btn.click(timeout=3000)
        time.sleep(1.5)
        dialog = pg.locator('div[role="dialog"]').last

        # Kiểm tra dòng đầu tiên trong menu Tài khoản đã là Fanpage mục tiêu chưa
        d_lines = [ln.strip() for ln in dialog.inner_text(timeout=2000).splitlines() if ln.strip()]
        current_name = d_lines[0] if d_lines else ""
        if target_page_name.lower() in current_name.lower() and "thành tài" not in current_name.lower():
            pg.keyboard.press("Escape")
            time.sleep(0.5)
            return True

        # Thử nút chuyển nhanh "Chuyển sang <target_page_name>"
        quick_switch = dialog.locator(f'div[role="button"][aria-label="Chuyển sang {target_page_name}"]').first
        if quick_switch.count() > 0 and quick_switch.is_visible(timeout=1200):
            quick_switch.click(timeout=3000)
            time.sleep(5.0)
        else:
            see_all = dialog.locator('div[role="button"][aria-label="Xem tất cả trang cá nhân"], div[role="button"]:has-text("Xem tất cả trang cá nhân")').first
            if see_all.count() > 0 and see_all.is_visible(timeout=1500):
                see_all.click(timeout=2000)
                time.sleep(1.8)

            target_btn = dialog.locator(f'div[role="button"][aria-label^="{target_page_name}"]').first
            if target_btn.count() > 0 and target_btn.is_visible(timeout=2000):
                target_btn.click(timeout=3000)
                time.sleep(5.0)
            else:
                pg.keyboard.press("Escape")
                return False

        # Xác minh lại lần cuối sau khi chuyển: dòng đầu tiên BẮT BUỘC là Fanpage mục tiêu và CẤM là Thành Tài
        acct_btn = pg.locator('[aria-label="Trang cá nhân của bạn"], [aria-label="Tài khoản"], [aria-label="Your profile"], [aria-label="Account"]').first
        if acct_btn.count() > 0:
            acct_btn.click(timeout=3000)
            time.sleep(1.5)
            dialog = pg.locator('div[role="dialog"]').last
            d_lines = [ln.strip() for ln in dialog.inner_text(timeout=2000).splitlines() if ln.strip()]
            active_name = d_lines[0] if d_lines else ""
            pg.keyboard.press("Escape")
            time.sleep(0.5)
            if target_page_name.lower() in active_name.lower() and "thành tài" not in active_name.lower():
                return True
    except Exception:
        pass
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
                                btn = pg.locator('[aria-label="Thích"]').nth(rank_i - 1)
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
                                c_btn = pg.locator('[aria-label="Viết bình luận"], [aria-label="Bình luận"]').nth(rank_c - 1)
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
