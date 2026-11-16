# Guida Completa: Replicare il Video Virale Freebuff con `@Eva` in Google Flow (Veo 3.1)

**Video originale analizzato:** `source_reference.mp4` (`720×1280`, `9:16`, `30 fps`, durata `12.13 s`)  
**Obiettivo:** Sostituire la ragazza con il tuo avatar AI **`@Eva`** (già impostato nei *Characters / Ingredients* di Google Flow), mantenere la grafica di **Freebuff (`freebuff.com`)** reale al 100% (senza artefatti "effetto AI"), tradurre tutte le scritte in italiano e chiudere con **`seguici e commenta "promo" per ricevere l'app`**.

---

## 1. I Metodi Aggiornati (Reddit `r/VEO3` / `r/GoogleFlow`, YouTube, X, TikTok)

Sintesi delle tecniche più efficaci usate dai creator AI UGC su Reddit, YouTube, X e TikTok per far sembrare un video generato con **Google Flow + Veo 3.1** indistinguibile da un TikTok/Reel girato col telefono:

1. **Regola Anti-AI UGC (Niente "cinematic 4k, studio lighting"):**
   - Le parole chiave *"cinematic"*, *"8k"*, *"ring light"* o *"studio lighting"* attivano l'estetica patinata tipica dell'AI ("plastic skin", occhi vitrei, movimento fluttuante).
   - **Cosa funziona su Google Flow / Veo 3.1:** forzare difetti reali da smartphone:
     `raw iPhone front-facing selfie camera, vertical 9:16, handheld micro-jitters, slight digital sensor grain, uneven warm indoor café lighting, no ring light, natural skin texture with visible pores, stray flyaway hairs, casual off-center arms-length framing`.
2. **Tag `@Eva` + `Ingredients to Video` (max 3 ingredienti):**
   - Su Google Flow (`flow.google`), imposta **Veo 3.1** (modalità **Highest Quality**, formato **9:16 Vertical**).
   - Nella modalità **Ingredients to Video**, usa `@Eva` come soggetto principale e allega:
     1) il profilo/reference di **`@Eva`** (già salvato nel progetto Flow);
     2) un riferimento visivo dell'ambiente bistrot (puoi usare i frame estratti `frames_raw/p1_start_00_20.png` o `p3_end_11_80.png` come **solo riferimento di stile/luce/location**, specificando esplicitamente nel prompt di sostituire la ragazza con `@Eva`);
     3) per la continuità tra Parte 1 e Parte 3, usa il **"Last-Frame / Asset Save Trick"** di Flow: salva un frame della clip generata nella Parte 1 e passalo come riferimento d'ambiente/outfit per la Parte 3, così maglia bianca, luce e parete del bar restano identici al 100%.
3. **Zero testi generati dentro Google Flow:**
   - Non chiedere MAI a Veo/Google Flow di scrivere scritte TikTok o emoji italiane: i modelli deformano i caratteri e rovinano i bordi. Genera i video **100% puliti senza testo** e aggiungi le scritte italiane in **CapCut** o nativamente su **Instagram / TikTok** usando il font classico bianco con bordo nero.
4. **Il segreto della community per la Grafica del MacBook (Parte 2 — "Real B-Roll Sandwich" vs "Frames to Video"):**
   - Anche con Veo 3.1, generare da zero una pagina web con codice, comando terminale `npm install -g freebuff` e numeri `$0/yr` vs `$1,200/yr` produce quasi sempre testo tremolante o illeggibile ("AI slop").
   - Hai **due strade pronte**, già preparate in questa cartella:
     - **OPZIONE A — "Real B-Roll Sandwich" (CONSIGLIATA su Reddit/TikTok, 0% effetto AI sulla grafica):** Generi con Google Flow solo la **Parte 1 (`@Eva` Hook)** e la **Parte 3 (`@Eva` CTA)** nello stesso bar, e in mezzo monti direttamente **`clips/parte2_macbook_clean_no_text.mp4`** (la ripresa reale del MacBook già ripulita dalle scritte inglesi). Poiché nella Parte 2 il volto non compare mai, il pubblico percepisce un video **100% reale e autentico** e la UI di Freebuff resta nitida al pixel.
     - **OPZIONE B — 100% dentro Google Flow con `Frames to Video`:** Se vuoi rigenerare o variare leggermente anche la Parte 2 dentro Google Flow, usa la modalità **Frames to Video** caricando negli slot **First Frame** / **Final Frame** i nostri **keyframe reali già ripuliti** in `frames_clean/`:
       - `frames_clean/p2a_cli_clean.png`
       - `frames_clean/p2b_zoom_chart_clean.png`
       - `frames_clean/p2c_chat_clean.png`
       - `frames_clean/p2d_web_clean.png`
       In questo modo Veo 3.1 non inventa la grafica da zero, ma anima soltanto la micro-oscillazione handheld tra i tuoi frame reali.

