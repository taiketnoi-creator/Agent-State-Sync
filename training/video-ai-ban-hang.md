# Training thực chiến — Video AI Bán Hàng

## Mục tiêu và phạm vi

**Video AI Bán Hàng** là tên chuẩn của đội cho video sản phẩm/affiliate dọc `9:16` được tạo một phần bằng Veo hoặc công cụ tạo video AI tương đương. Veo tạo các cảnh minh hoạ ngắn; hậu kỳ chịu trách nhiệm cho chữ, logo, caption, voice, nhạc, SFX, CTA và disclosure. Cảnh AI không phải bằng chứng thử nghiệm sản phẩm thật.

## Ranh giới format & Phân tách công cụ — hard gate

**Video AI Bán Hàng không phải Video Explainer và sử dụng bộ công cụ tạo video hoàn toàn khác nhau:**
- **Công cụ tạo hình ảnh/video gốc:** Bắt buộc tạo bằng phần mềm sinh Video AI chuyển động thật (**Google Veo / Kling / Runway**).
- **Giới hạn vai trò của Remotion trong Video AI Bán Hàng:** Trong định dạng này, **Remotion CHỈ ĐƯỢC SỬ DỤNG ĐỂ TẠO TEXT (Kinetic Text Overlay, nhãn disclosure, CTA)** phủ lên trên các clip video AI đã có và ghép track âm thanh.
- **Cấm dùng lẫn công cụ của Video Explainer:** Tuyệt đối không dùng Remotion để dựng slide/card, background tĩnh, hay pan/zoom ảnh AI tĩnh để thay thế các clip chuyển động do Veo/image-to-video tạo. Mọi video explainer/kiến thức công nghệ phải được sản xuất độc lập bằng `templates/remotion-cuongit-template`.

Điều kiện tối thiểu trước khi mở project hậu kỳ:

- Có ít nhất 4 video clip nguồn độc lập dạng `.mp4`/`.mov`, mỗi clip có chuyển động nội cảnh thật theo thời gian; không tính chuyển động tạo bằng cách scale/translate một ảnh tĩnh.
- Các beat Hook, tình huống, hero/demo và payoff phải có video clip nguồn. Ảnh tĩnh chỉ được dùng làm reference khi generate hoặc insert hỗ trợ tối đa 2 giây toàn video, không được chiếm một shot cốt lõi.
- Tối thiểu 80% thời lượng hình phải là footage chuyển động. Motion graphic, caption và CTA là lớp hậu kỳ, không được tính vào tỷ lệ này.
- Asset manifest phải ghi `asset_type=generated_video|licensed_footage|real_footage`, công cụ tạo, prompt/reference, thời lượng và shot sử dụng. `generated_image` không đủ điều kiện làm footage chính.
- Remotion/CapCut/Premiere chỉ ghép clip và làm hậu kỳ. Không được biến một bộ ảnh thành video rồi gắn nhãn Video AI Bán Hàng.

Nếu chưa có quyền truy cập Veo/image-to-video hoặc chưa có đủ clip nguồn, trả `BLOCKED_MISSING_MOTION_ASSETS`. Được phép bàn giao storyboard/prompt pack nhưng phải ghi rõ `PREPRODUCTION_ONLY`; tuyệt đối không render slideshow thay thế và không báo đã tạo video hoàn chỉnh.

Agent áp dụng: `mkt`, `content`, `edit`, `voice`; `mama` giữ các gate bàn giao. Tài liệu nguồn ban đầu: `D:\Phiên bản Ai agent\New Text Document.txt`, tiếp nhận ngày 2026-10-14.

## Luồng bắt buộc

1. `mkt` khóa đúng SKU/biến thể và tạo Product Truth Pack + claim ledger.
2. `content` viết kịch bản 20–35 giây, 4–6 shot, chỉ dùng claim đã xác minh.
3. `edit` tạo continuity bible, reference manifest, prompt pack và dựng hậu kỳ.
4. `voice` tạo một track voice-over tiếng Việt, caption và cue sheet âm thanh.
5. `mama` duyệt SKU → claim → script → visual/audio → pre-publication gate.

Không cho cùng một agent tự chọn SKU, tự tạo proof, tự xuất bản và tự chấm kết quả.

## Product Truth Pack và claim ledger

Trước khi viết kịch bản phải có:

- SKU, biến thể, link/anchor, ảnh sản phẩm thật và ngày kiểm tra.
- Ảnh tổng thể cùng ảnh chi tiết nắp, tay cầm, nút/bảng điều khiển nếu có.
- Claim, nguồn, SKU áp dụng, ngày kiểm tra và trạng thái `VERIFIED / UNKNOWN / NEEDS_EVIDENCE`.
- Giá, tồn kho, bảo hành và tính năng biến động phải kiểm tra lại sát thời điểm đăng.
- Claim thiếu nguồn phải bị bỏ hoặc đánh dấu `BLOCKED_BY_EVIDENCE`; không biến thành trải nghiệm cá nhân hay testimonial.

## Cấu trúc kịch bản và shot

Mặc định dùng 20–35 giây, 4–6 shot:

