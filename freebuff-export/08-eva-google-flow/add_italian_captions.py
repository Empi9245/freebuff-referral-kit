"""Add TikTok-style Italian captions + extracted iOS emojis to Part 2 (and assemble final video)."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from collections import deque
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(r"c:\Progetti Exeva\CuriousEva\freebuff-export\08-eva-google-flow")
RAW_DIR = BASE_DIR / "frames_raw"
CLIPS_DIR = BASE_DIR / "clips"
FONT_PATH = "C:/Windows/Fonts/segoeuib.ttf"


def extract_skull_pair() -> Image.Image:
    """Extract the two white skull emojis from p2a_cli_02_40.png with transparent background."""
    im = Image.open(RAW_DIR / "p2a_cli_02_40.png").convert("RGBA")
    # Crop tight around both skulls with 3px margin
    crop = im.crop((524, 360, 606, 407))
    w, h = crop.size
    px = crop.load()

    # Flood-fill transparent from all outer border pixels where pixel is dark/brown sofa (not white skull)
    visited = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()

    def is_bg(r: int, g: int, b: int) -> bool:
        # White skull surface is bright & neutral; brown sofa is darker & warmer
        return max(r, g, b) < 130 or (r - b > 22 and max(r, g, b) < 165)

    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))

    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h or visited[y][x]:
            continue
        visited[y][x] = True
        r, g, b, _ = px[x, y]
        if is_bg(r, g, b):
            px[x, y] = (0, 0, 0, 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    # Soften 1px alpha border cleanly
    bbox = crop.getbbox()
    return crop.crop(bbox) if bbox else crop


def extract_crying_pair() -> Image.Image:
    """Extract the two 😭 emojis from p2b_zoom_chart_05_00.png with transparent background."""
    im = Image.open(RAW_DIR / "p2b_zoom_chart_05_00.png").convert("RGBA")
    crop = im.crop((416, 393, 538, 452))
    w, h = crop.size
    px = crop.load()

    # Background is dark blue (~10, 38, 86). Flood-fill from borders on dark-blue pixels.
    visited = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()

    def is_bg(r: int, g: int, b: int) -> bool:
        # Yellow face has high r & g; blue tear stream is bright cyan/blue (g > 110, b > 170)
        return r < 45 and g < 75 and b < 130

    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))

    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h or visited[y][x]:
            continue
        visited[y][x] = True
        r, g, b, _ = px[x, y]
        if is_bg(r, g, b):
            px[x, y] = (0, 0, 0, 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    bbox = crop.getbbox()
    return crop.crop(bbox) if bbox else crop


def render_tiktok_overlay(
    lines: list[tuple[str, Image.Image | None]],
    y_start: int,
    font_size: int = 38,
    line_gap: int = 10,
    stroke_w: int = 4,
    canvas_size: tuple[int, int] = (720, 1280),
) -> Image.Image:
    """Render supersampled 2x TikTok-style white bold text with crisp black outline + optional emoji sprite."""
    scale = 2
    cw, ch = canvas_size
    layer = Image.new("RGBA", (cw * scale, ch * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT_PATH, font_size * scale)

    cy = y_start * scale
    for text, emoji_sprite in lines:
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w * scale)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        ew, eh = 0, 0
        scaled_emoji = None
        if emoji_sprite is not None:
            target_h = int(font_size * scale * 0.98)
            ratio = target_h / max(1, emoji_sprite.height)
            ew = int(emoji_sprite.width * ratio)
            eh = target_h
            scaled_emoji = emoji_sprite.resize((ew, eh), Image.Resampling.LANCZOS)

        gap_px = int(8 * scale) if scaled_emoji is not None else 0
        total_w = tw + gap_px + ew
        tx = (cw * scale - total_w) // 2 - bbox[0]
        ty = cy - bbox[1]

        draw.text(
            (tx, ty),
            text,
            font=font,
            fill=(255, 255, 255, 255),
            stroke_width=stroke_w * scale,
            stroke_fill=(0, 0, 0, 255),
        )

        if scaled_emoji is not None:
            ex = (cw * scale - total_w) // 2 + tw + gap_px
            ey = cy + (th - eh) // 2
            layer.alpha_composite(scaled_emoji, (ex, ey))

        cy += th + line_gap * scale

    return layer.resize(canvas_size, Image.Resampling.LANCZOS)


def apply_overlays_to_video(
    src_vid: Path,
    out_vid: Path,
    overlay_fn,
    target_size: tuple[int, int] = (720, 1280),
) -> None:
    """Apply frame-mapped RGBA overlays onto a silent video (`-an`)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        raw_frames = tmp_path / "raw"
        out_frames = tmp_path / "out"
        raw_frames.mkdir()
        out_frames.mkdir()

        # Normalize input to 720x1280 30fps bmp frames with crisp Lanczos upscale
        w, h = target_size
        vf = f"scale={w}:{h}:flags=lanczos:force_original_aspect_ratio=increase,crop={w}:{h},unsharp=3:3:0.35:3:3:0.0,fps=30"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(src_vid), "-vf", vf, str(raw_frames / "frame_%04d.bmp")],
            check=True,
            stderr=subprocess.DEVNULL,
        )

        frames = sorted(raw_frames.glob("frame_*.bmp"))
        for idx, fpath in enumerate(frames, start=1):
            im = Image.open(fpath).convert("RGBA")
            ov = overlay_fn(idx)
            if ov is not None:
                im = Image.alpha_composite(im, ov)
            im.convert("RGB").save(out_frames / fpath.name)

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                "30",
                "-i",
                str(out_frames / "frame_%04d.bmp"),
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