---

## 2. Struttura esatta in 3 Parti (Taglio frame-accurate dal video originale)

| Parte | Timecode Originale | Durata | File Clip di Riferimento | Cosa succede |
|---|---|---|---|---|
| **Parte 1 — Hook Selfie (`@Eva`)** | `00:00.00 – 00:02.33` | `2.33 s` | `clips/parte1_hook_selfie_ref.mp4` | Selfie iPhone nel bistrot. `@Eva` guarda di lato verso destra ("side-eye") sbirciando il portatile del vicino con espressione tra il divertito e l'incredulo. |
| **Parte 2 — POV MacBook Freebuff** | `00:02.33 – 00:10.63` | `8.30 s` | `clips/parte2_macbook_ui_ref.mp4`<br>`clips/parte2_macbook_clean_no_text.mp4` *(pulito)* | 4 micro-stacchi handheld sul MacBook: **2A** Home `freebuff.com` (`npm install -g freebuff`) → **2B** Zoom grafico prezzi (`$0/yr` vs `$1,200/yr`) → **2C** Tab `Chat` (`What can I help with?`) → **2D** Tab `Web` (`The crypto wallet you'll actually love`). |
| **Parte 3 — Outro CTA Selfie (`@Eva`)** | `00:10.63 – 00:12.13` | `1.50 s` | `clips/parte3_cta_selfie_ref.mp4` | Ritorno al selfie iPhone nello stesso bistrot. `@Eva` si sistema una ciocca vicino alla tempia sinistra e guarda dritta in camera con espressione complice e sicura. |

*Tutti i file `.mp4` in questa cartella (`source_reference.mp4` e le clip in `clips/`) sono stati esportati **senza traccia audio (`-an`, 100% muti)** così puoi caricarli direttamente in Google Flow senza interferenze sonore. La traccia audio originale separata resta salvata solo come guida ritmo in `clips/audio_originale.mp3` (ricorda: su Instagram/TikTok è meglio riagganciare il brano originale in-app dal catalogo ufficiale).*

---

## 3. I 3 Prompt Pronti per Google Flow (Copia & Incolla)

> **Impostazioni fisse in Google Flow per tutte le generazioni:**  
> - **Model:** `Omni Flash`  
> - **Risoluzione & Output:** `360p` (per consumare il minimo di crediti) · `x1` (1 output per generazione)  
> - **Aspect Ratio:** `9:16` (Vertical)  
> - **Audio:** **nessun audio richiesto** (ogni prompt forza video muto, zero parlato, labbra chiuse, zero musica/SFX)

---

### Tecniche Aggiornate 2026 (Reddit / X / YouTube) per Character Swap in Video con Omni Flash
1. **Carica il video di riferimento già ripulito dalle scritte:** usa `clips/parte1_ref_clean.mp4` e `clips/parte3_ref_clean.mp4` (muti `-an` e senza testi inglesi sovraimpressi), così `Omni Flash` non copia scarabocchi o lettere inglesi sulla fronte dell'avatar.
2. **Struttura SCAM + Explicit Role-Locking:** quando alleghi sia un **video reference** sia un **personaggio (`@Eva`)**, assegna esplicitamente i ruoli nei primi due versi (`Use the attached video ONLY as motion/camera/lighting/background plate; use @Eva ONLY as facial and hair identity`).
3. **Anti-"troppo perfetto/finto":** vieta espressamente a `Omni Flash` di applicare pelle liscia, luce da studio o color grading cinematografico, imponendogli di preservare la grana iPhone, la compressione reale e la luce imperfetta del bar dal video allegato.

