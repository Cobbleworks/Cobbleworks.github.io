"""Prepare plugin artwork and page headers from the source images (requires Pillow).

The generated WebP files are committed, so the site build itself stays dependency-free.
Run again only when source artwork changes:  python scripts/build_art.py <source-dir>
"""
from pathlib import Path
import sys

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/art'

# Full-resolution square artwork, keyed by plugin slug, with the horizontal focus (0-1)
# used when cropping to a wide header.
FULL_ART = {
    'super-enchantments': ('ChatGPT Image 1. Sept. 2026, 01_54_55(2).png', 0.45, 0.35),
    'custom-jukebox': ('ChatGPT Image 1. Sept. 2026, 02_26_05(3).png', 0.5, 0.45),
    'rail-boost': ('ChatGPT Image 1. Sept. 2026, 02_28_18(1).png', 0.6, 0.4),
    'map-revealer': ('ChatGPT Image 1. Sept. 2026, 15_30_28 (1).png', 0.5, 0.42),
    'blood-moon': ('ChatGPT Image 31. Aug. 2026, 22_51_05(3).png', 0.5, 0.5),
    'power-mining': ('ChatGPT Image 31. Aug. 2026, 22_59_51(3).png', 0.5, 0.4),
    'hookshot': ('ChatGPT Image 31. Aug. 2026, 23_03_06.png', 0.5, 0.45),
    'wireless-redstone': ('Minecraft-Hebel im Sonnenuntergang.png', 0.5, 0.5),
}
BANNER_INSET = 14  # removes the frame and shadow baked into the 818x196 banners
# Horizontal focus for banner-only card crops, chosen so the subject stays in frame.
CARD_FOCUS = {'advanced-achievements': 0.62, 'area-rewind': 0.62, 'blockfolk': 0.3,
              'piston-crusher': 0.45, 'useful-autocrafter': 0.5}
CARD_RATIO = 2.2


def crop_to(img, ratio, fx=0.5, fy=0.5):
    w, h = img.size
    if w / h > ratio:
        nw = round(h * ratio)
        x = round((w - nw) * fx)
        return img.crop((x, 0, x + nw, h))
    nh = round(w / ratio)
    y = round((h - nh) * fy)
    return img.crop((0, y, w, y + nh))


def save(img, name, width):
    img = img.resize((width, round(width * img.height / img.width)), Image.LANCZOS)
    img.save(OUT / f'{name}.webp', 'WEBP', quality=80, method=6)


def main(source):
    OUT.mkdir(parents=True, exist_ok=True)
    for banner in sorted((ROOT / 'assets/plugins').glob('*.png')):
        slug = banner.stem
        b = Image.open(banner).convert('RGB')
        b = b.crop((BANNER_INSET, BANNER_INSET, b.width - BANNER_INSET, b.height - BANNER_INSET))
        if slug in FULL_ART:
            name, fx, fy = FULL_ART[slug]
            full = Image.open(source / name).convert('RGB')
            save(crop_to(full, 16 / 9, fx, fy), f'{slug}-header', 1254)
            save(crop_to(full, CARD_RATIO, fx, fy), f'{slug}-card', 720)
        else:
            # Banner-only artwork is too small to fill a header, so the page shows the
            # banner itself at native size over a blurred backdrop made from it.
            save(b, f'{slug}-banner', b.width)
            backdrop = crop_to(b, 16 / 9).resize((320, 180), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
            save(backdrop, f'{slug}-backdrop', 640)
            save(crop_to(b, CARD_RATIO, CARD_FOCUS.get(slug, 0.5)), f'{slug}-card', round(b.height * CARD_RATIO))
    # The homepage header (assets/hero) is already optimised; only the closing band is built here.
    band = Image.open(source.parent / 'Mondscheinburg über dem Nebeltal.png').convert('RGB')
    for width in (960, 1672):
        save(band, f'moonlit-castle-{width}', width)
    print('Artwork written to', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'Cobblework plugin images')
