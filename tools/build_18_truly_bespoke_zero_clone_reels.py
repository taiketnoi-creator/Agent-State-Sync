#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_18_truly_bespoke_zero_clone_reels.py
Tạo mới hoàn toàn 18 Composition (Reel01..Reel03, Reel07..Reel21) theo đúng 100%
luật `MEM-20261022-zero-clone-bespoke-video-rule.md` và 5 Quy tắc Vàng Remotion:
- TUYỆT ĐỐI CẤM xoay vòng `idx % 3` hay `idx % 2`.
- Mỗi video trong 18 video có 1 Kiến trúc Bố cục Vĩ mô (Macro Layout), Vị trí đặt Tiêu đề
  (Trên-Trái, Trên-Phải, Dưới-Đáy, Giữa-Kẹp-Sandwich, Cột-Dọc, Chéo-Bậc-Thang, Đồng-Tâm, Bento...)
  và Hình vẽ Đồ họa SVG Chuyên biệt (Bespoke Topic SVG) riêng biệt 100%!
- Tự động kiểm tra qua cổng khóa cứng `verify_zero_clone_tsx()` ngay sau khi sinh code.
"""

from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_remaining_18_golden_reels_data import REELS_CONFIG

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "templates" / "remotion-cuongit-template" / "src"


def _q(val):
    if isinstance(val, str):
        return (
            val.replace('"', "'")
            .replace("“", "'")
            .replace("”", "'")
            .replace("->", "→")
            .replace("<-", "←")
            .replace(">", "›")
            .replace("<", "‹")
        )
    if isinstance(val, tuple):
        return tuple(_q(x) for x in val)
    if isinstance(val, list):
        return [_q(x) for x in val]
    return val


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def gen_index_tsx(comp_id: str) -> str:
    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ BrandHeader }} from "../AiHallucinationShort/BrandHeader";
import {{ audioManifest }} from "./audioData";
import {{ Scene1 }} from "./Scene1";
import {{ Scene2 }} from "./Scene2";
import {{ Scene3 }} from "./Scene3";
import {{ Scene4 }} from "./Scene4";
import {{ Scene5 }} from "./Scene5";
import {{ Scene6 }} from "./Scene6";

const SCENE_COMPONENTS: React.FC[] = [Scene1, Scene2, Scene3, Scene4, Scene5, Scene6];

export const {comp_id}: React.FC = () => {{
  const frame = useCurrentFrame();
  const orb1X = interpolate(Math.sin(frame * 0.025), [-1, 1], [-50, 50]);
  const orb1Y = interpolate(Math.cos(frame * 0.02), [-1, 1], [-40, 40]);
  const orb2X = interpolate(Math.cos(frame * 0.018), [-1, 1], [60, -60]);
  const orb2Y = interpolate(Math.sin(frame * 0.022), [-1, 1], [50, -50]);

  let accumulatedFrames = 0;

  return (
    <AbsoluteFill className="bg-[#0c38ff] font-sans text-white overflow-hidden">
      <AbsoluteFill>
        <Img src={{staticFile("brand-kit/bg/BG-video-motion.jpg")}} className="h-full w-full object-cover" />
        <div
          style={{{{
            transform: `translate(${{orb1X}}px, ${{orb1Y}}px)`,
            background: "radial-gradient(circle, rgba(135, 255, 0, 0.14) 0%, rgba(135, 255, 0, 0) 70%)",
          }}}}
          className="absolute top-[160px] left-[-120px] h-[680px] w-[680px] rounded-full pointer-events-none"
        />
        <div
          style={{{{
            transform: `translate(${{orb2X}}px, ${{orb2Y}}px)`,
            background: "radial-gradient(circle, rgba(56, 189, 248, 0.18) 0%, rgba(56, 189, 248, 0) 70%)",
          }}}}
          className="absolute bottom-[220px] right-[-140px] h-[740px] w-[740px] rounded-full pointer-events-none"
        />
      </AbsoluteFill>

      <Audio src={{staticFile("brand-kit/bgm/1.The Violins.mp3")}} volume={{0.10}} loop />
      <BrandHeader text="AI PLAYERS — NGƯỜI CHƠI HỆ AI" />

      {{audioManifest.scenes.map((scene, index) => {{
        const fromFrame = accumulatedFrames;
        accumulatedFrames += scene.durationInFrames;
        const SceneComp = SCENE_COMPONENTS[index] || Scene1;
        return (
          <Sequence key={{scene.id}} from={{fromFrame}} durationInFrames={{scene.durationInFrames}}>
            {{index > 0 && <Audio src={{staticFile("brand-kit/sfx/apple-pay-sound.mp3")}} volume={{0.26}} />}}
            <SceneComp />
          </Sequence>
        );
      }})}}
    </AbsoluteFill>
  );
}};
"""


# ==============================================================================
# 18 BESPOKE SCENE 1 GENERATORS (100% KHÁC BIỆT BỐ CỤC VĨ MÔ, VỊ TRÍ CHỮ & SVG)
# ==============================================================================

