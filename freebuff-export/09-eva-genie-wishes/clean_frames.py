"""Clean text overlays: 4-DOF temporal screen reconstruction for MacBook B-roll (Part 2) + Telea for Part 1."""
from __future__ import annotations

import os
import subprocess
import sys
import cv2
import numpy as np


BASE = r"c:\Progetti Exeva\CuriousEva\freebuff-export\09-eva-genie-wishes"
CLIPS = os.path.join(BASE, "clips")
CLEAN_SAMPLES = os.path.join(BASE, "frames_clean")

RNG = np.random.default_rng(2026)


def rounded_rect_mask(shape: tuple[int, int], rect: tuple[int, int, int, int], radius: int = 18) -> np.ndarray:
    """Draw a filled rounded-rectangle mask in grayscale uint8."""
    h, w = shape
    x1, y1, x2, y2 = rect
    mask = np.zeros((h, w), dtype=np.uint8)
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    cv2.rectangle(mask, (x1 + r, y1), (x2 - r, y2), 255, -1)
    cv2.rectangle(mask, (x1, y1 + r), (x2, y2 - r), 255, -1)
    for cx, cy in ((x1 + r, y1 + r), (x2 - r, y1 + r), (x1 + r, y2 - r), (x2 - r, y2 - r)):
        cv2.circle(mask, (cx, cy), r, 255, -1)
    return mask


def dilate_ellipse(mask: np.ndarray, rx: int, ry: int) -> np.ndarray:
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rx + 1, 2 * ry + 1))
    return cv2.dilate(mask, k)


def build_silhouette_mask(
    bgr: np.ndarray,
    roi: tuple[int, int, int, int],
    extra_circle: tuple[int, int, int] | None = None,
) -> np.ndarray:
    """Detect outlined white TikTok letters (+ optional emoji circle) for Part 1 avatar reference."""
    x1, y1, x2, y2 = roi
    crop = bgr[y1:y2, x1:x2]
    b, g, r = crop[:, :, 0], crop[:, :, 1], crop[:, :, 2]
    mx = np.maximum(np.maximum(b, g), r)
    mn = np.minimum(np.minimum(b, g), r)

    white = (mn > 200) & ((mx - mn) < 40)
    dark_core = mx < 55
    w_near = cv2.dilate(white.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) > 0
    stroke_core = dark_core & w_near
    s_near = cv2.dilate(stroke_core.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))) > 0
    letter_core = white & s_near

    combined = ((letter_core | stroke_core).astype(np.uint8)) * 255
    closed = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    mask_roi = cv2.dilate(closed, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 7)))

    full_mask = np.zeros(bgr.shape[:2], dtype=np.uint8)
    full_mask[y1:y2, x1:x2] = mask_roi
    if extra_circle is not None:
        cx, cy, rad = extra_circle
        cv2.circle(full_mask, (cx, cy), rad, 255, -1)
    return full_mask


def inpaint_with_grain(bgr: np.ndarray, mask: np.ndarray, radius: int = 5, sigma: float = 1.3) -> np.ndarray:
    """Run TELEA inpainting and add subtle sensor grain strictly inside the masked region."""
    if not np.any(mask):
        return bgr
    cleaned = cv2.inpaint(bgr, mask, inpaintRadius=radius, flags=cv2.INPAINT_TELEA)
    noise = RNG.normal(0.0, sigma, cleaned.shape).astype(np.float32)
    m_bool = mask > 0
    out = cleaned.astype(np.float32)
    out[m_bool] += noise[m_bool]
    return np.clip(out, 0, 255).astype(np.uint8)


def encode_frames_to_mp4(frames: list[np.ndarray], out_mp4: str, fps: float = 30.0) -> None:
    """Pipe BGR frames directly into mute H.264 MP4 via ffmpeg."""
    h, w = frames[0].shape[:2]
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{w}x{h}", "-pix_fmt", "bgr24", "-r", str(fps),
        "-i", "-",
        "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
        out_mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for fr in frames:
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    err = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed for {out_mp4}:\n{err}")


