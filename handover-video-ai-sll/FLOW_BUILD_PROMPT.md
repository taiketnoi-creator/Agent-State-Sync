# HƯỚNG DẪN BUILD "REVIEW VIDEO FACTORY" TRÊN GOOGLE FLOW

## 0. Nên dán prompt hay đưa code vào?
- **Dán prompt (khuyên dùng).** Build của Flow là công cụ "mô tả → AI tự sinh app". Nó tự kết nối sẵn Gemini, Nano Banana và Veo trong tài khoản Flow của bạn, không cần API key.
- **Đưa code vào: không nên.** Code tự viết sẽ phải gọi API riêng (cần key, trả phí riêng) và Build có thể không nhận code ngoài.
- **Chiến lược:** Chia thành **5 prompt nối tiếp**. Dán Prompt 1 để tạo app lõi → test → lần lượt dán Prompt 2, 3, 4, 5 vào ô chat của Build để nâng cấp. Dán tất cả một lần thì AI dễ bỏ sót hoặc tạo app lỗi.

## 1. Các bước thao tác
1. Mở **labs.google/flow** → đăng nhập → chọn **Build** (hoặc Tools → Create tool).
2. Copy **nguyên khối PROMPT 1** (phần trong ```text```) → dán → gửi.
3. Đợi app được tạo → bấm **Preview/Run** → test bằng bộ mẫu (mục 3).
4. Nếu chạy được, dán **PROMPT 2** vào ô chat của Build. Test lại. Tiếp tục với Prompt 3, 4, 5.
5. Sau mỗi prompt, **lưu phiên bản** (Save/Version) để có thể quay lại nếu bản sau bị lỗi.
6. Gặp lỗi: copy nguyên thông báo lỗi và dán vào chat của Build kèm câu `Fix this error and keep all existing features.` (hoặc gửi cho AI Assistant).

---

## PROMPT 1 – App lõi (nhập liệu → kịch bản → keyframe → QA → video → ghép)

