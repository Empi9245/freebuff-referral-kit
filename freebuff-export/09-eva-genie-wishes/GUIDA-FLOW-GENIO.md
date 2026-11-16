# Guida Google Flow — Reel 09 ("Genio: Hai 3 Desideri" / Freebuff)

**Stato attuale:**
- ✅ **Parte 2 B-Roll MacBook (`6.00s – 9.83s`)** pulita con ricostruzione temporale 4-DOF (zero contorni distorti!) in [`clips/parte2_macbook_italiano.mp4`](file:///c:/Progetti%20Exeva/CuriousEva/freebuff-export/09-eva-genie-wishes/clips/parte2_macbook_italiano.mp4).
- ✅ **Fix occhi post-produzione già applicato** sull'ultima generazione di `@Eva` (`clips/FINAL-REEL-EVA-ITALIANO.mp4`): rimossi i 3 frame di rotazione sclera (`f114–116`) e lo scorrimento innaturale laterale negli ultimi `0.65s` (`f126–143`).
- 📋 Sotto trovi i **prompt migliorati** (basati sulla ricerca Reddit / GitHub / X contro lo sguardo "finto" da AI) nel caso tu voglia rigenerarla da zero.

---

## Le 5 Regole Anti-"Sguardo Finto" (Reddit `r/VEO3`, `r/aivideo`, `r/StableDiffusion`, GitHub, X)

1. **Head-Lead Rule (mai occhi che ruotano da soli):** non scrivere *"looks sideways"* senza prima descrivere il movimento della testa/mento (`tilts her chin upward and slightly toward camera-left`), altrimenti la AI blocca la testa e fa scivolare solo le pupille come palline.
2. **Single-Target Gaze Lock:** gli occhi devono aprirsi **già puntati verso un unico punto fisso** senza un secondo cambio di direzione negli ultimi 1.5s.
3. **Coordinate "camera-left / camera-right" allineate al video reference:** nel video originale la ragazza apre gli occhi guardando **verso l'alto a sinistra dell'inquadratura (`camera-left`)**, per leggere la pillola in alto. Il testo "right" creava conflitto con il video reference!
4. **Cues Ottici Biologici:** `moist corneal catchlights`, `natural blinking transition`, `subtle upper-eyelid weight`, `micro-saccades synced with head posture`.
5. **Vincoli Anti-Artefatto (Flow-safe):** `continuous iris symmetry, zero lateral eyeball sliding within static eyelids, no erratic pupil darting, no white-sclera eye-roll`.

---

## Impostazioni Google Flow

- **Modello:** `Omni 1.2 Flash` · **Formato:** `9:16` · **Output:** `x1` (30 crediti)
- **Sempre allegato:** `avatar_ref/eva_front_single.png` (o `eva_turnaround_1.jpg`).
- **Opzione A:** allega anche [`clips/parte1_ref_clean.mp4`](file:///c:/Progetti%20Exeva/CuriousEva/freebuff-export/09-eva-genie-wishes/clips/parte1_ref_clean.mp4).

---

## Prompt Riscritti (Anti-"Occhi Finti" & Filter-Safe)

### Opzione A — Con Video Reference (`parte1_ref_clean.mp4` + `@Eva`)
```text
Vertical 9:16 handheld phone camera portrait video in an indoor room matching the exact framing, camera angle, background colors, warm natural lighting, and beat timing of the attached reference clip.
Subject: One single 28-year-old adult female software developer matching the attached character sheet (do not render multiple heads), high dark-brown bun hairstyle, round tortoiseshell eyeglasses, small silver hoop earrings, wearing a modest loose white long-sleeve crew-neck sweatshirt.
Action: From 0.0s to 4.5s, she holds her hands clasped together at chest height in a sincere wishing gesture with both eyelids relaxed and fully closed. From 4.5s to 6.0s, her chin and forehead tilt gently upward toward the top camera-left corner as her eyelids part smoothly into a soft, surprised expression: both dark-brown irises lock cleanly onto one single fixed off-camera spot toward the upper camera-left edge of the frame and remain steady with natural moist corneal catchlights and slight brow tension. Zero secondary gaze shifts after opening, no lateral eyeball sliding within stationary head alignment, no white-sclera rolling, continuous facial and iris symmetry.
Style: Unedited indoor smartphone video texture, subtle natural handheld breathing motion, soft ambient grain, shallow focus on eyes and eyewear. Silent clip with no speech, no dialogue, no audio, and no text on screen.
```

---

### Opzione B — Solo `@Eva` (Anti-Filtro Blindata + Sguardo Naturale, senza video reference)
Se Flow rifiuta la clip con Opzione A, **rimuovi `parte1_ref_clean.mp4`**, allega **SOLO `eva_front_single.png`** e usa:

```text
Vertical 9:16 handheld smartphone portrait video in a warm indoor room with a beige wall, a framed warm-toned artwork on the wall behind to camera-left, dark wood headboard trim, and an orange-patterned curtain edge on camera-right.
One single 28-year-old adult female software developer matching the attached character sheet (do not render multiple heads), high dark-brown bun hairstyle, round tortoiseshell eyeglasses, small silver hoop earrings, wearing a modest loose white long-sleeve crew-neck sweatshirt.
Framing: medium-close eye-level portrait shot from arm's length, subject centered in the lower-center foreground, crisp focus on eyeglasses and eyes, shallow depth of field.
Timeline Action:
0.0s to 4.4s: she keeps her hands clasped together at chest height in a heartfelt wishing gesture, eyelids smoothly closed, relaxed peaceful expression, very slight natural breathing motion.
4.4s to 6.0s: leading smoothly with her chin tilting slightly upward and a 12-degree head turn toward camera-left, her eyelids separate naturally without rolling upward, locking directly onto one single fixed focal point toward upper camera-left with surprised raised eyebrows and attentive stillness. Moist natural corneal catchlights behind her lenses, stable pupils with subtle natural focal micro-adjustments only, zero secondary sideways eyeball darting, zero scleral roll, authentic biological motion.
Style: Soft indoor ambient light and natural window fill, authentic unedited phone camera footage texture, 24fps organic motion, silent clip with no speech, no dialogue, no audio, and no text on screen.
```
