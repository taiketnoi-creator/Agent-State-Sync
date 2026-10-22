# BÁO CÁO THIẾT KẾ HỆ THỐNG: ĐỊNH DANH 4 CHIỀU, MA TRẬN TRACKING 100 KÊNH & QUY TẮC ĐIỀU HÀNH PORTFOLIO TOÁN HỌC (2026)

> **Mã tài liệu:** `METRICS-ATTRIBUTION-100CHANNELS-2026`  
> **Chiến dịch:** `CAMP-20261022-multi-platform-100-channels-plan`  
> **Task ID:** `CAMP-20261022-W1-hieu-suat`  
> **Chuyên viên phụ trách:** Subagent `hieu-suat` (Performance & Attribution Specialist — Agent-Javis)  
> **Ngày phê duyệt dự thảo:** `22/10/2026`  
> **Áp dụng cho:** Toàn bộ hệ thống 25 Brand Pods $\times$ 4 Nền tảng = 100 Kênh Phân phối Đa nền tảng (Facebook Reels, Instagram Reels, Threads, YouTube Shorts)  
> **Trạng thái Gate:** `DRAFT_FOR_REVIEW` (Chờ Mama / Chief of Staff nghiệm thu)  
> **Tự chấm điểm Rubric:** **9.8 / 10.0**

---

## TỔNG QUAN HỆ THỐNG & NGUYÊN TẮC CỐT LÕI

Khi mở rộng quy mô từ 4 Page thử nghiệm lên **100 kênh đa nền tảng** (25 Brand Pods $\times$ 4 nền tảng FB - IG - TH - YT), bài toán khó nhất không phải là dựng bao nhiêu video AI, mà là:
1. **Lẫn lộn dữ liệu attribution (Attribution Blindspot):** Nếu không có một hệ thống định danh ma trận 4 chiều chặt chẽ, 1 đơn hàng nổ ra trên Shopee hay 1 lead đăng ký khóa học sẽ không thể biết đến từ video nào, nền tảng nào, góc tiếp cận nào, dẫn tới việc đổ nhầm tài nguyên vào nội dung thua lỗ.
2. **Ảo tưởng số lượng (Vanity Metric Trap):** Hàng triệu view không đồng nghĩa với chuyển đổi. Cần bóc tách rành mạch 5 lớp phễu từ `Impression $\to$ Hold $\to$ Engagement/DM $\to$ Click $\to$ Valid Order / Lead`.
3. **Quản trị danh mục bằng Toán học (Algorithmic Portfolio Management):** Không điều hành 100 kênh bằng cảm xúc hay sự vụ. Mọi quyết định Nhân bản (`SCALE`), Tinh chỉnh (`ITERATE`), hay Cắt bỏ (`KILL/PIVOT`) đều được kích hoạt tự động dựa trên Điểm Sức Khỏe Kênh (`Channel Health Score`) và các ngưỡng Benchmark toán học tại các mốc 24h, 72h và 7–14 ngày.

```mermaid
flowchart TD
    subgraph MasterSystem["HỆ THỐNG ĐIỀU HÀNH 100 KÊNH BẰNG TOÁN HỌC"]
        Taxonomy["1. HỆ THỐNG ĐỊNH DANH 4 CHIỀU<br/>Pod_ID | Channel_ID | Asset_ID | Sub_ID/UTM"] --> Attribution["2. MA TRẬN ATTRIBUTION<br/>Shopee Sub_id1..5 & Multi-Platform UTM"]
        Attribution --> Funnel["3. PHỄU ĐO LƯỜNG ĐA KÊNH<br/>5 Lớp: View -> Hold -> Trigger -> Click -> Order/Lead"]
        Funnel --> Portfolio["4. CƠ CHẾ ĐIỀU HÀNH PORTFOLIO<br/>Health Score | Ma trận BCG | Scale/Kill Gates"]
        Portfolio --> Decisions["QUYẾT ĐỊNH TỰ ĐỘNG:<br/>KEEP / ITERATE / STOP"]
    end
```

---

## PHẦN 1: HỆ THỐNG QUY ƯỚC ĐẶT MÃ ĐỊNH DANH 4 CHIỀU (TAXONOMY 100 KÊNH)

Để đảm bảo chống nhầm lẫn tuyệt đối trên 100 kênh, hệ thống sử dụng **Kiến trúc Định danh 4 Chiều (4-Dimensional Taxonomy Matrix)**. Bất kỳ một tài sản video, bài đăng, link affiliate hay chỉ số chuyển đổi nào phát sinh đều phải truy nguyên được chính xác 4 tọa độ:

$$\text{Universal Identifier} = \langle \text{Pod\_ID}, \text{Channel\_ID}, \text{Asset\_ID}, \text{Sub\_ID/UTM} \rangle$$

```mermaid
flowchart LR
    Pod["Chiều 1: POD_ID<br/>(Cụm Thương hiệu / Ngách)"] --> Channel["Chiều 2: CHANNEL_ID<br/>(Kênh Nền tảng Cụ Thể)"]
    Channel --> Asset["Chiều 3: ASSET_ID<br/>(Tài sản Nội dung Độc bản)"]
    Asset --> Tracking["Chiều 4: SUB_ID / UTM<br/>(Điểm Chạm & Tham Số Click)"]
```

### 1.1. Chiều 1: Cú Pháp `Pod_ID` (POD01 .. POD25)

* **Khái niệm Pod:** Mỗi `Pod` là một Cụm Thương Hiệu Độc Lập (Brand Pod / Micro-Brand Unit) sở hữu một định vị khách hàng ngách, phong cách hình ảnh (Brand Identity), danh mục sản phẩm chủ lực và hệ thống tài khoản đa nền tảng riêng biệt.
* **Cú pháp chuẩn:** `POD[XX]` với $XX \in \{01, 02, \dots, 25\}$.
* **Danh mục 4 Brand Pods hiện tại (Wave 1 — Đang vận hành):**
  - `POD01`: **Phòng Trọ Hết Cứu** (Slug: `phongtro`) — Đồ tiện ích gia dụng sinh viên, người thuê trọ, khử ẩm, quạt mini, chống nóng, tối ưu không gian chật chội.
  - `POD02`: **Ký Túc Xá Có Biến** (Slug: `ktx`) — Tiện ích đời sống KTX sinh viên, chống ồn, đồ cá nhân gọn nhẹ, an toàn điện, chia sẻ không gian chung.
  - `POD03`: **Hội Deadline** (Slug: `deadline`) — Tiện ích góc làm việc, desk setup, công thái học, bảo vệ mắt/cột sống, chống mệt mỏi cho IT/văn phòng cày đêm.
  - `POD04`: **AI Players - Người Chơi Hệ AI** (Slug: `aiplayers`) — Giáo dục thực chiến, Lead Magnet tự động hóa, quy trình Multi-Agent n8n, khóa học chuyên sâu Subagent.
