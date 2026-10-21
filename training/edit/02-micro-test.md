# Bước 2 — Micro-test: Máy cạo lông xù

## Đề bài

Từ kịch bản Máy cạo lông xù đã pass, tạo Motion Prompt cho đúng ba cảnh: Hook áo xù lông, macro ASMR máy cạo và so sánh Before/After.

## Cảnh 1 — Hook áo xù lông

- **Cỡ cảnh:** Medium close-up chuyển sang insert close-up.
- **Góc máy:** Eye-level, slow push-in; cut to a 45-degree fabric detail angle.
- **Rigid lock:** `Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing`.

### Motion Prompt

```text
[00-01s] Medium close-up of a fictional young adult entering a casual café in an unbranded black wool sweater covered with obvious pale fabric pills. Eye-level camera, soft natural window light, vertical 9:16 composition, quick comedic reaction from an anonymous companion in the blurred background.
[01-02s] The camera performs a fast controlled push-in toward the sweater surface while the wearer looks down in embarrassed surprise. Keep facial features generic and non-identifiable.
[02-03s] Cut to a 45-degree insert close-up of the dense fabric pills, with shallow depth of field and a clean highlight tracing the rough texture. Hold the texture sharply for the visual punchline.
Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing. No celebrity likeness, no copyrighted character, no logo, no readable text, no face distortion, no duplicated limbs, no changing garment color, no unstable fabric texture.
```

## Cảnh 2 — Macro máy cạo lông xù ASMR

- **Cỡ cảnh:** Extreme macro close-up.
- **Góc máy:** Top-down 35-degree macro angle, short lateral tracking move.
- **Rigid lock:** `Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing`.

### Motion Prompt

```text
[00-02s] Extreme macro close-up of a generic unbranded handheld fabric shaver resting flat against a black wool sweater. Top-down 35-degree angle, 100 mm macro lens look, stable soft key light, subtle edge light, crisp focus on the shaving head and fabric fibers.
[02-05s] One natural human hand guides the shaver in a single straight left-to-right pass. The camera tracks laterally at the same speed as the device. Fabric pills disappear only beneath the shaving path, revealing a visibly smoother strip while surrounding texture remains unchanged.
[05-07s] The hand stops and lifts the device vertically by two centimeters, revealing the clean strip. Hold the frame for a satisfying ASMR payoff with stable focus and no camera shake.
Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing. No warped device, no changing blade shape, no duplicated product, no extra fingers, no fabric tearing, no floating debris, no logo, no readable text, no sudden texture replacement.
```

## Cảnh 3 — So sánh Before/After

- **Cỡ cảnh:** Locked overhead comparison close-up.
- **Góc máy:** 90-degree top-down, static camera.
- **Rigid lock:** `Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing`.

### Motion Prompt

```text
[00-01s] Locked 90-degree overhead close-up of one continuous black wool garment divided visually by a thin neutral guide line. The left half shows dense fabric pills; the right half shows the same fabric smooth and tidy. Even studio lighting, identical exposure and color on both sides.
[01-03s] A generic unbranded fabric shaver enters from the bottom edge and pauses directly over the center boundary, establishing that both halves belong to the same garment. Keep the camera perfectly static.
[03-05s] The device exits downward. Maintain the split comparison unchanged for two seconds so the rough left side and smooth right side are immediately readable.
Rigid product geometry, preserved scale, stable macro lighting, natural hand kinematics, zero morphing. No split garment duplication, no changing garment color, no moving boundary, no warped device, no extra hands, no logo, no readable text, no celebrity likeness, no copyrighted character.
```

**Trạng thái:** `READY_FOR_SCORING`.
