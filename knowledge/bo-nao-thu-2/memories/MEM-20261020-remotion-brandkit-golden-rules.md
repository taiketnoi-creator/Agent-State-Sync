# MEM-20261020-remotion-brandkit-golden-rules — Bộ 5 Quy Tắc Vàng Dựng Video Remotion Brand-Kit (Đã Nghiệm Thu Cùng CEO)

- **ID:** `MEM-20261020-remotion-brandkit-golden-rules`
- **Loại:** `decision`
- **Trạng thái:** `VALIDATED`
- **Ngày chốt:** `2026-10-20`
- **Nguồn phê duyệt:** CEO nghiệm thu trực tiếp qua thực chiến video `ai-hallucination-45s.mp4` (`templates/remotion-cuongit-template/src/AiHallucinationShort/`)
- **Phạm vi áp dụng:** Toàn bộ video dạng giải thích công nghệ, tin tức AI, quy trình AI (`REMOTION_EXPLAINER` / Video Slide thế hệ mới) của đội `Agent-Javis`.

---

## Nội dung Quyết định & 5 Quy Tắc Cốt Lõi

1. **Màu Chữ Tiêu Đề & Tài Nguyên `public/brand-kit/`:**
   - Màu tiêu đề chính (`headingPrimary`), điểm nhấn icon và từ khóa highlight trong phụ đề khóa cứng ở mã màu **`#87ff00`**. Các màu chữ khác giữ nguyên (`#FFFFFF` / `text-white/90`).
   - Hình nền nạp từ `brand-kit/bg/BG-video-motion.jpg` (giữ nguyên độ rực rỡ 100%, không phủ lớp đen làm tối nền, có hiệu ứng thở Ken Burns nhẹ và quầng sáng trôi nổi).
   - Nhạc nền: `brand-kit/bgm/1.The Violins.mp3` (`volume={0.10}`).
   - SFX: `brand-kit/sfx/apple-pay-sound.mp3` (`volume={0.26}`) khi chuyển cảnh và `brand-kit/sfx/discord-notification.mp3` (`volume={0.22}`) khi bật thẻ Card.

2. **Khung Kính Trong Suốt (`Transparent Frosted Glass` — Cấm Khung Đen):**
   - Bỏ hoàn toàn các khung nền đen `bg-slate-900/90` hay `bg-slate-950`.
   - Toàn bộ thẻ Card chính dùng kính trong suốt `bg-white/[0.08] border border-white/30 backdrop-blur-md`; thẻ con bên trong dùng `bg-white/[0.10] border border-white/25 backdrop-blur-sm`.

3. **Sáng Tạo Liên Tục & Cấm Gò Bó Vào 1 Format Cố Định (`Anti-Clone & Free Creative Format`):**
   - **Chỉ giữ cố định Brand Shell** (nền xanh `BG-video-motion.jpg` tĩnh + 2 Neon Orbs, màu nhấn `#87ff00`, chất liệu kính mờ `backdrop-blur-md`, `BrandHeader` và `SubtitleBox` 1 dòng không khung).
   - **Không gò bó vào 1 format hay 6 cảnh cứng nhắc:** Số lượng cảnh, nhịp độ cắt cảnh, bố cục đồ họa và hiệu ứng chuyển động (Orbital Map, Bento Grid, Live Code Terminal, Bio-Scanner ECG, LIDAR HUD, DNA Helix, Timeline, La bàn...) phải **sáng tạo liên tục và biến hóa linh hoạt 100% theo mạch nội dung của từng bài**, tuyệt đối cấm copy-paste bố cục từ video trước sang video sau.

4. **Phụ Đề Trượt Từ Dưới Lên — Không Khung Bao, Khóa 1 Dòng & Chuẩn Cụm Nghĩa Tiếng Việt:**
   - Không dùng khung viền hay icon loa bao quanh phụ đề.
   - Hiệu ứng trượt nguyên cụm từ dưới lên (`translateY: 36px -> 0px`), khóa cứng 1 dòng duy nhất (`whitespace-nowrap`).
   - Chia cụm 3–7 từ theo đúng mệnh đề dấu câu tiếng Việt (`phrases: string[]` trong `audioData.ts`) và bảo vệ từ ghép 2 âm tiết (`COMPOUND_PAIRS`), tuyệt đối không cắt đôi từ ghép hay để rớt 1 chữ lẻ xuống dòng.

5. **Voiceover Vbee AIVoice Thuần Việt Mượt 100%:**
   - Viết lời thoại thuần Việt (không dùng chữ viết tắt tiếng Anh gạch nối), kết hợp từ điển phiên âm `TECH_PHONETIC_RULES` và gỡ bỏ `silenceremove` khỏi FFmpeg để giữ trọn âm đuôi tự nhiên của giọng đọc Vbee.
