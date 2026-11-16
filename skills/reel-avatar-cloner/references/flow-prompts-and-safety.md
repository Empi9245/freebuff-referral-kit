# Google Flow Prompts, Anti-Filter & Anti-Uncanny-Eye Guide (Manual Generation)

This reference holds all proven Google Flow (`Omni 1.2 Flash`) rules learned in production and verified across Reddit (`r/VEO3`, `r/aivideo`, `r/GoogleFlow`, `r/StableDiffusion`), GitHub (`awesome-ai-video-prompts`, `LivePortrait`, `FacePoke`), and X creator workflows so you never waste credits, trigger false-positive blocks, or get robotic/uncanny eye movements.

---

## 1. Fixed Google Flow Settings

- **Model:** `Omni 1.2 Flash`
- **Aspect Ratio:** `9:16` (Vertical)
- **Outputs:** `x1` (30 credits per generation)
- **Audio:** Always strip audio from reference clips before uploading (`-an`) and specify silent video in the prompt.

---

## 2. Character Anchor — `@Eva`

When referencing Eva (`avatar_ref/eva_turnaround_1.jpg` or `resources/eva_front_single.png`):
- **MUST specify single person:** *"One single 28-year-old adult female software developer matching the attached character sheet (do not render multiple heads)"*
- **Safe description (no filter triggers):**
  `high dark-brown bun hairstyle, round tortoiseshell eyeglasses, small silver hoop earrings, light natural freckles, wearing a modest loose white long-sleeve crew-neck sweatshirt`

---

## 3. Anti-Filter Rules (Preventing False-Positive "Sexual Content" Blocks)

Google Flow's `Omni 1.2 Flash` runs **both** a text filter and a **pre-generation visual frame scanner** on attached reference clips.

### Words that trigger false positives — NEVER USE:
| Avoid | Safe Replacement |
|---|---|
| `chestnut` (contains `chest`) | `dark-brown` |
| `selfie` | `handheld phone camera portrait shot` |
| `tight` / `center-bottom` | `close portrait shot from arm's length` / `lower-center foreground` |
| `lips` / `mouth` / `skin` | `calm, friendly, confident expression` / `unedited mobile camera video texture` |
| `girl` / `young` | `28-year-old adult female software developer` |
| `touching/brushing hair` | `lowers her left hand away from her glasses` |
| `bedroom` / `bed` | `cozy indoor study room with beige wall, framed wall artwork, wooden headboard trim, patterned curtain edge` |
| `tank top` / `sleeveless` | `modest loose white long-sleeve crew-neck sweatshirt` |
| `horn` (wall decor) | omit background object name or use `warm indoor wall interior` |
| `replace the girl` | omit "replace" phrasing; describe the scene directly |

### Visual Reference Rule:
1. Try attaching the **cleaned mute reference clip** (`parteX_ref_clean.mp4`) + Eva's character sheet (`eva_front_single.png` or `eva_turnaround_1.jpg`) first.
2. **If Google Flow blocks the prompt claiming sexual content even with safe text**, the visual scanner is rejecting the real person's close-up clip or bedroom/sleeveless background! Immediately:
   - **Remove** the original person's video clip (`parteX_ref_clean.mp4`) from the prompt box.
   - Attach **ONLY Eva's character sheet** (or a previously approved Flow clip of Eva in a similar setting).
   - Use **Template B (Bulletproof Anti-Filter)**.

---

## 4. Anti-Uncanny-Eye & Gaze-Alignment Laws (Fixing "Fake AI Eyes")

Video diffusion models fail on eyes when prompts fight the driving reference video, move pupils without head motion, or chain multiple gaze targets in <2 seconds. Always apply these **5 Laws**:

1. **Inspect Reference Gaze BEFORE Writing the Prompt:**
   Extract boundary frames of `parteX_ref_clean.mp4` (`f_start..f_end`) and verify where the original subject actually looks (e.g., in Reel 09 `0:00–4.6s` she keeps eyelids closed, and at `4.6s–6.0s` she tilts her chin up and looks **toward upper `camera-left`** — NEVER prompt `"right"` when the driving video looks `"camera-left"`!).
2. **Head-Lead Rule (Never Prompt Pure Eyeball Rotation):**
   Never write `"eyes look sideways"` or `"shifts gaze right"` with a stationary head — models freeze the head axis and slide irises horizontally like marbles (*eyeball sliding* + *scleral show*). Always lead gaze shifts with **chin/head motion**:
   `"her chin and forehead tilt gently upward toward upper camera-left as her eyelids part..."`