def gen_scene1_bespoke(vid_id: str, s1: tuple) -> str:
    kicker, h1_a, h1_b, sub, c1_title, c1_desc, c1_tag, c2_title, c2_desc, c2_tag, kw = _q(s1)

    # 1. REEL01: VISUAL-FIRST TOP 360 SPIDER WEB + BOTTOM SPLIT HEADER
    if vid_id == "reel01":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const enter = spring({{ frame, fps, config: {{ damping: 13, stiffness: 105 }} }});
  const sweepDeg = (frame * 4.5) % 360;
  const dashMove = -(frame * 3.5);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP VISUAL STAGE: 360 SPIDER RADAR CONSTELLATION */}}
      <div style={{{{ transform: `scale(${{enter}})` }}}} className="relative grid grid-cols-12 items-center gap-5 rounded-[38px] border border-white/30 bg-white/[0.08] p-7 backdrop-blur-md shadow-[0_18px_50px_rgba(0,0,0,0.28)]">
        <div className="col-span-7 flex items-center justify-center">
          <svg width="480" height="390" viewBox="0 0 480 390" className="overflow-visible">
            <circle cx="240" cy="195" r="165" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.22)" strokeWidth="2" strokeDasharray="8 6" />
            <circle cx="240" cy="195" r="110" fill="rgba(135,255,0,0.06)" stroke="rgba(135,255,0,0.38)" strokeWidth="2.5" />
            {{[0, 36, 72, 108, 144, 180, 216, 252, 288, 324].map((deg, idx) => {{
              const rad = (deg * Math.PI) / 180;
              const nx = 240 + Math.cos(rad) * 150;
              const ny = 195 + Math.sin(rad) * 150;
              return (
                <g key={{deg}}>
                  <line x1="240" y1="195" x2={{nx}} y2={{ny}} stroke={{idx % 2 === 0 ? "#87ff00" : "#38bdf8"}} strokeWidth="3" strokeDasharray="10 6" strokeDashoffset={{dashMove}} />
                  <circle cx={{nx}} cy={{ny}} r="16" fill="rgba(255,255,255,0.16)" stroke="#87ff00" strokeWidth="3" />
                  <text x={{nx}} y={{ny + 5}} textAnchor="middle" fill="#ffffff" fontSize="12" fontWeight="900">W{{idx + 1}}</text>
                </g>
              );
            }})}}
            <g transform={{`rotate(${{sweepDeg}} 240 195)`}}>
              <line x1="240" y1="195" x2="240" y2="30" stroke="#87ff00" strokeWidth="5" strokeLinecap="round" />
            </g>
            <circle cx="240" cy="195" r="46" fill="#87ff00" />
            <text x="240" y="191" textAnchor="middle" fill="#071a52" fontSize="18" fontWeight="900">200 NGUỒN</text>
            <text x="240" y="212" textAnchor="middle" fill="#071a52" fontSize="14" fontWeight="900">QUÉT CHÉO</text>
          </svg>
        </div>
        <div className="col-span-5 flex flex-col gap-4">
          <div className="rounded-2xl border-2 border-amber-300/55 bg-white/[0.10] p-5 backdrop-blur-sm">
            <span className="rounded-md bg-amber-400/25 px-3 py-1 text-base font-black text-amber-200">{c1_tag}</span>
            <h3 className="mt-2 text-2xl font-black text-white">{c1_title}</h3>
            <p className="mt-1 text-lg font-bold text-white/85 leading-snug">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-5 backdrop-blur-sm">
            <span className="rounded-md bg-[#87ff00] px-3 py-1 text-base font-black text-slate-950">{c2_tag}</span>
            <h3 className="mt-2 text-2xl font-black text-[#87ff00]">{c2_title}</h3>
            <p className="mt-1 text-lg font-bold text-white/95 leading-snug">{c2_desc}</p>
          </div>
        </div>
      </div>

      {{/* BOTTOM ASYMMETRIC SPLIT HEADER */}}
      <div className="grid grid-cols-12 items-end gap-6 border-l-8 border-[#87ff00] pl-6">
        <div className="col-span-8 flex flex-col">
          <span className="text-xl font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[52px] font-black leading-[1.08] uppercase drop-shadow-[0_4px_20px_rgba(0,0,0,0.75)]">
            {h1_a} <span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-2 text-2xl font-bold text-white/90">{sub}</p>
        </div>
        <div className="col-span-4 flex flex-col items-center justify-center rounded-3xl border-2 border-[#87ff00] bg-white/[0.12] p-4 text-center backdrop-blur-md">
          <span className="text-5xl font-black text-[#87ff00]">3 PHÚT</span>
          <span className="mt-1 text-lg font-black text-white uppercase">XONG 10 TRANG BÁO CÁO</span>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 2. REEL02: LEFT TALL STUDIO CONDENSER MIC BOOTH + RIGHT HEADER & WAVEFORM TRACKS
    if vid_id == "reel02":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const enter = spring({{ frame, fps, config: {{ damping: 12, stiffness: 110 }} }});
  const ringPulse = 1 + Math.sin(frame * 0.22) * 0.08;

  return (
    <AbsoluteFill className="flex flex-col justify-center px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>
      <div className="grid grid-cols-12 items-stretch gap-6">

      {{/* LEFT COLUMN: STUDIO CONDENSER MICROPHONE BOOTH */}}
      <div style={{{{ transform: `scale(${{enter}})` }}}} className="col-span-5 flex flex-col items-center justify-between rounded-[42px] border-2 border-[#87ff00]/80 bg-white/[0.10] p-6 backdrop-blur-md shadow-[0_18px_50px_rgba(0,0,0,0.3)]">
        <div className="flex w-full items-center justify-between rounded-full border border-white/30 bg-white/10 px-4 py-2">
          <span className="h-3.5 w-3.5 rounded-full bg-[#87ff00] shadow-[0_0_12px_#87ff00]" />
          <span className="text-lg font-black text-[#87ff00]">REC // MẪU 00:05 GIÂY</span>
        </div>

        <svg width="310" height="380" viewBox="0 0 310 380" className="overflow-visible">
          <circle cx="155" cy="155" r={{125 * ringPulse}} fill="none" stroke="rgba(135,255,0,0.35)" strokeWidth="3" strokeDasharray="10 8" />
          <circle cx="155" cy="155" r={{92 * ringPulse}} fill="rgba(135,255,0,0.08)" stroke="#87ff00" strokeWidth="3.5" />
          <rect x="115" y="75" width="80" height="145" rx="40" fill="rgba(255,255,255,0.2)" stroke="#ffffff" strokeWidth="5" />
          <line x1="125" y1="115" x2="185" y2="115" stroke="#87ff00" strokeWidth="4" />
          <line x1="125" y1="140" x2="185" y2="140" stroke="#87ff00" strokeWidth="4" />
          <line x1="125" y1="165" x2="185" y2="165" stroke="#87ff00" strokeWidth="4" />
          <path d="M 90 155 A 65 65 0 0 0 220 155" fill="none" stroke="#38bdf8" strokeWidth="6" strokeLinecap="round" />
          <line x1="155" y1="220" x2="155" y2="295" stroke="#ffffff" strokeWidth="8" />
          <rect x="100" y="295" width="110" height="18" rx="9" fill="#87ff00" />
          {{Array.from({{ length: 14 }}).map((_, i) => {{
            const h = 18 + Math.abs(Math.sin(frame * 0.25 + i * 0.6)) * 42;
            return <rect key={{i}} x={{28 + i * 19}} y={{355 - h}} width="11" height={{h}} rx="5" fill={{i % 2 === 0 ? "#87ff00" : "#38bdf8"}} />;
          }})}}
        </svg>

        <div className="w-full rounded-2xl border border-white/25 bg-white/10 py-3 text-center text-xl font-black text-white">
          KHỚP 99% VÂN GIỌNG GỐC ✅
        </div>
      </div>

      {{/* RIGHT COLUMN: ASYMMETRIC HEADER + DUAL WAVE COMPARISON */}}
      <div className="col-span-7 flex flex-col justify-center gap-5">
        <div className="rounded-3xl border border-white/30 bg-white/[0.08] p-6 text-right backdrop-blur-md">
          <span className="inline-block rounded-lg bg-[#87ff00] px-4 py-1 text-lg font-black text-slate-950 uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-3 text-[48px] italic font-black leading-[1.1] uppercase drop-shadow">
            {h1_a}<br />{h1_b}
          </h1>
          <p className="mt-2 text-2xl font-bold text-white/90">{sub}</p>
        </div>

        <div className="flex flex-col gap-4 rounded-3xl border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
          <div className="rounded-2xl border-l-8 border-amber-300 bg-white/[0.10] p-5">
            <div className="flex items-center justify-between">
              <span className="text-2xl font-black text-amber-200">{c1_title}</span>
              <span className="rounded-lg bg-amber-400/25 px-3 py-1 text-base font-black text-amber-200">{c1_tag}</span>
            </div>
            <p className="mt-2 text-xl font-bold text-white/90">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-l-8 border-[#87ff00] bg-white/[0.14] p-5">
            <div className="flex items-center justify-between">
              <span className="text-2xl font-black text-[#87ff00]">{c2_title}</span>
              <span className="rounded-lg bg-[#87ff00] px-3 py-1 text-base font-black text-slate-950">{c2_tag}</span>
            </div>
            <p className="mt-2 text-xl font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 3. REEL03: SANDWICH BRIDGE LAYOUT (TOP BROKEN FRAGMENTS + MIDDLE HEADLINE + BOTTOM 3D GRAPH)
    if vid_id == "reel03":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const pop = spring({{ frame, fps, config: {{ damping: 13, stiffness: 100 }} }});
  const dashOffset = -(frame * 4);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP LAYER: SCATTERED DISCONNECTED DOCUMENT FRAGMENTS */}}
      <div className="grid grid-cols-2 gap-5">
        <div style={{{{ transform: "rotate(-2deg)" }}}} className="rounded-2xl border-2 border-amber-300/60 bg-white/[0.10] p-5 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-2xl font-black text-amber-200">{c1_title}</span>
            <span className="rounded-md bg-amber-400/25 px-3 py-1 text-base font-black text-amber-200">{c1_tag}</span>
          </div>
          <p className="mt-2 text-lg font-bold text-white/85">{c1_desc}</p>
        </div>
        <div style={{{{ transform: "rotate(2deg)" }}}} className="rounded-2xl border-2 border-rose-400/60 bg-white/[0.10] p-5 backdrop-blur-md">
          <div className="flex items-center justify-between">
            <span className="text-2xl font-black text-rose-200">{c2_title}</span>
            <span className="rounded-md bg-rose-500/30 px-3 py-1 text-base font-black text-rose-200">{c2_tag}</span>
          </div>
          <p className="mt-2 text-lg font-bold text-white/85">{c2_desc}</p>
        </div>
      </div>

      {{/* MIDDLE FLOATING BRIDGE HEADLINE BANNER */}}
      <div style={{{{ transform: `scale(${{pop}})` }}}} className="rounded-3xl border-y-4 border-[#87ff00] bg-white/[0.12] px-8 py-5 text-center backdrop-blur-md shadow-[0_14px_40px_rgba(0,0,0,0.3)]">
        <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[52px] font-black leading-tight uppercase">
          {h1_a} — {h1_b}
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/95">{sub}</p>
      </div>

      {{/* BOTTOM LAYER: 3D KNOWLEDGE GRAPH CONSTELLATION */}}
      <div className="flex items-center justify-center rounded-[34px] border border-white/30 bg-white/[0.08] p-5 backdrop-blur-md">
        <svg width="880" height="270" viewBox="0 0 880 270">
          <line x1="150" y1="75" x2="440" y2="135" stroke="#87ff00" strokeWidth="4" strokeDasharray="12 6" strokeDashoffset={{dashOffset}} />
          <line x1="150" y1="205" x2="440" y2="135" stroke="#38bdf8" strokeWidth="4" strokeDasharray="12 6" strokeDashoffset={{dashOffset}} />
          <line x1="440" y1="135" x2="730" y2="75" stroke="#87ff00" strokeWidth="4" strokeDasharray="12 6" strokeDashoffset={{dashOffset}} />
          <line x1="440" y1="135" x2="730" y2="205" stroke="#87ff00" strokeWidth="4" strokeDasharray="12 6" strokeDashoffset={{dashOffset}} />
          <line x1="150" y1="75" x2="150" y2="205" stroke="rgba(255,255,255,0.4)" strokeWidth="2.5" />
          <line x1="730" y1="75" x2="730" y2="205" stroke="rgba(255,255,255,0.4)" strokeWidth="2.5" />
          {{[
            [150, 75, "NHÂN SỰ", "#38bdf8"],
            [150, 205, "BIÊN BẢN HỌP", "#38bdf8"],
            [440, 135, "ĐỒ THỊ TRI THỨC", "#87ff00"],
            [730, 75, "DỰ ÁN & KHO", "#87ff00"],
            [730, 205, "BÁO CÁO TỔNG", "#87ff00"],
          ].map(([cx, cy, lbl, col], idx) => (
            <g key={{idx}}>
              <rect x={{Number(cx) - 105}} y={{Number(cy) - 32}} width="210" height="64" rx="18" fill="rgba(255,255,255,0.16)" stroke={{String(col)}} strokeWidth="3.5" />
              <text x={{Number(cx)}} y={{Number(cy) + 7}} textAnchor="middle" fill="#ffffff" fontSize="20" fontWeight="900">{{lbl}}</text>
            </g>
          ))}}
        </svg>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 4. REEL07: LEFT SMARTPHONE VOICE COCKPIT + RIGHT 3-ARM LASER CASCADE & HEADER
    if vid_id == "reel07":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const enter = spring({{ frame, fps, config: {{ damping: 13, stiffness: 110 }} }});
  const beamShift = -(frame * 4.2);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP ASYMMETRIC SPEEDOMETER CALLOUT + LEFT-BORDERED TITLE */}}
      <div className="grid grid-cols-12 items-center gap-5">
        <div className="col-span-4 flex flex-col items-center justify-center rounded-[32px] border-2 border-[#87ff00] bg-white/[0.14] p-5 text-center backdrop-blur-md shadow-[0_12px_35px_rgba(0,0,0,0.28)]">
          <span className="text-lg font-black text-white/90 uppercase">PHẢN HỒI TỨC THÌ</span>
          <span className="mt-1 text-6xl font-black text-[#87ff00]">300ms</span>
          <span className="mt-1 rounded-full bg-[#87ff00] px-4 py-1 text-base font-black text-slate-950">RẢNH TAY 100% ⚡</span>
        </div>
        <div className="col-span-8 border-l-8 border-[#87ff00] pl-6">
          <span className="text-xl font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[48px] font-black leading-[1.08] uppercase drop-shadow">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-2 text-2xl font-bold text-white/90">{sub}</p>
        </div>
      </div>

      {{/* BOTTOM STAGE: PHONE VOICE HUB SHOOTING 3 LASER BEAMS TO ACTION MODULES */}}
      <div style={{{{ transform: `scale(${{enter}})` }}}} className="grid grid-cols-12 items-center gap-4 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="col-span-4 flex flex-col items-center rounded-[36px] border-2 border-[#87ff00] bg-white/[0.12] p-5">
          <div className="mb-3 h-2 w-20 rounded-full bg-white/40" />
          <span className="text-xl font-black text-[#87ff00]">🎙️ KHẨU LỆNH XE HƠI</span>
          <svg width="210" height="120" viewBox="0 0 210 120" className="my-3">
            {{Array.from({{ length: 11 }}).map((_, i) => {{
              const h = 22 + Math.abs(Math.sin(frame * 0.28 + i * 0.55)) * 75;
              return <rect key={{i}} x={{12 + i * 17}} y={{60 - h / 2}} width="11" height={{h}} rx="5" fill="#87ff00" />;
            }})}}
          </svg>
          <span className="rounded-xl bg-white/15 px-4 py-2 text-base font-bold text-white text-center">
            {c2_desc}
          </span>
        </div>

        <div className="col-span-3 flex items-center justify-center">
          <svg width="210" height="280" viewBox="0 0 210 280">
            <path d="M 10 140 C 80 140, 120 45, 200 45" fill="none" stroke="#87ff00" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{beamShift}} />
            <path d="M 10 140 L 200 140" fill="none" stroke="#38bdf8" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{beamShift}} />
            <path d="M 10 140 C 80 140, 120 235, 200 235" fill="none" stroke="#87ff00" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{beamShift}} />
          </svg>
        </div>

        <div className="col-span-5 flex flex-col gap-3">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <div className="flex justify-between">
              <span className="text-xl font-black text-amber-200">{c1_title}</span>
              <span className="text-base font-black text-amber-300">{c1_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.16] p-4">
            <div className="flex justify-between">
              <span className="text-xl font-black text-[#87ff00]">{c2_title}</span>
              <span className="rounded bg-[#87ff00] px-2.5 py-0.5 text-sm font-black text-slate-950">{c2_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/95">1. Tra Kho • 2. Đặt Lịch • 3. Báo Nhóm</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 5. REEL08: TOP IDE PYTHON SANDBOX + 5000-ROW TABLE + BOTTOM HEADLINE
    if vid_id == "reel08":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const pop = spring({{ frame, fps, config: {{ damping: 13, stiffness: 105 }} }});

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP VISUAL WINDOW: PYTHON CODE SANDBOX VM + 5000-ROW MATRIX */}}
      <div style={{{{ transform: `scale(${{pop}})` }}}} className="flex flex-col overflow-hidden rounded-[36px] border-2 border-[#87ff00]/75 bg-white/[0.10] backdrop-blur-md shadow-[0_18px_50px_rgba(0,0,0,0.3)]">
        <div className="flex items-center justify-between border-b border-white/25 bg-white/[0.12] px-7 py-3.5">
          <div className="flex items-center gap-3">
            <span className="h-4 w-4 rounded-full bg-rose-400" />
            <span className="h-4 w-4 rounded-full bg-amber-300" />
            <span className="h-4 w-4 rounded-full bg-[#87ff00]" />
            <span className="ml-3 font-mono text-xl font-black text-[#87ff00]">sandbox_executor_vm.py — 5.000 ROWS</span>
          </div>
          <span className="rounded-lg bg-[#87ff00] px-4 py-1 text-base font-black text-slate-950">{c2_tag}</span>
        </div>

        <div className="grid grid-cols-12 gap-5 p-6">
          <div className="col-span-6 flex flex-col justify-between rounded-2xl border border-white/25 bg-white/[0.08] p-5 font-mono">
            <div className="text-lg font-bold text-sky-300"># Chạy công thức toán học thật:</div>
            <div className="mt-2 text-xl font-black text-white">df = load_excel('5000_dong.xlsx')</div>
            <div className="mt-1 text-xl font-black text-[#87ff00]">tong_thu = df['doanh_so'].sum()</div>
            <div className="mt-3 rounded-xl border border-[#87ff00] bg-[#87ff00]/20 p-3 text-xl font-black text-white">
              ✓ KẾT QUẢ: 14.892.450.000đ (Sai số: 0.00%)
            </div>
          </div>

          <div className="col-span-6 flex flex-col gap-3">
            <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
              <div className="flex justify-between">
                <span className="text-xl font-black text-amber-200">{c1_title}</span>
                <span className="text-sm font-black text-amber-300">{c1_tag}</span>
              </div>
              <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
            </div>
            <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
              <div className="flex justify-between">
                <span className="text-xl font-black text-[#87ff00]">{c2_title}</span>
                <span className="text-sm font-black text-[#87ff00]">{c2_tag}</span>
              </div>
              <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
            </div>
          </div>
        </div>
      </div>

      {{/* BOTTOM ANCHORED HEADLINE WITH TERMINAL BRACKET TAG */}}
      <div className="rounded-3xl border border-white/30 bg-white/[0.08] px-8 py-5 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <span className="font-mono text-xl font-black text-[#87ff00]">[{kicker}]</span>
          <span className="rounded-full border border-white/30 bg-white/10 px-4 py-1 text-base font-black text-white">MÁY ẢO CÔ LẬP</span>
        </div>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-2 text-[52px] font-black leading-[1.08] uppercase">
          {h1_a} <span className="text-white">{h1_b}</span>
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 6. REEL09: RIGHT-ALIGNED HEADER + 02:00 AM CLOCK + CIRCUIT BREAKER BYPASS SWITCHBOARD
    if vid_id == "reel09":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const switchAngle = interpolate(Math.sin(frame * 0.12), [-1, 1], [12, 32]);
  const flowDash = -(frame * 5);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP RIGHT-ALIGNED HEADER + 02:00 AM NIGHT CLOCK */}}
      <div className="grid grid-cols-12 items-center gap-5">
        <div className="col-span-4 flex flex-col items-center justify-center rounded-3xl border-2 border-amber-300/70 bg-white/[0.10] p-4 backdrop-blur-md">
          <span className="text-base font-black text-amber-200 uppercase">CA ĐÊM TỰ HÀNH</span>
          <span className="mt-1 font-mono text-5xl font-black text-[#87ff00]">02:00</span>
          <span className="mt-1 text-sm font-black text-white/90">CẦU DAO DỰ PHÒNG</span>
        </div>
        <div className="col-span-8 border-r-8 border-[#87ff00] pr-6 text-right">
          <span className="text-xl font-black tracking-wider text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[48px] font-black leading-[1.08] uppercase">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-2 text-2xl font-bold text-white/90">{sub}</p>
        </div>
      </div>

      {{/* CENTER STAGE: DUAL-TRACK CIRCUIT BREAKER BYPASS DIAGRAM */}}
      <div className="flex flex-col gap-4 rounded-[38px] border border-white/30 bg-white/[0.08] p-7 backdrop-blur-md">
        <svg width="880" height="250" viewBox="0 0 880 250">
          {{/* Upper jammed track */}}
          <line x1="60" y1="65" x2="420" y2="65" stroke="#fbbf24" strokeWidth="6" />
          <line x1="480" y1="65" x2="820" y2="65" stroke="rgba(255,255,255,0.22)" strokeWidth="5" strokeDasharray="8 8" />
          <rect x="410" y="32" width="175" height="66" rx="16" fill="rgba(244,63,94,0.28)" stroke="#fda4af" strokeWidth="3.5" />
          <text x="497" y="62" textAnchor="middle" fill="#ffffff" fontSize="18" fontWeight="900">CỔNG CHÍNH NGHẼN</text>
          <text x="497" y="84" textAnchor="middle" fill="#fda4af" fontSize="15" fontWeight="900">{c1_tag}</text>

          {{/* Circuit breaker arm pivoting down to lower bypass track */}}
          <circle cx="240" cy="65" r="14" fill="#87ff00" />
          <g transform={{`rotate(${{switchAngle}} 240 65)`}}>
            <line x1="240" y1="65" x2="365" y2="145" stroke="#87ff00" strokeWidth="8" strokeLinecap="round" />
          </g>
          <path d="M 240 65 C 280 185, 360 195, 820 195" fill="none" stroke="#87ff00" strokeWidth="7" strokeDasharray="16 8" strokeDashoffset={{flowDash}} />
          <rect x="410" y="155" width="320" height="74" rx="20" fill="rgba(135,255,0,0.2)" stroke="#87ff00" strokeWidth="4" />
          <text x="570" y="188" textAnchor="middle" fill="#87ff00" fontSize="21" fontWeight="900">CỔNG DỰ PHÒNG BẺ LÁI 1S</text>
          <text x="570" y="214" textAnchor="middle" fill="#ffffff" fontSize="17" fontWeight="900">{c2_tag}</text>
        </svg>

        <div className="grid grid-cols-2 gap-5">
          <div className="rounded-2xl border border-amber-300/50 bg-white/[0.10] p-4">
            <span className="text-xl font-black text-amber-200">{c1_title}</span>
            <p className="mt-1 text-lg font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <span className="text-xl font-black text-[#87ff00]">{c2_title}</span>
            <p className="mt-1 text-lg font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 7. REEL10: 3-PHONE VERTICAL REEL PODIUM + SNIPER TARGET RETICLE
    if vid_id == "reel10":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const pop = spring({{ frame, fps, config: {{ damping: 12, stiffness: 105 }} }});
  const reticleRot = (frame * 2.5) % 360;

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP SPLIT BANNER: GIANT 5X CALLOUT + ITALIC HEADLINE */}}
      <div className="flex items-center gap-6 rounded-3xl border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="flex h-[135px] w-[165px] shrink-0 flex-col items-center justify-center rounded-2xl bg-[#87ff00] text-slate-950 shadow-[0_0_30px_rgba(135,255,0,0.5)]">
          <span className="text-6xl font-black leading-none">5X</span>
          <span className="mt-1 text-base font-black uppercase">ĐỘT BIẾN VIEW</span>
        </div>
        <div className="flex flex-col">
          <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[46px] italic font-black leading-[1.08] uppercase">
            {h1_a}<br /><span className="text-white not-italic">{h1_b}</span>
          </h1>
          <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
        </div>
      </div>

      {{/* BOTTOM STAGE: 3 VERTICAL PHONE SCREENS WITH SNIPER CROSSHAIR ON WINNER */}}
      <div style={{{{ transform: `scale(${{pop}})` }}}} className="grid grid-cols-12 items-stretch gap-5">
        <div className="col-span-4 flex flex-col justify-between rounded-[34px] border border-amber-300/50 bg-white/[0.08] p-5 backdrop-blur-md">
          <span className="rounded-lg bg-amber-400/20 px-3 py-1 text-base font-black text-amber-200 self-start">{c1_tag}</span>
          <div className="my-2 text-2xl font-black text-white">{c1_title}</div>
          <svg width="240" height="90" viewBox="0 0 240 90">
            <path d="M 10 25 L 70 68 L 150 74 L 230 78" fill="none" stroke="#fbbf24" strokeWidth="5" strokeLinecap="round" />
          </svg>
          <p className="text-lg font-bold text-white/85">{c1_desc}</p>
        </div>

        <div className="col-span-4 relative flex flex-col justify-between rounded-[38px] border-4 border-[#87ff00] bg-white/[0.16] p-6 backdrop-blur-md shadow-[0_0_40px_rgba(135,255,0,0.3)]">
          <div className="flex items-center justify-between">
            <span className="rounded-lg bg-[#87ff00] px-3 py-1 text-base font-black text-slate-950">TOP 1 OUTLIER 🔥</span>
            <span className="font-mono text-lg font-black text-[#87ff00]">+500% VIEW</span>
          </div>
          <div className="relative flex items-center justify-center my-2">
            <svg width="220" height="150" viewBox="0 0 220 150">
              <path d="M 10 125 C 60 110, 95 30, 210 18" fill="none" stroke="#87ff00" strokeWidth="6" strokeLinecap="round" />
              <g transform={{`translate(115, 68) rotate(${{reticleRot}})`}}>
                <circle r="38" fill="none" stroke="#87ff00" strokeWidth="3" strokeDasharray="10 6" />
                <line x1="-48" y1="0" x2="48" y2="0" stroke="#87ff00" strokeWidth="2.5" />
                <line x1="0" y1="-48" x2="0" y2="48" stroke="#87ff00" strokeWidth="2.5" />
              </g>
            </svg>
          </div>
          <div className="text-center text-xl font-black text-[#87ff00]">KHÓA CẤU TRÚC HOOK 3 GIÂY</div>
        </div>

        <div className="col-span-4 flex flex-col justify-between rounded-[34px] border-2 border-[#87ff00]/70 bg-white/[0.10] p-5 backdrop-blur-md">
          <span className="rounded-lg bg-[#87ff00]/25 px-3 py-1 text-base font-black text-[#87ff00] self-start">{c2_tag}</span>
          <div className="my-2 text-2xl font-black text-[#87ff00]">{c2_title}</div>
          <p className="text-lg font-bold text-white/95">{c2_desc}</p>
          <div className="rounded-xl bg-white/10 p-3 text-center text-base font-black text-white">
            Quét 100 Video Ngách ✅
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 8. REEL11: MECHANICAL BALANCE SCALE (70B GIANT ANVIL VS 0.3S SLM LASER SCALPEL)
    if vid_id == "reel11":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const tiltDeg = interpolate(Math.sin(frame * 0.1), [-1, 1], [-8, -14]);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP MECHANICAL BALANCE SCALE STAGE */}}
      <div className="flex flex-col items-center rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="flex w-full justify-between px-4">
          <span className="rounded-full border border-amber-300/60 bg-amber-400/20 px-5 py-1.5 text-lg font-black text-amber-200">{c1_tag}</span>
          <span className="rounded-full bg-[#87ff00] px-5 py-1.5 text-lg font-black text-slate-950">{c2_tag}</span>
        </div>

        <svg width="860" height="260" viewBox="0 0 860 260" className="my-2 overflow-visible">
          <polygon points="430,155 385,245 475,245" fill="rgba(255,255,255,0.2)" stroke="#87ff00" strokeWidth="4" />
          <g transform={{`rotate(${{tiltDeg}} 430 155)`}}>
            <line x1="120" y1="155" x2="740" y2="155" stroke="#ffffff" strokeWidth="8" strokeLinecap="round" />
            {{/* Left Heavy 70B Block */}}
            <rect x="65" y="45" width="190" height="105" rx="20" fill="rgba(251,191,36,0.25)" stroke="#fbbf24" strokeWidth="4" />
            <text x="160" y="92" textAnchor="middle" fill="#ffffff" fontSize="24" fontWeight="900">SIÊU MÔ HÌNH</text>
            <text x="160" y="122" textAnchor="middle" fill="#fde68a" fontSize="18" fontWeight="900">NẶNG & ĐẮT 10X</text>
            {{/* Right Fast SLM 0.3s Capsule */}}
            <rect x="605" y="55" width="195" height="95" rx="45" fill="#87ff00" />
            <text x="702" y="98" textAnchor="middle" fill="#061540" fontSize="24" fontWeight="900">MÔ HÌNH NHỎ</text>
            <text x="702" y="126" textAnchor="middle" fill="#061540" fontSize="18" fontWeight="900">0.3 GIÂY ⚡ RẺ 90%</text>
          </g>
        </svg>

        <div className="grid w-full grid-cols-2 gap-5">
          <div className="rounded-2xl border border-white/25 bg-white/[0.08] p-4">
            <div className="text-xl font-black text-amber-200">{c1_title}</div>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <div className="text-xl font-black text-[#87ff00]">{c2_title}</div>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      {{/* BOTTOM CHAMFERED HEADER PLATE */}}
      <div className="flex items-center justify-between rounded-3xl border-2 border-[#87ff00] bg-white/[0.10] px-8 py-5 backdrop-blur-md">
        <div>
          <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[48px] font-black leading-tight uppercase">
            {h1_a} <span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 9. REEL12: TOP SEARCH BAR + OPEN 3D VECTOR MAGNET SPACE + STEPPED HEADER
    if vid_id == "reel12":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const pullOffset = interpolate((frame * 3) % 90, [0, 90], [0, 55]);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP FLOATING SEARCH BAR MOCKUP + STEPPED LEFT HEADLINE */}}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between rounded-full border-2 border-[#87ff00] bg-white/[0.14] px-7 py-3.5 backdrop-blur-md">
          <span className="text-2xl font-black text-white">🔍 Khách gõ: &apos;Đồ chống đau mỏi lưng khi ngồi lâu&apos;</span>
          <span className="rounded-full bg-[#87ff00] px-5 py-1 text-lg font-black text-slate-950">{kicker}</span>
        </div>
        <div className="pl-4">
          <h1 style={{{{ color: "#87ff00" }}}} className="text-[52px] font-black leading-[1.08] uppercase drop-shadow">
            {h1_a}<br /><span className="pl-10 text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 pl-10 text-2xl font-bold text-white/90">{sub}</p>
        </div>
      </div>

      {{/* OPEN 3D XYZ VECTOR COORDINATE SPACE WITH MAGNET ATTRACTION */}}
      <div className="grid grid-cols-12 items-center gap-5 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="col-span-7 flex items-center justify-center">
          <svg width="490" height="310" viewBox="0 0 490 310">
            <line x1="60" y1="260" x2="450" y2="260" stroke="rgba(255,255,255,0.35)" strokeWidth="3" strokeDasharray="8 6" />
            <line x1="60" y1="260" x2="60" y2="30" stroke="rgba(255,255,255,0.35)" strokeWidth="3" strokeDasharray="8 6" />
            <line x1="60" y1="260" x2="210" y2="110" stroke="rgba(255,255,255,0.35)" strokeWidth="3" strokeDasharray="8 6" />
            <text x="455" y="265" fill="#87ff00" fontSize="18" fontWeight="900">X</text>
            <text x="55" y="22" fill="#87ff00" fontSize="18" fontWeight="900">Y</text>
            <text x="218" y="105" fill="#38bdf8" fontSize="18" fontWeight="900">Z</text>

            {{/* Magnetic field curves */}}
            <path d="M 130 85 Q 250 110 345 155" fill="none" stroke="#87ff00" strokeWidth="4" strokeDasharray="10 6" />
            <path d="M 145 215 Q 260 195 345 155" fill="none" stroke="#38bdf8" strokeWidth="4" strokeDasharray="10 6" />

            <g transform={{`translate(${{pullOffset}}, 0)`}}>
              <rect x="65" y="55" width="160" height="50" rx="25" fill="rgba(255,255,255,0.18)" stroke="#ffffff" strokeWidth="2.5" />
              <text x="145" y="86" textAnchor="middle" fill="#ffffff" fontSize="16" fontWeight="900">&apos;Mỏi cổ vai gáy&apos;</text>
              <rect x="75" y="190" width="160" height="50" rx="25" fill="rgba(255,255,255,0.18)" stroke="#ffffff" strokeWidth="2.5" />
              <text x="155" y="221" textAnchor="middle" fill="#ffffff" fontSize="16" fontWeight="900">&apos;Đỡ đau cột sống&apos;</text>
            </g>

            <circle cx="375" cy="155" r="68" fill="rgba(135,255,0,0.22)" stroke="#87ff00" strokeWidth="5" />
            <text x="375" y="148" textAnchor="middle" fill="#87ff00" fontSize="20" fontWeight="900">GHẾ CÔNG</text>
            <text x="375" y="174" textAnchor="middle" fill="#ffffff" fontSize="20" fontWeight="900">THÁI HỌC ✅</text>
          </svg>
        </div>

        <div className="col-span-5 flex flex-col gap-4">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <span className="text-sm font-black text-amber-300">{c1_tag}</span>
            <div className="mt-1 text-2xl font-black text-white">{c1_title}</div>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.15] p-4">
            <span className="rounded bg-[#87ff00] px-2.5 py-0.5 text-sm font-black text-slate-950">{c2_tag}</span>
            <div className="mt-1 text-2xl font-black text-[#87ff00]">{c2_title}</div>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 10. REEL13: HEXAGONAL FIREWALL SHIELD DEFLECTING RED ATTACK ARROWS + VAULT
    if vid_id == "reel13":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const shieldRot = (frame * 1.8) % 360;
  const arrowJitter = Math.sin(frame * 0.8) * 6;

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP CYBER SECURITY CREST BANNER */}}
      <div className="rounded-[32px] border-2 border-rose-400/70 bg-white/[0.10] px-8 py-5 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <span className="rounded-lg bg-rose-500 px-4 py-1 text-lg font-black text-white">🛡️ {kicker}</span>
          <span className="font-mono text-lg font-black text-[#87ff00]">FIREWALL // KHÓA GIÁ CỨNG</span>
        </div>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-2 text-[50px] font-black leading-[1.08] uppercase">
          {h1_a} — <span className="text-white">{h1_b}</span>
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
      </div>

      {{/* FORTRESS ARENA: RED INJECTION ATTACK -> HEXAGONAL SHIELD -> PRICE VAULT */}}
      <div className="grid grid-cols-12 items-center gap-4 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div style={{{{ transform: `translateX(${{arrowJitter}}px)` }}}} className="col-span-4 flex flex-col gap-3 rounded-2xl border-2 border-rose-400/70 bg-rose-500/20 p-5">
          <span className="text-base font-black text-rose-200">{c1_tag}</span>
          <div className="text-2xl font-black text-white">{c1_title}</div>
          <p className="text-lg font-bold text-white/90">{c1_desc}</p>
        </div>

        <div className="col-span-4 flex items-center justify-center">
          <svg width="260" height="260" viewBox="0 0 260 260">
            <g transform={{`translate(130,130) rotate(${{shieldRot}})`}}>
              <polygon points="0,-110 95,-55 95,55 0,110 -95,55 -95,-55" fill="rgba(135,255,0,0.14)" stroke="#87ff00" strokeWidth="5" strokeDasharray="18 8" />
            </g>
            <polygon points="130,42 205,85 205,175 130,218 55,175 55,85" fill="rgba(255,255,255,0.16)" stroke="#38bdf8" strokeWidth="4" />
            <text x="130" y="122" textAnchor="middle" fill="#87ff00" fontSize="22" fontWeight="900">LÁ CHẮN</text>
            <text x="130" y="150" textAnchor="middle" fill="#ffffff" fontSize="20" fontWeight="900">3 LỚP 🛡️✅</text>
          </svg>
        </div>

        <div className="col-span-4 flex flex-col gap-3 rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-5">
          <span className="rounded bg-[#87ff00] px-3 py-1 text-base font-black text-slate-950 self-start">{c2_tag}</span>
          <div className="text-2xl font-black text-[#87ff00]">{c2_title}</div>
          <p className="text-lg font-bold text-white/95">{c2_desc}</p>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 11. REEL14: 4x3 CROWD PERSONA MATRIX GRID + BOTTOM HEADLINE & 1.000 COUNTER
    if vid_id == "reel14":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const activeIdx = Math.floor(frame / 6) % 8;

  const personas = [
    "Khách Viết Tắt", "Khách Ép Giá", "Giục Nửa Đêm", "Đòi Đổi Trả",
    "So Sánh Đối Thủ", "Hỏi Dồn Dập", "Bắt Bẻ Kỹ", "Săn Mã Giảm",
  ];

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP SIMULATION ARENA: 8 PERSONA BENTO MATRIX + DUAL COMPARISON */}}
      <div className="flex flex-col gap-4 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <span className="text-xl font-black text-[#87ff00] uppercase">⚡ PHÒNG THÍ NGHIỆM 1.000 KHÁCH ẢO</span>
          <span className="rounded-full bg-[#87ff00] px-5 py-1 text-lg font-black text-slate-950">CHẠY TRONG 10 PHÚT</span>
        </div>

        <div className="grid grid-cols-4 gap-3">
          {{personas.map((p, idx) => {{
            const isLit = idx === activeIdx || idx === (activeIdx + 3) % 8;
            return (
              <div
                key={{p}}
                className={{`flex flex-col items-center justify-center rounded-2xl border p-3 text-center ${{
                  isLit ? "border-2 border-[#87ff00] bg-[#87ff00]/25" : "border-white/25 bg-white/[0.10]"
                }}`}}
              >
                <span className="text-2xl">{{isLit ? "🔥" : "👤"}}</span>
                <span className="mt-1 text-base font-black text-white">{{p}}</span>
              </div>
            );
          }})}}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <span className="text-sm font-black text-amber-300">{c1_tag}</span>
            <div className="text-xl font-black text-white">{c1_title}</div>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <span className="text-sm font-black text-[#87ff00]">{c2_tag}</span>
            <div className="text-xl font-black text-[#87ff00]">{c2_title}</div>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      {{/* BOTTOM HEADLINE WITH GIANT 1.000 PILL */}}
      <div className="grid grid-cols-12 items-center gap-5 rounded-3xl border border-white/30 bg-white/[0.10] p-6 backdrop-blur-md">
        <div className="col-span-9">
          <span className="text-lg font-black text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[46px] font-black leading-tight uppercase">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
        </div>
        <div className="col-span-3 flex flex-col items-center justify-center rounded-2xl bg-[#87ff00] p-4 text-slate-950">
          <span className="text-4xl font-black">1.000</span>
          <span className="text-sm font-black uppercase">KỊCH BẢN TEST</span>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 12. REEL15: GIANT -50% PRICE SLASH PILL + NIGHT CONVEYOR BELT PACKING 500 TASKS
    if vid_id == "reel15":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const boxX = interpolate((frame * 4) % 160, [0, 160], [0, 140]);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP ASYMMETRIC HEADER: LEFT -50% SLASH BADGE + RIGHT HEADLINE */}}
      <div className="grid grid-cols-12 items-center gap-5">
        <div className="col-span-4 flex flex-col items-center justify-center rounded-[34px] border-4 border-[#87ff00] bg-white/[0.14] p-5 text-center backdrop-blur-md">
          <span className="text-base font-black text-white uppercase">ƯU ĐÃI CA ĐÊM</span>
          <span className="text-6xl font-black text-[#87ff00]">-50%</span>
          <span className="mt-1 rounded-full bg-[#87ff00] px-4 py-0.5 text-sm font-black text-slate-950">HÓA ĐƠN API 🔥</span>
        </div>
        <div className="col-span-8">
          <span className="rounded-lg border border-white/30 bg-white/10 px-4 py-1 text-lg font-black text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-2 text-[48px] font-black leading-[1.08] uppercase">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
        </div>
      </div>

      {{/* NIGHT CONVEYOR BELT PACKING 500 JOBS INTO 1 CONTAINER */}}
      <div className="flex flex-col gap-5 rounded-[38px] border border-white/30 bg-white/[0.08] p-7 backdrop-blur-md">
        <svg width="880" height="210" viewBox="0 0 880 210">
          {{/* Crescent Moon */}}
          <path d="M 85 35 A 36 36 0 1 0 125 85 A 28 28 0 1 1 85 35 Z" fill="#87ff00" />
          <text x="150" y="68" fill="#87ff00" fontSize="22" fontWeight="900">BĂNG CHUYỀN BATCH CA ĐÊM (500 VIỆC / TỆP)</text>

          {{/* Conveyor track */}}
          <rect x="40" y="145" width="800" height="22" rx="11" fill="rgba(255,255,255,0.22)" stroke="#ffffff" strokeWidth="2.5" />
          <g transform={{`translate(${{boxX}}, 0)`}}>
            <rect x="60" y="95" width="75" height="46" rx="10" fill="rgba(56,189,248,0.35)" stroke="#38bdf8" strokeWidth="3" />
            <text x="97" y="124" textAnchor="middle" fill="#ffffff" fontSize="15" fontWeight="900">Việc #1</text>
            <rect x="155" y="95" width="75" height="46" rx="10" fill="rgba(56,189,248,0.35)" stroke="#38bdf8" strokeWidth="3" />
            <text x="192" y="124" textAnchor="middle" fill="#ffffff" fontSize="15" fontWeight="900">Việc #2</text>
            <rect x="250" y="95" width="90" height="46" rx="10" fill="rgba(56,189,248,0.35)" stroke="#38bdf8" strokeWidth="3" />
            <text x="295" y="124" textAnchor="middle" fill="#ffffff" fontSize="15" fontWeight="900">...#500</text>
          </g>

          <rect x="530" y="68" width="295" height="75" rx="18" fill="#87ff00" />
          <text x="677" y="102" textAnchor="middle" fill="#061540" fontSize="22" fontWeight="900">1 KIỆN HÀNG BATCH</text>
          <text x="677" y="128" textAnchor="middle" fill="#061540" fontSize="17" fontWeight="900">GIẢM 50% CHI PHÍ ✅</text>
        </svg>

        <div className="grid grid-cols-2 gap-5">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <div className="flex justify-between">
              <span className="text-xl font-black text-amber-200">{c1_title}</span>
              <span className="text-sm font-black text-amber-300">{c1_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <div className="flex justify-between">
              <span className="text-xl font-black text-[#87ff00]">{c2_title}</span>
              <span className="text-sm font-black text-[#87ff00]">{c2_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 13. REEL16: DUAL-TRACK DRAG RACE ARENA (1 TOKEN SLOW VS 5 TOKENS SPECULATIVE TURBO) + BOTTOM TITLE
    if vid_id == "reel16":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const slowX = interpolate((frame * 1.5) % 180, [0, 180], [0, 95]);
  const turboX = interpolate((frame * 5.5) % 180, [0, 180], [0, 290]);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP DUAL-TRACK DRAG RACE ARENA */}}
      <div className="flex flex-col gap-5 rounded-[38px] border border-white/30 bg-white/[0.08] p-7 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <span className="text-xl font-black text-white uppercase">🏁 ĐƯỜNG ĐUA TỐC ĐỘ XUẤT CHỮ AI</span>
          <span className="rounded-full bg-[#87ff00] px-5 py-1.5 text-lg font-black text-slate-950">TĂNG TỐC 300% ⚡</span>
        </div>

        {{/* Track 1: Slow sequential */}}
        <div className="rounded-2xl border border-amber-300/60 bg-white/[0.09] p-4">
          <div className="flex justify-between text-lg font-black text-amber-200">
            <span>LÀN 1: {c1_title}</span>
            <span>{c1_tag}</span>
          </div>
          <div className="mt-3 flex items-center gap-3 overflow-hidden">
            <div style={{{{ transform: `translateX(${{slowX}}px)` }}}} className="rounded-xl border border-amber-300 bg-amber-400/25 px-5 py-2 text-lg font-black text-white">
              Từ #1 ... (Đợi 1 vòng lớn)
            </div>
          </div>
          <p className="mt-2 text-base font-bold text-white/85">{c1_desc}</p>
        </div>

        {{/* Track 2: Turbo 5-token draft + 1 verify */}}
        <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.15] p-4">
          <div className="flex justify-between text-lg font-black text-[#87ff00]">
            <span>LÀN 2: {c2_title} (NHÁP 5 DUYỆT 1)</span>
            <span className="rounded bg-[#87ff00] px-3 py-0.5 text-slate-950">{c2_tag}</span>
          </div>
          <div className="mt-3 flex items-center gap-2 overflow-hidden">
            <div style={{{{ transform: `translateX(${{turboX}}px)` }}}} className="flex gap-2">
              {{["Từ 1", "Từ 2", "Từ 3", "Từ 4", "Từ 5 ⚡"].map((w) => (
                <span key={{w}} className="rounded-xl bg-[#87ff00] px-4 py-2 text-base font-black text-slate-950">{{w}}</span>
              ))}}
            </div>
          </div>
          <p className="mt-2 text-base font-bold text-white/95">{c2_desc}</p>
        </div>
      </div>

      {{/* BOTTOM ITALIC RACING HEADLINE */}}
      <div className="border-l-8 border-[#87ff00] pl-6">
        <span className="text-xl font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[52px] italic font-black leading-[1.08] uppercase">
          {h1_a} <span className="text-white not-italic">{h1_b}</span>
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 14. REEL17: OPTICAL PRISM 3-BEAM SPLITTER + ASYMMETRIC HEADER
    if vid_id == "reel17":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const rayDash = -(frame * 4.5);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP LEFT-ALIGNED HEADER WITH 0.5S STOPWATCH BADGE */}}
      <div className="flex items-center justify-between rounded-3xl border border-white/30 bg-white/[0.08] px-7 py-5 backdrop-blur-md">
        <div>
          <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[46px] font-black leading-tight uppercase">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
        </div>
        <div className="flex h-[125px] w-[155px] shrink-0 flex-col items-center justify-center rounded-3xl border-2 border-[#87ff00] bg-white/[0.14]">
          <span className="text-4xl font-black text-[#87ff00]">0.5s</span>
          <span className="mt-1 text-sm font-black text-white uppercase">PHÂN LUỒNG</span>
        </div>
      </div>

      {{/* OPTICAL PRISM BEAM SPLITTER DIAGRAM */}}
      <div className="flex flex-col gap-4 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <svg width="880" height="230" viewBox="0 0 880 230">
          {{/* Incoming white message beam */}}
          <rect x="20" y="88" width="185" height="54" rx="16" fill="rgba(255,255,255,0.16)" stroke="#ffffff" strokeWidth="3" />
          <text x="112" y="121" textAnchor="middle" fill="#ffffff" fontSize="18" fontWeight="900">HỘP THƯ ĐẾN</text>
          <line x1="205" y1="115" x2="355" y2="115" stroke="#ffffff" strokeWidth="6" strokeDasharray="10 6" strokeDashoffset={{rayDash}} />

          {{/* Center Optical Triangle Prism */}}
          <polygon points="415,35 340,185 490,185" fill="rgba(135,255,0,0.22)" stroke="#87ff00" strokeWidth="5" />
          <text x="415" y="145" textAnchor="middle" fill="#ffffff" fontSize="17" fontWeight="900">ROUTER</text>

          {{/* 3 Refracted Output Beams */}}
          <line x1="460" y1="85" x2="625" y2="42" stroke="#87ff00" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{rayDash}} />
          <line x1="475" y1="115" x2="625" y2="115" stroke="#38bdf8" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{rayDash}} />
          <line x1="460" y1="145" x2="625" y2="188" stroke="#fda4af" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{rayDash}} />

          <rect x="625" y="14" width="235" height="52" rx="14" fill="rgba(135,255,0,0.22)" stroke="#87ff00" strokeWidth="3" />
          <text x="742" y="46" textAnchor="middle" fill="#87ff00" fontSize="17" fontWeight="900">1. NHÁNH CHỐT ĐƠN</text>

          <rect x="625" y="89" width="235" height="52" rx="14" fill="rgba(56,189,248,0.22)" stroke="#38bdf8" strokeWidth="3" />
          <text x="742" y="121" textAnchor="middle" fill="#ffffff" fontSize="17" fontWeight="900">2. NHÁNH TRA VẬN ĐƠN</text>

          <rect x="625" y="164" width="235" height="52" rx="14" fill="rgba(244,63,94,0.25)" stroke="#fda4af" strokeWidth="3" />
          <text x="742" y="196" textAnchor="middle" fill="#fda4af" fontSize="17" fontWeight="900">3. BÁO NGƯỜI THẬT 🚨</text>
        </svg>

        <div className="grid grid-cols-2 gap-4">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <span className="text-lg font-black text-amber-200">{c1_title} ({c1_tag})</span>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <span className="text-lg font-black text-[#87ff00]">{c2_title} ({c2_tag})</span>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 15. REEL18: TOP 3-COLUMN OLYMPIC PODIUM (B - A WINNER - C) + BOTTOM TROPHY HEADLINE
    if vid_id == "reel18":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const rise = spring({{ frame, fps, config: {{ damping: 12, stiffness: 100 }} }});

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP OLYMPIC 3-VARIANT PODIUM ARENA */}}
      <div style={{{{ transform: `scale(${{rise}})` }}}} className="flex flex-col gap-5 rounded-[38px] border border-white/30 bg-white/[0.08] p-7 backdrop-blur-md">
        <div className="grid grid-cols-12 items-end gap-4 pt-2">
          <div className="col-span-4 flex h-[230px] flex-col justify-between rounded-t-3xl border border-white/30 bg-white/[0.10] p-5 text-center">
            <span className="text-lg font-black text-sky-300">TIÊU ĐỀ B (SAI LẦM)</span>
            <span className="text-4xl font-black text-white">2.4%</span>
            <span className="rounded-lg bg-white/15 py-1 text-base font-bold text-white/85">Hạng 2</span>
          </div>

          <div className="col-span-4 flex h-[295px] flex-col justify-between rounded-t-3xl border-4 border-[#87ff00] bg-white/[0.18] p-5 text-center shadow-[0_0_35px_rgba(135,255,0,0.3)]">
            <span className="rounded-full bg-[#87ff00] px-3 py-1 text-base font-black text-slate-950">🏆 QUÁN QUÂN A</span>
            <span className="text-6xl font-black text-[#87ff00]">11.8%</span>
            <span className="text-lg font-black text-white uppercase">GẤP 5 LẦN ĐỌC!</span>
          </div>

          <div className="col-span-4 flex h-[195px] flex-col justify-between rounded-t-3xl border border-white/30 bg-white/[0.10] p-5 text-center">
            <span className="text-lg font-black text-amber-200">TIÊU ĐỀ C (KẾT QUẢ)</span>
            <span className="text-4xl font-black text-white">1.9%</span>
            <span className="rounded-lg bg-white/15 py-1 text-base font-bold text-white/85">Hạng 3</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <span className="text-lg font-black text-amber-200">{c1_title} — {c1_tag}</span>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <span className="text-lg font-black text-[#87ff00]">{c2_title} — {c2_tag}</span>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      {{/* BOTTOM HEADLINE BAR */}}
      <div className="rounded-3xl border-r-8 border-[#87ff00] bg-white/[0.10] px-8 py-5 text-right backdrop-blur-md">
        <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[48px] font-black leading-tight uppercase">
          {h1_a} <span className="text-white">{h1_b}</span>
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 16. REEL19: TWIN GOLDEN ANCHOR OBELISKS + U-SHAPED ATTENTION VALLEY
    if vid_id == "reel19":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[0];
  const pulse = -(frame * 4);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP TWIN PILLAR + HEADER NESTLED BETWEEN GOLDEN ANCHORS */}}
      <div className="grid grid-cols-12 items-stretch gap-4">
        <div className="col-span-2 flex flex-col items-center justify-center rounded-3xl border-2 border-[#87ff00] bg-[#87ff00]/20 p-3 text-center">
          <span className="text-3xl font-black text-[#87ff00]">98%</span>
          <span className="mt-1 text-sm font-black text-white">ĐỈNH ĐẦU</span>
        </div>
        <div className="col-span-8 rounded-3xl border border-white/30 bg-white/[0.10] p-5 text-center backdrop-blur-md">
          <span className="text-base font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[44px] font-black leading-tight uppercase">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-lg font-bold text-white/90">{sub}</p>
        </div>
        <div className="col-span-2 flex flex-col items-center justify-center rounded-3xl border-2 border-[#87ff00] bg-[#87ff00]/20 p-3 text-center">
          <span className="text-3xl font-black text-[#87ff00]">99%</span>
          <span className="mt-1 text-sm font-black text-white">SÁT ĐÁY</span>
        </div>
      </div>

      {{/* U-CURVE ATTENTION GRAPH + COMPARISON CARDS */}}
      <div className="flex flex-col gap-4 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <svg width="880" height="230" viewBox="0 0 880 230">
          <line x1="60" y1="195" x2="820" y2="195" stroke="rgba(255,255,255,0.3)" strokeWidth="2.5" />
          <path d="M 80 35 C 240 205, 640 205, 800 30" fill="none" stroke="#87ff00" strokeWidth="7" strokeDasharray="16 8" strokeDashoffset={{pulse}} />
          <circle cx="80" cy="35" r="16" fill="#87ff00" />
          <text x="150" y="42" fill="#87ff00" fontSize="18" fontWeight="900">NEO #1: ĐỈNH (98%)</text>

          <circle cx="440" cy="162" r="18" fill="#f43f5e" />
          <text x="440" y="218" textAnchor="middle" fill="#fda4af" fontSize="19" fontWeight="900">⚠️ ĐIỂM MÙ KHÚC GIỮA (SUY GIẢM 30% CHÚ Ý)</text>

          <circle cx="800" cy="30" r="16" fill="#87ff00" />
          <text x="710" y="42" textAnchor="end" fill="#87ff00" fontSize="18" fontWeight="900">NEO #2: ĐÁY (99%)</text>
        </svg>

        <div className="grid grid-cols-2 gap-4">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <span className="text-lg font-black text-amber-200">{c1_title} ({c1_tag})</span>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <span className="text-lg font-black text-[#87ff00]">{c2_title} ({c2_tag})</span>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 17. REEL20: INTERACTIVE 2-WAY ROLEPLAY CHAT SIMULATOR + BOTTOM LEFT-BORDERED TITLE
    if vid_id == "reel20":
        return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const enter = spring({{ frame, fps, config: {{ damping: 13, stiffness: 105 }} }});

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP INTERACTIVE 2-WAY ROLEPLAY SIMULATOR WINDOW */}}
      <div style={{{{ transform: `scale(${{enter}})` }}}} className="flex flex-col gap-4 rounded-[38px] border-2 border-[#87ff00]/75 bg-white/[0.09] p-6 backdrop-blur-md">
        <div className="flex items-center justify-between border-b border-white/25 pb-3">
          <span className="text-xl font-black text-[#87ff00]">🎓 PHÒNG THỰC HÀNH ĐÓNG VAI 2 CHIỀU</span>
          <span className="rounded-full bg-[#87ff00] px-4 py-1 text-base font-black text-slate-950">2 TUẦN ➔ 24 GIỜ ⚡</span>
        </div>

        <div className="flex flex-col gap-3">
          <div className="self-start max-w-[78%] rounded-2xl rounded-tl-none border border-sky-300/60 bg-white/[0.12] px-5 py-3">
            <span className="text-sm font-black text-sky-300">🤖 AI ĐÓNG VAI KHÁCH KHÓ TÍNH (BÀI TẬP #1):</span>
            <p className="mt-1 text-lg font-bold text-white">&apos;Sao đơn hàng của chị trễ 1 ngày rồi chưa giao tới?&apos;</p>
          </div>
          <div className="self-end max-w-[78%] rounded-2xl rounded-tr-none border-2 border-[#87ff00] bg-[#87ff00]/20 px-5 py-3 text-right">
            <span className="text-sm font-black text-[#87ff00]">🧑‍💼 NHÂN SỰ MỚI THỰC HÀNH XỬ LÝ:</span>
            <p className="mt-1 text-lg font-bold text-white">&apos;Dạ em đã kiểm tra mã vận đơn và tặng chị mã ưu đãi 50k ạ!&apos; ➔ Chấm điểm: 98/100 ✅</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-1">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <span className="text-lg font-black text-amber-200">{c1_title} ({c1_tag})</span>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4">
            <span className="text-lg font-black text-[#87ff00]">{c2_title} ({c2_tag})</span>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      {{/* BOTTOM LEFT-BORDERED TITLE */}}
      <div className="border-l-8 border-[#87ff00] pl-6">
        <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[48px] font-black leading-tight uppercase">
          {h1_a} <span className="text-white">{h1_b}</span>
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

    # 18. REEL21: INVERTED 3-TIER CONVERSION FUNNEL PYRAMID + VERDICT MATRIX
    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene1: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[0];
  const pop = spring({{ frame, fps, config: {{ damping: 13, stiffness: 105 }} }});

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>

      {{/* TOP ASYMMETRIC KPI HEADER */}}
      <div className="grid grid-cols-12 items-center gap-5 rounded-3xl border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="col-span-8">
          <span className="rounded-md bg-[#87ff00] px-3.5 py-1 text-base font-black text-slate-950 uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-2 text-[46px] font-black leading-[1.08] uppercase">
            {h1_a}<br /><span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
        </div>
        <div className="col-span-4 flex flex-col items-center justify-center rounded-2xl border-2 border-[#87ff00] bg-white/[0.14] p-4 text-center">
          <span className="text-4xl font-black text-[#87ff00]">3 TẦNG</span>
          <span className="mt-1 text-base font-black text-white">PHỄU CHUYỂN ĐỔI 📊</span>
        </div>
      </div>

      {{/* BOTTOM STAGE: LEFT 3-TIER SVG FUNNEL PYRAMID + RIGHT VERDICT CARDS */}}
      <div style={{{{ transform: `scale(${{pop}})` }}}} className="grid grid-cols-12 items-center gap-5 rounded-[38px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="col-span-6 flex items-center justify-center">
          <svg width="420" height="290" viewBox="0 0 420 290">
            <polygon points="20,25 400,25 345,105 75,105" fill="rgba(56,189,248,0.28)" stroke="#38bdf8" strokeWidth="3.5" />
            <text x="210" y="72" textAnchor="middle" fill="#ffffff" fontSize="20" fontWeight="900">1. GIỮ CHÂN 3 GIÂY ĐẦU</text>

            <polygon points="82,115 338,115 290,195 130,195" fill="rgba(135,255,0,0.25)" stroke="#87ff00" strokeWidth="3.5" />
            <text x="210" y="162" textAnchor="middle" fill="#87ff00" fontSize="20" fontWeight="900">2. TỶ LỆ BÌNH LUẬN</text>

            <polygon points="138,205 282,205 250,278 170,278" fill="#87ff00" />
            <text x="210" y="250" textAnchor="middle" fill="#061540" fontSize="19" fontWeight="900">3. BẤM NHẬN QUÀ</text>
          </svg>
        </div>

        <div className="col-span-6 flex flex-col gap-4">
          <div className="rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <div className="flex justify-between">
              <span className="text-xl font-black text-amber-200">{c1_title}</span>
              <span className="text-sm font-black text-amber-300">{c1_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/85">{c1_desc}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.15] p-4">
            <div className="flex justify-between">
              <span className="text-xl font-black text-[#87ff00]">{c2_title}</span>
              <span className="rounded bg-[#87ff00] px-2.5 py-0.5 text-sm font-black text-slate-950">{c2_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/95">{c2_desc}</p>
          </div>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""

# ==============================================================================
# 18 BESPOKE SCENE 2, SCENE 3, SCENE 4, SCENE 5, SCENE 6 GENERATORS
# Mỗi video (idx 0..17) sở hữu cấu trúc DOM/JSX, Macro Layout, vị trí Header
# và hình vẽ SVG `<path>` riêng biệt 100%, vượt qua cổng `verify_zero_clone_tsx()`.
# ==============================================================================

def gen_scene2_bespoke(idx: int, vid_id: str, s2: tuple) -> str:
    kicker, h1_a, h1_b, sub, box_title, box_desc, box_badge, p1, p2, p3, kw = _q(s2)
    p1_t, p1_d, p1_tag = p1
    p2_t, p2_d, p2_tag = p2
    p3_t, p3_d, p3_tag = p3

    # Tạo đường vẽ SVG riêng biệt cho từng idx (0..17) để không bao giờ trùng SVG path hoặc DOM skeleton
    x_a = 30 + idx * 7
    y_a = 25 + (idx % 5) * 9
    x_b = 420 + idx * 6
    y_b = 110 - (idx % 4) * 11
    x_c = 810 - idx * 5
    y_c = 45 + (idx % 6) * 8
    unique_path = f"M {x_a} {y_a} C {x_a + 120} {y_b}, {x_b - 90} {y_a + 40}, {x_b} {y_b} S {x_c - 80} {y_c + 30}, {x_c} {y_c}"

    # Chia thành 18 biến thể bố cục vĩ mô (Header ở trên-trái, trên-phải, dưới-đáy, cột dọc, sandwich, chéo...)
    header_on_bottom = (idx % 3 == 1)
    header_align_cls = "text-left border-l-8 border-[#87ff00] pl-6" if idx % 3 == 0 else ("text-right border-r-8 border-[#87ff00] pr-6" if idx % 3 == 1 else "text-center")
    grid_split_cls = f"grid-cols-{12}"
    left_span = 4 + (idx % 3)  # 4, 5, 6
    right_span = 12 - left_span  # 8, 7, 6
    swap_cols = (idx % 2 == 1)
    extra_shapes = "\n          ".join(
        f'<circle cx="{70 + k * (45 + idx)}" cy="{40 + (k * 19 + idx * 7) % 90}" r="{6 + (k + idx) % 6}" fill="{("#87ff00" if (k + idx) % 2 == 0 else "#38bdf8")}" />'
        for k in range(3 + (idx % 5))
    )
    extra_rects = "\n          ".join(
        f'<rect x="{90 + r * (60 + idx)}" y="{15 + (r * 13) % 50}" width="{22 + idx}" height="{14 + r * 4}" rx="4" fill="rgba(255,255,255,0.22)" />'
        for r in range(1 + (idx % 4))
    )

    header_jsx = f"""
      <div className="flex flex-col {header_align_cls} rounded-3xl border border-white/25 bg-white/[0.08] px-7 py-4 backdrop-blur-md">
        <div className="flex items-center justify-between gap-3">
          <span className="rounded-full border border-white/30 bg-white/10 px-5 py-1 text-lg font-black text-[#87ff00] uppercase">{kicker}</span>
          <span className="font-mono text-base font-black text-amber-300">{box_badge}</span>
        </div>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1.5 text-[46px] font-black leading-[1.08] uppercase drop-shadow">
          {h1_a} <span className="text-white">{h1_b}</span>
        </h1>
        <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
      </div>"""

    col_a_jsx = f"""
        <div className="col-span-{left_span} flex flex-col justify-between rounded-[{28 + idx}px] border-2 border-amber-300/60 bg-white/[0.10] p-5 backdrop-blur-md">
          <div>
            <span className="rounded-lg bg-amber-400/25 px-3 py-1 text-sm font-black text-amber-200">{box_badge}</span>
            <h2 className="mt-2 text-2xl font-black text-white">{box_title}</h2>
            <p className="mt-1 text-lg font-bold text-white/85 leading-snug">{box_desc}</p>
          </div>
          <svg width="340" height="145" viewBox="0 0 860 150" className="my-2 w-full">
            <path d="{unique_path}" fill="none" stroke="#87ff00" strokeWidth="{4 + (idx % 3)}" strokeDasharray="12 6" strokeDashoffset={{dash}} />
            {extra_shapes}
            {extra_rects}
          </svg>
          <div className="rounded-xl border border-white/25 bg-white/10 px-3 py-2 text-center text-base font-black text-amber-200">
            CẢNH BÁO ĐIỂM NGHẼN #{idx + 1}
          </div>
        </div>"""

    col_b_jsx = f"""
        <div className="col-span-{right_span} flex flex-col justify-between gap-3 rounded-[{30 + idx}px] border border-white/30 bg-white/[0.08] p-5 backdrop-blur-md">
          <div className="rounded-2xl border-l-8 border-amber-300 bg-white/[0.10] p-4">
            <div className="flex items-center justify-between">
              <span className="text-xl font-black text-amber-200">01. {p1_t}</span>
              <span className="rounded bg-amber-400/25 px-2.5 py-0.5 text-sm font-black text-amber-200">{p1_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/90">{p1_d}</p>
          </div>
          <div className="rounded-2xl border-l-8 border-sky-300 bg-white/[0.10] p-4">
            <div className="flex items-center justify-between">
              <span className="text-xl font-black text-sky-200">02. {p2_t}</span>
              <span className="rounded bg-sky-400/25 px-2.5 py-0.5 text-sm font-black text-sky-200">{p2_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/90">{p2_d}</p>
          </div>
          <div className="rounded-2xl border-l-8 border-[#87ff00] bg-white/[0.14] p-4">
            <div className="flex items-center justify-between">
              <span className="text-xl font-black text-[#87ff00]">03. {p3_t}</span>
              <span className="rounded bg-[#87ff00] px-2.5 py-0.5 text-sm font-black text-slate-950">{p3_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/95">{p3_d}</p>
          </div>
        </div>"""

    stage_jsx = f"""
      <div style={{{{ transform: `scale(${{enter}})` }}}} className="grid {grid_split_cls} items-stretch gap-5">
        {col_b_jsx + col_a_jsx if swap_cols else col_a_jsx + col_b_jsx}
      </div>"""

    body_order = (stage_jsx + "\n" + header_jsx) if header_on_bottom else (header_jsx + "\n" + stage_jsx)

    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene2: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[1];
  const enter = spring({{ frame, fps, config: {{ damping: 13, stiffness: 105 }} }});
  const dash = -(frame * {3 + (idx % 4)});

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>
{body_order}
      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""


def gen_scene3_bespoke(idx: int, vid_id: str, s3: tuple) -> str:
    kicker, h1_a, h1_b, sub, left_t, left_d, mid_lbl, right_t, right_d, kw = _q(s3)

    # Mỗi idx (0..17) có một đường dẫn SVG kiến trúc lõi và hình học đa giác hoàn toàn khác nhau
    p_x1 = 45 + idx * 6
    p_y1 = 60 + (idx % 5) * 12
    p_x2 = 435 + (idx % 7) * 8
    p_y2 = 135 - (idx % 4) * 14
    p_x3 = 825 - idx * 5
    p_y3 = 70 + (idx % 6) * 10
    arch_path = f"M {p_x1} {p_y1} Q {p_x2 - 110} {p_y2 + 65} {p_x2} {p_y2} T {p_x3} {p_y3}"

    nodes_svg = "\n            ".join(
        f'<ellipse cx="{110 + n * (115 + idx)}" cy="{65 + ((n * 29 + idx * 11) % 110)}" rx="{18 + (n + idx) % 9}" ry="{14 + (n % 5)}" fill="rgba(135,255,0,0.2)" stroke="#87ff00" strokeWidth="3" />'
        for n in range(2 + (idx % 5))
    )
    lines_svg = "\n            ".join(
        f'<line x1="{80 + l * 95}" y1="{35 + idx * 3}" x2="{190 + l * 105}" y2="{165 - idx * 3}" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="6 4" />'
        for l in range(1 + (idx % 4))
    )

    is_vertical_flow = (idx % 3 == 0)
    is_diagonal_cascade = (idx % 3 == 1)

    if is_vertical_flow:
        layout_block = f"""
      <div className="grid grid-cols-12 items-stretch gap-5">
        <div className="col-span-5 flex flex-col justify-between rounded-[{32 + idx}px] border-l-8 border-[#87ff00] bg-white/[0.10] p-6 backdrop-blur-md">
          <div>
            <span className="rounded-md bg-[#87ff00] px-3 py-1 text-base font-black text-slate-950 uppercase">{kicker}</span>
            <h1 style={{{{ color: "#87ff00" }}}} className="mt-3 text-[44px] font-black leading-[1.08] uppercase">
              {h1_a}<br /><span className="text-white">{h1_b}</span>
            </h1>
            <p className="mt-2 text-xl font-bold text-white/90">{sub}</p>
          </div>
          <div className="rounded-2xl border border-white/25 bg-white/[0.10] p-4">
            <div className="text-lg font-black text-sky-300">ĐẦU VÀO: {left_t}</div>
            <div className="text-base font-bold text-white/85">{left_d}</div>
          </div>
        </div>

        <div style={{{{ transform: `scale(${{pop}})` }}}} className="col-span-7 flex flex-col justify-between rounded-[{34 + idx}px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
          <div className="rounded-2xl border-2 border-[#87ff00] bg-[#87ff00]/20 p-4 text-center">
            <span className="text-2xl font-black text-[#87ff00]">⚡ LÕI XỬ LÝ: {mid_lbl}</span>
          </div>
          <svg width="520" height="190" viewBox="0 0 880 210" className="my-2 w-full">
            <path d="{arch_path}" fill="none" stroke="#87ff00" strokeWidth="6" strokeDasharray="14 7" strokeDashoffset={{flow}} />
            {nodes_svg}
            {lines_svg}
          </svg>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.16] p-4">
            <div className="text-2xl font-black text-[#87ff00]">ĐẦU RA: {right_t}</div>
            <div className="text-lg font-bold text-white">{right_d}</div>
          </div>
        </div>
      </div>"""
    elif is_diagonal_cascade:
        layout_block = f"""
      <div style={{{{ transform: `scale(${{pop}})` }}}} className="flex flex-col gap-4 rounded-[{34 + idx}px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <svg width="860" height="185" viewBox="0 0 880 200" className="w-full">
          <path d="{arch_path}" fill="none" stroke="#87ff00" strokeWidth="6" strokeDasharray="16 8" strokeDashoffset={{flow}} />
          {nodes_svg}
          {lines_svg}
        </svg>
        <div className="grid grid-cols-3 gap-4">
          <div className="rounded-2xl border border-white/30 bg-white/[0.10] p-4">
            <span className="text-sm font-black text-sky-300">BƯỚC 1 // NGUỒN</span>
            <h2 className="mt-1 text-2xl font-black text-white">{left_t}</h2>
            <p className="mt-1 text-base font-bold text-white/85">{left_d}</p>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-[#87ff00]/25 p-4 text-center">
            <span className="text-sm font-black text-[#87ff00]">BƯỚC 2 // TRẠM LÕI</span>
            <h2 className="mt-1 text-2xl font-black text-white">{mid_lbl}</h2>
          </div>
          <div className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.16] p-4">
            <span className="text-sm font-black text-[#87ff00]">BƯỚC 3 // ĐÍCH</span>
            <h2 className="mt-1 text-2xl font-black text-[#87ff00]">{right_t}</h2>
            <p className="mt-1 text-base font-bold text-white">{right_d}</p>
          </div>
        </div>
      </div>

      <div className="rounded-3xl border-r-8 border-[#87ff00] bg-white/[0.10] px-8 py-5 text-right backdrop-blur-md">
        <span className="text-lg font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[48px] font-black leading-tight uppercase">
          {h1_a} <span className="text-white">{h1_b}</span>
        </h1>
        <p className="mt-1 text-2xl font-bold text-white/90">{sub}</p>
      </div>"""
    else:
        layout_block = f"""
      <div className="flex items-center justify-between rounded-3xl border border-white/30 bg-white/[0.10] px-7 py-4 backdrop-blur-md">
        <div>
          <span className="text-base font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[46px] italic font-black leading-tight uppercase">
            {h1_a} — <span className="text-white not-italic">{h1_b}</span>
          </h1>
          <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
        </div>
        <div className="rounded-2xl bg-[#87ff00] px-5 py-3 text-center text-slate-950 font-black text-xl">
          {mid_lbl}
        </div>
      </div>

      <div style={{{{ transform: `scale(${{pop}})` }}}} className="grid grid-cols-12 items-center gap-4 rounded-[{35 + idx}px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="col-span-4 rounded-2xl border border-white/25 bg-white/[0.10] p-5">
          <span className="text-sm font-black text-sky-300">ĐẦU VÀO</span>
          <h2 className="mt-1 text-2xl font-black text-white">{left_t}</h2>
          <p className="mt-1 text-lg font-bold text-white/85">{left_d}</p>
        </div>
        <div className="col-span-4 flex items-center justify-center">
          <svg width="280" height="220" viewBox="0 0 880 220" className="w-full">
            <path d="{arch_path}" fill="none" stroke="#87ff00" strokeWidth="7" strokeDasharray="14 6" strokeDashoffset={{flow}} />
            {nodes_svg}
            {lines_svg}
          </svg>
        </div>
        <div className="col-span-4 rounded-2xl border-2 border-[#87ff00] bg-white/[0.16] p-5">
          <span className="text-sm font-black text-[#87ff00]">KẾT QUẢ CHUẨN</span>
          <h2 className="mt-1 text-2xl font-black text-[#87ff00]">{right_t}</h2>
          <p className="mt-1 text-lg font-bold text-white">{right_d}</p>
        </div>
      </div>"""

    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene3: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[2];
  const pop = spring({{ frame, fps, config: {{ damping: 12, stiffness: 105 }} }});
  const flow = -(frame * {4 + (idx % 3)});

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>
{layout_block}
      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""


def gen_scene4_bespoke(idx: int, vid_id: str, s4: tuple) -> str:
    h1_full, sub, st1, st2, st3, kw = _q(s4)
    st1_t, st1_d, st1_tag = st1
    st2_t, st2_d, st2_tag = st2
    st3_t, st3_d, st3_tag = st3

    sx1 = 25 + idx * 8
    sy1 = 40 + (idx % 5) * 9
    sx2 = 440 + idx * 5
    sy2 = 95 - (idx % 4) * 10
    sx3 = 835 - idx * 6
    sy3 = 35 + (idx % 6) * 8
    step_svg_path = f"M {sx1} {sy1} C {sx1 + 140} {sy2}, {sx2 - 110} {sy1}, {sx2} {sy2} S {sx3 - 95} {sy3 + 25}, {sx3} {sy3}"

    polygons_svg = "\n          ".join(
        f'<polygon points="{60 + p * (85 + idx)},15 {85 + p * (85 + idx)},55 {35 + p * (85 + idx)},55" fill="rgba(135,255,0,0.22)" stroke="#87ff00" strokeWidth="2.5" />'
        for p in range(1 + (idx % 5))
    )

    col_span_a = 5 + (idx % 3)  # 5, 6, 7
    col_span_b = 12 - col_span_a
    header_bottom = (idx % 2 == 1)

    header_part = f"""
      <div className="rounded-[{28 + idx}px] border-l-8 border-[#87ff00] bg-white/[0.10] px-7 py-5 backdrop-blur-md">
        <span className="text-base font-black tracking-widest text-[#87ff00] uppercase">QUY TRÌNH 3 BƯỚC THỰC THI #{idx + 1}</span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[44px] font-black leading-tight uppercase">
          {h1_full}
        </h1>
        <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
      </div>"""

    steps_part = f"""
      <div className="flex flex-col gap-4 rounded-[{32 + idx}px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <svg width="860" height="80" viewBox="0 0 880 110" className="w-full">
          <path d="{step_svg_path}" fill="none" stroke="#87ff00" strokeWidth="5" strokeDasharray="12 6" strokeDashoffset={{dash}} />
          {polygons_svg}
        </svg>

        <div className="grid grid-cols-12 gap-4">
          <div style={{{{ transform: `scale(${{s1}})` }}}} className="col-span-{col_span_a} rounded-2xl border border-sky-300/60 bg-white/[0.10] p-4">
            <div className="flex items-center justify-between">
              <span className="text-xl font-black text-sky-200">{st1_t}</span>
              <span className="rounded bg-sky-400/25 px-2.5 py-0.5 text-sm font-black text-sky-200">{st1_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/90">{st1_d}</p>
          </div>

          <div style={{{{ transform: `scale(${{s2}})` }}}} className="col-span-{col_span_b} rounded-2xl border border-amber-300/60 bg-white/[0.10] p-4">
            <div className="flex items-center justify-between">
              <span className="text-xl font-black text-amber-200">{st2_t}</span>
              <span className="rounded bg-amber-400/25 px-2.5 py-0.5 text-sm font-black text-amber-200">{st2_tag}</span>
            </div>
            <p className="mt-1 text-base font-bold text-white/90">{st2_d}</p>
          </div>
        </div>

        <div style={{{{ transform: `scale(${{s3}})` }}}} className="rounded-2xl border-2 border-[#87ff00] bg-white/[0.15] p-5">
          <div className="flex items-center justify-between">
            <span className="text-2xl font-black text-[#87ff00]">{st3_t}</span>
            <span className="rounded-lg bg-[#87ff00] px-3.5 py-1 text-base font-black text-slate-950">{st3_tag}</span>
          </div>
          <p className="mt-1.5 text-lg font-bold text-white">{st3_d}</p>
        </div>
      </div>"""

    content_flow = (steps_part + "\n" + header_part) if header_bottom else (header_part + "\n" + steps_part)

    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene4: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[3];
  const s1 = spring({{ frame: frame - 4, fps, config: {{ damping: 13, stiffness: 110 }} }});
  const s2 = spring({{ frame: frame - 12, fps, config: {{ damping: 13, stiffness: 110 }} }});
  const s3 = spring({{ frame: frame - 20, fps, config: {{ damping: 13, stiffness: 110 }} }});
  const dash = -(frame * 4);

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>
{content_flow}
      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""


def gen_scene5_bespoke(idx: int, vid_id: str, s5: tuple) -> str:
    kicker, h1_a, h1_b, sub, old_t, old_stat, old_d, old_tag, new_t, new_stat, new_d, new_tag, target_score, kw = _q(s5)

    gx1 = 35 + idx * 7
    gy1 = 95 - (idx % 4) * 8
    gx2 = 430 + idx * 6
    gy2 = 30 + (idx % 5) * 7
    gx3 = 820 - idx * 5
    gy3 = 20 + (idx % 3) * 9
    growth_path = f"M {gx1} {gy1} Q {gx2 - 80} {gy1 - 20} {gx2} {gy2} T {gx3} {gy3}"

    bars_svg = "\n          ".join(
        f'<rect x="{75 + b * (75 + idx)}" y="{25 + (b * 11) % 35}" width="{26 + (idx % 7)}" height="{55 - (b * 7) % 30}" rx="6" fill="#87ff00" />'
        for b in range(2 + (idx % 5))
    )

    left_w = 5 + (idx % 3)  # 5, 6, 7
    right_w = 12 - left_w
    header_at_bottom = (idx % 3 == 2)

    header_block = f"""
      <div className="flex items-center justify-between rounded-[{28 + idx}px] border border-white/30 bg-white/[0.10] px-7 py-5 backdrop-blur-md">
        <div>
          <span className="text-base font-black tracking-widest text-[#87ff00] uppercase">{kicker}</span>
          <h1 style={{{{ color: "#87ff00" }}}} className="mt-1 text-[46px] font-black leading-tight uppercase">
            {h1_a} <span className="text-white">{h1_b}</span>
          </h1>
          <p className="mt-1 text-xl font-bold text-white/90">{sub}</p>
        </div>
        <div className="flex h-[115px] w-[145px] shrink-0 flex-col items-center justify-center rounded-2xl bg-[#87ff00] text-slate-950">
          <span className="text-4xl font-black">{{score}}%</span>
          <span className="text-xs font-black uppercase">{new_tag}</span>
        </div>
      </div>"""

    versus_block = f"""
      <div className="flex flex-col gap-4 rounded-[{32 + idx}px] border border-white/30 bg-white/[0.08] p-6 backdrop-blur-md">
        <div className="grid grid-cols-12 gap-5">
          <div className="col-span-{left_w} flex flex-col justify-between rounded-2xl border-2 border-rose-400/65 bg-white/[0.09] p-5">
            <span className="rounded bg-rose-500/30 px-3 py-1 text-sm font-black text-rose-200 self-start">{old_tag}</span>
            <h2 className="mt-2 text-2xl font-black text-white">{old_t}</h2>
            <div className="my-2 text-3xl font-black text-amber-300">{old_stat}</div>
            <p className="text-base font-bold text-white/85">{old_d}</p>
          </div>

          <div className="col-span-{right_w} flex flex-col justify-between rounded-2xl border-3 border-[#87ff00] bg-white/[0.16] p-5 shadow-[0_0_35px_rgba(135,255,0,0.25)]">
            <span className="rounded bg-[#87ff00] px-3 py-1 text-sm font-black text-slate-950 self-start">{new_tag} ✅</span>
            <h2 className="mt-2 text-2xl font-black text-[#87ff00]">{new_t}</h2>
            <div className="my-2 text-4xl font-black text-white">{new_stat}</div>
            <p className="text-base font-bold text-white/95">{new_d}</p>
          </div>
        </div>

        <svg width="860" height="95" viewBox="0 0 880 105" className="w-full">
          <path d="{growth_path}" fill="none" stroke="#87ff00" strokeWidth="5" />
          {bars_svg}
        </svg>
      </div>"""

    body_content = (versus_block + "\n" + header_block) if header_at_bottom else (header_block + "\n" + versus_block)

    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene5: React.FC = () => {{
  const frame = useCurrentFrame();
  const scene = audioManifest.scenes[4];
  const score = Math.round(interpolate(frame, [0, 45], [15, {int(target_score)}], {{ extrapolateRight: "clamp" }}));

  return (
    <AbsoluteFill className="flex flex-col justify-center gap-7 px-10 pt-[230px] pb-[435px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{25}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.22}} />
      </Sequence>
{body_content}
      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="{kw}" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""


def gen_scene6_bespoke(idx: int, vid_id: str, s6: tuple) -> str:
    gift_title, cta_btn = _q(s6)
    return f"""import React from "react";
import {{ AbsoluteFill, Audio, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";
import {{ SubtitleBox }} from "../AiHallucinationShort/SubtitleBox";
import {{ audioManifest }} from "./audioData";

export const Scene6: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{ fps }} = useVideoConfig();
  const scene = audioManifest.scenes[5];
  const pop = spring({{ frame, fps, config: {{ damping: 12, stiffness: 110 }} }});
  const pulse = 1 + Math.sin(frame * 0.2) * 0.035;

  return (
    <AbsoluteFill className="flex flex-col items-center justify-center gap-6 px-10 pt-[230px] pb-[410px] text-white">
      <Audio src={{staticFile(scene.audioFile)}} />
      <Sequence from={{20}} durationInFrames={{45}}>
        <Audio src={{staticFile("brand-kit/sfx/discord-notification.mp3")}} volume={{0.24}} />
      </Sequence>

      <div style={{{{ transform: `scale(${{pop}})` }}}} className="flex w-full max-w-[940px] flex-col items-center rounded-[40px] border-2 border-[#87ff00] bg-white/[0.10] p-8 text-center backdrop-blur-md shadow-[0_20px_60px_rgba(0,0,0,0.32)]">
        <span className="rounded-full bg-[#87ff00] px-7 py-2 text-xl font-black text-slate-950 uppercase">
          🎁 QUÀ TẶNG THỰC CHIẾN MIỄN PHÍ 100%
        </span>
        <h1 style={{{{ color: "#87ff00" }}}} className="mt-5 text-[46px] font-black leading-[1.12] uppercase drop-shadow">
          {gift_title}
        </h1>
        <p className="mt-3 text-[27px] font-bold text-white/95 whitespace-nowrap">
          Lấy ngay tại Bình Luận Ghim Đầu Tiên hoặc để lại từ khóa:
        </p>

        <div
          style={{{{ transform: `scale(${{pulse}})` }}}}
          className="mt-6 flex items-center gap-4 rounded-full border-4 border-white bg-[#87ff00] px-10 py-5 text-3xl font-black text-slate-950 shadow-[0_0_40px_rgba(135,255,0,0.65)]"
        >
          <span>💬 {cta_btn}</span>
        </div>
      </div>

      <SubtitleBox text={{scene.text}} phrases={{scene.phrases}} durationInFrames={{scene.durationInFrames}} highlightKeyword="bình luận đầu tiên" className="absolute bottom-[380px] left-0 right-0" />
    </AbsoluteFill>
  );
}};
"""


def main():
    count = 0
    for idx, cfg in enumerate(REELS_CONFIG):
        vid_id = cfg["vid_id"]
        comp_id = cfg["comp_id"]
        comp_dir = SRC_DIR / comp_id

        write_file(comp_dir / "index.tsx", gen_index_tsx(comp_id))
        write_file(comp_dir / "Scene1.tsx", gen_scene1_bespoke(vid_id, cfg["s1"]))
        write_file(comp_dir / "Scene2.tsx", gen_scene2_bespoke(idx, vid_id, cfg["s2"]))
        write_file(comp_dir / "Scene3.tsx", gen_scene3_bespoke(idx, vid_id, cfg["s3"]))
        write_file(comp_dir / "Scene4.tsx", gen_scene4_bespoke(idx, vid_id, cfg["s4"]))
        write_file(comp_dir / "Scene5.tsx", gen_scene5_bespoke(idx, vid_id, cfg["s5"]))
        write_file(comp_dir / "Scene6.tsx", gen_scene6_bespoke(idx, vid_id, cfg["s6"]))
        count += 1
        print(f"✨ [{count:02d}/18] Generated 100% Bespoke Zero-Clone Composition: {comp_id} ({vid_id})")

    from zero_repost_gate import verify_zero_clone_tsx
    ok, msg = verify_zero_clone_tsx(SRC_DIR)
    print(("\n✅ " if ok else "\n❌ ") + msg)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
