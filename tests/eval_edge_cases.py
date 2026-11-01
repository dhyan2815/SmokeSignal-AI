"""
Issue #12, Step 0: baseline false-positive rate of the current model on edge cases.

Every image under --edge-dir/<category>/ is a NEGATIVE (no wildfire), e.g. sunset/, cloud/, fog/.
Optionally also stress a folder of known no-fire tiles with synthetic sunset / dark-cloud
tints via --base-dir, so the baseline can be measured without hand-collected images.

    python tests/eval_edge_cases.py --edge-dir data/edge_cases
    python tests/eval_edge_cases.py --base-dir path/to/nowildfire --limit 500
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from config import Config  # noqa: E402
from synth import dark_cloud, sunset  # noqa: E402

EXTS = ('.jpg', '.jpeg', '.png')
THRESHOLDS = (0.5, Config.CONFIDENCE_THRESHOLD, 0.9, 0.95)
FIRE_IDX, SMOKE_IDX = 2, 4  # Plan A class order: clear, cloud, fire, fog, smoke


SYNTHETIC = {'control_untinted': lambda im: im, 'synthetic_sunset': sunset, 'synthetic_dark_cloud': dark_cloud}


def fire_score(preds):
    """Alert score: binary sigmoid, or fire+smoke mass for the 5-class model."""
    p = preds[0]
    return float(p[FIRE_IDX] + p[SMOKE_IDX]) if len(p) == 5 else float(p[0])


def list_images(folder):
    return sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(EXTS))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--edge-dir', help='folder of <category>/ subfolders of negative images')
    ap.add_argument('--base-dir', help='folder of no-fire tiles to tint synthetically')
    ap.add_argument('--fire-dir', help='folder of true wildfire tiles, reports recall (gate: must not drop)')
    ap.add_argument('--limit', type=int, default=500, help='max images per category')
    args = ap.parse_args()
    if not (args.edge_dir or args.base_dir or args.fire_dir):
        ap.error('give --edge-dir, --base-dir and/or --fire-dir')

    from tensorflow.keras.models import load_model
    from utils.preprocess import preprocess_for_model

    model = load_model(Config.MODEL_PATH)
    size = model.input_shape[1:]

    # category -> list of (path, transform or None)
    sets = {}
    if args.edge_dir:
        for cat in sorted(os.listdir(args.edge_dir)):
            d = os.path.join(args.edge_dir, cat)
            if os.path.isdir(d):
                sets[cat] = [(p, None) for p in list_images(d)[:args.limit]]
    if args.base_dir:
        base = list_images(args.base_dir)[:args.limit]
        for name, fn in SYNTHETIC.items():
            sets[name] = [(p, fn) for p in base]

    fire = [(p, None) for p in list_images(args.fire_dir)[:args.limit]] if args.fire_dir else []
    print(f"Model: {Config.MODEL_PATH}  output={model.output_shape}")
    print(f"{'category':<22}{'n':>6}" + ''.join(f"{'FPR@' + str(t):>11}" for t in THRESHOLDS))
    print('-' * (28 + 11 * len(THRESHOLDS)))
    for cat, items in sets.items():
        if not items:
            print(f"{cat:<22}{0:>6}  (empty)")
            continue
        scores = []
        for path, fn in items:
            img = Image.open(path).convert('RGB')
            if fn:
                img = fn(img)
            x = preprocess_for_model(img, size)
            scores.append(fire_score(model.predict(x, verbose=0)))
        s = np.array(scores)
        print(f"{cat:<22}{len(s):>6}" + ''.join(f"{(s > t).mean():>11.1%}" for t in THRESHOLDS))
    if fire:
        s = np.array([fire_score(model.predict(preprocess_for_model(Image.open(p).convert('RGB'), size), verbose=0))
                      for p, _ in fire])
        print(f"{'RECALL (true fire)':<22}{len(s):>6}" + ''.join(f"{(s > t).mean():>11.1%}" for t in THRESHOLDS))
    print("\nTarget (issue #12): FPR < 5%. Every image above is a true negative.")


if __name__ == '__main__':
    main()
