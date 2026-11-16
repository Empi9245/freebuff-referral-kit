"""Clean English TikTok text overlays using exact silhouette masks + OpenCV Telea inpainting (zero halos)."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageFilter, ImageDraw


BASE_DIR = Path(r"c:\Progetti Exeva\CuriousEva\freebuff-export\08-eva-google-flow")
RAW_DIR = BASE_DIR / "frames_raw"
CLEAN_DIR = BASE_DIR / "frames_clean"
CLIPS_DIR = BASE_DIR / "clips"


def build_letter_silhouette_mask(
    bgr: np.ndarray,
    box: tuple[int, int, int, int],
    white_thresh: int = 190,
    diff_thresh: int = 50,
    emoji_x_min: int | None = None,
    emoji_mode: str = "none",
    dilate_px: int = 5,
    max_y: int | None = None,
) -> np.ndarray:
    """Build a tight silhouette mask around ONLY the overlay text, black stroke, and emojis (no solid box)."""
    h, w = bgr.shape[:2]
    x0, y0, x1, y1 = box
    roi = bgr[y0:y1, x0:x1]
    b, g, r = roi[:, :, 0].astype(np.int16), roi[:, :, 1].astype(np.int16), roi[:, :, 2].astype(np.int16)
    mn = np.minimum(np.minimum(r, g), b)
    mx = np.maximum(np.maximum(r, g), b)
    diff = mx - mn

    # White letter cores
    is_white = (mn > white_thresh) & (diff < diff_thresh)
    roi_mask = is_white.copy()

    # Optional emojis at the right end of a line
    if emoji_x_min is not None and emoji_x_min < x1:
        ex0 = max(0, emoji_x_min - x0)
        sub_r, sub_g, sub_b = r[:, ex0:], g[:, ex0:], b[:, ex0:]
        sub_mn, sub_mx = mn[:, ex0:], mx[:, ex0:]
        if emoji_mode == "skulls":
            # White/gray skulls + dark eye sockets near bright skull pixels
            sk = sub_mn > 125
            roi_mask[:, ex0:] |= sk
        elif emoji_mode == "crying":
            # Yellow face (g - b > 30) or cyan tears (b - r > 45) or bright highlights
            cr = ((sub_g - sub_b) > 30) | ((sub_b - sub_r) > 45) | ((sub_mn > 160) & (sub_mx - sub_mn < 50))
            roi_mask[:, ex0:] |= cr

    full_mask = np.zeros((h, w), dtype=np.uint8)
    full_mask[y0:y1, x0:x1] = roi_mask.astype(np.uint8) * 255

    if dilate_px > 0:
        k = dilate_px * 2 + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        full_mask = cv2.dilate(full_mask, kernel)

    if max_y is not None:
        full_mask[max_y:, :] = 0

    return full_mask


def telea_inpaint_with_grain(
    bgr: np.ndarray,
    mask: np.ndarray,
    radius: int = 4,
    grain_sigma: float = 1.4,
) -> np.ndarray:
    """Inpaint only the silhouette mask via Telea, then match subtle sensor grain inside the mask."""
    if not np.any(mask):
        return bgr
    inpainted = cv2.inpaint(bgr, mask, inpaintRadius=radius, flags=cv2.INPAINT_TELEA)
    if grain_sigma > 0:
        rng = np.random.default_rng(42)
        noise = rng.normal(0.0, grain_sigma, size=bgr.shape).astype(np.float32)
        m = (mask > 0)[:, :, None]
        noisy = np.clip(inpainted.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        inpainted = np.where(m, noisy, inpainted)
    return inpainted


def extract_static_part2_masks() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute exact per-segment silhouette masks using the cleanest reference frames."""
    # 2A: static caption "he doesn't know / there's a free version 💀💀" from frame 02_40 (clean wall behind text!)
    im_2a = cv2.imread(str(RAW_DIR / "p2a_cli_02_40.png"))
    mask_2a_line1 = build_letter_silhouette_mask(
        im_2a, (190, 310, 530, 355), white_thresh=165, diff_thresh=60, dilate_px=7
    )
    mask_2a_line2 = build_letter_silhouette_mask(
        im_2a,
        (104, 358, 612, 410),
        white_thresh=165,
        diff_thresh=60,
        emoji_x_min=522,
        emoji_mode="skulls",
        dilate_px=7,
    )
    mask_2a = cv2.bitwise_or(mask_2a_line1, mask_2a_line2)

    # 2B: "holy mog😭😭" from p2b_zoom_chart_05_00.png
    im_2b = cv2.imread(str(RAW_DIR / "p2b_zoom_chart_05_00.png"))
    mask_2b = build_letter_silhouette_mask(
        im_2b,
        (178, 390, 536, 456),
        white_thresh=150,
        diff_thresh=65,
        emoji_x_min=412,
        emoji_mode="crying",
        dilate_px=8,
    )

    # 2C: "free chatgpt dupe" from p2c_chat_07_20.png
    im_2c = cv2.imread(str(RAW_DIR / "p2c_chat_07_20.png"))
    mask_2c = build_letter_silhouette_mask(
        im_2c, (172, 536, 548, 590), white_thresh=150, diff_thresh=65, dilate_px=8
    )

    # 2D: "free website builder" from p2d_web_09_50.png (strictly y < 380 to never touch $42,391.20!)
    im_2d = cv2.imread(str(RAW_DIR / "p2d_web_09_50.png"))
    mask_2d = build_letter_silhouette_mask(
        im_2d, (120, 332, 606, 378), white_thresh=160, diff_thresh=65, dilate_px=6, max_y=380
    )
    return mask_2a, mask_2b, mask_2c, mask_2d


