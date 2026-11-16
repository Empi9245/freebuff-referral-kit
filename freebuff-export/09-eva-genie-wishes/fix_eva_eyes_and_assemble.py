"""Surgical eye-fix & final assembly for 09-eva-genie-wishes (removes f114-116 roll & f126-143 eyeball slide)."""
from __future__ import annotations

import json
import os
import subprocess
import cv2
import numpy as np
from PIL import Image

from add_italian_captions import (
    BASE,
    CLIPS,
    alpha_blend_bgr,
    build_p1_middle_overlay,
    build_top_pill_overlay,
    encode_mp4,
)


def resample_part1_clean_eyes(raw_mp4: str, out_clean_norm: str) -> list[np.ndarray]:
    """Read 24fps raw Flow clip, remove f114-116 roll and f126-143 sideways eyeball slide, emit 180 frames @ 30fps (720x1280)."""
    cap = cv2.VideoCapture(raw_mp4)
    raw_frames: list[np.ndarray] = []
    while True:
        ret, fr = cap.read()
        if not ret:
            break
        # Upscale each 360x640 raw frame cleanly to 720x1280 Lanczos
        fr720 = cv2.resize(fr, (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        raw_frames.append(fr720)
    cap.release()

    # Segment 1: raw[0..113] (4.75s @ 24fps) -> 142 frames @ 30fps (0.00s..4.70s), natural speed
    out_frames: list[np.ndarray] = []
    n_seg1 = 142
    for i in range(n_seg1):
        t_src = (i / 30.0) * 24.0
        idx_src = min(113, int(round(t_src)))
        out_frames.append(raw_frames[idx_src].copy())

    # Segment 2: skip raw[114..116] (eye roll), build 38 smooth natural open-eye frames (frames 142..179 = 1.267s)
    # Clean open-eye opening ramp: 117 (2f), 118 (2f), 119 (3f), 120 (3f), 121 (3f), 122 (3f), 123 (3f), 124 (4f) = 23f
    # Followed by gentle settled hold/ease-back across 124..120 (zero glasses ghosting, natural attentive micro-motion) = 15f
    seg2_indices = [
        117, 117,
        118, 118,
        119, 119, 119,
        120, 120, 120,
        121, 121, 121,
        122, 122, 122,
        123, 123, 123,
        124, 124, 124, 124,
        123, 123, 123,
        122, 122, 122,
        121, 121, 121,
        120, 120, 120,
        121, 121, 122,
    ]
    assert len(seg2_indices) == 38, f"Expected 38 frames, got {len(seg2_indices)}"
    for idx_src in seg2_indices:
        out_frames.append(raw_frames[idx_src].copy())

    assert len(out_frames) == 180
    encode_mp4(out_frames, out_clean_norm, fps=30.0)
    return out_frames


def main() -> None:
    raw_mp4 = os.path.join(CLIPS, "eva_flow_part1_raw.mp4")
    norm_clean_mp4 = os.path.join(CLIPS, "eva_flow_part1_eyes_fixed.mp4")
    p1_ita_mp4 = os.path.join(CLIPS, "parte1_eva_italiano.mp4")
    p2_ita_mp4 = os.path.join(CLIPS, "parte2_macbook_italiano.mp4")
    aud_mp3 = os.path.join(CLIPS, "audio_originale.mp3")
    final_mute = os.path.join(CLIPS, "FINAL-REEL-EVA-ITALIANO.mp4")
    final_audio = os.path.join(CLIPS, "FINAL-REEL-EVA-ITALIANO-CON-AUDIO.mp4")

    clean_frames = resample_part1_clean_eyes(raw_mp4, norm_clean_mp4)

    # Save contact sheet of fixed eye frames (30fps frames 135..179 step 3 -> 15 tiles, 5x3)
    crops = []
    for fidx in range(135, 180, 3):
        crop = clean_frames[fidx][320:540, 200:520].copy()
        cv2.putText(crop, f"f{fidx} ({fidx/30:.2f}s)", (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        crops.append(crop)
    rows = [np.hstack(crops[i : i + 5]) for i in range(0, len(crops), 5)]
    sheet = np.vstack(rows)
    sheet_path = os.path.join(BASE, "frames_clean", "p1_eva_eyes_fixed_sheet.png")
    cv2.imwrite(sheet_path, sheet)
    print(f"Saved eye fix contact sheet -> {sheet_path}")

    # Apply Italian captions cleanly onto fixed Part 1 frames
    stars_rgba = Image.open(os.path.join(BASE, "emoji_stars_trio.png")).convert("RGBA")
    pers_rgba = Image.open(os.path.join(BASE, "emoji_persevere.png")).convert("RGBA")
    pill_1a = np.array(build_top_pill_overlay(stars_rgba, "hai 3 desideri", (88, 202, 632, 291)))
    pill_1b = np.array(build_top_pill_overlay(stars_rgba, "hai ancora 3 desideri", (40, 202, 679, 291)))
    mid_1a = np.array(build_p1_middle_overlay(pers_rgba))

    captioned: list[np.ndarray] = []
    for idx, frame in enumerate(clean_frames):
        if idx <= 163:
            res = alpha_blend_bgr(frame, pill_1a)
            res = alpha_blend_bgr(res, mid_1a)
        else:
            res = alpha_blend_bgr(frame, pill_1b)
        captioned.append(res)
        if idx == 50:
            cv2.imwrite(os.path.join(BASE, "frames_clean", "p1_eva_ita_f050.png"), res)
        elif idx == 170:
            cv2.imwrite(os.path.join(BASE, "frames_clean", "p1_eva_ita_f170.png"), res)

    encode_mp4(captioned, p1_ita_mp4, fps=30.0)
    print(f"Re-rendered Part 1 Italian (180 frames) -> {p1_ita_mp4}")

    # Re-concatenate final mute + audio reels
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", p1_ita_mp4, "-i", p2_ita_mp4,
            "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
            "-map", "[v]", "-an",
            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            final_mute,
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", final_mute, "-i", aud_mp3,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            final_audio,
        ],
        check=True,
    )

    for f in [norm_clean_mp4, p1_ita_mp4, final_mute, final_audio]:
        info = subprocess.check_output(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", f],
            text=True,
        )
        d = json.loads(info)
        streams = [(s["codec_type"], s.get("width"), s.get("height"), s.get("r_frame_rate"), s.get("nb_frames")) for s in d["streams"]]
        print(os.path.basename(f), "bytes=", os.path.getsize(f), "dur=", d["format"]["duration"], "streams=", streams)


if __name__ == "__main__":
    main()