def clean_part1() -> None:
    in_mp4 = os.path.join(CLIPS, "parte1_genie_avatar_ref.mp4")
    out_mp4 = os.path.join(CLIPS, "parte1_ref_clean.mp4")
    cap = cv2.VideoCapture(in_mp4)
    cleaned_frames: list[np.ndarray] = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        mask = rounded_rect_mask((h, w), (144, 130, 576, 208), radius=20)
        if idx <= 163:
            mask |= rounded_rect_mask((h, w), (88, 200, 632, 290), radius=20)
            mid_mask = build_silhouette_mask(
                frame,
                roi=(92, 740, 630, 862),
                extra_circle=(563, 825, 29),
            )
            mask |= mid_mask
        else:
            mask |= rounded_rect_mask((h, w), (40, 200, 680, 292), radius=20)
        mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        cleaned = inpaint_with_grain(frame, mask, radius=7, sigma=1.3)
        cleaned_frames.append(cleaned)
        if idx in (50, 163, 164, 170):
            cv2.imwrite(os.path.join(CLEAN_SAMPLES, f"p1_clean_f{idx:03d}.png"), cleaned)
        idx += 1
    cap.release()
    encode_frames_to_mp4(cleaned_frames, out_mp4, fps=30.0)
    print(f"Cleaned Part 1 ({len(cleaned_frames)} frames) -> {out_mp4}")


# --- 4-DOF Temporal Screen Reconstruction for Part 2 ---

def get_white_core(
    frames: list[np.ndarray],
    s: int,
    e: int,
    roi: tuple[int, int, int, int],
) -> np.ndarray:
    """Static temporal-invariant white glyph core across frames [s..e]."""
    x1, y1, x2, y2 = roi
    stack = np.stack([frames[i][y1:y2, x1:x2] for i in range(s, e + 1)], axis=0)
    min_bgr = np.min(stack, axis=0)
    white = (np.min(min_bgr, axis=2) > 170).astype(np.uint8) * 255
    full = np.zeros(frames[0].shape[:2], dtype=np.uint8)
    full[y1:y2, x1:x2] = white
    return full


def horizontal_scanline_inpaint(img_f: np.ndarray, mask_bool: np.ndarray) -> np.ndarray:
    """Fill residual pixels strictly along horizontal scanlines to preserve crisp UI card edges."""
    out = img_f.copy()
    ys, _ = np.where(mask_bool)
    if len(ys) == 0:
        return out
    for y in np.unique(ys):
        row_m = mask_bool[y]
        valid_x = np.where(~row_m)[0]
        if len(valid_x) == 0:
            continue
        missing_x = np.where(row_m)[0]
        for c in range(3):
            out[y, missing_x, c] = np.interp(missing_x, valid_x, out[y, valid_x, c])
    blurred = cv2.GaussianBlur(out, (11, 3), 2.5)
    out[mask_bool] = blurred[mask_bool]
    return out