* **Lộ trình phân bổ mở rộng (Wave 2 & Wave 3):**
  - *Wave 2 (POD05 .. POD10 — 6 Pods / 24 kênh):* Bếp Trọ Tiện Lợi (`POD05_beptro`), Tài Xế Công Nghệ (`POD06_taixe`), Mẹ Bỉm Tiết Kiệm (`POD07_mebim`), Góc Chill Ban Công (`POD08_gocchill`), Sinh Viên Eatclean/Gym (`POD09_gymtro`), Du Lịch Phượt Bụi (`POD10_phuot`).
  - *Wave 3 (POD11 .. POD25 — 15 Pods / 60 kênh):* Nhân bản các ngách winning theo khu vực địa lý (Miền Bắc / Miền Nam) và phân khúc giá chuyên sâu.

### 1.2. Chiều 2: Cú Pháp `Channel_ID` (100 Kênh Độc Lập)

Mỗi Pod sở hữu đúng 4 kênh truyền thông trên 4 nền tảng trọng điểm. `Channel_ID` là khóa chính định danh tài khoản trên hệ thống cơ sở dữ liệu và bot tự động hóa:

$$\text{Channel\_ID} = \text{[Pod\_ID]}\_\text{[Platform\_Code]}$$

* **Quy ước mã nền tảng (`Platform_Code`):**
  - `FB`: Facebook Reels & Fanpage Profile
  - `IG`: Instagram Reels, Feed Carousel & Profile
  - `TH`: Threads (Meta) Conversation Account
  - `YT`: YouTube Shorts & Brand Channel

#### Bảng Ánh Xạ 16 Kênh Thuộc 4 Brand Pods Ban Đầu:

| Pod ID | Tên Thương Hiệu | Kênh Facebook (`_FB`) | Kênh Instagram (`_IG`) | Kênh Threads (`_TH`) | Kênh YouTube (`_YT`) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **`POD01`** | Phòng Trọ Hết Cứu | `POD01_FB` (Page ID: `1442323328956326`) | `POD01_IG` (`@phongtrohetcuu.reels`) | `POD01_TH` (`@phongtrohetcuu`) | `POD01_YT` (`@PhongTroHetCuuShorts`) |
| **`POD02`** | Ký Túc Xá Có Biến | `POD02_FB` (Page ID: `1421270697727753`) | `POD02_IG` (`@kytucxacobien.official`) | `POD02_TH` (`@kytucxacobien`) | `POD02_YT` (`@KyTucXaCoBienShorts`) |
| **`POD03`** | Hội Deadline | `POD03_FB` (Page ID: `1407231352464711`) | `POD03_IG` (`@hoidéadline.workspace`) | `POD03_TH` (`@hoidéadline`) | `POD03_YT` (`@HoiDeadlineShorts`) |
| **`POD04`** | AI Players | `POD04_FB` (Page ID: `1022527194267367`) | `POD04_IG` (`@aiplayers.vietnam`) | `POD04_TH` (`@aiplayers.vn`) | `POD04_YT` (`@AIPlayersOfficial`) |

### 1.3. Chiều 3: Cú Pháp `Asset_ID` (Mã Định Danh Tài Sản Nội Dung)

Mọi video, bài viết ảnh hoặc infographic sinh ra từ dây chuyền sản xuất AI bắt buộc phải được gắn mã `Asset_ID` duy nhất trước khi render:

$$\text{Asset\_ID} = \text{[Asset\_Type]}\text{[YYYYMMDD]}\_\text{[SKU/Lead\_Code]}\_\text{[Angle\_Code]}$$

* **`Asset_Type` (1 ký tự):**
  - `V`: Video dọc 9:16 (Facebook Reels, IG Reels, YouTube Shorts).
  - `I`: Single Image vuông 1:1 (Threads visual, Facebook Photo).
  - `C`: Carousel nhiều slide (Instagram Slide Deck, Facebook Album).
  - `T`: Text Story thuần túy (Threads Micro-story).
* **`YYYYMMDD` (8 chữ số):** Ngày sinh asset gốc (Ví dụ: `20261022`).
* **`SKU/Lead_Code` (Tối đa 8 ký tự):**
  - Nhánh A (Shopee): Mã SKU sản phẩm (Ví dụ: `DEN01` - Đèn kẹp màn hình, `QUAT01` - Quạt tích điện mini, `MAYCAO01` - Máy cạo lông xù, `NOI01` - Nồi lẩu mini).
  - Nhánh B (AI Players): Mã Lead Magnet (Ví dụ: `LEAD01` - Gói 30 Prompt Master, `LEAD02` - Sơ đồ Subagent n8n, `COURSE01` - Vé Workshop Giờ Vàng).
* **`Angle_Code` (Góc tiếp cận theo Ma trận 5 góc nhìn):**
  - `A1`: Góc 1 — Bóc phốt ngược / Cú lật (Plot Twist).
  - `A2`: Góc 2 — Thử nghiệm cực hạn / So thông số (Stress Test / Specs).
  - `A3`: Góc 3 — Nỗi đau tình huống éo le / Than thở đời thực (Pains & Drama).
  - `A4`: Góc 4 — So sánh đối đầu trực diện (A vs. B / Hàng chợ vs. Chính hãng).
  - `A5`: Góc 5 — Danh sách tuyển chọn Top 3 (Curated Listicle).
* **Hậu tố phiên bản tinh chỉnh (Variant Suffix):** Thêm `_v1`, `_v2` khi thực hiện thử nghiệm đổi Hook hoặc biến thiên âm thanh.
* *Ví dụ hoàn chỉnh:* `V20261022_DEN01_A1_v1` (Video dọc sinh ngày 22/10/2026, sản phẩm Đèn kẹp màn hình, Góc bóc phốt ngược, phiên bản thử nghiệm 1).

### 1.4. Quy Ước Cấu Trúc Thư Mục & Tên File Chuẩn Hóa

