#!/usr/bin/env python
"""Compress a folder of photos into a web album and rewrite the gallery block of an album page.

Usage (run from anywhere):
  python _tools/build-album.py <source_folder> <album_slug> [--page corporate-knu.html] [--prefix k] [--cover N]

Example:
  python _tools/build-album.py "C:/Fatek_9702/web_side_原始檔/corporate/knu" knu --page corporate-knu.html --cover 3

Output (under images/corporate/<album_slug>/):
  <prefix>_0001.jpg ...        grid thumbnails, 800 px on the long edge
  large/<prefix>_0001.jpg ...  lightbox images, 1800 px on the long edge
  cover.jpg                    4:3 crop, 800x600, from photo number --cover (default 1)

The page's <!-- ALBUM:START --> ... <!-- ALBUM:END --> block is replaced with one <a class="album-item">
per photo (lazy loaded, width/height set so the layout does not jump). Re-running is safe: old
generated images are deleted first, so the album always matches the source folder.

JPG/PNG are read directly. HEIC needs `pip install pillow-heif`; without it HEIC files are skipped
with a warning.
"""
import argparse
import os
import re
import shutil
import sys

from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pillow_heif = None

EXTS = {'.jpg', '.jpeg', '.png', '.heic'}
THUMB_EDGE = 800
LARGE_EDGE = 1800


def save_resized(im, path, edge, quality):
    im = im.copy()
    im.thumbnail((edge, edge), Image.LANCZOS)
    im.save(path, 'JPEG', quality=quality, optimize=True, progressive=True)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('slug')
    ap.add_argument('--page', default=None)
    ap.add_argument('--prefix', default='k')
    ap.add_argument('--cover', type=int, default=1)
    a = ap.parse_args()

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out = os.path.join(root, 'images', 'corporate', a.slug)
    page = os.path.join(root, a.page) if a.page else None

    files = sorted(f for f in os.listdir(a.source) if os.path.splitext(f)[1].lower() in EXTS)
    if not files:
        sys.exit('no photos found in ' + a.source)

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'large'))

    items = []
    n = 0
    for f in files:
        if f.lower().endswith('.heic') and pillow_heif is None:
            print('skip (needs pillow-heif):', f)
            continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(a.source, f))).convert('RGB')
        n += 1
        name = '%s_%04d.jpg' % (a.prefix, n)
        w, h = save_resized(im, os.path.join(out, name), THUMB_EDGE, 78)
        save_resized(im, os.path.join(out, 'large', name), LARGE_EDGE, 82)
        if n == a.cover:
            ImageOps.fit(im, (800, 600), Image.LANCZOS).save(
                os.path.join(out, 'cover.jpg'), 'JPEG', quality=80, optimize=True, progressive=True)
        items.append((name, w, h))

    base = 'images/corporate/%s' % a.slug
    lines = []
    for i, (name, w, h) in enumerate(items, 1):
        lines.append(
            '                <a class="album-item" href="%s/large/%s">'
            '<img src="%s/%s" width="%d" height="%d" alt="活動照片 %d" loading="lazy" decoding="async"></a>'
            % (base, name, base, name, w, h, i))
    block = '<!-- ALBUM:START -->\n' + '\n'.join(lines) + '\n<!-- ALBUM:END -->'

    if page:
        with open(page, 'rb') as fh:
            text = fh.read().decode('utf-8')
        new, cnt = re.subn(r'<!-- ALBUM:START -->.*?<!-- ALBUM:END -->', lambda m: block, text, flags=re.S)
        if cnt != 1:
            sys.exit('ALBUM markers not found exactly once in ' + page)
        with open(page, 'wb') as fh:
            fh.write(new.encode('utf-8'))
        print('updated', page)
    else:
        print(block)

    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(out) for f in fs)
    print('%d photos, %.1f MB written to %s' % (len(items), total / 1e6, out))


if __name__ == '__main__':
    main()