def clean_part2_video_and_keyframes() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    mask_2a, mask_2b, mask_2c, mask_2d = extract_static_part2_masks()

    # Save cleaned Part 2 PNG keyframes
    for raw_name, clean_name, m in [
        ("p2a_cli_02_40.png", "p2a_cli_clean.png", mask_2a),
        ("p2b_zoom_chart_05_00.png", "p2b_zoom_chart_clean.png", mask_2b),
        ("p2c_chat_07_20.png", "p2c_chat_clean.png", mask_2c),
        ("p2d_web_09_50.png", "p2d_web_clean.png", mask_2d),
    ]:
        bgr = cv2.imread(str(RAW_DIR / raw_name))
        out_bgr = telea_inpaint_with_grain(bgr, m, radius=5, grain_sigma=1.3)
        cv2.imwrite(str(CLEAN_DIR / clean_name), out_bgr)

    # Clean Part 2 video frame-by-frame
    src_vid = CLIPS_DIR / "parte2_macbook_ui_ref.mp4"
    out_vid = CLIPS_DIR / "parte2_macbook_clean_no_text.mp4"

    cap = cv2.VideoCapture(str(src_vid))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with tempfile.TemporaryDirectory() as tmp:
        raw_mp4 = Path(tmp) / "temp_raw.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(raw_mp4), fourcc, fps, (w, h))

        idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            idx += 1
            if idx <= 54:
                m = mask_2a
            elif idx <= 122:
                m = mask_2b
            elif idx <= 185:
                m = mask_2c
            else:
                m = mask_2d

            cleaned = telea_inpaint_with_grain(frame, m, radius=5, grain_sigma=1.3)
            writer.write(cleaned)

        cap.release()
        writer.release()

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_mp4),
                "-c:v",
                "libx264",
                "-crf",
                "15",
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(out_vid),
            ],
            check=True,
            stderr=subprocess.DEVNULL,
        )
    print(f"Cleaned Part 2 ({idx} frames) saved to {out_vid}", flush=True)


# --- Part 1 & Part 3 selective cleaning helpers (preserved for reference clips) ---
def clean_selfie_video(src_vid: Path, out_vid: Path, box: tuple[int, int, int, int], emoji_x: int | None = None) -> None:
    cap = cv2.VideoCapture(str(src_vid))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with tempfile.TemporaryDirectory() as tmp:
        raw_mp4 = Path(tmp) / "temp_selfie.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(raw_mp4), fourcc, fps, (w, h))
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            m = build_letter_silhouette_mask(
                frame,
                box,
                white_thresh=205,
                diff_thresh=40,
                emoji_x_min=emoji_x,
                emoji_mode="crying" if emoji_x else "none",
                dilate_px=6,
            )
            writer.write(telea_inpaint_with_grain(frame, m, radius=5, grain_sigma=1.2))
        cap.release()
        writer.release()
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(raw_mp4), "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-an", str(out_vid)],
            check=True,
            stderr=subprocess.DEVNULL,
        )


if __name__ == "__main__":
    clean_part2_video_and_keyframes()
