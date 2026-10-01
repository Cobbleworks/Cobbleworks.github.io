"""Cobbleworks plugin icon family: hand-placed 16x16 pixel art rendered to crisp SVG.

Shared rules: one warm near-black outline, light from the top left, three tones per
material, transparent background, subject filling the centre 14x14 pixels.
"""
from pathlib import Path

PALETTE = {
    'K': '#16120f',  # outline
    'w': '#f4f1ea', 'l': '#c5ccd2', 'g': '#8b97a1', 'd': '#5a6670', 'D': '#38414a',  # stone / iron
    'Y': '#ffe08a', 'y': '#f5b83d', 'o': '#e8903a', 'O': '#b0642a',  # gold / copper
    'e': '#c08a52', 'b': '#8a5a32', 'B': '#5a3820',  # wood
    'a': '#efd9a7', 'A': '#cfae6e',  # parchment
    'R': '#ff8068', 'r': '#e0393b', 'm': '#9a2029', 'M': '#6b1520',  # red
    'G': '#8fd66a', 'n': '#4c9e3c', 'N': '#2e6a2a',  # green
    'C': '#a6eef6', 'c': '#4cb8d0', 'u': '#2b7aa6', 'U': '#1f4a72',  # cyan / blue
    'P': '#d6a8ff', 'p': '#9a5fe0', 'q': '#5e3399',  # purple
    's': '#eab48c', 'S': '#bf8459', 'h': '#6b4226', 'H': '#4a2c18',  # skin / hair
}