```text
Build a tool called "Review Video Factory". It turns 1 product into 4 short vertical review videos (9:16, 36–48s each). The SAME creator face, body, voice and product must appear consistently in every shot. UI language: Vietnamese. Clean dark theme. Use a step-by-step wizard with a progress bar: 1 Nhập liệu → 2 Kịch bản → 3 Keyframe → 4 Video → 5 Xuất bản.

## STEP 1 – INPUT
Form fields:
- Ảnh khuôn mặt (image, required)
- Ảnh dáng người (image, required)
- Ảnh sản phẩm (image, required)
- Tên sản phẩm (text, required)
- Kịch bản thô / Thông tin sản phẩm (long text, required)
- Điều cấm nói (long text, optional) – claims the scripts must never make
- Vùng miền & Phong cách giọng (dropdown: Miền Bắc, Miền Nam, Miền Trung – Giới tính Nam/Nữ tự động khóa theo ảnh khuôn mặt; plus a free-text "Mô tả thêm giọng")
Input validation: before continuing, ask Gemini to check the 3 images. Warn (but allow override) if: the face is blurry, covered or not frontal; the body image does not show the full body; the product image has multiple objects or a busy background.
Button "Viết kịch bản".

## STEP 2 – ANALYSIS + STORY BIBLE + SCRIPTS (Gemini, JSON)
### 2A. Analyze inputs first (auto-detect, user can correct)
From the 3 images + text, Gemini must detect and show in an editable "Phân tích" card:
- creator_gender (male/female – auto-locks voice gender), age range, style/vibe (e.g. trẻ trung, công sở, năng động, sang trọng).
- product_category, one of: skincare_cosmetics, fashion_accessories, electronics_gadget, food_drink, home_kitchen, health_supplement, mom_baby, beauty_tool, sport_fitness, other.
- product_size (small handheld / medium / large), how it is held and used, and the visible result of using it.
- target_audience (gender + age) and the main pain point.
The user can change gender/category in dropdowns before continuing.

### 2B. Category playbook (adapt setting, props, actions, demo)
- skincare_cosmetics: bathroom vanity or bedroom dressing table, morning light; demo = dispense onto fingertips, apply to cheek, close-up of texture and glowing skin.
- fashion_accessories: bedroom with mirror or street café; demo = wear it, mirror turn, fabric/detail close-up, walking shot.
- electronics_gadget: desk setup or living room; demo = unbox, press buttons, screen on, use in a real situation.
- food_drink: kitchen counter or dining table; demo = open, pour/plate, steam or texture close-up, first-bite reaction.
- home_kitchen: kitchen or living room; demo = messy before → use product → clean after.
- health_supplement: morning kitchen routine; demo = take a dose with a glass of water, energetic daily activity (no medical claims).
- mom_baby: bright nursery or living room, gentle tone; never show a baby's face in close-up.
- beauty_tool: vanity; demo = use on hair/face, before/after result.
- sport_fitness: home gym or park; demo = in-use motion shots.
- other: the most natural real-life usage location.
Gender adaptation:
- Self-address "mình"; address the audience to match target_audience ("chị em", "anh em", "mọi người"); vocabulary and energy match the creator's gender/age.
- Outfit, poses and gestures natural for that gender and vibe. Voice gender MUST automatically equal creator_gender.

### 2C. Story Bible per video (continuity lock)
For each of the 4 videos define ONE fixed story_bible (English) used in every scene of that video:
location (one main location; max one change, only if the angle needs before/after), time_of_day, lighting setup + direction, color palette, outfit (exact items and colors, unchanged all video), hairstyle, props, where the product rests when not held.
The 4 videos use different locations/outfits so they don't look identical.

### 2D. Scripts
- Act as an elite TikTok creative director. Write EXACTLY 4 Vietnamese scripts with different angles: 1) Pain Point / Problem-Solver, 2) Storytelling / Personal experience, 3) Myth-busting / Before-After, 4) Direct review / Unbox & speed test.
- Each script: EXACTLY 6 scenes, 6–8s each, 15–20 Vietnamese words per scene (1 second = 2.5 words). Energetic, natural TikTok tone. The 6 lines must flow as ONE continuous speech (use connectors so each scene continues the previous one).
- Scene structure: 1 Hook, 2 Agitate problem, 3 Product reveal, 4 Product close-up demo (per category playbook), 5 Proof/result & reaction, 6 CTA pointing to cart.
- Shot progression: medium → close-up → medium with product → macro → close reaction → medium CTA. Keep the 180° rule: creator stays on the same side of frame, facing the same direction.
- CONTINUITY: each scene has start_state_en and end_state_en (position, pose, hands, gaze, product location: in right hand / on table / not visible). Scene N+1 start_state MUST equal scene N end_state. Example: scene 2 ends "reaching toward the table" → scene 3 starts "picking up the product from the table".
- COMPLIANCE: only use facts from the user's product info. No invented numbers, no medical/cure claims, no absolute claims ("tốt nhất", "100%", "vĩnh viễn"), never say anything in "Điều cấm nói".
- For each video write an on-screen hook text (max 6 words, Vietnamese).
- Extract ultra-precise English descriptions of the creator (gender, face, hair, skin, age, body build) and the product (shape, colors, material, logo, packaging, real size relative to a hand).
- Create ONE fixed English voice description (gender = creator_gender, age, user's chosen Vietnamese regional accent, pace, energy, timbre), reused in every clip.
Return raw JSON:
{
  "analysis": { "creator_gender": "...", "age_range": "...", "vibe": "...", "product_category": "...", "product_size": "...", "usage": "...", "target_audience": "...", "pain_point": "..." },
  "creator_desc_en": "...", "product_desc_en": "...", "voice_desc_en": "...",
  "videos": [ { "video_id": 1, "angle": "...", "hook_text_vi": "...",
    "story_bible_en": { "location": "...", "time_of_day": "...", "lighting": "...", "palette": "...", "outfit": "...", "hair": "...", "props": "...", "product_rest_position": "..." },
    "scenes": [ { "n": 1, "duration_s": 6, "shot_type": "creator | creator_with_product | product_only",
      "framing": "medium | close-up | macro | wide", "camera_angle": "eye-level | slight high | low",
      "start_state_en": "...", "end_state_en": "...",
      "voiceover_vi": "...", "action_en": "...",
      "veo_motion_en": "camera movement + subject motion from start_state to end_state",
      "transition_to_next": "match cut | hand pass | push-in | whip pan | none" } ] } ]
}
Post-processing: count words per scene. If a scene has more than 20 words (or more than duration_s × 2.5), ask Gemini to shorten it while keeping meaning and flow.
Show the analysis card, then the 4 scripts as editable cards (voiceover, hook, story bible). Show word count + estimated seconds per scene, red if too long.
APPROVAL CHECKPOINT: the user must click "Duyệt kịch bản" to continue.

## STEP 3 – KEYFRAMES (Nano Banana) + PARALLEL AUTO QA (2-Wave High-Speed Batch)
To maximize speed while keeping 100% visual continuity, generate all 24 keyframes in just 2 parallel waves instead of waiting 1→6 sequentially:
- **WAVE 1 (Master Anchor Batch – 4 images in parallel):** Simultaneously generate Scene 1 for all 4 videos using the input reference images (`face + body`, or `face + body + product`). These 4 images establish the exact outfit, room, lighting, and creator look for each video.
- **WAVE 2 (Remaining 20 Scenes in parallel):** As soon as a video's Scene 1 keyframe is ready, immediately fire Scenes 2, 3, 4, 5, and 6 for that video ALL AT ONCE in parallel (up to 20 concurrent generations across the 4 videos).
References by shot_type (face image always first):
- creator → face + body images + Scene 1 Anchor keyframe (for scenes 2–6)
- creator_with_product → face + body + product images + Scene 1 Anchor keyframe (for scenes 2–6)
- product_only → product image + Scene 1 Anchor keyframe (for matching background/lighting)
Prompt:
"Create a photorealistic vertical 9:16 keyframe that belongs to the exact same continuous video shoot as the Scene 1 Anchor reference image.
IDENTITY: the identical {creator_gender} person from the face image (same identity, exact facial features, skin tone, hairstyle) with the exact body shape from the body image. {creator_desc_en}.
PRODUCT: exact design from the product image (same shape, colors, logo, packaging) at correct real-world scale ({product_size}) relative to the hands. {product_desc_en}. No morphing, no extra text, no watermark.
CONTINUITY (must match Scene 1 Anchor and Story Bible): location {location}, {time_of_day}, lighting {lighting}, palette {palette}, exact same outfit {outfit}, hair {hair}, props {props}. Creator stays on the same side of frame facing the same direction.
THIS SHOT: {framing}, {camera_angle}, {shot_type}. Starting state: {start_state_en}. Action: {action_en}.
STYLE: authentic TikTok creator footage, natural skin texture, realistic hands with five fingers gripping the product naturally, Sony A7SIII 35mm f/1.4, shallow depth of field."
PARALLEL ASYNC AUTO QA: display each keyframe in the 4×6 grid immediately upon generation. In the background, run Gemini QA across all 24 keyframes in parallel (comparing against the input references and Scene 1 Anchor), returning JSON {"face_score":0-10,"product_score":0-10,"continuity_score":0-10,"gender_match":true/false,"hands_ok":true/false,"issues":"..."}. Any single cell with a relevant score < 8, gender_match=false, or hands_ok=false automatically regenerates in parallel with the issues appended as corrections (max 2 retries); if still failing, show a red warning badge.
Show a 4×6 grid (one row per video, scenes 1–6) with live progress, QA scores, a "Tạo lại" button and a replacement upload per cell.
APPROVAL CHECKPOINT: show the estimated number of Veo generations, then the user clicks "Duyệt keyframe & tạo video".

## STEP 4 – VIDEO (Veo), 24-Clip Parallel Batch with Seamless Frame Locking
Since all 24 keyframes are already approved in Step 3, generate all 24 video clips IN PARALLEL at once (no sequential waiting):
- If Veo first-and-last-frame (frames-to-video) is available: for Scene N (N=1..5), pass Scene N's keyframe as the first frame and Scene N+1's keyframe as the last frame (for Scene 6: pass Scene 6's keyframe as first frame). Because both frames already exist from Step 3, all 24 clips can run simultaneously while still locking seamless transitions!
- Otherwise: run image-to-video from Scene N's keyframe in parallel for all 24 clips and guide the ending pose with `{end_state_en}`.
Settings: 9:16, 8 seconds, with audio.
Prompt: "Continuous shot. {veo_motion_en}. The creator moves smoothly from: {start_state_en} to: {end_state_en}. Keep the exact same location, lighting, outfit and camera side as the input frame. Voice: {voice_desc_en}, keep this identical {creator_gender} voice across all clips. The {creator_gender} creator speaks Vietnamese to camera with accurate lip-sync: \"{voiceover_vi}\". Natural micro-expressions and hand gestures; the product stays rigid, unchanged and correctly scaled. No background music, no on-screen text. Vertical 9:16."
For product_only scenes: hands may appear (same skin tone and outfit sleeves), no face; same voice as off-screen narration.
Show parallel progress bars per clip, preview each clip as soon as it finishes, and allow regenerating any single clip. Retry automatically once on failure.

## STEP 5 – ASSEMBLE & EXPORT
For each video:
- Trim each clip to its duration_s and concatenate the 6 clips in order.
- Burn in Vietnamese subtitles from voiceover_vi (white bold, black outline, lower third, synced per scene).
- Show hook_text_vi as big bold text in the upper-middle area during the first 2.5 seconds.
Output: 4 final videos with a preview player, "Tải xuống" per video, and "Tải tất cả". File names: {product}_{angle}_v{id}.mp4.

## GENERAL
- Process the 4 videos in parallel where possible; show overall progress.
- Keep all intermediate results so the user can go back to any step and regenerate a single item without restarting.
```

