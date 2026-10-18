"""Generate the app icons in icons/ (home-screen, PWA and favicon sizes)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'icons')
FONT = r'C:\Windows\Fonts\seguibl.ttf'  # Segoe UI Black
S = 1024  # master size

TOP, BOTTOM = (45, 140, 255), (88, 86, 214)  # site blue -> indigo
GREEN = (52, 199, 89)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def master(content_scale=1.0):
    img = Image.new('RGB', (S, S))
    px = img.load()
    for y in range(S):
        for x in range(S):
            t = (0.75 * y + 0.25 * x) / S  # diagonal gradient
            px[x, y] = lerp(TOP, BOTTOM, min(1, t))

    # soft highlight in the top-left for depth
    glow = Image.new('L', (S, S), 0)
    ImageDraw.Draw(glow).ellipse((-S * .35, -S * .45, S * .75, S * .55), fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(S * .08))
    img = Image.composite(Image.new('RGB', (S, S), (255, 255, 255)), img, glow)

    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = S / 2
    k = content_scale

    # "ML" wordmark
    font = ImageFont.truetype(FONT, int(430 * k))
    text = 'ML'
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    w, h = r - l, b - t
    tx, ty = c - w / 2 - l, c - h / 2 - t - 40 * k
    shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((tx, ty + 18 * k), text, font=font, fill=(20, 20, 80, 90))
    layer = Image.alpha_composite(layer, shadow.filter(ImageFilter.GaussianBlur(16 * k)))
    d = ImageDraw.Draw(layer)
    d.text((tx, ty), text, font=font, fill='white')

    # underline pill: progress-bar motif
    bw, bh = 520 * k, 46 * k
    by = c + h / 2 + 50 * k
    d.rounded_rectangle((c - bw / 2, by, c + bw / 2, by + bh), radius=bh / 2, fill=(255, 255, 255, 70))
    d.rounded_rectangle((c - bw / 2, by, c - bw / 2 + bw * .68, by + bh), radius=bh / 2, fill='white')

    # green tick badge, top-right of the wordmark
    r_ = 118 * k
    bx, byy = c + w / 2 - 10 * k, c - h / 2 - 70 * k
    d.ellipse((bx - r_ - 14 * k, byy - r_ - 14 * k, bx + r_ + 14 * k, byy + r_ + 14 * k), fill=(255, 255, 255))
    d.ellipse((bx - r_, byy - r_, bx + r_, byy + r_), fill=GREEN)
    lw = int(34 * k)
    pts = [(bx - 52 * k, byy + 2 * k), (bx - 14 * k, byy + 42 * k), (bx + 58 * k, byy - 40 * k)]
    d.line(pts, fill='white', width=lw, joint='curve')
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2), fill='white')

    return Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB')


def rounded(img, radius_frac=0.2237):
    """Rounded-square version for favicons (phones apply their own mask)."""
    n = img.size[0]
    mask = Image.new('L', (n * 4, n * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, n * 4 - 1, n * 4 - 1), radius=n * 4 * radius_frac, fill=255)
    mask = mask.resize((n, n), Image.LANCZOS)
    out = img.convert('RGBA')
    out.putalpha(mask)
    return out


os.makedirs(OUT, exist_ok=True)
full = master()
safe = master(content_scale=0.8)  # maskable: keep content inside the safe zone

for size in (180, 192, 512):
    full.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, f'icon-{size}.png'), optimize=True)
safe.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, 'icon-maskable-512.png'), optimize=True)
for size in (32, 64):
    rounded(full.resize((size * 4, size * 4), Image.LANCZOS)).resize((size, size), Image.LANCZOS).save(
        os.path.join(OUT, f'favicon-{size}.png'), optimize=True)
print('Icons written to', OUT)
