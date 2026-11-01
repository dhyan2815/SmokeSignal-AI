"""
Synthetic edge-case transforms for issue #12 (sunset / dark cloud / fog / smoke on aerial tiles).

Each fn takes a PIL RGB image and an optional numpy Generator. With rng=None the parameters
are the fixed midpoints, so tests/eval_edge_cases.py stays reproducible.
These are approximations of the real phenomena; real aerial images should supplement them.
"""
import numpy as np
from PIL import Image

GRAY = np.array([1.0, 1.0, 1.0], dtype=np.float32)


def _p(rng, lo, hi):
    return (lo + hi) / 2 if rng is None else float(rng.uniform(lo, hi))


def _noise(h, w, rng, cells=6):
    """Smooth 0..1 noise field, upscaled from a coarse random grid."""
    g = np.random.default_rng(0) if rng is None else rng
    small = Image.fromarray((g.random((cells, cells)) * 255).astype(np.uint8))
    return np.asarray(small.resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0


def _out(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def _blend(a, color, alpha):
    return a * (1 - alpha[..., None]) + np.asarray(color, dtype=np.float32) * alpha[..., None]


def sunset(img, rng=None):
    """Warm orange cast, slightly dimmer (low sun)."""
    a = np.asarray(img, dtype=np.float32)
    gain = np.array([_p(rng, 1.1, 1.4), _p(rng, 0.75, 0.95), _p(rng, 0.4, 0.7)])
    return _out(a * gain * _p(rng, 0.7, 1.0))


def dark_cloud(img, rng=None):
    """Darken + desaturate with a top-down shadow gradient (monsoon cover)."""
    a = np.asarray(img, dtype=np.float32)
    mix = _p(rng, 0.4, 0.8)
    a = (1 - mix) * a + mix * a.mean(axis=2, keepdims=True)
    shade = np.linspace(_p(rng, 0.2, 0.5), _p(rng, 0.6, 0.9), a.shape[0])[:, None, None]
    return _out(a * shade)


def cloud(img, rng=None):
    """Dark cover plus patchy gray cloud banks."""
    a = np.asarray(dark_cloud(img, rng), dtype=np.float32)
    n = _noise(*a.shape[:2], rng)
    alpha = np.clip((n - 0.4) * 2.5, 0, 1) * _p(rng, 0.5, 0.85)
    return _out(_blend(a, [105, 108, 112], alpha))


def fog(img, rng=None):
    """Global low-contrast light-gray veil with uneven density."""
    a = np.asarray(img, dtype=np.float32)
    alpha = np.clip(_p(rng, 0.5, 0.8) + 0.2 * (_noise(*a.shape[:2], rng) - 0.5), 0, 1)
    return _out(_blend(a, [205, 208, 210], alpha))


def smoke(img, rng=None):
    """Localized gray plume(s); the rest of the tile is untouched."""
    a = np.asarray(img, dtype=np.float32)
    n = _noise(*a.shape[:2], rng, cells=4)
    alpha = np.clip((n - _p(rng, 0.45, 0.6)) * 4, 0, 1) * _p(rng, 0.6, 0.9)
    gray = _p(rng, 110, 170)
    return _out(_blend(a, [gray, gray, gray + 5], alpha))