---

## PROMPT 2 – Nhạc nền, ảnh bìa, gói đăng bài

```text
Add these features and keep everything that already exists:
1. Background music: in Step 5 add a dropdown "Nhạc nền" (Không, Sôi động, Nhẹ nhàng, Truyền cảm hứng) and an option to upload my own audio. Mix the music at low volume and automatically duck it under the voice.
2. Thumbnail: for each video generate a 9:16 cover with Nano Banana using the creator + product references, an excited expression, and the hook_text_vi as big bold Vietnamese text. Allow regenerating it.
3. Posting pack: for each video ask Gemini to write a TikTok caption (max 150 characters, with a CTA), 8–12 relevant Vietnamese hashtags, and a YouTube Shorts title. Each item gets a copy button.
4. "Tải tất cả" downloads a zip with 4 videos, 4 thumbnails, and a captions.txt file.
```

## PROMPT 3 – Hồ sơ Creator lưu sẵn

```text
Add a "Hồ sơ Creator" feature and keep everything that already exists:
- After the first successful run, offer "Lưu hồ sơ" to save the face image, body image, creator_desc_en, voice choice and voice_desc_en under a name.
- In Step 1 add a dropdown "Chọn hồ sơ có sẵn". Choosing a profile auto-fills the face/body/voice fields so I only need to enter the product.
- Allow editing and deleting profiles.
```

