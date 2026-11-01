"""
Issue #12, Step 3: honest evaluation of the 5-class model on the held-out TEST split.

    python src/evaluate_multiclass.py [--model model/wildfire_detector_multiclass.keras] [--alert-threshold 0.5]

Gates (alert score = P(fire) + P(smoke)):
  1. Regression: on the ORIGINAL test tiles, binary precision/recall within 2 points of baseline.
  2. Fire recall (original tiles) not degraded by more than 2 points.
  3. FPR < 5% on synthetic sunset / cloud / fog negatives (reported per category).
"""
import argparse
import json
import os
from collections import defaultdict

import numpy as np
from PIL import ImageFile
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE_PRECISION, BASE_RECALL = 0.9609, 0.9681  # binary model on the original test split
MAX_DROP = 0.02
MAX_FPR = 0.05


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='model/wildfire_detector_multiclass.keras')
    ap.add_argument('--data', default='data/multiclass/test')
    ap.add_argument('--alert-threshold', type=float, default=0.5)
    args = ap.parse_args()

    model = load_model(args.model)
    labels = json.load(open(os.path.join(os.path.dirname(args.model), 'class_labels.json')))
    classes = [labels[str(i)] for i in range(len(labels))]
    gen = ImageDataGenerator(rescale=1 / 255.).flow_from_directory(
        args.data, target_size=model.input_shape[1:3], batch_size=128, class_mode='categorical',
        classes=classes, shuffle=False)
    probs = model.predict(gen, verbose=0)
    y = gen.classes
    pred = probs.argmax(1)
    alert = probs[:, classes.index('fire')] + probs[:, classes.index('smoke')]
    is_alert = alert > args.alert_threshold
    names = [os.path.basename(f) for f in gen.filenames]
    synthetic = np.array([n.startswith('syn_') for n in names])

    print('=== 5-class (argmax), all test images ===')
    print(classification_report(y, pred, target_names=classes, digits=3))
    print('confusion (rows=true, cols=pred):', classes)
    print(confusion_matrix(y, pred))

    # 1+2: original tiles only; positives = fire, negatives = clear
    fire_i, clear_i = classes.index('fire'), classes.index('clear')
    orig = ~synthetic
    pos, neg = orig & (y == fire_i), orig & (y == clear_i)
    tp, fp, fn = is_alert[pos].sum(), is_alert[neg].sum(), (~is_alert[pos]).sum()
    precision, recall = tp / (tp + fp), tp / (tp + fn)
    ok_p, ok_r = precision >= BASE_PRECISION - MAX_DROP, recall >= BASE_RECALL - MAX_DROP
    print(f"\n=== Regression on original tiles (threshold {args.alert_threshold}) ===")
    print(f"precision {precision:.2%} (baseline {BASE_PRECISION:.2%}) {'PASS' if ok_p else 'FAIL'}")
    print(f"recall    {recall:.2%} (baseline {BASE_RECALL:.2%}) {'PASS' if ok_r else 'FAIL'}")

    # 3: synthetic categories from filename: syn_<transform>_<tile>.jpg in <class>/
    cats = defaultdict(list)
    for n, f, a in zip(names, gen.filenames, is_alert):
        if n.startswith('syn_'):
            cats[(f.split('/')[0].split('\\')[0], n.split('_')[1])].append(a)
    print('\n=== Synthetic edge cases (test split) ===')
    all_fpr_ok = True
    for (cls, t), v in sorted(cats.items()):
        rate = float(np.mean(v))
        if cls in ('clear', 'cloud', 'fog'):  # negatives: alert rate is the FPR
            ok = rate < MAX_FPR
            all_fpr_ok &= ok
            print(f"{t + ' / ' + cls:<22} n={len(v):<5} FPR {rate:6.1%}  {'PASS' if ok else 'FAIL'}")
        else:  # fire / smoke positives: alert rate is recall
            print(f"{t + ' / ' + cls:<22} n={len(v):<5} alert-rate (recall) {rate:6.1%}")

    verdict = ok_p and ok_r and all_fpr_ok
    print(f"\nOVERALL: {'PASS' if verdict else 'FAIL'}")


if __name__ == '__main__':
    main()
