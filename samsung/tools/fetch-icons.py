#!/usr/bin/env python3
"""Downloads the app logos the home screen shows on its tiles, as 256x256 PNGs in home/icons.

The logos belong to their owners and aren't kept in the repository, so run this once before
building. They come from the public App Store listings (no account needed). Needs Pillow:
`python3 -m pip install Pillow`.

    python3 tools/fetch-icons.py              # all of them
    python3 tools/fetch-icons.py netflix      # just these
"""
import io
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

from PIL import Image

OUT = pathlib.Path(__file__).resolve().parent.parent / 'home' / 'icons'
HEADERS = {'User-Agent': 'refab-home-fetch-icons'}

# file name -> App Store search term and a pattern the listing's name must match, so a lookalike
# app never sneaks in.
APPS = {
    'netflix': ('Netflix', r'^Netflix'),
    'youtube': ('YouTube', r'^YouTube$'),
    'hbomax': ('HBO Max', r'^(HBO )?Max'),
    'peacock': ('Peacock TV', r'^Peacock'),
    'primevideo': ('Amazon Prime Video', r'^(Amazon )?Prime Video'),
    'spotify': ('Spotify', r'^Spotify'),
    'smartthings': ('SmartThings', r'^SmartThings'),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
        return r.read()


def save_square(data, target, size=256):
    img = Image.open(io.BytesIO(data)).convert('RGBA')
    # Fill transparent rounded corners with the icon's own edge colour, so the tile's corners
    # (rounded again by the home screen) don't show a different colour.
    edge = img.getpixel((int(img.width * 0.06), img.height // 2))
    if edge[3] < 200:
        edge = img.getpixel((img.width // 2, int(img.height * 0.06)))
    canvas = Image.new('RGB', (size, size), edge[:3])
    img.thumbnail((size, size), Image.LANCZOS)
    canvas.paste(img, ((size - img.width) // 2, (size - img.height) // 2), img)
    canvas.save(target, 'PNG')


def main(only):
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (term, match) in APPS.items():
        if only and name not in only:
            continue
        query = urllib.parse.urlencode({'term': term, 'entity': 'software', 'country': 'us', 'limit': 10})
        results = json.loads(get('https://itunes.apple.com/search?' + query))['results']
        hit = next((r for r in results if re.search(match, r['trackName'])), None)
        if not hit:
            print(f'no App Store listing matched {term!r}; skipping {name}', file=sys.stderr)
            continue
        save_square(get(re.sub(r'\.jpg$', '.png', hit['artworkUrl512'])), OUT / f'{name}.png')
        print(f'{name:<12} {hit["trackName"]}')
    print(f'icons saved to {OUT}')


if __name__ == '__main__':
    main(sys.argv[1:])