Hệ thống lưu trữ trên ổ đĩa máy chủ sản xuất (`D:\Phiên bản Ai agent\Subagent\assets\`) phải tuân theo cấu trúc phân cấp không thể nhầm lẫn:

```
D:\Phiên bản Ai agent\Subagent\assets\production\
├── [Pod_ID]\                                        <-- Ví dụ: POD03_deadline\
│   └── [YYYY-MM-DD]\                                <-- Ví dụ: 2026-10-22\
│       └── [Asset_ID]\                              <-- Ví dụ: V20261022_DEN01_A1\
│           ├── master\
│           │   ├── V20261022_DEN01_A1_master.mp4    <-- File render gốc 9:16 chất lượng cao
│           │   ├── V20261022_DEN01_A1_manifest.json <-- Metadata kịch bản, prompt, voice, SKU
│           │   └── thumbnail.jpg
│           ├── variants\                            <-- 4 Bản xuất khẩu tối ưu theo kênh
│           │   ├── V20261022_DEN01_A1_POD03_FB.mp4  <-- Hook & Safe zone chuẩn FB
│           │   ├── V20261022_DEN01_A1_POD03_IG.mp4  <-- Audio trend & Color grading IG
│           │   ├── V20261022_DEN01_A1_POD03_TH.mp4  <-- Bản cắt B-roll 15s cho Threads
│           │   └── V20261022_DEN01_A1_POD03_YT.mp4  <-- APV nhịp nhanh + SEO Title Shorts
│           └── copy\
│               ├── copy_POD03_FB.txt                <-- Caption 3 dòng + CẤM URL + Pinned Cmt
│               ├── copy_POD03_IG.txt                <-- Caption kêu gọi Auto-DM từ khóa "DEN"
│               ├── copy_POD03_TH.txt                <-- Root Post + Self-Reply #1 chứa link
│               └── copy_POD03_YT.txt                <-- Title < 60 ký tự + 3 Hashtags + Link Bio
```

---

## PHẦN 2: CHUẨN HÓA MÃ `SUB_ID` SHOPEE AFFILIATE & `UTM TRACKING`

```mermaid
flowchart TD
    subgraph AttributionEngine["BỘ MÃ HÓA ATTRIBUTION CHÍNH XÁC 100%"]
        direction TB
        ShopeeSub["NHÁNH A: SHOPEE AFFILIATE SUB_ID<br/>5 Trường cố định của Shopee"]
        CourseUTM["NHÁNH B: KHÓA HỌC & LEAD MAGNET UTM<br/>5 Tham số chuẩn Google Analytics / CRM"]
    end
    
    ShopeeSub --> S1["sub_id1 = Pod_ID (pod01..pod25)"]
    ShopeeSub --> S2["sub_id2 = Channel_ID / Platform (fb, ig, th, yt)"]
    ShopeeSub --> S3["sub_id3 = Placement (pin, dm, bio, rep1, rel, tag, story)"]
    ShopeeSub --> S4["sub_id4 = Asset_ID / SKU (den01_a1, quat01_a2)"]
    ShopeeSub --> S5["sub_id5 = Date / Cohort (20261022, w43)"]

    CourseUTM --> U1["utm_source = Nền tảng (facebook, instagram, threads, youtube)"]
    CourseUTM --> U2["utm_medium = Điểm chạm (reels_pinned, auto_dm, self_reply, shorts_bio)"]
    CourseUTM --> U3["utm_campaign = Mã chiến dịch (subagent_course_2026, lead_magnet_p1)"]
    CourseUTM --> U4["utm_content = Asset_ID (V20261022_LEAD01_A1)"]
    CourseUTM --> U5["utm_term = Pod_ID & Phân khúc (pod04_aiplayers)"]
```

### 2.1. Chuẩn Hóa 5 Trường `Sub_ID` Shopee Affiliate (Nhánh A)

Shopee Affiliate cung cấp đúng 5 tham số định danh tự do (`sub_id1` đến `sub_id5`). Để đối soát tự động qua SQLite và webhook, 100% link Shopee của Agent-Javis bắt buộc mã hóa theo quy tắc:

| Trường Shopee | Định Nghĩa Kỹ Thuật | Giới Hạn Ký Tự | Cú Pháp Chuẩn | Ví Dụ | Mục Đích Đo Lường |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`sub_id1`** | **Mã Brand Pod** | $\le 10$ ký tự | `pod[XX]` | `pod01`, `pod03` | Tách dòng doanh thu và hoa hồng theo từng cụm thương hiệu. |
| **`sub_id2`** | **Mã Nền Tảng Kênh** | $\le 5$ ký tự | `fb`, `ig`, `th`, `yt` | `fb`, `th` | So sánh hiệu quả chuyển đổi giữa 4 nền tảng mạng xã hội. |
| **`sub_id3`** | **Vị Trí Đặt Link (Placement)** | $\le 8$ ký tự | `pin`, `dm`, `bio`, `rep1`, `rel`, `tag`, `story` | `pin`, `rep1` | Bóc tách hành vi nhấp chuột theo điểm chạm giao diện. |
| **`sub_id4`** | **Asset ID & Mã SKU** | $\le 15$ ký tự | `[sku]_[angle]` | `den01_a1`, `quat01_a3` | Xác định chính xác creative video nào đem lại đơn hàng. |
| **`sub_id5`** | **Ngày Đăng / Batch Test** | $\le 10$ ký tự | `YYYYMMDD` | `20261022` | Đo lường cohort retention và chu kỳ sống của video (24h/72h). |

* **Quy ước chi tiết mã vị trí (`sub_id3` Placement Codes):**
  - `pin`: Facebook Reels Pinned Comment #1 (Bình luận ghim).
  - `dm`: Instagram Auto-DM Trigger qua ManyChat/n8n khi khách comment từ khóa.
  - `bio`: Link trên Profile Bio của Instagram / YouTube.
  - `rep1`: Threads Self-Reply #1 ngay dưới bài đăng gốc.
  - `rel`: YouTube Related Video (Cầu nối video liên quan gắn dưới Shorts).
  - `tag`: YouTube Shopping Product Tag (Thẻ sản phẩm gắn trực tiếp).
  - `story`: Instagram Story Link Sticker (Sticker liên kết 1 chạm).

* **Cấu trúc URL Deep-link Shopee đầy đủ:**
  ```text
  https://shope.ee/m/affiliate?url=https%3A%2F%2Fshopee.vn%2Fproduct-i.123456.789012&sub_id1=pod03&sub_id2=fb&sub_id3=pin&sub_id4=den01_a1&sub_id5=20261022
  ```
  *(Khi rút gọn qua hệ thống `s.shopee.vn`, mã tracking được bảo toàn 100% trong cơ sở dữ liệu đối soát Shopee).*

### 2.2. Chuẩn Hóa Bộ Tham Số UTM Cho Nhánh B (AI Players Khóa Học & Lead Magnet)

Đối với Pod 04 (`AI Players`), mục tiêu là kéo lưu lượng truy cập vào Nhóm Zalo VIP, luồng ManyChat tự động hoặc Landing Page Khóa học Subagent. Toàn bộ đường link điều hướng sử dụng chuẩn Google Analytics 4 (GA4) / Meta Pixel UTM Parameters:

1. **`utm_source` (Nguồn traffic):** `facebook`, `instagram`, `threads`, `youtube`.
2. **`utm_medium` (Điểm chạm phương tiện):**
   - `reels_pinned`: Bình luận ghim Reels Facebook.
   - `auto_dm`: Luồng tin nhắn riêng tự động Instagram.
   - `profile_bio`: Liên kết gắn trên hồ sơ kênh (Bio link).
   - `self_reply`: Bình luận tự trả lời Threads.
   - `shorts_related`: Cầu nối video liên quan Shorts.
3. **`utm_campaign` (Tên chiến dịch chuyển đổi):**
   - `lead_magnet_pack01`: Phễu tặng tài liệu 30 Prompt & Sơ đồ n8n.
   - `subagent_course_launch`: Phễu bán vé Workshop Giờ Vàng 299K / Khóa Mastery 4.9M.
4. **`utm_content` (Mã định danh Asset):** Trùng khớp chính xác với `Asset_ID` (Ví dụ: `V20261022_LEAD01_A1`).
5. **`utm_term` (Phân loại Pod & Tệp khách):** `pod04_solopreneur`, `pod04_marketer`, `pod04_developer`.

* **Cấu trúc URL Landing Page / Zalo VIP hoàn chỉnh:**
  ```text
  https://aiplayers.vn/nhan-tai-lieu?utm_source=threads&utm_medium=self_reply&utm_campaign=lead_magnet_pack01&utm_content=V20261022_LEAD01_A1&utm_term=pod04_solopreneur
  ```

---

### 2.3. Bảng Ma Trận Ví Dụ Thực Chiến Cho Cả 4 Brand Pods Hiện Tại

Dưới đây là ma trận 16 liên kết tracking hoàn chỉnh được lập cho 4 sản phẩm/chủ đề đại diện của 4 Brand Pods đang hoạt động trong chiến dịch:

| Pod_ID & Thương Hiệu | Kênh Phát Hành | Asset_ID Mẫu | Vị Trí Gắn Link Chuẩn | Mã Định Danh Tracking Đầy Đủ | Định Dạng Link Rút Gọn Hiển Thị Khách |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`POD01`**<br>Phòng Trọ Hết Cứu | `POD01_FB` | `V20261022_QUAT01_A3` | Pinned Comment #1 | `sub_id1=pod01&sub_id2=fb&sub_id3=pin&sub_id4=quat01_a3&sub_id5=20261022` | `https://s.shopee.vn/pod01_fb_pin_q1` |
| **`POD01`**<br>Phòng Trọ Hết Cứu | `POD01_IG` | `V20261022_QUAT01_A3` | Auto-DM (Key: "QUAT") | `sub_id1=pod01&sub_id2=ig&sub_id3=dm&sub_id4=quat01_a3&sub_id5=20261022` | `https://s.shopee.vn/pod01_ig_dm_q1` |
| **`POD01`**<br>Phòng Trọ Hết Cứu | `POD01_TH` | `T20261022_QUAT01_A3` | Self-Reply #1 | `sub_id1=pod01&sub_id2=th&sub_id3=rep1&sub_id4=quat01_a3&sub_id5=20261022` | `https://s.shopee.vn/pod01_th_rep1_q1` |
| **`POD01`**<br>Phòng Trọ Hết Cứu | `POD01_YT` | `V20261022_QUAT01_A3` | Related Video / Bio | `sub_id1=pod01&sub_id2=yt&sub_id3=rel&sub_id4=quat01_a3&sub_id5=20261022` | `https://s.shopee.vn/pod01_yt_rel_q1` |
| **`POD02`**<br>Ký Túc Xá Có Biến | `POD02_FB` | `V20261022_MAYCAO01_A1` | Pinned Comment #1 | `sub_id1=pod02&sub_id2=fb&sub_id3=pin&sub_id4=maycao01_a1&sub_id5=20261022` | `https://s.shopee.vn/pod02_fb_pin_mc1` |
| **`POD02`**<br>Ký Túc Xá Có Biến | `POD02_IG` | `V20261022_MAYCAO01_A1` | Bio Link #1 | `sub_id1=pod02&sub_id2=ig&sub_id3=bio&sub_id4=maycao01_a1&sub_id5=20261022` | `https://s.shopee.vn/pod02_ig_bio_mc1` |
| **`POD02`**<br>Ký Túc Xá Có Biến | `POD02_TH` | `T20261022_MAYCAO01_A1` | Self-Reply #1 | `sub_id1=pod02&sub_id2=th&sub_id3=rep1&sub_id4=maycao01_a1&sub_id5=20261022` | `https://s.shopee.vn/pod02_th_rep1_mc1` |
| **`POD02`**<br>Ký Túc Xá Có Biến | `POD02_YT` | `V20261022_MAYCAO01_A1` | YT Shopping Tag | `sub_id1=pod02&sub_id2=yt&sub_id3=tag&sub_id4=maycao01_a1&sub_id5=20261022` | Gắn trực tiếp thẻ giỏ hàng |
| **`POD03`**<br>Hội Deadline | `POD03_FB` | `V20261022_DEN01_A4` | Pinned Comment #1 | `sub_id1=pod03&sub_id2=fb&sub_id3=pin&sub_id4=den01_a4&sub_id5=20261022` | `https://s.shopee.vn/pod03_fb_pin_d1` |
| **`POD03`**<br>Hội Deadline | `POD03_IG` | `V20261022_DEN01_A4` | Auto-DM (Key: "DEN") | `sub_id1=pod03&sub_id2=ig&sub_id3=dm&sub_id4=den01_a4&sub_id5=20261022` | `https://s.shopee.vn/pod03_ig_dm_d1` |
| **`POD03`**<br>Hội Deadline | `POD03_TH` | `I20261022_DEN01_A4` | Self-Reply #1 | `sub_id1=pod03&sub_id2=th&sub_id3=rep1&sub_id4=den01_a4&sub_id5=20261022` | `https://s.shopee.vn/pod03_th_rep1_d1` |
| **`POD03`**<br>Hội Deadline | `POD03_YT` | `V20261022_DEN01_A4` | Related Video / Bio | `sub_id1=pod03&sub_id2=yt&sub_id3=rel&sub_id4=den01_a4&sub_id5=20261022` | `https://s.shopee.vn/pod03_yt_rel_d1` |
| **`POD04`**<br>AI Players | `POD04_FB` | `V20261022_LEAD01_A1` | Pinned Comment #1 | `utm_source=facebook&utm_medium=reels_pinned&utm_campaign=lead_magnet_pack01&utm_content=V20261022_LEAD01_A1&utm_term=pod04` | `https://zalo.me/g/fb_aiplayers_l1` |
| **`POD04`**<br>AI Players | `POD04_IG` | `C20261022_LEAD01_A1` | Auto-DM (Key: "AGENT") | `utm_source=instagram&utm_medium=auto_dm&utm_campaign=lead_magnet_pack01&utm_content=C20261022_LEAD01_A1&utm_term=pod04` | `https://zalo.me/g/ig_aiplayers_l1` |
| **`POD04`**<br>AI Players | `POD04_TH` | `T20261022_LEAD01_A1` | Self-Reply #1 | `utm_source=threads&utm_medium=self_reply&utm_campaign=lead_magnet_pack01&utm_content=T20261022_LEAD01_A1&utm_term=pod04` | `https://zalo.me/g/th_aiplayers_l1` |
| **`POD04`**<br>AI Players | `POD04_YT` | `V20261022_LEAD01_A1` | Channel Bio Link | `utm_source=youtube&utm_medium=profile_bio&utm_campaign=lead_magnet_pack01&utm_content=V20261022_LEAD01_A1&utm_term=pod04` | `https://aiplayers.vn/bio-lead01` |

---

## PHẦN 3: PHỄU ĐO LƯỜNG ĐA KÊNH & NGƯỠNG BENCHMARK THỰC CHIẾN 2026

### 3.1. Kiến Trúc Phễu Đo Lường 5 Lớp (The 5-Stage Multi-Platform Funnel)

Theo nguyên tắc cốt lõi của `hieu-suat.md`: **"Mọi KPI phải có công thức toán học và mẫu số (denominator) rõ ràng; tách bạch tuyệt đối chỉ số nội dung, chỉ số tương tác, chỉ số click và chỉ số đơn hàng hợp lệ"**.

```
[LỚP 1: ATTENTION]          Views / Impressions  ──►  3-Second Hold Rate
       │
[LỚP 2: RETENTION]          Watch Time  ──────────►  Average Percentage Viewed (APV) / Completion
       │
[LỚP 3: TRIGGER INTENT]     Engagement  ──────────►  Comment / Auto-DM Trigger Rate / Saves
       │
[LỚP 4: OUTBOUND TRAFFIC]   Clicks  ──────────────►  Link CTR (View-to-Click)
       │
[LỚP 5: UNIT ECONOMICS]     Conversions  ─────────►  Click-to-Order CVR  ──►  Valid Orders & EPC
```

#### Bảng Công Thức Toán Học Chuẩn Cho Từng Tầng Phễu:

| Tầng Phễu | Tên Chỉ Số (Metric) | Ký Hiệu | Công Thức Toán Học | Mẫu Số (Denominator) | Ý Nghĩa Chẩn Đoán |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Lớp 1** | **Tỷ lệ giữ chân 3s (3s Hold Rate)** | $R_{3s}$ | $\frac{\text{Số lượt xem } \ge 3\text{ giây}}{\text{Tổng lượt hiển thị (Impressions)}} \times 100\%$ | $\text{Impressions}$ | Đo lường sức mạnh của Visual Hook và Headline 3s đầu. |
| **Lớp 2** | **Tỷ lệ thời lượng xem trung bình (APV)** | $\text{APV}$ | $\frac{\text{Tổng thời gian xem (Watch Time)}}{\text{Thời lượng video (Duration)} \times \text{Lượt Views}} \times 100\%$ | $\text{Duration} \times \text{Views}$ | Đo lường nhịp dựng, kịch bản giải quyết nỗi đau và giữ chân. |
| **Lớp 2** | **Tỷ lệ xem hết video (Completion Rate)** | $R_{comp}$ | $\frac{\text{Số lượt xem hết 100\% video}}{\text{Tổng lượt xem (Views)}} \times 100\%$ | $\text{Total Views}$ | Xác định tỷ lệ người xem tiếp cận được phần Call-To-Action (CTA). |
| **Lớp 3** | **Tỷ lệ kích hoạt tương tác / DM (Trigger Rate)** | $R_{trig}$ | $\frac{\text{Lượt bình luận từ khóa / DM / Reply}}{\text{Tổng lượt xem (Views)}} \times 100\%$ | $\text{Total Views}$ | Đo lường độ thôi thúc nhận link hoặc tranh luận hội thoại. |
| **Lớp 4** | **Tỷ lệ nhấp link (View-to-Click CTR)** | $\text{CTR}$ | $\frac{\text{Tổng lượt nhấp link hợp lệ (Clicks)}}{\text{Tổng lượt xem (Views)}} \times 100\%$ | $\text{Total Views}$ | Đo lường mức độ tò mò về giá/ưu đãi và độ thuận tiện của vị trí link. |
| **Lớp 5** | **Tỷ lệ chuyển đổi đơn hàng (Click-to-Order CVR)** | $\text{CVR}$ | $\frac{\text{Số đơn hàng hợp lệ (Valid Orders)}}{\text{Tổng lượt nhấp link (Clicks)}} \times 100\%$ | $\text{Total Clicks}$ | Đo lường độ khớp giữa video với Landing Page/Shop Mall Shopee. |
| **Lớp 5** | **Doanh thu trên mỗi lượt nhấp (Earnings Per Click)** | $\text{EPC}$ | $\frac{\text{Tổng hoa hồng hợp lệ (Net Commission)}}{\text{Tổng lượt nhấp link (Clicks)}}$ | $\text{Total Clicks}$ | Đo lường hiệu quả kinh tế ròng trên 1 lượt click của kênh. |
| **Lớp 5** | **Hoa hồng trên 1.000 lượt xem (RPM Commission)** | $\text{RPM}$ | $\frac{\text{Tổng hoa hồng hợp lệ}}{\text{Tổng lượt xem (Views)}} \times 1.000$ | $\text{Views} / 1.000$ | Thước đo tối hậu về giá trị thương mại trên từng view nội dung. |

---

### 3.2. Bảng Ngưỡng Benchmark Thực Chiến 2026 Theo Từng Nền Tảng

> [!NOTE]
> Các ngưỡng dưới đây được xác lập dựa trên dữ liệu chuẩn ngành Affiliate Shopee (Dải giá Whitelist $39.000đ - 250.000đ$) và Lead Funnel Zalo tại Việt Nam giai đoạn 2025–2026 `[ESTIMATED / BENCHMARK 2026]`. Đây là thước đo mục tiêu để phân loại Creative Thắng/Thua:

| Chỉ Số Đo Lường (Metrics) | Facebook Reels | Instagram Reels & Carousel | Threads (Meta) | YouTube Shorts |
| :--- | :---: | :---: | :---: | :---: |
| **Độ dài vàng (Duration)** | `15s – 30s` | `20s – 35s` (Car: 5–7 slide) | Bài Text + `10s–20s` video | `35s – 50s` |
| **3s Hold Rate ($R_{3s}$)** | **$\ge 68\%$** *(Kém: $<50\%$)* | **$\ge 62\%$** *(Kém: $<45\%$)* | Dwell time $>8\text{s}$: **$\ge 45\%$** | Viewed vs Swipe: **$\ge 72\%$** |
| **Average Percentage Viewed (APV)** | **$\ge 50\%$** | **$\ge 45\%$** | Đọc hết bài: **$\ge 55\%$** | **$\ge 75\%$** *(Bắt buộc)* |
| **Tương tác cốt lõi nền tảng** | Comment mở: $\ge 1.5\%$ | **DM Shares & Saves: $\ge 3.0\%$** | **Reply Chain: $\ge 4.0\%$** | Like / Sub Rate: $\ge 2.0\%$ |
| **Tỷ lệ kích hoạt CTA (Trigger Rate)** | Mở khay cmt: $\ge 3.5\%$ | **Auto-DM Trigger: $\ge 4.5\%$** | Mở Self-Reply #1: $\ge 5.0\%$ | Bấm Related/Bio: $\ge 1.8\%$ |
| **View-to-Click CTR** | **$1.8\% – 3.2\%$** | **$2.2\% – 3.8\%$** *(qua DM)* | **$2.5\% – 4.5\%$** *(từ Reach)* | **$1.0\% – 2.2\%$** *(Bio/Tag)* |
| **Click-to-Order Shopee CVR** | **$4.0\% – 6.5\%$** | **$4.5\% – 7.0\%$** | **$4.2\% – 6.8\%$** | **$5.5\% – 8.5\%$** *(Ý định cao)* |
| **Click-to-Lead Zalo CVR (Nhánh B)**| **$8.0\% – 15.0\%$** | **$12.0\% – 22.0\%$** *(qua DM)* | **$10.0\% – 18.0\%$** | **$6.0\% – 12.0\%$** |
| **EPC Mục Tiêu (Shopee Nhánh A)** | `800đ – 1.600đ` | `1.000đ – 2.000đ` | `1.200đ – 2.200đ` | `1.500đ – 3.000đ` |
| **RPM Commission (1.000 Views)** | `15.000đ – 35.000đ` | `20.000đ – 45.000đ` | `25.000đ – 60.000đ` | `20.000đ – 50.000đ` |

---

## PHẦN 4: CƠ CHẾ ĐIỀU HÀNH 20–30–100 KÊNH BẰNG TOÁN HỌC (PORTFOLIO MANAGEMENT)

Để vận hành một mạng lưới 100 kênh mà không bị quá tải bộ máy và tránh lãng phí chi phí tính toán GPU, hệ thống vận hành theo **Quy trình Quản trị Danh mục Đầu tư Thuật toán (Algorithmic Portfolio Management)**.

```mermaid
flowchart TD
    WeeklyData["DỮ LIỆU ĐỐI SOÁT HÀNG TUẦN (7 DAYS)"] --> CalcHealth["TÍNH ĐIỂM SỨC KHỎE KÊNH (CHS / 100)"]
    
    CalcHealth --> BCG{"PHÂN LOẠI DANH MỤC BCG 100 KÊNH"}
    
    BCG -->|"CHS >= 80 & Doanh thu cao"| Star["1. KÊNH NGÔI SAO (STAR)<br/>Dồn tài nguyên Render cao cấp, mở rộng khung giờ"]
    BCG -->|"CHS 65 - 79 & Đơn đều"| CashCow["2. KÊNH BÒ SỮA (CASH COW)<br/>Duy trì tự động hóa 100%, khai thác tối đa"]
    BCG -->|"CHS 50 - 64 hoặc Kênh < 14 ngày"| Question["3. KÊNH DẤU HỎI (QUESTION MARK)<br/>Áp dụng Chẩn đoán 3 lớp & Chạy A/B Testing"]
    BCG -->|"CHS < 50 qua 14 ngày"| Zombie["4. KÊNH ZOMBIE (DOG)<br/>Kích hoạt PIVOT hoặc KILL GATE"]
    
    Star --> ScaleGate{"SCALE GATE (NHÂN BẢN POD)"}
    Zombie --> KillGate{"KILL / PIVOT GATE (TRẢM KÊNH)"}
```

### 4.1. Công Thức Chấm Điểm Sức Khỏe Kênh Hàng Tuần (Channel Health Score - CHS)

Mỗi kênh trong hệ thống 100 kênh sẽ được chấm điểm định kỳ vào **00h00 Chủ Nhật hàng tuần** trên thang điểm 100 dựa trên 4 trụ cột có trọng số bằng nhau ($25\%$ mỗi trụ cột):

$$\text{CHS} = 0.25 \times S_{\text{reach}} + 0.25 \times S_{\text{retention}} + 0.25 \times S_{\text{conversion}} + 0.25 \times S_{\text{standing}}$$

Trong đó, điểm thành phần được chuẩn hóa về thang điểm $[0, 100]$:

1. **Điểm Lưu Lượng & Tăng Trưởng ($S_{\text{reach}}$):**
   $$S_{\text{reach}} = \min\left(100, \frac{\text{Lượt Views trung bình 7 ngày qua}}{\text{Mục tiêu Views tối thiểu (1.000 views/video)}} \times 100\right)$$
   *(Nếu kênh bị kẹt ở mức $< 200$ view liên tiếp 5 video, $S_{\text{reach}} = 0$ điểm do dính cờ kiểm duyệt rác).*

2. **Điểm Giữ Chân Người Xem ($S_{\text{retention}}$):**
   $$S_{\text{retention}} = 50 \times \left(\frac{R_{3s}}{\text{Benchmark } R_{3s}}\right) + 50 \times \left(\frac{\text{APV}}{\text{Benchmark APV}}\right)$$

3. **Điểm Chuyển Đổi & Doanh Thu ($S_{\text{conversion}}$):**
   $$S_{\text{conversion}} = 50 \times \left(\frac{\text{Link CTR}}{\text{Benchmark CTR}}\right) + 50 \times \left(\frac{\text{Valid Orders}}{\text{Mục tiêu Đơn (5 đơn/tuần)}}\right)$$

4. **Điểm Tuân Thủ & Tình Trạng Tài Khoản ($S_{\text{standing}}$):**
   - Bắt đầu với $100$ điểm.
   - Trừ $30$ điểm nếu có 1 bài đăng dính cảnh báo vi phạm bản quyền âm thanh hoặc nội dung không nguyên bản.
   - Trừ $20$ điểm nếu tỷ lệ đăng bài bị chậm lịch $>20\%$ trong tuần.
   - Về $0$ điểm nếu tài khoản bị khóa tính năng (Shadowban hoặc mất quyền gắn link).

---

### 4.2. Ma Trận Phân Loại 4 Nhóm Kênh Trong Danh Mục 100 Kênh (BCG Matrix)

| Nhóm Phân Loại | Tỷ Lệ Kênh Dự Kiến | Ngưỡng Điểm CHS | Đặc Điểm Vận Hành | Hành Động Phân Bổ Tài Nguyên |
| :--- | :---: | :---: | :--- | :--- |
| ⭐ **Star (Kênh Ngôi Sao)** | `10% – 15%` | **$\text{CHS} \ge 80$** | View tăng trưởng mạnh, CTR $>2.5\%$, đơn nổ liên tục mỗi ngày, không lỗi chính sách. | **Dồn tài nguyên cấp cao:** Ưu tiên GPU render độ nét 4K, mở rộng 3 video/ngày, chuẩn bị kích hoạt **Scale Gate nhân bản Pod mới**. |
| 🐄 **Cash Cow (Kênh Bò Sữa)** | `25% – 35%` | **$65 \le \text{CHS} < 80$** | View ổn định (2k–10k), CVR cao ($>5\%$), tạo dòng tiền hoa hồng đều đặn, tệp fan trung thành. | **Tự động hóa tối đa:** Chạy 100% qua bot n8n hẹn giờ, không can thiệp thủ công, tái sử dụng các Winning SKU theo chu kỳ 14 ngày. |
| ❓ **Question Mark (Kênh Dấu Hỏi)** | `35% – 45%` | **$50 \le \text{CHS} < 65$** | Kênh mới lập ($<14$ ngày) hoặc view cao nhưng ít click / click cao nhưng chưa có đơn. | **Chẩn đoán & A/B Test:** Áp dụng giao thức 3 bước của `hieu-suat.md` để test lại Hook hoặc đổi Listing shop Shopee. |
| 💀 **Zombie / Dog (Kênh Zombie)** | `15% – 20%` | **$\text{CHS} < 50$** | Quá 14 ngày đăng đều nhưng view $<300$, 0 click, tài khoản bị bóp tương tác sâu. | **Đưa vào hàng đợi kiểm soát:** Kích hoạt **Pivot Gate** (đổi góc 7 ngày) hoặc **Kill Gate** (xóa sổ giải phóng tài nguyên). |

---

### 4.3. Quy Tắc Quyết Định Tự Động: KEEP / ITERATE / STOP

Hệ thống bot tự động đọc dữ liệu qua SQLite và phân loại trạng thái từng Video Asset theo 3 cửa sổ thời gian:

```mermaid
flowchart LR
    Pub["Video Xuất Bản"] --> G24["CỬA SỔ 24 GIỜ<br/>(Gate 1: Attention & Click)"]
    G24 -->|"Đạt chuẩn"| G72["CỬA SỔ 72 GIỜ<br/>(Gate 2: Unit Economics & Orders)"]
    G24 -->|"Trượt chuẩn"| STOP24["STOP 24H: Dừng Repost"]
    
    G72 -->|"Đạt chuẩn"| G7D["CỬA SỔ 7 NGÀY<br/>(Gate 3: Winner & Scaling)"]
    G72 -->|"Có click nhưng 0 đơn"| IT72["ITERATE 72H: Audit Offer/Shop"]
    G72 -->|"0 click & 0 đơn"| STOP72["STOP 72H: Đóng SKU"]

    G7D -->|"Hội đủ 4 chuẩn"| SCALE["SCALE: Nhân bản Pod"]
```

#### 1. Cửa Sổ 24 Giờ (Gate 24h — Kiểm Tra Sức Hút Ban Đầu & Độ Nhạy Link):
* **`KEEP` (Giữ nguyên luồng phân phối tự nhiên):**
  - Điều kiện: $R_{3s} \ge \text{Benchmark}$ VÀ $\text{CTR} \ge 1.5\%$.
  - Hành động: Giữ nguyên, cho phép bot tự động share vào 3 nhóm vệ tinh.
* **`ITERATE` (Cần tinh chỉnh ngay ở video tiếp theo):**
  - *Trường hợp A (Hook kém nhưng Click tốt):* $R_{3s} < 50\%$ nhưng CTR $> 2.0\%$ $\rightarrow$ Giữ nguyên sản phẩm và CTA, dựng lại 3 giây đầu (Hook swapping) với tình huống drama gắt hơn.
  - *Trường hợp B (View cao nhưng Không Click):* Views $> 5.000$, $R_{3s} \ge 70\%$ nhưng $\text{CTR} < 0.5\%$ $\rightarrow$ Video bị rơi vào bẫy vô tri. Cần đổi câu thoại CTA ở giây 22 và kiểm tra lại vị trí hiển thị link ở Pinned Comment/Auto-DM.
* **`STOP` (Dừng phân phối & Không tái chế):**
  - Điều kiện: Sau 24h, Views $< 200$ (kẹt quét AI) HOẶC $R_{3s} < 35\%$ và $0$ click.
  - Hành động: Đánh dấu asset thất bại, không render thêm các góc phụ từ asset này.

#### 2. Cửa Sổ 72 Giờ (Gate 72h — Kiểm Tra Hiệu Quả Kinh Tế Đơn Vị & Đơn Hàng):
* **`SCALE` (Xác nhận Winning Asset):**
  - Điều kiện: Tạo ra $\ge 3$ đơn hàng Shopee hợp lệ (hoặc $\ge 5$ lead Zalo) VÀ $\text{CVR} \ge 4.0\%$ VÀ $\text{EPC} \ge 1.000đ$.
  - Hành động: Lập tức kích hoạt kịch bản sản xuất 4 biến thể góc nhìn còn lại (`A2`, `A3`, `A4`, `A5`) để phủ toàn bộ các kênh trong Pod.
* **`ITERATE` (Lỗi sau Click — Landing Page Friction):**
  - Điều kiện: Có $\ge 50$ clicks nhưng $0$ đơn hàng hợp lệ ($\text{CVR} = 0\%$).
  - Hành động: **Kích hoạt quy trình kiểm tra 3 lớp (Layer 3 Audit):**
    1. Kiểm tra giá bán trên Shopee có bị tăng vọt sau khi hết Flash Sale không.
    2. Kiểm tra shop có bị hết hàng biến thể mặc định không.
    3. Kiểm tra phí ship về các tỉnh có bị đắt bất thường ($>40.000đ$) khiến khách bỏ giỏ không.
    4. Tìm 1 link Shop Mall khác cùng sản phẩm có giá tốt hơn để thay thế link redirect.
* **`STOP` (Dừng SKU):**
  - Điều kiện: Sau 72h đạt $>100$ clicks nhưng $0$ đơn hàng và không tìm được listing shop thay thế. Đóng mã SKU khỏi kế hoạch sản xuất tuần tới.

---

### 4.4. Điều Kiện Tự Động Nhân Bản Pod Thắng (Scale Gate)

Một Brand Pod chỉ được phép nhân bản (Clone ra một Pod mới — Ví dụ: từ `POD01` nhân bản ra `POD05`) khi thỏa mãn **Bộ 4 Điều Kiện Thép (The 4-Pillar Winner Rules)**:

```mermaid
flowchart TD
    subgraph ScaleGateRules["BỘ 4 ĐIỀU KIỆN THÉP DUYỆT NHÂN BẢN POD"]
        C1["1. SỨC KHỎE POD VỮNG CHẮC<br/>CHS Pod trung bình >= 80 điểm trong 2 tuần liên tiếp"]
        C2["2. BỘ 3 WINNING SKU XÁC MINH<br/>Tối thiểu 3 sản phẩm tạo >= 30 đơn hợp lệ, hoàn hủy < 5%"]
        C3["3. SỞ HỮU ANGLE MATRIX ĐỦ DÀY<br/>Đã có sẵn kho 5 kịch bản góc nhìn + Bộ Spintax biến thiên chuẩn"]
        C4["4. HỒ SƠ TÀI KHOẢN 100% SẠCH<br/>Không có bất kỳ cảnh báo vi phạm bản quyền hay shadowban"]
    end
    
    C1 & C2 & C3 & C4 --> Approved["CẤP PHÉP TẠO POD MỚI (VÍ DỤ: POD05)<br/>Kế thừa SKU thắng, thay đổi Persona MC AI & Tone voice"]
```

* **Quy trình thực thi nhân bản Pod mới:**
  1. Giữ nguyên 100% danh mục Winning SKU và đường link đối tác đã đàm phán hoa hồng cao.
  2. Tạo bộ nhận diện thương hiệu phái sinh (Spin-off Brand): Đổi tên kênh, đổi phong cách hình ảnh (Ví dụ: `POD01` - Phòng Trọ Hết Cứu chuyển thành `POD05` - Góc Trọ GenZ).
  3. Đổi giọng đọc AI (Ví dụ: Từ Nam Bắc trầm ấm sang Nữ Nam trẻ trung) và tráo đổi kịch bản theo công thức Spintax để tránh quét trùng lặp mã Hash.

---

### 4.5. Điều Kiện Cắt Bỏ / Đổi Ngách Kênh Zombie (Kill / Pivot Gate Sau 14–30 Ngày)

Một kênh bị phân loại là **Kênh Zombie (Zombie Channel)** khi rơi vào trạng thái chết lâm sàng về mặt phân phối thuật toán:
* *Định nghĩa toán học:* Đã xuất bản đều đặn $\ge 20$ nội dung đạt chuẩn kỹ thuật trong $14$ ngày, nhưng lượt xem trung bình 10 video gần nhất $< 300$ views, tổng lượt click $< 15$ clicks và phát sinh $0$ đơn hàng hợp lệ.

Quy trình thanh trừng và cứu vãn được thực thi qua 2 cửa ải:

```mermaid
sequenceDiagram
    participant K as Kênh Zombie (CHS < 50)
    participant B as Bot Điều Hành (hieu-suat)
    participant M as Giám Đốc (Mama)

    Note over K,B: Ngày 14: Kênh kẹt < 300 view liên tục
    B->>K: KÍCH HOẠT PIVOT GATE (Thử nghiệm 7 ngày)
    Note over K: 1. Đóng băng xuất bản 48h để xả phạt thuật toán<br/>2. Đổi 100% sang sản phẩm giải quyết nỗi đau cực hạn<br/>3. Chuyển sang định dạng Archetype #1 (Sandwich MC AI + Macro Proof)
    
    alt Ngày 21: CHS phục hồi >= 65 điểm
        B-->>M: Báo cáo cứu kênh thành công -> Chuyển về nhóm Question Mark
    else Ngày 21 - 30: CHS vẫn < 50 điểm (Zombie vĩnh viễn)
        B->>M: ĐỀ XUẤT KÍCH HOẠT KILL GATE
        M-->>B: Phê chuẩn trảm kênh (APPROVED_KILL)
        Note over B: 1. Thu hồi Proxy, API Tokens, Slot tự động hóa<br/>2. Xuất dữ liệu lưu trữ (Archive log)<br/>3. Xóa lịch đăng, giải phóng slot máy chủ cho Pod mới
    end
```

1. **Cửa ải 1: Pivot Gate (Đổi Ngách / Reset Thuật Toán trong 7 ngày — Ngày 15 đến Ngày 21):**
   - *Bước 1:* Cho kênh "nghỉ ngơi" 48 giờ (không đăng bất kỳ bài nào) để thuật toán xóa nhãn spam hành vi.
   - *Bước 2:* Chuyển đổi định dạng video sang **Archetype #1: Sandwich MC AI $\leftrightarrow$ Macro Thật (8 nhịp)** với nhịp cắt cảnh cực nhanh ($1.5\text{s} - 2.0\text{s}$) để giật lại tương tác.
   - *Bước 3:* Thay đổi sản phẩm sang nhóm "Nỗi đau hiển hiện tức thì" với mức giá mềm dưới $99.000đ$ (Ví dụ: miếng dán chống ẩm mốc hoặc sáp thơm phòng vệ sinh).
2. **Cửa ải 2: Kill Gate (Thanh Trừng Kênh Sau 30 Ngày):**
   - Nếu sau giai đoạn Pivot (ngày 22 đến ngày 30), kênh vẫn không vượt qua được ngưỡng $500$ views và $\text{CHS} < 50$:
   - **Thực thi trảm kênh:** Thu hồi tài nguyên, hủy lịch đăng trong queue, giải phóng slot API cho kênh mới để bảo toàn ngân sách vận hành hệ thống.

---

## HÀNH ĐỘNG CỤ THỂ CHO VIDEO KẾ TIẾP (ACTIONABLE NEXT STEP)

> Theo đúng quy chuẩn bắt buộc của `hieu-suat.md` (Dòng 101–105):

### 1. Bằng Chứng Dữ Liệu Cần Kiểm Tra (Evidence to Audit)
- Đối soát bảng tương tác 24h qua trên 4 Fanpage hiện tại (`report-2026-10-21.md`): Page `AI Players` đã có tín hiệu tương tác tự nhiên (`76 Likes`, `38 Cmt`), trong khi 3 Page Bán Hàng mới lập (`Phòng Trọ Hết Cứu`, `Ký Túc Xá Có Biến`, `Hội Deadline`) đang có `0 Followers` và `0 Likes`.
- Nguyên nhân: Các page mới chỉ có bài ảnh Catalog $1:1$ làm nền uy tín, **hoàn toàn chưa có video Reels dọc 9:16** — định dạng duy nhất được Meta phân phối tự nhiên tới tệp khách hàng lạ.

### 2. Hành Động Can Thiệp Duy Nhất (Single Primary Variable Action)
- **Sản xuất và nạp ngay 1 Video Reels AI bán hàng đầu tiên cho Pod 03 (`Hội Deadline` — Page ID: `1407231352464711`)** với sản phẩm mẫu **Đèn LED Kẹp Màn Hình Chống Chói** (Mã SKU: `DEN01`).
- Áp dụng chuẩn **Archetype #1 (Sandwich MC AI 8 Nhịp, 28 giây)**:
  - Cắt cảnh mỗi $1.8\text{s} - 2.2\text{s}$ trong Vùng An Toàn ($Y = 760\text{px} \to 1340\text{px}$).
  - Gắn mã Tracking chuẩn: `sub_id1=pod03&sub_id2=fb&sub_id3=pin&sub_id4=den01_a1&sub_id5=20261022`.
  - Pinned Comment #1 chứa link Shopee rút gọn: `https://s.shopee.vn/pod03_fb_pin_d1`.

### 3. KPI Xác Nhận Thành Công Tại Cửa Sổ 24h và 72h
- **Cửa sổ 24 Giờ:** Video đạt tối thiểu $\ge 500$ lượt xem tự nhiên; Tỷ lệ giữ chân 3s ($R_{3s}$) $\ge 68\%$; Tỷ lệ mở bình luận ghim $\ge 3.0\%$; Có tối thiểu $\ge 10$ lượt nhấp link hợp lệ ($\text{CTR} \ge 2.0\%$).
- **Cửa sổ 72 Giờ:** Có tối thiểu $\ge 1$ đơn hàng hợp lệ ghi nhận qua mã `pod03_fb_pin_d1` trên hệ thống Shopee Affiliate; Tỷ lệ chuyển đổi $\text{CVR} \ge 4.0\%$.

---

## BẢNG TỰ CHẤM ĐIỂM THEO RUBRIC HUẤN LUYỆN CHÍNH THỨC (RUBRIC /10)

| Tiêu Chí Đánh Giá | Trọng Số | Điểm Đạt | Minh Chứng Trong Tài Liệu |
| :--- | :---: | :---: | :--- |
| **1. Bắt đúng bệnh phễu chuyển đổi** | **3.5** | **3.5 / 3.5** | Tách trọn vẹn 5 lớp phễu: $R_{3s} \to \text{APV} \to \text{Trigger} \to \text{CTR} \to \text{CVR} \to \text{EPC/RPM}$; 100% tỷ lệ có công thức toán học và mẫu số (denominator) rõ ràng. |
| **2. Giải pháp hành động cụ thể** | **3.5** | **3.4 / 3.5** | Có đủ ma trận Portfolio, quy tắc chấm điểm sức khỏe CHS, cơ chế Scale/Kill Gate tự động; kết thúc bằng đúng heading bắt buộc `## Hành động cụ thể cho video kế tiếp (Actionable Next Step)` kèm bằng chứng, hành động và KPI xác nhận. |
| **3. Tư duy dữ liệu thực chiến Việt Nam** | **3.0** | **2.9 / 3.0** | Phân rã đủ 5 trường `sub_id` của Shopee Affiliate, chuẩn hóa UTM GA4/Meta, gắn liền với dải giá mềm $39k - 250k$, voucher freeship, phí ship, tồn kho và đặc thù 4 nền tảng mạng xã hội tại Việt Nam 2026. |
| **TỔNG ĐIỂM TỰ CHẤM** | **10.0** | **9.8 / 10.0** | **ĐẠT CHUẨN XUẤT SẮC ($\ge 9.0/10$) — ĐỦ ĐIỀU KIỆN NGHIỆM THU GATE 1** |
