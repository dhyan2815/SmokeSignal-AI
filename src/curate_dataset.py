"""
Issue #12, Step 1: build data/multiclass/{train,valid,test}/{clear,cloud,fire,fog,smoke}.

    python src/curate_dataset.py --src "<wildfire dataset root with train/valid/test>"

- clear <- original nowildfire (hardlinked, no extra disk) + sunset-tinted nowildfire
- fire  <- original wildfire (hardlinked) + sunset-tinted wildfire (so a tint is not a "not fire" shortcut)
- cloud/fog/smoke <- synthetic transforms (src/synth.py) of nowildfire tiles
- Synthetic images are derived only from tiles of the SAME split, so there is no train/test leakage.
- Extra real images: drop them in --extra-dir/<class>/ and they are split 70/15/15 into that class.
- Writes manifest.csv (split, class, file, source, transform). data/multiclass is gitignored.
"""
import argparse
import csv
import os
import random
import shutil
import sys
from collections import Counter

import numpy as np
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import synth  # noqa: E402

CLASSES = ['clear', 'cloud', 'fire', 'fog', 'smoke']
SPLITS = ['train', 'valid', 'test']
EXTS = ('.jpg', '.jpeg', '.png')
# (target class, source folder, transform name, splits it appears in)
ALL, TEST_ONLY = tuple(SPLITS), ('test',)
SYNTH_PLAN = [
    ('clear', 'nowildfire', 'sunset', ALL),
    ('cloud', 'nowildfire', 'cloud', ALL),
    ('fog', 'nowildfire', 'fog', ALL),
    ('smoke', 'nowildfire', 'smoke', ALL),
    ('fire', 'wildfire', 'sunset', ALL),
    # hold-out generator families: never seen in training, so they measure generalization
    ('cloud', 'nowildfire', 'cloud_cumulus', TEST_ONLY),
    ('fog', 'nowildfire', 'fog_valley', TEST_ONLY),
    ('smoke', 'nowildfire', 'smoke_plume', TEST_ONLY),
]


def images(folder):
    return sorted(f for f in os.listdir(folder) if f.lower().endswith(EXTS))


def link(src, dst):
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--dst', default='data/multiclass')
    ap.add_argument('--extra-dir', help='<class>/ folders of real extra images')
    ap.add_argument('--n-train', type=int, default=2000, help='synthetic images per plan row, train')
    ap.add_argument('--n-eval', type=int, default=500, help='synthetic images per plan row, valid and test')
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()

    # outputs are generated and hardlinked (originals untouched), so a rerun starts clean
    if os.path.isdir(args.dst) and os.path.basename(os.path.normpath(args.dst)) == 'multiclass':
        shutil.rmtree(args.dst)

    rows = []
    for split in SPLITS:
        for c in CLASSES:
            os.makedirs(os.path.join(args.dst, split, c), exist_ok=True)

        # originals
        for cls, folder in (('clear', 'nowildfire'), ('fire', 'wildfire')):
            for f in images(os.path.join(args.src, split, folder)):
                link(os.path.join(args.src, split, folder, f), os.path.join(args.dst, split, cls, f))
                rows.append((split, cls, f, f, 'original'))

        # synthetic, one RNG per (split, plan row) so reruns are identical
        n = args.n_train if split == 'train' else args.n_eval
        for cls, folder, tname, in_splits in SYNTH_PLAN:
            if split not in in_splits:
                continue
            seed_rng = random.Random(f"{args.seed}-{split}-{cls}-{tname}")
            pool = images(os.path.join(args.src, split, folder))
            picks = seed_rng.sample(pool, min(n, len(pool)))
            rng = np.random.default_rng(seed_rng.getrandbits(32))
            fn = getattr(synth, tname)
            for f in picks:
                try:
                    img = Image.open(os.path.join(args.src, split, folder, f)).convert('RGB')
                except OSError:
                    print(f"skip unreadable: {split}/{folder}/{f}")
                    continue
                name = f"syn_{tname}__{os.path.splitext(f)[0]}.jpg"
                fn(img, rng).save(os.path.join(args.dst, split, cls, name), quality=90)
                rows.append((split, cls, name, f, f"synthetic_{tname}"))
            print(f"{split:<6} {cls:<6} synthetic_{tname}: {sum(1 for r in rows if r[:2] == (split, cls) and r[4] == 'synthetic_' + tname)}", flush=True)

    if args.extra_dir:
        for cls in CLASSES:
            d = os.path.join(args.extra_dir, cls)
            if not os.path.isdir(d):
                continue
            files = images(d)
            random.Random(args.seed).shuffle(files)
            cut = [0, int(.7 * len(files)), int(.85 * len(files)), len(files)]
            for i, split in enumerate(SPLITS):
                for f in files[cut[i]:cut[i + 1]]:
                    link(os.path.join(d, f), os.path.join(args.dst, split, cls, f"real_{f}"))
                    rows.append((split, cls, f"real_{f}", f, 'real'))

    with open(os.path.join(args.dst, 'manifest.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['split', 'class', 'file', 'source', 'transform'])
        w.writerows(rows)

    # verification summary
    counts = Counter((r[0], r[1]) for r in rows)
    kinds = Counter((r[0], r[4]) for r in rows)
    print(f"\n{'split':<7}" + ''.join(f"{c:>9}" for c in CLASSES))
    for s in SPLITS:
        print(f"{s:<7}" + ''.join(f"{counts[(s, c)]:>9}" for c in CLASSES))
    ok = all(kinds[(s, t)] >= 500 for s in ('valid', 'test') for t in ('synthetic_sunset', 'synthetic_cloud'))
    print(f"\n>=500 sunset and >=500 cloud in valid and test: {'PASS' if ok else 'FAIL'}")
    print("Note: synthetic sunset rows include both clear (no-fire) and fire tiles.")


if __name__ == '__main__':
    main()