## PROMPT 4 – Lịch sử dự án + ước tính credit

```text
Add these features and keep everything that already exists:
1. Project history: save every run (inputs, scripts, keyframes, clips, final videos, captions) as a project with date and product name. Add a "Lịch sử" page to reopen, duplicate (re-run with a new product), or delete a project.
2. Cost estimate: before Step 3 and before Step 4, show how many Nano Banana and Veo generations will be used (including possible QA retries) and ask for confirmation.
```

## PROMPT 5 – Vòng lặp học từ kết quả (khép kín)

```text
Add a performance feedback loop and keep everything that already exists:
- In each saved project add a "Kết quả sau đăng" form per video: views, average watch time (%), likes, comments, orders.
- Add a "Thống kê" page that ranks the 4 angles (Pain Point, Storytelling, Myth-busting, Direct review) and the hook texts by average performance across all projects.
- When writing new scripts in Step 2, send Gemini a short summary of the top-performing angles and hooks, with the instruction: "Learn from these winning patterns; keep the 4 different angles but apply the winning hook style and pacing."
```

## PROMPT 6 – Nâng cấp chuẩn "Sandwich A-Roll ↔ B-Roll 8 Nhịp Đa Sản Phẩm" & Xuất Raw Pack cho FFmpeg SLL

```text
Upgrade the script & scene architecture to the high-converting "8-Beat Hybrid A-Roll + B-Roll Sandwich" commercial format (adaptable to ANY product category) and add a "Tải Raw Pack (Cho FFmpeg / CapCut SLL)" export button, while keeping all existing features:

1. 8-Beat Hybrid A-Roll + B-Roll Scene Structure (per video, 36–42s total):
   - Scene 1 (0–2s, B-Roll Shock + A-Roll Hook): Visual contrast of the problem + creator stunned reaction (`shot_type: creator`, `is_hook_overlay: true`).
   - Scene 2 (2–7s, A-Roll Pain + Time Pressure): Creator struggling with the old method before using the product (`shot_type: creator`).
   - Scene 3 (7–13s, A-Roll Hero Reveal): Bright switch in lighting; creator smiles and introduces the exact product on the table/hand (`shot_type: creator_with_product`).
   - Scene 4 (13–20s, B-Roll Macro Result #1): Extreme close-up of the product's core result/texture/output in action (`shot_type: product_only`, no face, off-screen voiceover).
   - Scene 5 (20–24s, B-Roll Macro Result #2 + A-Roll Return): Second close-up angle of product performance cutting back to creator (`shot_type: product_only` or `creator_with_product`).
   - Scene 6 (24–31s, B-Roll Macro Interaction / Mechanism): Close-up hand interacting with the product (pressing button, pumping serum, flexing material, pouring) (`shot_type: product_only`). Never generate close-up AI text on buttons/screens; keep camera at a 35-degree angle with shallow depth of field.
   - Scene 7 (31–35s, B-Roll Hero Zoom for Trust Badge): Slow cinematic push-in on the whole product on a clean surface (`shot_type: product_only`, reserved for post-production 3D Warranty/Authentic Shield overlay).
   - Scene 8 (35–41s, A-Roll Emotional Payoff + CTA): Creator and/or family enjoying the effortless result and pointing to cart/inbox (`shot_type: creator_with_product`). Never generate AI text posters at the end.

2. Multi-Product Anti-Morphing Lock:
   - In every `creator_with_product` and `product_only` prompt, enforce: "Rigid product geometry, exact silhouette, exact lid/cap/material and color from the product reference image; zero morphing between scenes."

3. Export "Raw SLL Pack" for Local FFmpeg / Remotion Batch Mixing:
   - In Step 5, add a button "Tải Raw Scenes Pack (SLL)" that downloads a structured folder ZIP (`scene_1/clip_v1..v4.mp4` ... `scene_8/clip_v1..v4.mp4` + `voiceover.mp3` + `subtitles.json`) so external FFmpeg / Remotion pipelines can cross-mix 4 hooks × N demos into 12–20 unique videos and overlay crisp Vietnamese pop-up stickers, 3D warranty shields, and subtitles without AI text artifacts.
```

