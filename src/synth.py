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
    """Localized gray plume(s); resampled until the plume visibly covers 15-70% of the tile,
    so no image carries the `smoke` label while being near-identical to its clear source."""
    a = np.asarray(img, dtype=np.float32)
    for _ in range(1 if rng is None else 30):
        n = _noise(*a.shape[:2], rng, cells=4)
        alpha = np.clip((n - _p(rng, 0.4, 0.6)) * 4, 0, 1) * _p(rng, 0.6, 0.9)
        gray = _p(rng, 110, 190)
        out = _blend(a, [gray, gray, gray + 5], alpha)
        # coverage AND contrast gate: low-contrast plumes on gray tiles would still look like `clear`
        if 0.15 <= (alpha > 0.3).mean() <= 0.7 and np.abs(out - a).mean() >= 15:
            break
    return _out(out)


# --- hold-out families: used for test only, so the test measures generalization beyond the generators seen in training ---

def smoke_plume(img, rng=None):
    """Wind-directed plume: a chain of growing gaussian puffs from a random origin."""
    a = np.asarray(img, dtype=np.float32)
    h, w = a.shape[:2]
    g = np.random.default_rng() if rng is None else rng
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    ox, oy = g.uniform(0.1, 0.9) * w, g.uniform(0.1, 0.9) * h
    ang = g.uniform(0, 2 * np.pi)
    alpha = np.zeros((h, w), np.float32)
    for i in range(8):
        d = i * 0.1 * w
        cx, cy = ox + d * np.cos(ang), oy + d * np.sin(ang)
        s = (0.05 + 0.025 * i) * w
        alpha = np.maximum(alpha, np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / (2 * s * s))) * (0.9 - 0.06 * i))
    gray = g.uniform(120, 180)
    return _out(_blend(a, [gray, gray, gray + 5], alpha))


def fog_valley(img, rng=None):
    """Fog pooled in the lower part of the tile, thinning upward."""
    a = np.asarray(img, dtype=np.float32)
    h = a.shape[0]
    g = np.random.default_rng() if rng is None else rng
    top = g.uniform(0.2, 0.6)
    alpha = np.repeat(np.linspace(0.1, 0.9, h)[:, None], a.shape[1], 1) * (1 - top) + top * 0.3
    return _out(_blend(a, [215, 218, 220], np.clip(alpha, 0, 1)))


def cloud_cumulus(img, rng=None):
    """Bright white cumulus patches with a soft shadow, instead of a dark overcast."""
    a = np.asarray(img, dtype=np.float32)
    n = _noise(*a.shape[:2], rng, cells=5)
    alpha = np.clip((n - 0.55) * 4, 0, 1)
    shadow = np.roll(alpha, 12, axis=(0, 1)) * 0.35
    a = a * (1 - shadow[..., None])
    return _out(_blend(a, [245, 247, 250], alpha * 0.9))