---

### PROMPT 1 — Parte 1: Character Swap su Video Reference (`00:00.00 – 00:02.33`)

- **Modalità Google Flow:** `Omni Flash` · `360p` · `x1` · `9:16` (progetto **`frebuff refferal`**)
- **Ingredienti / Reference da allegare nel prompt box:**
  1. **Video Reference:** `clips/parte1_ref_clean.mp4` *(oppure `frames_clean/p1_start_clean.png` se l'interfaccia in quel momento accetta solo frame/immagini)*
  2. **Character Reference:** `@Eva` (già caricato nel progetto; disponibile anche il ritaglio singolo `eva_character/eva_front_single.png`)

```text
[ROLE ASSIGNMENT] Use the attached video clip as the strict primary motion, camera framing, lighting, and background plate. Use @Eva ONLY as the facial and hair identity reference to swap the person in the video.
[SUBJECT SWAP] Perform a seamless 1:1 character replacement of the girl in the source video with @Eva (single woman only — never render multiple heads from the character sheet): a young Mediterranean woman with a messy high chestnut-brown bun (topknot) with loose wavy face-framing strands, thin round tortoiseshell eyeglasses, light natural freckles across her nose and cheeks, a small beauty mark under her left eye, and small double silver hoop earrings. Keep the exact same neck position, shoulders, posture, and casual white long-sleeve top from the source video.
[ACTION & MOTION LOCK] Track and copy 100% of the original video's head position, eye movement, and timing: she sits in the lower-left foreground selfie framing, looks briefly at the camera lens, then shifts only her eyes sideways to the right (subtle knowing side-eye glance behind her tortoiseshell glasses) with closed lips and natural blinking, matching the exact handheld micro-shake of the source clip.
[REALISM & TEXTURE LOCK] Preserve the exact original café booth background (dark brick wall, warm wooden trim, beige patterned panel, white ceiling tiles) and preserve the raw, unedited, low-grade iPhone front-camera look of the reference video (natural sensor grain, slight compression, uneven warm indoor lighting, unretouched real skin texture). Do NOT apply studio lighting, beauty filters, plastic skin smoothing, or cinematic color grading.
[CONSTRAINTS] Completely silent video, no audio track needed, no speech, closed lips, zero text on screen, no subtitles, no emojis, no watermarks.
```

---

### Parte 2 — POV MacBook Freebuff UI (`00:02.33 – 00:10.63`) — GIÀ PRONTA CON SCRITTE IN ITALIANO

**NON serve rigenerare la Parte 2 in Google Flow.**  
Il file già pronto, muto e con le 4 scritte italiane in stile TikTok/Reels sovrapposte sulla UI reale di Freebuff è:
- **`clips/parte2_macbook_italiano.mp4`** (generato da `add_italian_captions.py` sopra `clips/parte2_macbook_clean_no_text.mp4`).

*(Se per qualsiasi motivo volessi comunque generare la Parte 2 dentro Google Flow, usa `Frames to Video` con i keyframe puliti in `frames_clean/` come mostrato sotto).*

#### Versione Unica (8 secondi — `Frames to Video`)
- **First Frame:** `frames_clean/p2a_cli_clean.png`
- **Final Frame:** `frames_clean/p2d_web_clean.png`

```text
Raw handheld iPhone rear-camera POV video, vertical 9:16 aspect ratio, shooting an open silver MacBook screen from behind on a warm café wooden table, matching the blurred tan wall, brown tufted sofa booth, and wall AC unit in the background.
Smooth realistic handheld camera motion transitioning cleanly from the exact dark-blue Freebuff homepage UI in the starting frame ("We make coding 100% free", "$ npm install -g freebuff" and the $0/yr vs $1,200/yr bar chart) to a slight forward handheld zoom, and then smoothly revealing the dark-blue Freebuff web builder preview in the ending frame.
Keep all laptop screen UI text, monospace code, bar charts, and metallic MacBook keyboard keys crisp, legible, and geometrically stable without warping or hallucinated symbols. Natural indoor lighting with subtle realistic screen glare and mild smartphone sensor grain.
Audio: completely silent video, no audio track needed, no voiceover, no ambient noise, no background music, no sound effects.
Constraints: zero overlay captions, no floating text, no emojis, no watermarks, authentic phone recording feel.
```

#### Versione Ultra-Fedele (consigliata se usi Flow per la Parte 2: divisa in 2 clip `Frames to Video`)
- **Clip 2A (`First Frame`: `frames_clean/p2a_cli_clean.png` -> `Final Frame`: `frames_clean/p2b_zoom_chart_clean.png`)**:
  ```text
  Raw handheld iPhone rear-camera POV video, 9:16 vertical, filming a silver MacBook on a café table. The camera smoothly pushes in and tilts slightly downward from the Freebuff homepage showing "$ npm install -g freebuff" in the first frame to a tight close-up on the green "Download for macOS" button and the pricing comparison bars ("Freebuff $0 / yr" vs "Claude Code $1,200 / yr") in the final frame. Keep every single UI label, icon, number, and aluminum keyboard key razor-sharp and identical to the reference frames. Authentic slight hand shake, mild screen reflection. Audio: completely silent video, no audio track needed, no speech, no music, no sound effects. Constraints: zero overlay text, no emojis, no watermarks.
  ```
- **Clip 2B (`First Frame`: `frames_clean/p2c_chat_clean.png` -> `Final Frame`: `frames_clean/p2d_web_clean.png`)**:
  ```text
  Raw handheld iPhone rear-camera POV video, 9:16 vertical, filming the same silver MacBook on a café table. Natural handheld micro-movement on the clean dark-blue Freebuff Chat interface ("What can I help with?"), followed by a quick natural camera cut to the dark-blue Freebuff Web builder interface ("The crypto wallet you'll actually love", "$42,391.20") in the final frame. Keep all UI typography, buttons, and keyboard geometry completely faithful to the input frames with zero distortion. Real smartphone camera optics. Audio: completely silent video, no audio track needed, no speech, no music, no sound effects. Constraints: zero overlay captions, no emojis, no watermarks.
  ```

---

### PROMPT 3 — Parte 3: Character Swap su Video Reference (`00:10.63 – 00:12.13`)

- **Modalità Google Flow:** `Omni Flash` · `360p` · `x1` · `9:16`
- **Ingredienti / Reference da allegare nel prompt box:**
  1. **Video Reference:** `clips/parte3_ref_clean.mp4` *(oppure `frames_clean/p3_end_clean.png` se l'interfaccia accetta solo immagini)*
  2. **Character Reference:** `@Eva` (già caricato nel progetto; più opzionale frame salvato dalla Parte 1 per continuità)

```text
[ROLE ASSIGNMENT] Use the attached video clip as the strict primary motion, camera framing, hand gesture, lighting, and background plate. Use @Eva ONLY as the facial and hair identity reference to swap the person in the video.
[SUBJECT SWAP] Perform a seamless 1:1 character replacement of the girl in the source video with @Eva (single woman only — never render multiple heads): messy high chestnut-brown bun with loose wavy face-framing strands, thin round tortoiseshell eyeglasses, light natural freckles across her nose and cheeks, small beauty mark under her left eye, and small double silver hoop earrings. Keep the exact same shoulders, hand movement, and casual white long-sleeve top from the source video.
[ACTION & MOTION LOCK] Track and copy 100% of the original video's movement and timing: her hand gently finishes brushing a strand of hair near her left temple and lowers down while she looks straight into the iPhone front camera lens through her round tortoiseshell glasses with the exact same calm, knowing expression and closed lips, matching the exact handheld camera sway of the source clip.
[REALISM & TEXTURE LOCK] Preserve the exact original café background (dark brick wall, framed beige panel, white ceiling tiles, vintage brass horn on the upper left) and preserve the raw, slightly soft, unedited iPhone front-camera sensor grain, compression, and uneven warm indoor lighting of the reference video. Do NOT make it look glossy, sharp, or AI-generated.
[CONSTRAINTS] Completely silent video, no audio track needed, no speech, closed lips, zero text on screen, no subtitles, no emojis, no watermarks.
```

---

## 4. Scritte Tradotte in Italiano + CTA Finale (per CapCut / Instagram / TikTok)

Aggiungi queste scritte **in post-produzione** (CapCut o direttamente nell'editor di Instagram/TikTok) sopra il montaggio pulito.  
**Stile grafico identico all'originale:** font sans-serif arrotondato/bold (su TikTok/CapCut è *TikTok Sans / Proxima Nova Bold* bianco con bordo/stroke nero sottile), centrato nella fascia superiore-media (safe zone `y = 260–550` su `1080×1920`, mai coperto dalla UI).

| Parte | Timecode | Testo Originale (EN) | Testo Tradotto Italiano (Pronto da incollare) | Alternativa più corta/punchy |
|---|---|---|---|---|
| **Parte 1** | `0:00.0 – 0:02.3` | `the guy next to me is using claude😂😂` | **`il tipo accanto a me sta usando claude😭😭`** | `il tipo accanto a me paga ancora claude😭😭` |
| **Parte 2A** | `0:02.3 – 0:04.1` | `he doesn't know there's a free version 💀💀` | **`non sa che esiste la versione gratis💀💀`** | `non sa che c'è gratis💀💀` |
| **Parte 2B** | `0:04.1 – 0:06.4` | `holy mog😭😭` | **`umiliato😭😭`** | `0€ contro 1.200€😭😭` |
| **Parte 2C** | `0:06.4 – 0:08.5` | `free chatgpt dupe` | **`alternativa gratis a chatgpt`** | `clone gratis di chatgpt` |
| **Parte 2D** | `0:08.5 – 0:10.6` | `free website builder` | **`crea siti web gratis`** | `siti web gratis in 1 click` |
| **Parte 3 (CTA)** | `0:10.6 – 0:12.1` | `comment "link" for the link` | **`seguici e commenta "promo" per ricevere l'app`** | **`seguici e commenta "promo"`**<br>**`per ricevere l'app`** *(su 2 righe)* |

> **Nota layout su 2 righe per la CTA finale:** proprio come nell'originale (`comment "link" / for the link`), scrivila su due righe centrate sopra gli occhi/fronte di `@Eva` senza coprirle lo sguardo:
> ```text
> seguici e commenta "promo"
> per ricevere l'app
> ```

---

## 5. Checklist Rapida Montaggio & Pubblicazione (Regole del Progetto)

1. **Montaggio in CapCut / Editor:**
   - Metti in timeline: `[Parte 1 @Eva 2.33s]` → `[Parte 2 MacBook pulita 8.30s]` → `[Parte 3 @Eva 1.50s]`.
   - Aggiungi le 6 card testuali italiane della tabella qui sopra.
   - Esporta **senza watermark CapCut/TikTok** (`1080×1920`, `30 fps`, `H.264`).
2. **Audio:** aggiungi la musica del trend direttamente **in-app** su Instagram/TikTok (o usa `clips/audio_originale.mp3` se pubblichi come audio originale).
3. **Caption pronta (validata con `ig-human` e `ig-caption`):**
   ```text
   Seguici e commenta PROMO per ricevere l'app gratis.

   Ero al bar. Il tipo accanto a me pagava 20 euro al mese per Claude, altri 20 per Cursor e usava ChatGPT a pagamento.

   Zero senso. Con Freebuff fai coding ai dal terminale, usi la chat con i modelli migliori e generi siti web a 0 euro, senza abbonamenti.

   Io non gli ho detto niente.

   ADV: link referral in bio, se lo usi ricevo sessioni extra.

   #freebuff #codingai #appgratis
   ```
4. **Regole anti-ban (`freebuff-export/07-distribuzione/REGOLE-LINK.md`):**
   - Attiva il toggle **Contenuto commerciale / Sponsorizzato** dove richiesto e lascia visibile `ADV`.
   - Su TikTok e Instagram **non incollare mai l'URL nei commenti a raffica**: a chi commenta `PROMO`, rispondi variando i messaggi indicando il link in bio (o invia in DM solo a chi commenta/richiede, evitando messaggi identici automatici a raffica su TikTok).
   - Se pubblichi media generato con Veo/Google Flow su Instagram/TikTok, attiva l'etichetta nativa **"Contenuto generato con AI"** come previsto dalle policy Meta/TikTok.
