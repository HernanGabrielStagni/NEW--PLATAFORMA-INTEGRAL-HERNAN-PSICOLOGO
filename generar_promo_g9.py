"""
Generador de video promocional - Plataforma Estudio G9
Espacio Semillas · Lección 9 · Constelaciones Organizacionales
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
import os, math, textwrap

# ── CONFIG ────────────────────────────────────────────────────────────────────
W, H   = 1080, 1080
FPS    = 24
OUTPUT = r"D:\00_HERNAN-MegaSync-26\5_VARIOS HERNAN\AI\00_CLAUDE MAIN\00_ NEW-PLATAFINTEGRAL\promo_plataforma_g9.mp4"

# ── PALETA (plataforma original) ──────────────────────────────────────────────
C = {
    "verde_osc":   (26,  61, 43),
    "verde_med":   (45, 106, 79),
    "verde_claro": (74, 127, 110),
    "dorado":      (201, 168, 76),
    "dorado_claro":(240, 208, 112),
    "blanco_cal":  (245, 240, 232),
    "blanco":      (255, 255, 255),
    "gris_suave":  (180, 175, 165),
    "negro":       (0,   0,   0),
    "transp":      (0,   0,   0, 0),
}

# ── FUENTES ───────────────────────────────────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"

def font(size, style="regular"):
    maps = {
        "bold":   ["arialbd.ttf", "Arial Bold.ttf", "arial.ttf"],
        "italic": ["ariali.ttf",  "Arial Italic.ttf", "arial.ttf"],
        "regular":["arial.ttf",   "Arial.ttf"],
        "light":  ["arialn.ttf",  "arial.ttf"],
    }
    for name in maps.get(style, maps["regular"]):
        path = os.path.join(FONT_DIR, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def ease_in_out(t):
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    if isinstance(a, tuple):
        return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))
    return a + (b - a) * t

def blend_images(img_a, img_b, t):
    """Cross-fade between two PIL images."""
    a = np.array(img_a).astype(float)
    b = np.array(img_b).astype(float)
    return Image.fromarray(np.clip(a * (1 - t) + b * t, 0, 255).astype(np.uint8))

def draw_rounded_rect(draw, x0, y0, x1, y1, r, fill, alpha=255):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill)

def draw_text_wrapped(draw, text, x, y, font_obj, fill, max_width, line_height):
    """Draw wrapped text, return final y."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_height
    return y

def draw_progress_bar(draw, x, y, w, h, progress, bg, fg, r=6):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=bg)
    if progress > 0:
        fill_w = max(r * 2, int(w * progress))
        draw.rounded_rectangle([x, y, x + fill_w, y + h], radius=r, fill=fg)

# ── FONDOS ────────────────────────────────────────────────────────────────────
def bg_dark(alpha=1.0):
    """Dark green gradient background."""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = lerp(C["verde_osc"], (15, 35, 25), t)
        draw.line([(0, y), (W, y)], fill=c)
    return img

def bg_warm():
    """Warm cream background."""
    img = Image.new("RGB", (W, H), C["blanco_cal"])
    draw = ImageDraw.Draw(img)
    # subtle gradient
    for y in range(H):
        t = y / H * 0.06
        c = lerp(C["blanco_cal"], (235, 228, 218), t)
        draw.line([(0, y), (W, y)], fill=c)
    return img

def add_noise_texture(img, amount=4):
    arr = np.array(img).astype(int)
    noise = np.random.randint(-amount, amount + 1, arr.shape)
    return Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))

def add_decorative_circles(img, color, positions):
    overlay = img.copy().convert("RGBA")
    od = ImageDraw.Draw(overlay)
    for (cx, cy, r, a) in positions:
        circle = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(circle)
        cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
        overlay = Image.alpha_composite(overlay.convert("RGBA"), circle)
    return overlay.convert("RGB")

def add_vertical_accent(img, color, x=0, width=10):
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, 0, x + width, H], fill=color)
    return img

# ══════════════════════════════════════════════════════════════════════════════
#  ESCENAS
# ══════════════════════════════════════════════════════════════════════════════