def reconstruct_segment_temporal(
    frames: list[np.ndarray],
    grays: list[np.ndarray],
    s: int,
    e: int,
    core_mask: np.ndarray,
    track_y: tuple[int, int] = (310, 850),
    target_rx: int = 11,
    target_ry: int = 10,
    donor_rx: int = 14,
    donor_ry: int = 13,
    min_y: int | None = None,
    force_horiz_x_lt_by_frame: dict[int, int] | None = None,
    crop_y: tuple[int, int] = (540, 820),
) -> dict[int, np.ndarray]:
    """Reconstruct text-occluded UI pixels from moving donor frames using 4-DOF affine tracking."""
    h, w = frames[0].shape[:2]
    cy0, cy1 = crop_y
    ch = cy1 - cy0

    text_mask = dilate_ellipse(core_mask, target_rx, target_ry)
    donor_excl = dilate_ellipse(core_mask, donor_rx, donor_ry)
    if min_y is not None:
        text_mask[:min_y, :] = 0
        donor_excl[:min_y, :] = 0

    track_base = np.zeros((h, w), dtype=np.uint8)
    track_base[track_y[0]:track_y[1], 40:680] = 255
    track_mask = cv2.bitwise_and(track_base, cv2.bitwise_not(donor_excl))

    M_step: dict[int, np.ndarray] = {}
    for i in range(s, e):
        pts0 = cv2.goodFeaturesToTrack(
            grays[i], maxCorners=500, qualityLevel=0.005, minDistance=5, mask=track_mask
        )
        if pts0 is None or len(pts0) < 12:
            M_step[i] = np.eye(3, dtype=np.float64)
            continue
        pts1, st, _ = cv2.calcOpticalFlowPyrLK(
            grays[i], grays[i + 1], pts0, None, winSize=(25, 25), maxLevel=4
        )
        good0 = pts0[st.flatten() == 1]
        good1 = pts1[st.flatten() == 1]
        if len(good0) < 12:
            M_step[i] = np.eye(3, dtype=np.float64)
            continue
        M, _ = cv2.estimateAffinePartial2D(good0, good1, method=cv2.RANSAC, ransacReprojThreshold=1.5)
        if M is None:
            M_step[i] = np.eye(3, dtype=np.float64)
        else:
            M_step[i] = np.vstack([M, [0.0, 0.0, 1.0]])

    def get_M_src_to_t(src: int, t: int) -> np.ndarray:
        M3 = np.eye(3, dtype=np.float64)
        if src < t:
            for k in range(src, t):
                M3 = M_step[k] @ M3
        elif src > t:
            for k in range(t, src):
                M3 = M_step[k] @ M3
            M3 = np.linalg.inv(M3)
        M_crop = M3[:2, :].copy()
        M_crop[1, 2] -= float(cy0)
        return M_crop

    clean_donor_valid = cv2.GaussianBlur((donor_excl == 0).astype(np.float32), (5, 5), 1.0)
    text_mask_c = text_mask[cy0:cy1, :] > 0
    target_valid_c = (donor_excl[cy0:cy1, :] == 0).astype(np.float32)
    outer_ring_c = (dilate_ellipse(core_mask, target_rx + 5, target_ry + 5)[cy0:cy1, :] > 0) & (
        donor_excl[cy0:cy1, :] == 0
    )
    alpha_c = cv2.GaussianBlur(text_mask_c.astype(np.float32), (7, 7), 1.5)

    results: dict[int, np.ndarray] = {}
    for t in range(s, e + 1):
        full_out = frames[t].copy()
        target_c = full_out[cy0:cy1, :].astype(np.float32)
        horiz_init = horizontal_scanline_inpaint(target_c, text_mask_c)

        acc_color = np.zeros((ch, w, 3), dtype=np.float64)
        acc_weight = np.zeros((ch, w), dtype=np.float64)

        for src in range(s, e + 1):
            if src == t:
                continue
            M_crop = get_M_src_to_t(src, t)
            warped_bgr = cv2.warpAffine(
                frames[src], M_crop, (w, ch), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
            ).astype(np.float32)
            warped_valid = cv2.warpAffine(
                clean_donor_valid,
                M_crop,
                (w, ch),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            )

            ring_valid = outer_ring_c & (warped_valid > 0.9)
            if np.sum(ring_valid) > 80:
                diff_med = np.median(target_c[ring_valid] - warped_bgr[ring_valid], axis=0)
                warped_bgr = np.clip(warped_bgr + diff_med, 0, 255)

            both_valid = target_valid_c * (warped_valid > 0.85).astype(np.float32)
            abs_diff = np.mean(np.abs(target_c - warped_bgr), axis=2) * both_valid
            local_err_num = cv2.GaussianBlur(abs_diff, (41, 41), 12.0)
            local_err_den = cv2.GaussianBlur(both_valid, (41, 41), 12.0) + 1e-4
            local_err = local_err_num / local_err_den
            local_match_w = np.exp(-((local_err / 6.5) ** 2))

            valid_w = np.clip((warped_valid - 0.75) * 4.0, 0.0, 1.0) ** 2
            temporal_w = 1.0 / (1.0 + 0.12 * abs(src - t))
            w_map = valid_w * temporal_w * local_match_w
            acc_color += warped_bgr.astype(np.float64) * w_map[:, :, None]
            acc_weight += w_map

        # If a specific frame has a UI hover transition on the left region, use clean scanline fill there
        if force_horiz_x_lt_by_frame and t in force_horiz_x_lt_by_frame:
            x_cut = force_horiz_x_lt_by_frame[t]
            acc_weight[:, :x_cut] = 0.0

        has_donor = acc_weight > 0.02
        rec_pct = 100.0 * float(np.mean(has_donor[text_mask_c])) if np.any(text_mask_c) else 0.0
        donor_rgb = np.where(
            has_donor[:, :, None],
            acc_color / np.maximum(acc_weight[:, :, None], 1e-4),
            horiz_init,
        )
        donor_conf = np.clip(acc_weight / 0.12, 0.0, 1.0)[:, :, None]
        prelim = donor_conf * donor_rgb + (1.0 - donor_conf) * horiz_init

        # Subtle sensor grain inside masked area only so filled texture matches real phone footage
        noise = RNG.normal(0.0, 1.15, prelim.shape).astype(np.float32)
        prelim = np.clip(prelim + noise, 0, 255)

        blended_c = target_c * (1.0 - alpha_c[:, :, None]) + prelim * alpha_c[:, :, None]
        full_out[cy0:cy1, :] = np.clip(blended_c, 0, 255).astype(np.uint8)
        results[t] = full_out
        if t in (15, 45, 63, 67, 70, 100):
            print(f"  Frame {t:3d}: temporal recovered {rec_pct:.1f}% of text mask")
    return results


