"""
Issue #12: validated ingestion of external (real) images into data/real_eval/<class>/.

Real images are held OUT of training by default: they are the honest check of whether
models trained on the Kaggle tiles + synthetic edge cases generalize.  Every image gets a
manifest row (source, url, licence, licence tier, perceptual hash).  Images are dropped if
they are near-duplicates (dHash hamming <= 4) of an existing tile or of an earlier ingest.

  # YOLO-label dataset: class ids -> our classes; earlier entries win when an image has several
  python src/ingest_external.py --name ignis --src data/raw_external/ignis/data \
      --yolo-map 3=fire,1=smoke,2=smoke --license CC-BY-4.0 --tier open \
      --url https://huggingface.co/datasets/matjs/ignis --existing-src "<kaggle dataset root>"

  # folder-per-class dataset (subfolder name == one of our classes)
  python src/ingest_external.py --name foo --src path/to/foo --folder-classes --license CC0 --tier open
"""
import argparse
import csv
import os
import sys

import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
CLASSES = {'clear', 'cloud', 'fire', 'fog', 'smoke'}
EXTS = ('.jpg', '.jpeg', '.png')
SIZE = 350  # match the Kaggle tiles
MAX_HAMMING = 4
POP16 = np.array([bin(i).count('1') for i in range(1 << 16)], dtype=np.uint8)


def dhash(img):
    a = np.asarray(img.convert('L').resize((9, 8), Image.LANCZOS), dtype=np.int16)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    return int(''.join('1' if b else '0' for b in bits), 2)


def hamming_min(h, pool):
    """Smallest hamming distance between hash h and a uint64 array of hashes."""
    if len(pool) == 0:
        return 64
    x = pool ^ np.uint64(h)
    d = sum(POP16[(x >> np.uint64(16 * i)) & np.uint64(0xFFFF)] for i in range(4))
    return int(d.min())


def existing_hashes(src, cache):
    if os.path.exists(cache):
        return np.load(cache)
    hs = []
    for split in ('train', 'valid', 'test'):
        for c in ('wildfire', 'nowildfire'):
            d = os.path.join(src, split, c)
            for f in os.listdir(d):
                try:
                    hs.append(dhash(Image.open(os.path.join(d, f))))
                except OSError:
                    pass
    arr = np.array(hs, dtype=np.uint64)
    np.save(cache, arr)
    return arr


def yolo_class(label_file, order):
    ids = {l.split()[0] for l in open(label_file) if l.strip()}
    for cid, cls in order:
        if cid in ids:
            return cls
    return None


def collect(args):
    items = []
    if args.folder_classes:
        for c in sorted(os.listdir(args.src)):
            d = os.path.join(args.src, c)
            if c in CLASSES and os.path.isdir(d):
                items += [(os.path.join(d, f), c) for f in sorted(os.listdir(d)) if f.lower().endswith(EXTS)]
    else:
        order = [tuple(p.split('=')) for p in args.yolo_map.split(',')]
        for split in sorted(os.listdir(args.src)):
            idir, ldir = os.path.join(args.src, split, 'images'), os.path.join(args.src, split, 'labels')
            if not os.path.isdir(idir):
                continue
            for f in sorted(os.listdir(idir)):
                lf = os.path.join(ldir, os.path.splitext(f)[0] + '.txt')
                c = yolo_class(lf, order) if os.path.exists(lf) else None
                if c:
                    items.append((os.path.join(idir, f), c))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True, help='source tag used as filename prefix')
    ap.add_argument('--src', required=True)
    ap.add_argument('--yolo-map', help='e.g. 3=fire,1=smoke,2=smoke (first match wins)')
    ap.add_argument('--folder-classes', action='store_true')
    ap.add_argument('--license', required=True)
    ap.add_argument('--tier', required=True, choices=['open', 'research'])
    ap.add_argument('--url', default='')
    ap.add_argument('--dst', default='data/real_eval')
    ap.add_argument('--existing-src', help='Kaggle dataset root, for dedup against existing tiles')
    args = ap.parse_args()
    if not args.folder_classes and not args.yolo_map:
        ap.error('give --yolo-map or --folder-classes')

    os.makedirs(args.dst, exist_ok=True)
    pool = np.array([], dtype=np.uint64)
    if args.existing_src:
        pool = existing_hashes(args.existing_src, os.path.join(args.dst, 'existing_phash.npy'))
        print(f"dedup pool: {len(pool)} existing tiles")
    else:
        print('WARNING: no --existing-src, skipping dedup against existing tiles')

    manifest = os.path.join(args.dst, 'manifest.csv')
    new_file = not os.path.exists(manifest)
    seen = []
    kept, dup_existing, dup_self, bad = {}, 0, 0, 0
    with open(manifest, 'a', newline='') as fh:
        w = csv.writer(fh)
        if new_file:
            w.writerow(['file', 'class', 'source', 'url', 'license', 'tier', 'phash', 'orig_path'])
        for path, cls in collect(args):
            try:
                img = Image.open(path).convert('RGB')
            except OSError:
                bad += 1
                continue
            s = min(img.size)
            l, t = (img.width - s) // 2, (img.height - s) // 2
            img = img.crop((l, t, l + s, t + s)).resize((SIZE, SIZE), Image.LANCZOS)
            h = dhash(img)
            if hamming_min(h, pool) <= MAX_HAMMING:
                dup_existing += 1
                continue
            if hamming_min(h, np.array(seen, dtype=np.uint64)) <= MAX_HAMMING:
                dup_self += 1
                continue
            seen.append(h)
            name = f"{args.name}_{os.path.splitext(os.path.basename(path))[0][:60]}.jpg"
            os.makedirs(os.path.join(args.dst, cls), exist_ok=True)
            img.save(os.path.join(args.dst, cls, name), quality=92)
            w.writerow([name, cls, args.name, args.url, args.license, args.tier, f"{h:016x}", path])
            kept[cls] = kept.get(cls, 0) + 1

    print(f"kept per class: {kept} | dropped: {dup_existing} dup of existing tiles, {dup_self} dup within source, {bad} unreadable")
    print(f"manifest: {manifest}")


if __name__ == '__main__':
    sys.exit(main())
