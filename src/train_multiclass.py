"""
Issue #12, Step 2: transfer-learn the binary wildfire CNN into a 5-class softmax model.

    python src/train_multiclass.py                       # full run
    python src/train_multiclass.py --steps 20 --epochs1 1 --epochs2 1 --out /tmp/smoke.keras   # quick check

Stage 1: freeze Conv2D/MaxPooling2D, train the head only (new Dense(5, softmax)).
Stage 2: unfreeze everything, fine-tune at 1e-5 with early stopping on val_loss.
Evaluation against the baseline lives in src/evaluate_multiclass.py (Step 3).
"""
import argparse
import json
import os

import cv2
import numpy as np
import tensorflow as tf
from PIL import ImageFile
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

ImageFile.LOAD_TRUNCATED_IMAGES = True  # a few tiles in the source dataset are truncated

CLASSES = ['clear', 'cloud', 'fire', 'fog', 'smoke']  # = flow_from_directory's alphabetical order
BATCH = 64


def hsv_jitter(x):
    """Random hue (+-15 deg), saturation and brightness (0.7-1.3) shift. x: float32 RGB 0-255."""
    hsv = cv2.cvtColor(np.clip(x, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 0] = (hsv[..., 0] + np.random.uniform(-7.5, 7.5)) % 180  # OpenCV hue is 0-179 (= degrees / 2)
    hsv[..., 1] = np.clip(hsv[..., 1] * np.random.uniform(0.7, 1.3), 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * np.random.uniform(0.7, 1.3), 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)


def build_model(base_path, size):
    base = models.load_model(base_path)
    # reuse the trained backbone + Dense(128); replace Dense(1, sigmoid) with Dense(5, softmax)
    return models.Sequential(
        [layers.Input(shape=(*size, 3))] + base.layers[:-1] + [layers.Dense(len(CLASSES), activation='softmax', name='head')]
    )


def compile_(model, lr):
    model.compile(optimizer=Adam(lr), loss='categorical_crossentropy', metrics=['accuracy'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='data/multiclass')
    ap.add_argument('--base', default='model/wildfire_detector_model.keras')
    ap.add_argument('--out', default='model/wildfire_detector_multiclass.keras')
    ap.add_argument('--epochs1', type=int, default=5)
    ap.add_argument('--epochs2', type=int, default=10)
    ap.add_argument('--steps', type=int, help='cap steps per epoch (smoke runs)')
    args = ap.parse_args()
    tf.keras.utils.set_random_seed(42)

    base_in = models.load_model(args.base).input_shape
    size = base_in[1:3]

    train_gen = ImageDataGenerator(
        rescale=1 / 255., rotation_range=20, horizontal_flip=True, width_shift_range=0.1,
        height_shift_range=0.1, zoom_range=0.15, fill_mode='reflect', preprocessing_function=hsv_jitter,
    ).flow_from_directory(os.path.join(args.data, 'train'), target_size=size, batch_size=BATCH,
                          class_mode='categorical', classes=CLASSES, seed=42)
    val_gen = ImageDataGenerator(rescale=1 / 255.).flow_from_directory(
        os.path.join(args.data, 'valid'), target_size=size, batch_size=BATCH,
        class_mode='categorical', classes=CLASSES, shuffle=False)

    w = compute_class_weight('balanced', classes=np.arange(len(CLASSES)), y=train_gen.classes)
    class_weight = dict(enumerate(w))
    print('class weights:', {CLASSES[i]: round(float(v), 2) for i, v in class_weight.items()})

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    model = build_model(args.base, size)
    kw = dict(class_weight=class_weight, steps_per_epoch=args.steps, validation_steps=args.steps)

    # Stage 1: head only
    for l in model.layers:
        l.trainable = not isinstance(l, (layers.Conv2D, layers.MaxPooling2D))
    compile_(model, 1e-3)
    h1 = model.fit(train_gen, validation_data=val_gen, epochs=args.epochs1,
                   callbacks=[ModelCheckpoint(args.out, monitor='val_loss', save_best_only=True)], **kw)
    best1 = min(h1.history['val_loss'])

    # Stage 2: fine-tune everything; only overwrite the checkpoint if it beats stage 1
    for l in model.layers:
        l.trainable = True
    compile_(model, 1e-5)
    h2 = model.fit(train_gen, validation_data=val_gen, epochs=args.epochs2,
                   callbacks=[EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
                              ModelCheckpoint(args.out, monitor='val_loss', save_best_only=True,
                                              initial_value_threshold=best1)], **kw)

    labels = os.path.join(os.path.dirname(args.out) or '.', 'class_labels.json')
    json.dump({str(i): c for i, c in enumerate(CLASSES)}, open(labels, 'w'), indent=2)
    best = min(best1, min(h2.history['val_loss']))
    print(f"\nbest val_loss={best:.4f}  model -> {args.out}  labels -> {labels}")


if __name__ == '__main__':
    main()