1. Hook: nêu vấn đề cụ thể trong 0–2 giây.
2. Recognition/Pain: tình huống đời thường được minh hoạ bằng AI.
3. Hero: sản phẩm đúng SKU xuất hiện rõ ràng.
4. Demo: một thao tác đơn giản trong một shot.
5. Trust: một lợi ích đã xác minh và một limitation/tiêu chí chọn.
6. CTA: một hành động, đúng link/anchor sản phẩm.

Mỗi clip Veo chỉ có một hành động chính. Generate clip 4/6/8 giây khi phù hợp rồi cắt thành shot ngắn ở hậu kỳ. Không để talking-head chiếm phần lớn thời lượng và không dùng cảnh nguy hiểm/lửa/khói để ngầm khẳng định an toàn tuyệt đối.

## Continuity bible

Khóa trước khi generate:

- Nhân vật: khuôn mặt, tuổi, tóc, trang phục và hành vi.
- Sản phẩm: hình học, tỷ lệ, màu, thân, nắp, tay cầm, nút, màn hình và vị trí chi tiết.
- Bối cảnh: mặt bàn/bếp, đạo cụ, ánh sáng, hướng bóng và camera language.
- Món ăn: một công thức, nguyên liệu, lượng, độ chín và trạng thái hợp lý xuyên suốt.

Ưu tiên image-to-video với ảnh tham chiếu đúng SKU. Tách thao tác phức hợp như mở nắp, khuấy và bấm nút thành các clip riêng. Mỗi Motion Prompt phải bằng tiếng Anh, có timeline, camera, ánh sáng, temporal behavior, negative constraints và khóa:

`Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing`

## Việc không giao cho Veo

- Không sinh text, giá, logo, UI, bảng điều khiển, badge bảo hành hoặc CTA trong hình.
- Không phụ thuộc thoại/lip-sync dài do Veo tạo; mặc định visual không thoại.
- Không dùng macro AI, hơi nước, món ăn hoặc before/after AI làm proof hiệu quả.
- Không dùng người nổi tiếng, deepfake, clone voice, mascot/footage/nhạc chưa có quyền.

Các phần trên được thêm ở Remotion, CapCut hoặc Premiere bằng asset đã xác minh. Dùng một track voice-over tiếng Việt xuyên suốt; caption phải đọc được khi tắt tiếng. Hiển thị rõ `Minh hoạ bằng AI`; nếu có link/giỏ hàng, thêm disclosure affiliate phù hợp.

## QA frame-by-frame

Xem toàn video ở tốc độ thường, sau đó rà đầu–giữa–cuối và frame chuyển tiếp của từng shot:

- Face/hands: không đổi mặt, thừa ngón, xuyên vật thể hoặc chuyển động phi tự nhiên.
- Product: không drift SKU, méo tỷ lệ, đổi nắp/nút/tay cầm/logo hay tự thêm bộ phận.
- Food: không đổi món, nguyên liệu, lượng hoặc độ chín vô lý.
- Scene: không nhảy đạo cụ/ánh sáng/background, không vật thể nổi hay nhân bản.
- Post: caption đúng chính tả, nằm trong safe zone và đọc được ở 360×640.
- Audio: voice khớp hình; disclosure không bị nhạc/SFX che; không phụ thuộc audio rời của clip AI.
- Commerce: claim có ID/nguồn; CTA và product anchor đúng SKU; không watermark, outro lạ hoặc quảng cáo nhiễm.
- Format identity: ít nhất 4 clip nguồn và 80% thời lượng là footage chuyển động; không có shot cốt lõi chỉ là ảnh tĩnh pan/zoom.

Một lỗi hard gate làm trạng thái thành `HOLD/REJECT`, không được xuất bản. Nếu fail format identity, video phải được phân loại lại thành `VIDEO_SLIDE` hoặc `MOTION_STORYBOARD`; không được giữ tên Video AI Bán Hàng.

## Bài test thực chiến

Đầu vào: một SKU thật, listing đã xác minh, ảnh tổng thể + ảnh chi tiết và ít nhất một claim có nguồn.

Đầu ra:

- Reel 9:16 dài 20–30 giây, 4–6 shot.
- Product Truth Pack, claim ledger, continuity bible và reference manifest.
- Prompt pack tiếng Anh, storyboard/timecode và timeline hậu kỳ.
- Một track voice Việt, caption, AI/affiliate disclosure và bảng QA từng shot.

Điều kiện đạt: Motion Prompt từ `9/10`; toàn video không có sai/drift SKU, continuity món ăn sai, lỗi tay/mặt rõ, chữ/logo/UI do AI sinh, claim thiếu nguồn, disclosure thiếu, link sai hoặc watermark/outro nhiễm. Cho phép tối đa hai vòng sửa và phải lưu điểm trung thực.

Điều kiện loại trực tiếp: không có ít nhất 4 clip chuyển động AI/footage, footage chuyển động dưới 80% thời lượng hoặc dùng ảnh tĩnh pan/zoom làm các cảnh chính. Video bị loại dù metadata, caption và âm thanh đều đạt.
