from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
import os, textwrap

W, H = 1080, 1080
FPS = 1
SECS = 6  # seconds per slide

OUTPUT = r"D:\00_HERNAN-MegaSync-26\5_VARIOS HERNAN\AI\00_CLAUDE MAIN\00_ NEW-PLATAFINTEGRAL\carrusel_psicologia.mp4"

# ── Paleta por slide ──────────────────────────────────────────────────────────
SLIDES = [
    {
        "bg": "#1A1A2E",
        "accent": "#E94560",
        "tag": "ANSIEDAD",
        "title": "Tu mente no\nes el peligro",
        "body": (
            "La ansiedad es una alarma que se disparó "
            "en el momento equivocado.\n"
            "No te define: es una respuesta, no tu identidad."
        ),
        "icon": "⚡",
        "num": "01",
    },
    {
        "bg": "#16213E",
        "accent": "#0F9B8E",
        "tag": "DEPRESIÓN",
        "title": "No es flojera.\nEs agotamiento.",
        "body": (
            "La depresión pesa diferente a la tristeza. "
            "Reconocerla es el primer paso para salir de ella.\n"
            "Pedir ayuda es un acto de valentía."
        ),
        "icon": "🌒",
        "num": "02",
    },
    {
        "bg": "#0F3460",
        "accent": "#E94560",
        "tag": "VÍNCULOS",
        "title": "Cómo te tratan\nlos demás empieza\nen cómo te tratas vos.",
        "body": (
            "Los patrones que repetís en tus relaciones "
            "tienen raíz. La terapia ayuda a verlos "
            "antes de que vuelvan a doler."
        ),
        "icon": "🔗",
        "num": "03",
    },
    {
        "bg": "#1B1B2F",
        "accent": "#F5A623",
        "tag": "AUTOESTIMA",
        "title": "La crítica interna\nmás dura suele\nser la propia.",
        "body": (
            "El diálogo interno moldea cada decisión. "
            "Aprender a hablarte diferente cambia "
            "lo que creés que merecés."
        ),
        "icon": "🪞",
        "num": "04",
    },
    {
        "bg": "#12122A",
        "accent": "#7B2FBE",
        "tag": "TERAPIA",
        "title": "No esperés\ntocar fondo.",
        "body": (
            "Ir al psicólogo no es una señal de crisis: "
            "es una inversión en vos. "
            "Empezar antes hace la diferencia."
        ),
        "icon": "🧠",
        "num": "05",
    },
]

# ── Helpers de fuente ─────────────────────────────────────────────────────────
def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Render de una slide ───────────────────────────────────────────────────────
def render_slide(s):
    img = Image.new("RGB", (W, H), hex_rgb(s["bg"]))
    d = ImageDraw.Draw(img)
    accent = hex_rgb(s["accent"])

    # Franja vertical izquierda
    d.rectangle([0, 0, 12, H], fill=accent)

    # Número grande de fondo (decorativo, semitransparente via RGBA layer)
    fn_big = load_font(320, bold=True)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    dim_color = tuple(min(255, c + 30) for c in hex_rgb(s["bg"])) + (45,)
    od.text((W - 20, H - 40), s["num"], font=fn_big, fill=dim_color, anchor="rb")
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)

    # TAG pill
    fn_tag = load_font(28, bold=True)
    tag_text = s["tag"]
    bbox = d.textbbox((0, 0), tag_text, font=fn_tag)
    tw = bbox[2] - bbox[0]
    pad = 20
    rx0, ry0 = 72, 72
    rx1, ry1 = rx0 + tw + pad * 2, ry0 + 44
    d.rounded_rectangle([rx0, ry0, rx1, ry1], radius=22, fill=accent)
    d.text((rx0 + pad, ry0 + 8), tag_text, font=fn_tag, fill="white")

    # ICONO
    fn_icon = load_font(90)
    d.text((72, 148), s["icon"], font=fn_icon, fill="white")

    # TÍTULO
    fn_title = load_font(72, bold=True)
    title_lines = s["title"].split("\n")
    y = 270
    for line in title_lines:
        d.text((72, y), line, font=fn_title, fill="white")
        y += 84

    # Línea separadora
    d.rectangle([72, y + 16, 320, y + 20], fill=accent)
    y += 52

    # CUERPO
    fn_body = load_font(36)
    wrapped = textwrap.fill(s["body"], width=34)
    for line in wrapped.split("\n"):
        d.text((72, y), line, font=fn_body, fill=(200, 200, 220))
        y += 50

    # Pie de página
    fn_foot = load_font(26)
    d.text((72, H - 70), "@psicologohernanstagni", font=fn_foot,
           fill=(*accent, 180))
    d.text((W - 72, H - 70), f"{s['num']} / 05", font=fn_foot,
           fill=(130, 130, 160), anchor="ra")

    return np.array(img)

# ── Compilar MP4 ─────────────────────────────────────────────────────────────
def main():
    frames = []
    for s in SLIDES:
        frame = render_slide(s)
        for _ in range(FPS * SECS):
            frames.append(frame)

    # Transición de 1 frame negro entre slides
    black = np.zeros((H, W, 3), dtype=np.uint8)
    final = []
    for i, s in enumerate(SLIDES):
        frame = render_slide(s)
        for _ in range(FPS * SECS):
            final.append(frame)
        if i < len(SLIDES) - 1:
            final.append(black)

    writer = imageio.get_writer(OUTPUT, fps=FPS, codec="libx264",
                                 quality=8, pixelformat="yuv420p")
    for f in final:
        writer.append_data(f)
    writer.close()
    print(f"MP4 guardado en: {OUTPUT}")

if __name__ == "__main__":
    main()