def clean_part2() -> None:
    in_mp4 = os.path.join(CLIPS, "parte2_macbook_broll_ref.mp4")
    out_mp4 = os.path.join(CLIPS, "parte2_macbook_clean.mp4")

    cap = cv2.VideoCapture(in_mp4)
    frames: list[np.ndarray] = []
    while True:
        ret, fr = cap.read()
        if not ret:
            break
        frames.append(fr)
    cap.release()
    grays = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

    # Step A: Clean top Genie pill strictly inside the replacement pill coords across all frames
    h, w = frames[0].shape[:2]
    top_mask = rounded_rect_mask((h, w), (150, 135, 573, 207), radius=18)
    top_mask |= rounded_rect_mask((h, w), (43, 203, 676, 290), radius=18)
    top_cleaned = [inpaint_with_grain(f, top_mask, radius=6, sigma=1.1) for f in frames]

    # Step B: Temporal 4-DOF screen reconstruction per sub-clip on original frames, then copy top pill area
    print("Cleaning 2A (frames 2..30)...")
    c2a = get_white_core(frames, 2, 30, (64, 612, 656, 660))
    r2a = reconstruct_segment_temporal(
        frames, grays, 2, 30, c2a, track_y=(320, 840), target_rx=11, target_ry=9, donor_rx=14, donor_ry=11, min_y=609
    )

    print("Cleaning 2B (frames 33..58)...")
    c2b = get_white_core(frames, 33, 58, (172, 610, 548, 662))
    r2b = reconstruct_segment_temporal(frames, grays, 33, 58, c2b, track_y=(320, 840))

    print("Cleaning 2C popup state (frames 60..66)...")
    c2c = get_white_core(frames, 60, 86, (140, 602, 588, 660))
    r2c_1 = reconstruct_segment_temporal(frames, grays, 60, 66, c2c, track_y=(480, 830))

    print("Cleaning 2C cards state (frames 67..86)...")
    r2c_2 = reconstruct_segment_temporal(
        frames,
        grays,
        67,
        86,
        c2c,
        track_y=(480, 830),
        force_horiz_x_lt_by_frame={67: 215},
    )

    print("Cleaning 2D (frames 89..114)...")
    c2d_main = get_white_core(frames, 89, 114, (205, 606, 515, 662))
    c2d_sub = get_white_core(frames, 91, 114, (240, 728, 480, 766))
    r2d_pre = reconstruct_segment_temporal(frames, grays, 89, 90, c2d_main, track_y=(320, 840))
    r2d_full = reconstruct_segment_temporal(frames, grays, 89, 114, c2d_main | c2d_sub, track_y=(320, 840))

    cleaned_frames: list[np.ndarray] = []
    for idx in range(len(frames)):
        if 2 <= idx <= 30:
            res = r2a[idx].copy()
        elif 33 <= idx <= 58:
            res = r2b[idx].copy()
        elif 60 <= idx <= 66:
            res = r2c_1[idx].copy()
        elif 67 <= idx <= 86:
            res = r2c_2[idx].copy()
        elif 89 <= idx <= 90:
            res = r2d_pre[idx].copy()
        elif 91 <= idx <= 114:
            res = r2d_full[idx].copy()
        else:
            res = frames[idx].copy()

        # Copy cleaned top pill region onto frame
        res[:300, :] = top_cleaned[idx][:300, :]
        cleaned_frames.append(res)
        if idx in (15, 45, 63, 67, 70, 100):
            cv2.imwrite(os.path.join(CLEAN_SAMPLES, f"p2_clean_f{idx:03d}.png"), res)

    encode_frames_to_mp4(cleaned_frames, out_mp4, fps=30.0)
    print(f"Cleaned Part 2 ({len(cleaned_frames)} frames) -> {out_mp4}")


if __name__ == "__main__":
    os.makedirs(CLEAN_SAMPLES, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "part1"):
        clean_part1()
    if mode in ("all", "part2"):
        clean_part2()