def scene_opening(t, total):
    """Escena 1: Apertura - Logo y título de la plataforma."""
    img = bg_dark()
    img = add_decorative_circles(img, C["dorado"], [
        (W - 80, 80,  200, 18),
        (80,     H - 80, 150, 12),
        (W // 2, H // 2, 350, 8),
    ])

    # Franja dorada izquierda
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 8, H], fill=C["dorado"])

    # Animación: fade-in del contenido
    progress = ease_in_out(min(1.0, t / 0.4))

    # Logo circle (círculo de marca)
    cx, cy, cr = W // 2, H // 2 - 130, 90
    anim_y = cy - int((1 - progress) * 60)
    draw.ellipse(
        [cx - cr, anim_y - cr, cx + cr, anim_y + cr],
        fill=C["dorado"],
        outline=C["dorado_claro"],
        width=3,
    )
    # Semilla icon (simplified)
    draw.ellipse([cx - 28, anim_y - 44, cx + 28, anim_y + 44],
                 fill=C["verde_osc"])
    draw.ellipse([cx - 18, anim_y - 34, cx + 18, anim_y + 34],
                 fill=C["dorado"])

    alpha = int(255 * progress)

    # ESPACIO SEMILLAS
    f_brand = font(38, "bold")
    brand_txt = "ESPACIO SEMILLAS"
    bb = draw.textbbox((0, 0), brand_txt, font=f_brand)
    bw = bb[2] - bb[0]
    brand_y = H // 2 + 10 - int((1 - progress) * 40)
    draw.text(((W - bw) // 2, brand_y), brand_txt,
              font=f_brand, fill=(*C["dorado"], alpha))

    # Separador
    sep_y = brand_y + 52
    sep_w = int(200 * progress)
    draw.rectangle([(W - sep_w) // 2, sep_y, (W + sep_w) // 2, sep_y + 3],
                   fill=(*C["dorado"], alpha))

    # Lección 9
    f_leccion = font(24, "regular")
    lec_txt = "Lección 9  ·  Constelaciones Organizacionales"
    bb2 = draw.textbbox((0, 0), lec_txt, font=f_leccion)
    lec_y = sep_y + 24
    draw.text(((W - (bb2[2] - bb2[0])) // 2, lec_y), lec_txt,
              font=f_leccion, fill=(*C["blanco_cal"], alpha))

    # Tagline
    f_tag = font(19, "italic")
    tag_txt = '"Yo tomo mi responsabilidad y dejo contigo la tuya."'
    bb3 = draw.textbbox((0, 0), tag_txt, font=f_tag)
    tag_y = lec_y + 50
    tag_alpha = int(255 * ease_in_out(max(0, (t - 0.5) / 0.4)))
    draw.text(((W - (bb3[2] - bb3[0])) // 2, tag_y), tag_txt,
              font=f_tag, fill=(*C["verde_claro"], tag_alpha))

    return img


def scene_auth(t, total):
    """Escena 2: Sistema de acceso con planes VIP / Pro / Trial."""
    img = bg_dark()
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 8, H], fill=C["dorado"])

    img = add_decorative_circles(img, C["verde_med"], [
        (W - 60, 200, 180, 15),
        (100, H - 100, 130, 12),
    ])
    draw = ImageDraw.Draw(img)

    progress = ease_in_out(min(1.0, t / 0.4))

    # Section tag
    f_tag = font(22, "bold")
    tag_txt = "ACCESO Y PLANES"
    draw.rounded_rectangle([60, 60, 60 + 260, 100], radius=20,
                            fill=(*C["dorado"], int(220 * progress)))
    draw.text((80, 68), tag_txt, font=f_tag,
              fill=(*C["verde_osc"], int(255 * progress)))

    # Title
    f_title = font(58, "bold")
    title_y = 140 - int((1 - progress) * 40)
    title_lines = ["Plataforma con", "acceso protegido"]
    for i, line in enumerate(title_lines):
        bb = draw.textbbox((0, 0), line, font=f_title)
        line_a = int(255 * ease_in_out(min(1.0, (t - i * 0.15) / 0.4)))
        draw.text((60, title_y + i * 68), line, font=f_title,
                  fill=(*C["blanco_cal"], line_a))

    # Login form mockup
    form_y = 320
    form_a = ease_in_out(min(1.0, max(0, (t - 0.3) / 0.4)))

    draw.rounded_rectangle(
        [60, form_y, W - 60, form_y + 200],
        radius=20,
        fill=(*C["verde_med"], int(60 * form_a)),
        outline=(*C["dorado"], int(60 * form_a)),
        width=1,
    )

    f_label = font(22, "regular")
    f_small = font(18, "regular")

    labels = [
        ("Email",     "alumno@ejemplo.com", form_y + 28),
        ("Contraseña","••••••••••••",        form_y + 104),
    ]
    for lbl, placeholder, ly in labels:
        draw.text((90, ly), lbl, font=font(18, "bold"),
                  fill=(*C["dorado"], int(200 * form_a)))
        draw.rounded_rectangle([90, ly + 26, W - 90, ly + 62], radius=10,
                                fill=(*C["verde_osc"], int(180 * form_a)))
        draw.text((108, ly + 36), placeholder, font=f_small,
                  fill=(*C["gris_suave"], int(180 * form_a)))

    # Plan badges
    plan_y = form_y + 250
    planes_a = ease_in_out(min(1.0, max(0, (t - 0.55) / 0.4)))
    planes = [
        ("VIP ✦",  C["dorado"],       C["verde_osc"],  "Acceso completo"),
        ("Pro",    C["verde_claro"],   C["verde_osc"],  "Contenidos + Quiz"),
        ("Trial",  (100, 100, 100),   C["blanco_cal"],  "Vista previa"),
    ]
    f_plan = font(24, "bold")
    f_pdesc = font(17, "regular")
    plan_x = 60
    for pname, bg, fg, desc in planes:
        pw = 280
        draw.rounded_rectangle([plan_x, plan_y, plan_x + pw, plan_y + 60],
                                radius=12, fill=(*bg, int(220 * planes_a)))
        bb = draw.textbbox((0, 0), pname, font=f_plan)
        draw.text((plan_x + 16, plan_y + 10), pname, font=f_plan,
                  fill=(*fg, int(255 * planes_a)))
        draw.text((plan_x + 16, plan_y + 38), desc, font=f_pdesc,
                  fill=(*fg, int(180 * planes_a)))
        plan_x += pw + 18

    return img


def scene_navigation(t, total):
    """Escena 3: Sidebar con 7 secciones y progreso."""
    img = bg_warm()
    draw = ImageDraw.Draw(img)

    progress = ease_in_out(min(1.0, t / 0.4))

    # Sidebar (izquierda)
    sb_w = 310
    draw.rounded_rectangle([40, 40, 40 + sb_w, H - 40], radius=20,
                            fill=(*C["verde_osc"], int(245 * progress)))

    sections = [
        ("🏠", "Bienvenida",       True,  "inicio"),
        ("▶", "Video Clases",      True,  "videos"),
        ("📊", "Presentaciones",   True,  "presentaciones"),
        ("🖼", "Infografías",      False, "infografias"),
        ("📄", "Documentos",       False, "documentos"),
        ("📖", "Síntesis General", False, "resumen"),
        ("✅", "Examen de Unidad", False, "quiz"),
    ]

    f_group = font(13, "bold")
    f_sec = font(22, "bold")
    f_sec_r = font(22, "regular")

    groups_lbl = [
        (None,      [0]),
        ("CLASES",  [1]),
        ("CONTENIDOS", [2, 3, 4]),
        ("EVALUACIÓN", [5, 6]),
    ]

    sy = 100
    g_idx = 0
    for g_label, idxs in groups_lbl:
        g_a = ease_in_out(min(1.0, max(0, (t - g_idx * 0.08) / 0.4)))
        if g_label:
            draw.text((70, sy), g_label, font=f_group,
                      fill=(*C["dorado"], int(160 * g_a)))
            sy += 30
        for idx in idxs:
            em, name, visited, _ = sections[idx]
            item_a = ease_in_out(min(1.0, max(0, (t - idx * 0.06) / 0.4)))
            is_active = (idx == 1)
            if is_active:
                draw.rounded_rectangle(
                    [56, sy - 4, 56 + sb_w - 32, sy + 40],
                    radius=12,
                    fill=(*C["dorado"], int(220 * item_a)),
                )
            text_color = C["verde_osc"] if is_active else C["blanco_cal"]
            draw.text((75, sy + 4), em + " " + name,
                      font=f_sec if is_active else f_sec_r,
                      fill=(*text_color, int(255 * item_a)))
            if visited and not is_active:
                draw.ellipse([sb_w - 10, sy + 10, sb_w + 10, sy + 30],
                             fill=(*C["dorado"], int(200 * item_a)))
            sy += 52
        sy += 10
        g_idx += 1

    # Progress area
    prog_y = H - 130
    prog_a = ease_in_out(min(1.0, max(0, (t - 0.6) / 0.4)))
    draw.line([(56, prog_y), (56 + sb_w - 32, prog_y)],
              fill=(*C["verde_claro"], int(80 * prog_a)), width=1)
    draw.text((75, prog_y + 14), "Progreso de la lección", font=font(18, "regular"),
              fill=(*C["blanco_cal"], int(160 * prog_a)))
    draw_progress_bar(draw, 75, prog_y + 42, sb_w - 60, 14,
                      0.43 * prog_a,
                      (*C["verde_osc"], int(180 * prog_a)),
                      (*C["dorado"], int(220 * prog_a)))
    draw.text((75, prog_y + 64), "3 de 7 secciones completadas", font=font(16, "regular"),
              fill=(*C["gris_suave"], int(160 * prog_a)))

    # Right panel title
    content_a = ease_in_out(min(1.0, max(0, (t - 0.2) / 0.4)))
    rx = 390
    draw.text((rx, 80), "Navegación intuitiva", font=font(46, "bold"),
              fill=(*C["verde_osc"], int(255 * content_a)))
    desc = (
        "Sidebar siempre visible con todas las\n"
        "secciones de la lección organizadas\n"
        "por grupos temáticos."
    )
    dy = 164
    for line in desc.split("\n"):
        draw.text((rx, dy), line, font=font(26, "regular"),
                  fill=(*C["verde_med"], int(220 * content_a)))
        dy += 40

    # Check marks (secciones visitadas)
    feat_y = dy + 50
    features = [
        "OK  Sección activa destacada en dorado",
        "OK  Tick de completado por sección",
        "OK  Barra de progreso en tiempo real",
        "OK  Diseño responsive (móvil + desktop)",
    ]
    for i, feat in enumerate(features):
        fa = ease_in_out(min(1.0, max(0, (t - 0.35 - i * 0.08) / 0.4)))
        draw.text((rx, feat_y + i * 48), feat, font=font(22, "regular"),
                  fill=(*C["verde_osc"], int(220 * fa)))

    return img


def scene_videoclases(t, total):
    """Escena 4: Video Clases - 3 clases grabadas."""
    img = bg_dark()
    img = add_decorative_circles(img, C["verde_med"], [
        (W - 100, 150, 220, 12),
        (50, H - 150, 180, 10),
    ])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 8, H], fill=C["dorado"])

    progress = ease_in_out(min(1.0, t / 0.4))

    f_tag = font(22, "bold")
    draw.rounded_rectangle([60, 56, 320, 98], radius=20,
                            fill=(*C["dorado"], int(220 * progress)))
    draw.text((80, 64), "VIDEO CLASES", font=f_tag,
              fill=(*C["verde_osc"], int(255 * progress)))

    draw.text((60, 136), "3 clases grabadas", font=font(62, "bold"),
              fill=(*C["blanco_cal"], int(255 * progress)))
    draw.text((60, 214), "en profundidad", font=font(48, "bold"),
              fill=(*C["dorado"], int(255 * progress)))

    videos = [
        ("01", "Fuerzas Ocultas en\nlas Organizaciones",
         "Las leyes sistémicas que\ngobiernan empresas y equipos"),
        ("02", "Dominio de las\nConstelaciones Org.",
         "Campo representacional y\nconciencia colectiva"),
        ("03", "Práctica de la\nConstelación",
         "Facilitación sistémica paso\na paso con frases sanadoras"),
    ]

    card_w = (W - 120 - 30) // 3
    card_x = 60
    for i, (num, title, desc) in enumerate(videos):
        ca = ease_in_out(min(1.0, max(0, (t - 0.25 - i * 0.12) / 0.45)))
        card_y = 310 - int((1 - ca) * 30)
        # Card
        draw.rounded_rectangle(
            [card_x, card_y, card_x + card_w, card_y + 350],
            radius=16,
            fill=(*C["verde_med"], int(80 * ca)),
            outline=(*C["dorado"], int(40 * ca)),
            width=1,
        )
        # Play button
        play_cx = card_x + card_w // 2
        play_cy = card_y + 95
        draw.ellipse(
            [play_cx - 44, play_cy - 44, play_cx + 44, play_cy + 44],
            fill=(*C["dorado"], int(200 * ca)),
        )
        # Triangle
        pts = [
            (play_cx - 14, play_cy - 22),
            (play_cx - 14, play_cy + 22),
            (play_cx + 24, play_cy),
        ]
        draw.polygon(pts, fill=(*C["verde_osc"], int(255 * ca)))

        # Number badge
        draw.ellipse(
            [card_x + 12, card_y + 12, card_x + 48, card_y + 48],
            fill=(*C["verde_osc"], int(200 * ca)),
        )
        draw.text((card_x + 18, card_y + 16), num, font=font(20, "bold"),
                  fill=(*C["dorado"], int(255 * ca)))

        # Title
        for j, line in enumerate(title.split("\n")):
            draw.text((card_x + 14, card_y + 168 + j * 36),
                      line, font=font(22, "bold"),
                      fill=(*C["blanco_cal"], int(255 * ca)))
        # Desc
        for j, line in enumerate(desc.split("\n")):
            draw.text((card_x + 14, card_y + 248 + j * 28),
                      line, font=font(17, "regular"),
                      fill=(*C["gris_suave"], int(200 * ca)))

        card_x += card_w + 15

    # Footer note
    note_a = ease_in_out(min(1.0, max(0, (t - 0.7) / 0.3)))
    draw.text((60, H - 80), "Reproducción integrada directo en la plataforma · Sin salir a YouTube",
              font=font(20, "regular"),
              fill=(*C["verde_claro"], int(180 * note_a)))

    return img