ICONS = {
'advanced-achievements': [
    "................",
    "...KKKKKKKKKK...",
    ".KKKYYYYYYyyKKK.",
    "KyKKYYYYYyyyKKyK",
    "KyyKYYyyyyyOKyyK",
    "KKyKYyyyyyyOKyKK",
    ".KKKyyyyyyyOKKK.",
    "...KyyyyyyOOK...",
    "....KyyyyOOK....",
    ".....KKyOKK.....",
    "......KyOK......",
    "......KyOK......",
    "....KKyyOOKK....",
    "...KbeeeeebBK...",
    "...KbbbbbbbBK...",
    "...KKKKKKKKKK...",
],
'area-rewind': [
    "................",
    ".....KKKKKK.....",
    "...KKCCCCCcKK...",
    "..KCcKKKKKKucK..",
    "KKCKK......KuK..",
    "KCCCK......KUK..",
    ".KCK........K...",
    "..K.KKKKKKKKKK..",
    "....KGGGGGGGnK..",
    "....KnGnnGnnNK..",
    "....KbebbebbBK..",
    "....KbbbebbbBK..",
    "....KebbbbebBK..",
    "....KbbebbbBBK..",
    "....KBBBBBBBBK..",
    "....KKKKKKKKKK..",
],
'blockfolk': [
    "................",
    "...KKKKKKKKKK...",
    "..KhhhhhhhhhhK..",
    "..KhhhhhhhhhHK..",
    "..KhssssssssHK..",
    "..KssssssssSSK..",
    "..KswKsssswKSK..",
    "..KswUsssswUSK..",
    "..KssssssssSSK..",
    "..KsssSSSSsSSK..",
    "..KssshHHhsSSK..",
    "..KSSSSSSSSSSK..",
    "...KKKKKKKKKK...",
    "..KucccccccuuK..",
    ".KuccccccccuuUK.",
    ".KKKKKKKKKKKKKK.",
],
'blood-moon': [
    "................",
    ".....KKKKKK.....",
    "...KKRRRRrrKK...",
    "..KRRRRrrrrrmK..",
    "..KRRmrrrrrrmK..",
    ".KRRmMrrrrrrrmK.",
    ".KRrrrrrrmMrrmK.",
    ".KRrrrrrrMMrrmK.",
    ".KrrrrrrrrrrmmK.",
    ".KrrmMrrrrrrmmK.",
    ".KrrrmrrrrrmmMK.",
    "..KrrrrrmMrmmK..",
    "..KmrrrrrmmmMK..",
    "...KKmmmmmMKK...",
    ".....KKKKKK.....",
    "................",
],
'custom-jukebox': [
    "................",
    ".....KKKKKK.....",
    "...KKDDDDDDKK...",
    "..KDDdDDDDDDDK..",
    "..KDdDDKKKDDDK..",
    ".KDDdDKoooKDDDK.",
    ".KDDDKoyyoOKDDK.",
    ".KDDDKoyKoOKDDK.",
    ".KDDDKooOOOKDDK.",
    ".KDDDDKOOOKDDDK.",
    ".KDDDDDKKKDDdDK.",
    "..KDDDDDDDDdDK..",
    "..KDDDDDDDdDDK..",
    "...KKDDDDDDKK...",
    ".....KKKKKK.....",
    "................",
],
'hookshot': [
    "..........KK....",
    ".........KlwK.KK",
    "....KK...KlgKKwK",
    "...KlwK..KlgKlgK",
    "...KlgK.KlgKlgK.",
    "....KlgKlgKlgK..",
    ".....KlggggdK...",
    "......KlgdKK....",
    ".....KdgK.......",
    "....KeK.........",
    "...KeK..........",
    "...KeK..........",
    "....KeK.........",
    "....KeK.........",
    "...KeK..........",
    "...KK...........",
],
'map-revealer': [
    "................",
    "KKKKKKKKKKKKKKKK",
    "KaaaaaaaaaaaaaAK",
    "KaAAAAAYGGnGGnAK",
    "KaAOOAAYGnnccnAK",
    "KaAAAOAYnGccnGAK",
    "KaAAOAAYGccGnnAK",
    "KaAAAAAYccGnNnAK",
    "KaAAOAAYcGnNNnAK",
    "KaAAAAAYGnnNnGAK",
    "KaAAAAAYnnGGGnAK",
    "KaAAAAAYGGGnnGAK",
    "KAAAAAAAAAAAAAAK",
    "KKKKKKKKKKKKKKKK",
    "................",
    "................",
],
'piston-crusher': [
    "................",
    ".KKKKKKKKKKKKKK.",
    ".KeeeeeeeeeeebK.",
    ".KlggggggggggdK.",
    ".KgdggdggdggddK.",
    ".KKKKKKKKKKKKKK.",
    "......KbBK......",
    "......KbBK......",
    "..KKKKKKKKKKKK..",
    "..KeeeeeeeeebK..",
    "..KKKKKKKKKKKK..",
    "..KlgglgKgglgK..",
    "g.KgdgdgdKgddK.l",
    "..KgddgKgdgddK..",
    "..KKKKKKKKKKKK..",
    "................",
],
'power-mining': [
    "................",
    "....KKKKKK......",
    "...KCCCCccKK....",
    "....KKKKcccuK...",
    "........KbcuuK..",
    ".......KbBKcuK..",
    "......KbBK.KcuK.",
    ".....KbBK..KcuK.",
    "....KbBK....KuK.",
    "...KbBK.....KuK.",
    "..KbBK.......KK.",
    ".KbBK.....Y.....",
    "KbBK............",
    "KBK.....Y...Y...",
    ".K..............",
    "................",
],
'rail-boost': [
    "................",
    "................",
    "...KKKKKKKKKKK..",
    "...KlllllllldK..",
    "oo.KlDDDDDDDdK..",
    "...KlgggggggdK..",
    "ooo.KlgggggdK...",
    "....KddddddddK..",
    "oo..KKKKKKKKKK..",
    ".....KDK..KDK...",
    ".....KKK..KKK...",
    "KKKKKKKKKKKKKKKK",
    "KlggllggllggllgK",
    "KKKKKKKKKKKKKKKK",
    ".KbbK.KbbK.KbbK.",
    ".KKKK.KKKK.KKKK.",
],
'super-enchantments': [
    "...........KKK..",
    "..P.......KCCK..",
    ".PpP.....KCcK.P.",
    "..P.....KCcuK...",
    ".......KCcuK....",
    "......KCcuK.....",
    ".....KCcuK......",
    "..KK.KcuK.......",
    "..KyKKuK....P...",
    "...KyyK....PpP..",
    "....KbyK....P...",
    "...KbKKyK.......",
    "..KbK..KK.......",
    ".KyK............",
    ".KK.............",
    "................",
],
'useful-autocrafter': [
    "................",
    ".KKKKKKKKKKKKKK.",
    ".KeeeeeeeeeeebK.",
    ".KeKKKKKKKKKKbK.",
    ".KeKbBKbBKbBKbK.",
    ".KeKBBKBBKBBKbK.",
    ".KeKKKKKKKKKKbK.",
    ".KeKbBKyOKbBKbK.",
    ".KeKBBKOOKBBKbK.",
    ".KeKKKKKKKKKKbK.",
    ".KeKbBKbBKbBKbK.",
    ".KeKBBKBBKBBKbK.",
    ".KeKKKKKKKKKKbK.",
    ".KbbbbbbbbbbbBK.",
    ".KKKKKKKKKKKKKK.",
    "................",
],
'wireless-redstone': [
    "................",
    ".........KK.....",
    "..KK......KrK...",
    ".KRRK......KrK..",
    "KRrrrK..KK..KrK.",
    "KrrrmK...KrK.KrK",
    ".KrmK.....KrK.Kr",
    ".KbBK.....KrK.Kr",
    ".KbBK....KrK.KrK",
    ".KbBK...KK..KrK.",
    ".KbBK......KrK..",
    ".KbBK.....KrK...",
    ".KbBK.....KK....",
    ".KbBK...........",
    ".KKKK...........",
    "................",
],
'superwarp': [
    "................",
    "..KKKKKKKKKKKK..",
    "..KDqDDqDDqDDK..",
    "..KqKKKKKKKKqK..",
    "..KDKPpppqpKDK..",
    "..KDKpPppqqKDK..",
    "..KqKppPqqpKqK..",
    "..KDKpqqPppKDK..",
    "..KDKqqppPpKDK..",
    "..KqKqpppqPKqK..",
    "..KDKppqqppKDK..",
    "..KDKpqqpppKDK..",
    "..KqKKKKKKKKqK..",
    "..KDqDDqDDqDDK..",
    "..KKKKKKKKKKKK..",
    "................",
],
'npc-pickup': [
    "......KKK.......",
    ".....KoooK......",
    "....KooooOK.....",
    "...KKKoOKKK.....",
    ".....KoOK.......",
    "...KKKKKKKK.....",
    "..KhhhhhhhHK....",
    "..KhssssssHK....",
    "..KswKsswKSK....",
    "..KssssssSSK....",
    "..KsshHhsSSK....",
    "..KSSSSSSSSK....",
    "...KKKKKKKK.....",
    "..KgggggggdK....",
    ".KggggggggddK...",
    ".KKKKKKKKKKKK...",
],
}