<!-- end prompt 6 -->
```

---

## 3. Bộ test mẫu (dùng sau mỗi prompt)
| Ô nhập | Gợi ý |
|---|---|
| Ảnh mặt | Chụp chính diện, đủ sáng, không đeo kính râm |
| Ảnh dáng | Toàn thân, nền đơn giản |
| Ảnh sản phẩm | Một sản phẩm, nền trắng |
| Thông tin | 3–5 gạch đầu dòng: công dụng, giá, ưu đãi |
| Điều cấm nói | VD: "không nói trị mụn, không nói rẻ nhất" |

**Checklist sau khi test:** ☐ đủ 4 kịch bản × 6 cảnh ☐ mỗi cảnh không quá 20 từ ☐ mặt và sản phẩm giống ảnh gốc (QA ≥ 8) ☐ giọng giống nhau giữa các clip ☐ phụ đề khớp lời ☐ video dài 36–48s.

## 4. Lỗi thường gặp → prompt sửa
- Mặt bị lệch: `Make face consistency stricter: raise the QA threshold to 8.5 and always attach the best-scoring creator keyframe as an extra reference.`
- Giọng vẫn khác nhau: `Disable Veo audio. Generate one voiceover track per video with Gemini TTS using voice_desc_en, then mix it over the silent clips during assembly.`
- Clip bị chậm hoặc thiếu thời lượng: `Always generate 8s clips and trim to duration_s during assembly.`
- Build báo không ghép được video hoặc chèn phụ đề: `If in-app video concatenation is not supported, export the 6 clips per video plus an .srt subtitle file and a ready-to-import CapCut order list instead.`