def scene_contenidos(t, total):
    """Escena 5: Presentaciones, Infografías, Documentos."""
    img = bg_warm()
    draw = ImageDraw.Draw(img)

    progress = ease_in_out(min(1.0, t / 0.4))

    # Title
    draw.text((60, 80), "Contenidos", font=font(66, "bold"),
              fill=(*C["verde_osc"], int(255 * progress)))
    draw.text((60, 162), "complementarios", font=font(52, "bold"),
              fill=(*C["dorado"], int(255 * progress)))

    contenidos = [
        {
            "icon": "📊",
            "label": "Presentaciones",
            "count": "3 archivos",
            "color": C["dorado"],
            "items": ["Arquitectura invisible org.", "Herramientas de facilitación", "Práctica en entornos org."],
        },
        {
            "icon": "🖼",
            "label": "Infografías",
            "count": "3 recursos",
            "color": C["verde_claro"],
            "items": ["Bases de constelaciones org.", "El alma de las org.", "Guía de aplicación práctica"],
        },
        {
            "icon": "📄",
            "label": "Documentos",
            "count": "PDFs + Audio",
            "color": (154, 74, 74),
            "items": ["Capítulo 9 del curso", "Guía maestra de estudio", "Audio: sanación de empresas"],
        },
    ]

    col_w = (W - 120 - 40) // 3
    col_x = 60
    for i, cont in enumerate(contenidos):
        ca = ease_in_out(min(1.0, max(0, (t - 0.2 - i * 0.12) / 0.4)))
        cy = 280 - int((1 - ca) * 25)

        # Card
        draw.rounded_rectangle(
            [col_x, cy, col_x + col_w, cy + 440],
            radius=18,
            fill=(*C["verde_osc"], int(230 * ca)),
        )

        # Top color accent
        draw.rounded_rectangle(
            [col_x, cy, col_x + col_w, cy + 6],
            radius=3,
            fill=(*cont["color"], int(255 * ca)),
        )

        # Icon + label
        draw.text((col_x + 20, cy + 24), cont["icon"], font=font(48), fill="white")
        draw.text((col_x + 20, cy + 90), cont["label"], font=font(28, "bold"),
                  fill=(*C["blanco_cal"], int(255 * ca)))

        # Count badge
        bb = draw.textbbox((0, 0), cont["count"], font=font(18, "bold"))
        bw = bb[2] - bb[0] + 24
        draw.rounded_rectangle(
            [col_x + 20, cy + 132, col_x + 20 + bw, cy + 164],
            radius=10,
            fill=(*cont["color"], int(180 * ca)),
        )
        draw.text((col_x + 32, cy + 138), cont["count"], font=font(18, "bold"),
                  fill=(*C["verde_osc"], int(255 * ca)))

        # Items list
        iy = cy + 188
        for item in cont["items"]:
            ia = ease_in_out(min(1.0, max(0, (t - 0.35 - i * 0.1) / 0.4)))
            draw.ellipse([col_x + 20, iy + 8, col_x + 30, iy + 18],
                         fill=(*cont["color"], int(200 * ia)))
            draw.text((col_x + 38, iy), item, font=font(19, "regular"),
                      fill=(*C["blanco_cal"], int(200 * ia)))
            iy += 44

        # Download note
        dl_a = ease_in_out(min(1.0, max(0, (t - 0.6) / 0.35)))
        draw.text((col_x + 20, cy + 390), "⬇  Descarga según plan", font=font(17, "italic"),
                  fill=(*cont["color"], int(160 * dl_a)))

        col_x += col_w + 20

    return img


