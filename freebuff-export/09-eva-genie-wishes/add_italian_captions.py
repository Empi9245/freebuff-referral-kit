"""2x supersampled TikTok-style Italian caption renderer for 09-eva-genie-wishes."""
from __future__ import annotations

import os
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


BASE = r"c:\Progetti Exeva\CuriousEva\freebuff-export\09-eva-genie-wishes"
CLIPS = os.path.join(BASE, "clips")
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"


def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def draw_outlined_text_2x(
    draw: ImageDraw.ImageDraw,
    center_xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int] = (255, 255, 255, 255),
    stroke_fill: tuple[int, int, int, int] = (0, 0, 0, 255),
    stroke_width: int = 8,
) -> None:
    cx, cy = center_xy
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2 - bbox[0]
    ty = cy - th // 2 - bbox[1]
    draw.text(
        (tx, ty),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def build_top_pill_overlay(
    stars_rgba: Image.Image,
    line2_text: str,
    row2_rect_1x: tuple[int, int, int, int],
) -> Image.Image:
    """Pre-render the stepped top black pill ('Genio: ⭐⭐⭐ / <line2>') at 2x (1440x2560)."""
    W2, H2 = 1440, 2560
    canvas = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Row 1 black rounded pill covers English (152..571, 136..207) at 2x with slight margin
    r1 = (146 * 2, 132 * 2, 577 * 2, 208 * 2)
    r2 = tuple(v * 2 for v in row2_rect_1x)
    draw.rounded_rectangle(r1, radius=42, fill=(0, 0, 0, 255))
    draw.rounded_rectangle(r2, radius=44, fill=(0, 0, 0, 255))
    # Bridge the tiny vertical join notch between Row 1 and Row 2 cleanly so no horizontal gap shows
    draw.rectangle((r1[0] + 36, r1[3] - 18, r1[2] - 36, r2[1] + 18), fill=(0, 0, 0, 255))

    f_r1 = _load_font(FONT_BOLD, 88)
    label1 = "Genio:"
    b1 = draw.textbbox((0, 0), label1, font=f_r1)
    lw1, lh1 = b1[2] - b1[0], b1[3] - b1[1]

    stars_target_h = 92
    stars_target_w = int(round(stars_rgba.width * (stars_target_h / stars_rgba.height)))
    stars_2x = stars_rgba.resize((stars_target_w, stars_target_h), Image.Resampling.LANCZOS)

    gap = 18
    total_w1 = lw1 + gap + stars_target_w
    start_x1 = (r1[0] + r1[2]) // 2 - total_w1 // 2
    center_y1 = (r1[1] + r1[3]) // 2
    draw.text((start_x1 - b1[0], center_y1 - lh1 // 2 - b1[1]), label1, font=f_r1, fill=(255, 255, 255, 255))
    canvas.alpha_composite(stars_2x, (start_x1 + lw1 + gap, center_y1 - stars_target_h // 2 - 2))

    # Row 2 text
    f_r2 = _load_font(FONT_BOLD, 88)
    b2 = draw.textbbox((0, 0), line2_text, font=f_r2)
    max_w2 = (r2[2] - r2[0]) - 64
    if (b2[2] - b2[0]) > max_w2:
        f_r2 = _load_font(FONT_BOLD, int(88 * max_w2 / (b2[2] - b2[0])))
        b2 = draw.textbbox((0, 0), line2_text, font=f_r2)
    lw2, lh2 = b2[2] - b2[0], b2[3] - b2[1]
    tx2 = (r2[0] + r2[2]) // 2 - lw2 // 2 - b2[0]
    ty2 = (r2[1] + r2[3]) // 2 - lh2 // 2 - b2[1]
    draw.text((tx2, ty2), line2_text, font=f_r2, fill=(255, 255, 255, 255))

    return canvas.resize((720, 1280), Image.Resampling.LANCZOS)


def build_p2_center_overlay(
    main_text: str,
    sub_lines: list[str] | None = None,
    cy_1x: int = 635,
    font_size_2x: int = 96,
    stroke_w_2x: int = 9,
) -> Image.Image:
    """Pre-render Part 2 center outlined TikTok label (+ optional CTA lines) at 2x -> 720x1280."""
    W2, H2 = 1440, 2560
    canvas = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    font_size = font_size_2x
    font = _load_font(FONT_BOLD, font_size)
    bbox = draw.textbbox((0, 0), main_text, font=font, stroke_width=stroke_w_2x)
    if (bbox[2] - bbox[0]) > 1240:
        font_size = int(font_size * 1240 / (bbox[2] - bbox[0]))
        font = _load_font(FONT_BOLD, font_size)

    draw_outlined_text_2x(draw, (720, cy_1x * 2), main_text, font, stroke_width=stroke_w_2x)

    if sub_lines:
        f_sub = _load_font(FONT_BOLD, 54)
        y_start = 718 * 2
        for idx, line in enumerate(sub_lines):
            draw_outlined_text_2x(draw, (720, y_start + idx * 62), line, f_sub, stroke_width=7)

    return canvas.resize((720, 1280), Image.Resampling.LANCZOS)


def build_p1_middle_overlay(persevere_rgba: Image.Image) -> Image.Image:
    """Pre-render Part 1A quote ('\"ti prego fammi avere / claude code gratis a vita😣\"') at 2x -> 720x1280."""
    W2, H2 = 1440, 2560
    canvas = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    font = _load_font(FONT_BOLD, 80)
    line1 = '"ti prego fammi avere'
    line2_prefix = "claude code gratis a vita"
    line2_suffix = '"'

    draw_outlined_text_2x(draw, (720, 770 * 2), line1, font, stroke_width=8)

    # Measure line 2 with embedded 😣 emoji
    b_pre = draw.textbbox((0, 0), line2_prefix, font=font, stroke_width=8)
    b_suf = draw.textbbox((0, 0), line2_suffix, font=font, stroke_width=8)
    emo_size = 86
    emo_2x = persevere_rgba.resize((emo_size, emo_size), Image.Resampling.LANCZOS)
    total_w = (b_pre[2] - b_pre[0]) - 6 + emo_size - 6 + (b_suf[2] - b_suf[0])

    # Auto-scale down slightly if wider than 1280px at 2x
    if total_w > 1280:
        scale = 1280 / total_w
        font = _load_font(FONT_BOLD, int(80 * scale))
        emo_size = int(86 * scale)
        emo_2x = persevere_rgba.resize((emo_size, emo_size), Image.Resampling.LANCZOS)
        draw_outlined_text_2x(draw, (720, 770 * 2), line1, font, stroke_width=8)
        b_pre = draw.textbbox((0, 0), line2_prefix, font=font, stroke_width=8)
        b_suf = draw.textbbox((0, 0), line2_suffix, font=font, stroke_width=8)
        total_w = (b_pre[2] - b_pre[0]) - 6 + emo_size - 6 + (b_suf[2] - b_suf[0])

    cy2 = 824 * 2
    sx = 720 - total_w // 2
    h_pre = b_pre[3] - b_pre[1]
    draw.text(
        (sx - b_pre[0], cy2 - h_pre // 2 - b_pre[1]),
        line2_prefix,
        font=font,
        fill=(255, 255, 255, 255),
        stroke_width=8,
        stroke_fill=(0, 0, 0, 255),
    )
    ex = sx + (b_pre[2] - b_pre[0]) - 6
    canvas.alpha_composite(emo_2x, (ex, cy2 - emo_size // 2))

    sx2 = ex + emo_size - 6
    h_suf = b_suf[3] - b_suf[1]
    draw.text(
        (sx2 - b_suf[0], cy2 - h_suf // 2 - b_suf[1]),
        line2_suffix,
        font=font,
        fill=(255, 255, 255, 255),
        stroke_width=8,
        stroke_fill=(0, 0, 0, 255),
    )

    return canvas.resize((720, 1280), Image.Resampling.LANCZOS)


def alpha_blend_bgr(frame_bgr: np.ndarray, overlay_rgba: np.ndarray) -> np.ndarray:
    """Composite pre-rendered 720x1280 RGBA overlay over BGR video frame."""
    alpha = overlay_rgba[:, :, 3:4].astype(np.float32) / 255.0
    rgb_over = overlay_rgba[:, :, :3][:, :, ::-1].astype(np.float32)  # RGB -> BGR
    base_f = frame_bgr.astype(np.float32)
    blended = base_f * (1.0 - alpha) + rgb_over * alpha
    return np.clip(blended, 0, 255).astype(np.uint8)


def encode_mp4(frames: list[np.ndarray], out_mp4: str, fps: float = 30.0) -> None:
    h, w = frames[0].shape[:2]
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{w}x{h}", "-pix_fmt", "bgr24", "-r", str(fps),
        "-i", "-",
        "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
        out_mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for fr in frames:
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    err = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {out_mp4}:\n{err}")


def render_part2_italian(
    cta_lines: list[str] | None = None,
    out_name: str = "parte2_macbook_italiano.mp4",
) -> None:
    cta_lines = cta_lines or ['seguici e commenta "promo"', "per ricevere l'app"]
    stars_rgba = Image.open(os.path.join(BASE, "emoji_stars_trio.png")).convert("RGBA")
    pill_top = np.array(build_top_pill_overlay(stars_rgba, "hai ancora 3 desideri", (40, 202, 679, 291)))
    ov_2a = np.array(build_p2_center_overlay("CLAUDE CODE GRATIS", cy_1x=635, font_size_2x=92, stroke_w_2x=9))
    ov_2b = np.array(build_p2_center_overlay("REPLIT GRATIS", cy_1x=635, font_size_2x=104, stroke_w_2x=10))
    ov_2c = np.array(build_p2_center_overlay("LOVABLE GRATIS", cy_1x=631, font_size_2x=108, stroke_w_2x=10))
    ov_2d_main = np.array(build_p2_center_overlay("TUTTO GRATIS", cy_1x=634, font_size_2x=106, stroke_w_2x=10))
    ov_2d_cta = np.array(
        build_p2_center_overlay(
            "TUTTO GRATIS",
            cta_lines,
            cy_1x=634,
            font_size_2x=106,
            stroke_w_2x=10,
        )
    )

    in_mp4 = os.path.join(CLIPS, "parte2_macbook_clean.mp4")
    out_mp4 = os.path.join(CLIPS, out_name)
    cap = cv2.VideoCapture(in_mp4)
    out_frames: list[np.ndarray] = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        res = alpha_blend_bgr(frame, pill_top)
        if 2 <= idx <= 30:
            res = alpha_blend_bgr(res, ov_2a)
        elif 33 <= idx <= 58:
            res = alpha_blend_bgr(res, ov_2b)
        elif 60 <= idx <= 86:
            res = alpha_blend_bgr(res, ov_2c)
        elif 89 <= idx <= 90:
            res = alpha_blend_bgr(res, ov_2d_main)
        elif 91 <= idx <= 114:
            res = alpha_blend_bgr(res, ov_2d_cta)
        out_frames.append(res)
        if idx in (15, 45, 63, 67, 70, 100):
            cv2.imwrite(os.path.join(BASE, "frames_clean", f"p2_ita_f{idx:03d}.png"), res)
        idx += 1
    cap.release()
    encode_mp4(out_frames, out_mp4, fps=30.0)
    print(f"Rendered Part 2 Italian ({len(out_frames)} frames) -> {out_mp4}")


def render_part1_italian(eva_clip_mp4: str, out_mp4: str) -> None:
    """Phase 2 helper: scale Eva's clip to 720x1280 @ 30fps, 180 frames, and burn Italian captions."""
    stars_rgba = Image.open(os.path.join(BASE, "emoji_stars_trio.png")).convert("RGBA")
    pers_rgba = Image.open(os.path.join(BASE, "emoji_persevere.png")).convert("RGBA")

    pill_1a = np.array(build_top_pill_overlay(stars_rgba, "hai 3 desideri", (88, 202, 632, 291)))
    pill_1b = np.array(build_top_pill_overlay(stars_rgba, "hai ancora 3 desideri", (40, 202, 679, 291)))
    mid_1a = np.array(build_p1_middle_overlay(pers_rgba))

    norm_tmp = os.path.join(CLIPS, "_eva_p1_norm.mp4")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", eva_clip_mp4,
            "-an", "-vf", "scale=720:1280:force_original_aspect_ratio=increase:flags=lanczos,crop=720:1280,fps=30",
            "-frames:v", "180",
            "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", norm_tmp,
        ],
        check=True,
    )
    cap = cv2.VideoCapture(norm_tmp)
    out_frames: list[np.ndarray] = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx <= 163:
            res = alpha_blend_bgr(frame, pill_1a)
            res = alpha_blend_bgr(res, mid_1a)
        else:
            res = alpha_blend_bgr(frame, pill_1b)
        out_frames.append(res)
        if idx in (50, 170):
            tag = "f050" if idx == 50 else "f170"
            cv2.imwrite(os.path.join(BASE, "frames_clean", f"p1_eva_ita_{tag}.png"), res)
        idx += 1
    cap.release()
    # Pad cleanly if Google Flow generated <180 frames (hold final frame to match 6.000s timing)
    while len(out_frames) < 180 and out_frames:
        res_last = out_frames[-1].copy()
        out_frames.append(res_last)
    encode_mp4(out_frames[:180], out_mp4, fps=30.0)
    print(f"Rendered Part 1 Italian ({len(out_frames[:180])} frames) -> {out_mp4}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        render_part1_italian(sys.argv[1], sys.argv[2])
    else:
        render_part2_italian()