def svg(rows):
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), rows
    parts = []
    for y, row in enumerate(rows):
        x = 0
        while x < 16:
            ch = row[x]
            if ch == '.':
                x += 1
                continue
            start = x
            while x < 16 and row[x] == ch:
                x += 1
            parts.append(f'<rect x="{start}" y="{y}" width="{x - start}" height="1" fill="{PALETTE[ch]}"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">'
            + ''.join(parts) + '</svg>\n')


def build(dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    for name, rows in ICONS.items():
        (dest / f'{name}.svg').write_text(svg(rows), encoding='utf-8')


def preview(path, scale=12):
    from PIL import Image, ImageDraw
    names = list(ICONS)
    cols = 5
    cell = 16 * scale + 40
    sheet = Image.new('RGB', (cols * cell, ((len(names) + cols - 1) // cols) * (cell + 24)), '#14202a')
    d = ImageDraw.Draw(sheet)
    for i, name in enumerate(names):
        ox, oy = (i % cols) * cell + 20, (i // cols) * (cell + 24) + 16
        for s, bx, by in [(scale, ox, oy), (2, ox + 16 * scale - 32, oy + 16 * scale + 4)]:
            for y, row in enumerate(ICONS[name]):
                for x, ch in enumerate(row):
                    if ch != '.':
                        d.rectangle([bx + x * s, by + y * s, bx + (x + 1) * s - 1, by + (y + 1) * s - 1], fill=PALETTE[ch])
        d.text((ox, oy + 16 * scale + 6), name, fill='white')
    sheet.save(path)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        preview(sys.argv[1])
    else:
        build(Path(__file__).resolve().parent.parent / 'assets/icons')