def scene_progreso(t, total):
    """Escena 6: Sistema de tracking de progreso."""
    img = bg_dark()
    img = add_decorative_circles(img, C["dorado"], [
        (W - 80, H - 80, 200, 10),
        (80, 80, 160, 8),
    ])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 8, H], fill=C["dorado"])

    progress = ease_in_out(min(1.0, t / 0.4))

    # Tag
    draw.rounded_rectangle([60, 56, 370, 100], radius=20,
                            fill=(*C["dorado"], int(220 * progress)))
    draw.text((80, 64), "SEGUIMIENTO DE AVANCE", font=font(20, "bold"),
              fill=(*C["verde_osc"], int(255 * progress)))

    # Title
    draw.text((60, 136), "Tu progreso,", font=font(64, "bold"),
              fill=(*C["blanco_cal"], int(255 * progress)))
    draw.text((60, 212), "siempre visible.", font=font(64, "bold"),
              fill=(*C["dorado"], int(255 * progress)))

    # Header progress bar mock
    header_a = ease_in_out(min(1.0, max(0, (t - 0.25) / 0.4)))
    header_y = 320
    draw.rounded_rectangle(
        [60, header_y, W - 60, header_y + 80],
        radius=16,
        fill=(*C["verde_med"], int(70 * header_a)),
        outline=(*C["dorado"], int(40 * header_a)),
        width=1,
    )
    draw.text((80, header_y + 14), "Lección 9  ·  Constelaciones Org.",
              font=font(22, "bold"),
              fill=(*C["blanco_cal"], int(220 * header_a)))
    bar_progress = 0.57 * header_a
    draw_progress_bar(draw, 80, header_y + 52, W - 160, 12,
                      bar_progress,
                      (*C["verde_osc"], int(200 * header_a)),
                      (*C["dorado"], int(255 * header_a)))

    # Section items with check states
    items_a = ease_in_out(min(1.0, max(0, (t - 0.35) / 0.4)))
    items = [
        ("OK", "Bienvenida",        True),
        ("OK", "Video Clases",      True),
        ("OK", "Presentaciones",    True),
        ("OK", "Infografías",       True),
        ("○", "Documentos",        False),
        ("○", "Síntesis General",  False),
        ("○", "Examen de Unidad",  False),
    ]
    cols = 2
    item_w = (W - 140) // cols
    for i, (icon, name, done) in enumerate(items):
        col = i % cols
        row = i // cols
        ix = 70 + col * item_w
        iy = 440 + row * 58
        ia = ease_in_out(min(1.0, max(0, (t - 0.30 - i * 0.06) / 0.4)))

        bg_c = C["verde_med"] if done else (30, 50, 40)
        icon_c = C["dorado"] if done else C["verde_claro"]

        draw.rounded_rectangle(
            [ix, iy, ix + item_w - 20, iy + 46],
            radius=10,
            fill=(*bg_c, int(90 * ia)),
        )
        draw.text((ix + 14, iy + 10), icon, font=font(22, "bold"),
                  fill=(*icon_c, int(255 * ia)))
        draw.text((ix + 44, iy + 12), name, font=font(22, "regular"),
                  fill=(*C["blanco_cal"], int(220 * ia)))

    # Footer stat
    stat_a = ease_in_out(min(1.0, max(0, (t - 0.7) / 0.3)))
    draw.text((60, H - 90),
              "4 de 7 secciones completadas  ·  57% del curso",
              font=font(22, "regular"),
              fill=(*C["verde_claro"], int(200 * stat_a)))

    return img