3. **Single-Target Gaze Lock (Decide Gaze Target BEFORE Eyelids Open):**
   Never chain `"eyes closed -> opens eyes -> looks forward -> darts sideways"`. Have eyelids part directly onto **one single fixed focal point** and hold steadily for the remaining 1.5s:
   `"eyelids separate smoothly without rolling upward, both dark-brown irises lock cleanly onto one single fixed off-camera spot toward upper camera-left and remain steady"`
4. **Always Use Viewer Coordinates (`camera-left` / `camera-right`) & `"gazing"`:**
   Screen-space `camera-left` / `camera-right` removes viewer-vs-subject ambiguity, and `gazing` / `gaze locks` outperforms `looking` (which causes dead-eye stares).
5. **Biological Optical Cues & Explicit Anti-Warp Constraints (Flow-Safe):**
   Include: `"moist natural corneal catchlights behind her lenses, gentle brow tension, continuous facial and iris symmetry, zero lateral eyeball sliding within stationary eyelids, zero white-sclera rolling, 24fps organic handheld motion"`.

### Zero-Credit Post-Production Fixes (When One Good Generation Only Drifts at the End)
- **Method A — Temporal Trim / Cadence Hold:** If frames `0..open` and the first `10–15` open-eye frames are lifelike while a 2-frame lid-roll or final `0.5s` eyeball drift happens, excise only the bad tail/roll frames and cleanly hold/ease across the clean open-eye window.
- **Method B — Open-Source Neural Eye Retargeting (Zero Retries):** `PowerHouseMan/ComfyUI-AdvancedLivePortrait` (`cyberterm/ComfyUI-AdvancedLivePortrait-Universal` fork) `ExpressionEditor` (`pupil_x`, `pupil_y`, `blink` sliders), `jbilcke-hf/FacePoke`, or `KlingAIResearch/LivePortrait` (`flag_eye_retargeting`).

---

## 5. Proven Prompt Templates (Ready to Copy-Paste)

### Template A — With Cleaned Reference Video (`parteX_ref_clean.mp4` + `@Eva`)
```text
Vertical 9:16 handheld phone camera portrait video in an indoor room matching the exact framing, camera angle, background colors, warm natural lighting, and beat timing of the attached reference clip.
Subject: One single 28-year-old adult female software developer matching the attached character sheet (do not render multiple heads), high dark-brown bun hairstyle, round tortoiseshell eyeglasses, small silver hoop earrings, wearing a modest loose white long-sleeve crew-neck sweatshirt.
Action: From 0.0s to {T_SWITCH}s, {SAFE BEAT 1 WITH HEAD POSTURE & EYELID STATE}. From {T_SWITCH}s to {T_END}s, leading smoothly with {CHIN/HEAD ROTATION DIRECTION}, {EYELID TRANSITION} directly onto one single fixed off-camera spot toward {camera-left / camera-right / lens-center} with {EXPRESSION} and natural moist corneal catchlights. Zero secondary gaze shifts after opening, no lateral eyeball sliding within stationary head alignment, no white-sclera rolling, continuous facial and iris symmetry.
Style: Unedited indoor smartphone video texture, subtle natural handheld breathing motion, soft ambient grain, shallow focus on eyes and eyewear. Silent clip with no speech, no dialogue, no audio, and no text on screen.
```

### Template B — Bulletproof Anti-Filter (`@Eva` Character Sheet Only, Zero False Positives)
```text
Vertical 9:16 handheld smartphone portrait video in {SAFE_INDOOR_SETTING — e.g. "a warm indoor room with a beige wall, a framed warm-toned artwork on the wall behind to camera-left, wooden trim, and a warm curtain edge on camera-right"}.
One single 28-year-old adult female software developer matching the attached character sheet (do not render multiple heads), high dark-brown bun hairstyle, round tortoiseshell eyeglasses, small silver hoop earrings, wearing a modest loose white long-sleeve crew-neck sweatshirt.
Framing: medium-close eye-level portrait shot from arm's length, subject centered in the lower-center foreground, crisp focus on eyeglasses and eyes, shallow depth of field.
Timeline Action:
0.0s to {T_SWITCH}s: {BEAT 1 — natural breathing, hands posture, eyelid state}.
{T_SWITCH}s to {T_END}s: leading smoothly with {HEAD/CHIN MOTION}, {EYELID PARTING / GAZE LOCK onto one single fixed focal point in camera-left / camera-right coordinates}, moist natural corneal catchlights behind her lenses, stable pupils with subtle biological micro-adjustments only, zero secondary sideways eyeball darting, zero scleral roll, authentic organic motion.
Style: Soft indoor ambient lighting and natural window fill, authentic unedited phone camera footage texture, 24fps organic motion, silent clip with no speech, no dialogue, no audio, and no text on screen.
```