def build_part2_italian(verify_dir: Path | None = None) -> Path:
    skulls = extract_skull_pair()
    crying = extract_crying_pair()

    ov_2a = render_tiktok_overlay(
        [("non sa che esiste", None), ("la versione gratis", skulls)],
        y_start=316,
        font_size=36,
        line_gap=6,
    )
    ov_2b = render_tiktok_overlay(
        [("umiliato", crying)],
        y_start=398,
        font_size=40,
    )
    ov_2c = render_tiktok_overlay(
        [("alternativa gratis a chatgpt", None)],
        y_start=544,
        font_size=35,
    )
    ov_2d = render_tiktok_overlay(
        [("crea siti web gratis", None)],
        y_start=336,
        font_size=38,
    )

    def get_ov(frame_idx: int) -> Image.Image:
        if frame_idx <= 54:
            return ov_2a
        if frame_idx <= 122:
            return ov_2b
        if frame_idx <= 185:
            return ov_2c
        return ov_2d

    src = CLIPS_DIR / "parte2_macbook_clean_no_text.mp4"
    out = CLIPS_DIR / "parte2_macbook_italiano.mp4"
    apply_overlays_to_video(src, out, get_ov)
    print(f"Part 2 Italian video saved to {out}", flush=True)

    if verify_dir is not None:
        verify_dir.mkdir(parents=True, exist_ok=True)
        for ts, name in [("0.3", "verify_2a.png"), ("2.6", "verify_2b.png"), ("4.8", "verify_2c.png"), ("7.1", "verify_2d.png")]:
            subprocess.run(
                ["ffmpeg", "-y", "-ss", ts, "-i", str(out), "-frames:v", "1", str(verify_dir / name)],
                check=True,
                stderr=subprocess.DEVNULL,
            )
    return out


def assemble_final(p1_raw: Path, p3_raw: Path, out_final: Path) -> None:
    crying = extract_crying_pair()
    ov_p1 = render_tiktok_overlay(
        [("il tipo accanto a me", None), ("sta usando claude", crying)],
        y_start=275,
        font_size=36,
        line_gap=6,
    )
    ov_p3 = render_tiktok_overlay(
        [('seguici e commenta "promo"', None), ("per ricevere l'app", None)],
        y_start=315,
        font_size=34,
        line_gap=6,
    )

    p2_it = CLIPS_DIR / "parte2_macbook_italiano.mp4"
    if not p2_it.exists():
        build_part2_italian()

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        p1_it = tmp_path / "p1_it.mp4"
        p3_it = tmp_path / "p3_it.mp4"
        concat_txt = tmp_path / "concat.txt"

        apply_overlays_to_video(p1_raw, p1_it, lambda _: ov_p1)
        apply_overlays_to_video(p3_raw, p3_it, lambda _: ov_p3)

        concat_txt.write_text(
            f"file '{p1_it.as_posix()}'\nfile '{p2_it.as_posix()}'\nfile '{p3_it.as_posix()}'\n",
            encoding="utf-8",
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_txt),
                "-c:v",
                "libx264",
                "-crf",
                "15",
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(out_final),
            ],
            check=True,
            stderr=subprocess.DEVNULL,
        )
    print(f"Final assembled silent reel saved to {out_final}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assemble", nargs=2, metavar=("P1_MP4", "P3_MP4"), help="Assemble final video with P1 and P3 clips.")
    parser.add_argument("--out", default=str(CLIPS_DIR / "FINAL-REEL-EVA-ITALIANO.mp4"))
    parser.add_argument("--verify", action="store_true", help="Extract verification frames for Part 2.")
    args = parser.parse_args()

    if args.assemble:
        assemble_final(Path(args.assemble[0]), Path(args.assemble[1]), Path(args.out))
    else:
        vdir = BASE_DIR / "frames_clean" / "_verify_it" if args.verify else None
        build_part2_italian(verify_dir=vdir)


if __name__ == "__main__":
    main()