def scene_quiz(t, total):
    """Escena 7: Evaluación - Quiz de unidad."""
    # Gradiente verde oscuro como en la app
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t_y = y / H
        c = lerp(C["verde_osc"], lerp(C["verde_med"], (15, 40, 28), 0.5), t_y)
        draw.line([(0, y), (W, y)], fill=c)

    img = add_decorative_circles(img, C["dorado"], [
        (W // 2 - 100, H // 2 - 50, 400, 12),
        (W - 60, 80,   200, 8),
        (80,     H - 80, 150, 8),
    ])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 8, H], fill=C["dorado"])

    progress = ease_in_out(min(1.0, t / 0.4))

    # Award circle
    cx, cy = W // 2, H // 2 - 120
    r = 80
    cy_anim = cy - int((1 - progress) * 50)
    draw.ellipse(
        [cx - r, cy_anim - r, cx + r, cy_anim + r],
        fill=(*C["dorado"], int(230 * progress)),
    )
    # Trophy icon (simplified)
    draw.ellipse([cx - 30, cy_anim - 38, cx + 30, cy_anim + 20],
                 fill=(*C["verde_osc"], int(255 * progress)))
    draw.rectangle([cx - 6, cy_anim + 14, cx + 6, cy_anim + 38],
                   fill=(*C["verde_osc"], int(255 * progress)))
    draw.rectangle([cx - 20, cy_anim + 34, cx + 20, cy_anim + 44],
                   fill=(*C["verde_osc"], int(255 * progress)))

    # Evaluation label
    f_ev = font(38, "bold")
    ev_txt = "Evaluación · Lección 9"
    bb = draw.textbbox((0, 0), ev_txt, font=f_ev)
    ev_y = H // 2 - 8
    draw.text(((W - (bb[2] - bb[0])) // 2, ev_y), ev_txt, font=f_ev,
              fill=(*C["dorado"], int(255 * progress)))

    # Description
    desc_a = ease_in_out(min(1.0, max(0, (t - 0.35) / 0.4)))
    f_desc = font(26, "regular")
    desc_txt = "¿Estás listo para evaluar lo aprendido?"
    bb2 = draw.textbbox((0, 0), desc_txt, font=f_desc)
    draw.text(((W - (bb2[2] - bb2[0])) // 2, ev_y + 56), desc_txt,
              font=f_desc, fill=(*C["blanco_cal"], int(230 * desc_a)))

    # Quiz button mock
    btn_a = ease_in_out(min(1.0, max(0, (t - 0.5) / 0.4)))
    btn_y = ev_y + 136
    btn_w = 380
    draw.rounded_rectangle(
        [(W - btn_w) // 2, btn_y, (W + btn_w) // 2, btn_y + 64],
        radius=32,
        fill=(*C["dorado"], int(230 * btn_a)),
    )
    btn_txt = "ABRIR QUIZ EXTERNO  ↗"
    bb3 = draw.textbbox((0, 0), btn_txt, font=font(22, "bold"))
    draw.text(
        ((W - (bb3[2] - bb3[0])) // 2, btn_y + 18),
        btn_txt, font=font(22, "bold"),
        fill=(*C["verde_osc"], int(255 * btn_a)),
    )

    # Stats
    stats_a = ease_in_out(min(1.0, max(0, (t - 0.65) / 0.35)))
    stats = [
        "20 preguntas de opción múltiple",
        "Temario completo de la Lección 9",
        "Resultado inmediato al finalizar",
    ]
    sy = btn_y + 108
    for s in stats:
        bb = draw.textbbox((0, 0), s, font=font(22, "regular"))
        draw.text(((W - (bb[2] - bb[0])) // 2, sy), s,
                  font=font(22, "regular"),
                  fill=(*C["blanco_cal"], int(180 * stats_a)))
        sy += 42

    return img


def scene_closing(t, total):
    """Escena 8: Cierre - CTA."""
    img = bg_dark()
    img = add_decorative_circles(img, C["dorado"], [
        (W // 2, H // 2, 500, 15),
        (W - 60, 60, 220, 12),
        (60, H - 60, 180, 10),
    ])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 8, H], fill=C["dorado"])

    progress = ease_in_out(min(1.0, t / 0.4))

    # Logo mark
    cx, cy = W // 2, H // 2 - 200
    r = 60
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(*C["dorado"], int(220 * progress)))
    draw.ellipse([cx - 18, cy - 30, cx + 18, cy + 30],
                 fill=(*C["verde_osc"], int(255 * progress)))
    draw.ellipse([cx - 10, cy - 18, cx + 10, cy + 18],
                 fill=(*C["dorado"], int(255 * progress)))

    # Brand
    f_brand = font(44, "bold")
    brand = "ESPACIO SEMILLAS"
    bb = draw.textbbox((0, 0), brand, font=f_brand)
    bw = bb[2] - bb[0]
    by = cy + 80
    draw.text(((W - bw) // 2, by), brand, font=f_brand,
              fill=(*C["dorado"], int(255 * progress)))

    # Separator
    sep_a = ease_in_out(min(1.0, max(0, (t - 0.3) / 0.4)))
    sep_y = by + 58
    sep_w = int(160 * sep_a)
    draw.rectangle([(W - sep_w) // 2, sep_y, (W + sep_w) // 2, sep_y + 3],
                   fill=(*C["dorado"], int(200 * sep_a)))

    # Feature summary
    feat_a = ease_in_out(min(1.0, max(0, (t - 0.4) / 0.4)))
    feats = [
        "Video Clases  ·  Presentaciones  ·  Infografías",
        "Documentos  ·  Síntesis General  ·  Quiz de Evaluación",
        "Progreso en tiempo real  ·  Planes VIP / Pro / Trial",
    ]
    fy = sep_y + 36
    for feat in feats:
        bb = draw.textbbox((0, 0), feat, font=font(22, "regular"))
        draw.text(((W - (bb[2] - bb[0])) // 2, fy), feat,
                  font=font(22, "regular"),
                  fill=(*C["blanco_cal"], int(180 * feat_a)))
        fy += 42

    # URL / CTA
    url_a = ease_in_out(min(1.0, max(0, (t - 0.6) / 0.4)))
    url_txt = "hernangabrielstagni.github.io/plataforma-estudio-g9"
    bb = draw.textbbox((0, 0), url_txt, font=font(24, "regular"))
    url_y = fy + 60
    draw.rounded_rectangle(
        [(W - (bb[2] - bb[0]) - 40) // 2, url_y - 14,
         (W + (bb[2] - bb[0]) + 40) // 2, url_y + 46],
        radius=28,
        fill=(*C["verde_med"], int(80 * url_a)),
        outline=(*C["dorado"], int(80 * url_a)),
        width=1,
    )
    draw.text(((W - (bb[2] - bb[0])) // 2, url_y), url_txt,
              font=font(24, "regular"),
              fill=(*C["dorado"], int(220 * url_a)))

    # Final fade-out
    if t > 0.75:
        fade = (t - 0.75) / 0.25
        overlay = Image.new("RGB", (W, H), C["negro"])
        img = blend_images(img, overlay, ease_in_out(fade))

    return img


# ══════════════════════════════════════════════════════════════════════════════
#  PIPELINE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

SCENES = [
    (scene_opening,    7.0),   # 7 s
    (scene_auth,       7.0),   # 7 s
    (scene_navigation, 8.0),   # 8 s
    (scene_videoclases,8.0),   # 8 s
    (scene_contenidos, 8.0),   # 8 s
    (scene_progreso,   7.0),   # 7 s
    (scene_quiz,       7.0),   # 7 s
    (scene_closing,    7.0),   # 7 s
]
# Total: 59 segundos

TRANSITION_SECS = 0.5  # cross-fade entre escenas

def build_video():
    total_s = sum(d for _, d in SCENES)
    print(f"Escenas: {len(SCENES)}  |  Duración total: {total_s:.0f}s  |  FPS: {FPS}")
    print(f"Total de frames: {int(total_s * FPS + len(SCENES) * TRANSITION_SECS * FPS)}")

    writer = imageio.get_writer(
        OUTPUT, fps=FPS, codec="libx264",
        quality=8, pixelformat="yuv420p",
        macro_block_size=1,
    )

    rendered_scenes = []
    print("Renderizando escenas...")
    for i, (scene_fn, duration) in enumerate(SCENES):
        frames = []
        n_frames = int(duration * FPS)
        for f in range(n_frames):
            t = f / n_frames
            frame = scene_fn(t, duration)
            frames.append(frame)
        rendered_scenes.append(frames)
        print(f"  OK Escena {i+1}/{len(SCENES)}: {scene_fn.__name__}  ({duration:.0f}s, {n_frames} frames)")

    print("Compilando video con transiciones...")
    trans_frames = int(TRANSITION_SECS * FPS)

    for i, frames in enumerate(rendered_scenes):
        # Escribir frames de la escena (sin los últimos trans_frames si hay siguiente)
        if i < len(rendered_scenes) - 1:
            for frame in frames[:-trans_frames]:
                writer.append_data(np.array(frame))
            # Transición cross-fade
            for tf in range(trans_frames):
                blend_t = tf / trans_frames
                blended = blend_images(frames[-trans_frames + tf],
                                       rendered_scenes[i + 1][tf],
                                       ease_in_out(blend_t))
                writer.append_data(np.array(blended))
        else:
            # Última escena: todos los frames
            for frame in frames:
                writer.append_data(np.array(frame))

    writer.close()
    print(f"\nDONE - Video guardado en:\n   {OUTPUT}")


if __name__ == "__main__":
    np.random.seed(42)
    build_video()
