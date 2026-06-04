"""
Generate synthetic OOD (Out-of-Distribution) test images for robustness testing.

Creates programmatic approximations of edge-case scenarios:
- Night/dark forest images
- Cloudy/smoky scenes
- Different geographic region appearances (desert, tropical, tundra)
- Low and high resolution variants
- Completely OOD images (non-satellite)

These are synthetic approximations since real satellite imagery for these
edge cases would need to be gathered from external sources.
"""

import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "ood_images")
np.random.seed(42)


def save_img(array, path):
    img = Image.fromarray((np.clip(array, 0, 1) * 255).astype(np.uint8))
    img.save(path)
    return path


def generate_night_dark_images():
    out = os.path.join(OUTPUT_DIR, "night_dark")
    os.makedirs(out, exist_ok=True)

    # 1. Very dark forest (near-black with slight green undertone)
    base = np.random.normal(0.03, 0.02, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.02  # slight green
    save_img(base, os.path.join(out, "night_forest_very_dark.png"))

    # 2. Night forest with faint moonlight patches
    base = np.random.normal(0.08, 0.03, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.04  # green tint
    # Add a faint bright patch (moonlight through canopy)
    base[20:35, 25:40, :] += 0.12
    save_img(base, os.path.join(out, "night_forest_moonlight.png"))

    # 3. Dark scene with small fire-like glow (simulating a campfire at night)
    base = np.random.normal(0.04, 0.02, (64, 64, 3)).astype(np.float32)
    # Small orange/warm glow in center
    cx, cy = 32, 32
    for i in range(64):
        for j in range(64):
            dist = np.sqrt((i - cx) ** 2 + (j - cy) ** 2)
            if dist < 8:
                warmth = max(0, 0.5 * (1 - dist / 8))
                base[i, j, 0] += warmth * 0.8
                base[i, j, 1] += warmth * 0.3
                base[i, j, 2] += warmth * 0.05
    save_img(base, os.path.join(out, "night_fire_glow.png"))

    # 4. Pitch black satellite view (sensor failure / no moon)
    base = np.random.normal(0.01, 0.005, (64, 64, 3)).astype(np.float32)
    save_img(base, os.path.join(out, "pitch_black_sensor.png"))

    # 5. Night with scattered tiny lights (human settlement at night)
    base = np.random.normal(0.03, 0.01, (64, 64, 3)).astype(np.float32)
    for _ in range(8):
        x, y = np.random.randint(5, 59), np.random.randint(5, 59)
        base[x - 1 : x + 2, y - 1 : y + 2, 0] += 0.4
        base[x - 1 : x + 2, y - 1 : y + 2, 1] += 0.35
        base[x - 1 : x + 2, y - 1 : y + 2, 2] += 0.2
    save_img(base, os.path.join(out, "night_settlement_lights.png"))

    # Also create higher-res versions for resolution testing
    for name in ["night_forest_very_dark.png", "night_fire_glow.png"]:
        img = Image.open(os.path.join(out, name))
        # Create 256x256 version
        img_large = img.resize((256, 256), Image.BILINEAR)
        img_large.save(os.path.join(out, name.replace(".png", "_256.png")))
        # Create 16x16 version
        img_tiny = img.resize((16, 16), Image.BILINEAR)
        img_tiny.save(os.path.join(out, name.replace(".png", "_16.png")))

    print(f"  Generated {len(os.listdir(out))} night/dark images")


def generate_cloudy_smoky_images():
    out = os.path.join(OUTPUT_DIR, "cloudy_smoky")
    os.makedirs(out, exist_ok=True)

    # 1. Heavy cloud cover (white/gray patches over green/brown terrain)
    base = np.random.normal(0.3, 0.05, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.1  # base green terrain
    # Add cloud overlay
    cloud = np.random.normal(0.7, 0.15, (64, 64, 3)).astype(np.float32)
    cloud_mask = np.random.random((64, 64, 1)) > 0.4
    base = np.where(cloud_mask, cloud, base)
    save_img(base, os.path.join(out, "heavy_cloud_cover.png"))

    # 2. Thin smoke haze (overall desaturated/washed out)
    base = np.random.normal(0.4, 0.05, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] += 0.15  # reddish-brown tint from smoke
    base[:, :, 1] += 0.08
    base = np.clip(base + np.random.normal(0, 0.03, base.shape), 0, 1)
    save_img(base, os.path.join(out, "thin_smoke_haze.png"))

    # 3. Dense smoke plume (localized thick gray/white area)
    base = np.random.normal(0.25, 0.04, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.08  # forest base
    # Dense smoke in upper portion
    smoke_intensity = np.zeros((64, 64, 1), dtype=np.float32)
    for i in range(64):
        for j in range(64):
            dist_from_source = np.sqrt((i - 50) ** 2 + (j - 32) ** 2)
            if dist_from_source < 25:
                smoke_intensity[i, j, 0] = 0.6 * max(0, 1 - dist_from_source / 25)
    smoke_color = np.array([0.7, 0.68, 0.65]).reshape(1, 1, 3)
    base = base * (1 - smoke_intensity) + smoke_color * smoke_intensity
    save_img(base, os.path.join(out, "dense_smoke_plume.png"))

    # 4. Cloud shadow on terrain (dark patches that could mimic fire scars)
    base = np.random.normal(0.35, 0.05, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.1  # green terrain
    # Dark shadow patches
    for _ in range(3):
        x, y = np.random.randint(10, 50), np.random.randint(10, 50)
        r = np.random.randint(5, 15)
        for i in range(max(0, x - r), min(64, x + r)):
            for j in range(max(0, y - r), min(64, y + r)):
                if np.sqrt((i - x) ** 2 + (j - y) ** 2) < r:
                    base[i, j] *= 0.4
    save_img(base, os.path.join(out, "cloud_shadows_terrain.png"))

    # 5. Smoky sunset (reddish sky with smoke)
    base = np.random.normal(0.4, 0.06, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] += 0.25  # heavy red
    base[:, :, 1] += 0.05
    base[:, :, 2] -= 0.05
    # Add some gray smoke wisps
    for _ in range(5):
        x, y = np.random.randint(5, 59), np.random.randint(5, 59)
        base[x - 2 : x + 3, y - 2 : y + 3, :] += 0.15
    save_img(base, os.path.join(out, "smoky_sunset.png"))

    print(f"  Generated {len(os.listdir(out))} cloudy/smoky images")


def generate_different_geography_images():
    out = os.path.join(OUTPUT_DIR, "different_geography")
    os.makedirs(out, exist_ok=True)

    # 1. Desert/arid terrain (sandy, very little vegetation)
    base = np.random.normal(0.6, 0.06, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] += 0.1  # sandy red
    base[:, :, 1] += 0.05  # some yellow
    base[:, :, 2] -= 0.05  # low blue
    save_img(base, os.path.join(out, "desert_arid_terrain.png"))

    # 2. Tropical dense forest (very green, high saturation)
    base = np.random.normal(0.2, 0.04, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.25  # heavy green
    base[:, :, 0] -= 0.03  # low red
    save_img(base, os.path.join(out, "tropical_dense_forest.png"))

    # 3. Tundra/snow-covered terrain (white/blue-gray)
    base = np.random.normal(0.75, 0.06, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] -= 0.03  # slight blue tint
    base[:, :, 2] += 0.05
    save_img(base, os.path.join(out, "tundra_snow_cover.png"))

    # 4. Australian outback (reddish-brown terrain)
    base = np.random.normal(0.4, 0.05, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] += 0.2  # strong red
    base[:, :, 1] += 0.03
    base[:, :, 2] -= 0.08
    save_img(base, os.path.join(out, "australian_outback.png"))

    # 5. Amazon rainforest (dark green with river)
    base = np.random.normal(0.15, 0.03, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.2  # dense green
    # Add a winding river (brown/tan)
    for i in range(64):
        river_x = int(32 + 10 * np.sin(i * 0.15))
        if 0 <= river_x < 64:
            base[i, max(0, river_x - 2) : min(64, river_x + 3), 0] += 0.3
            base[i, max(0, river_x - 2) : min(64, river_x + 3), 1] += 0.2
            base[i, max(0, river_x - 2) : min(64, river_x + 3), 2] += 0.05
    save_img(base, os.path.join(out, "amazon_rainforest_river.png"))

    # 6. Siberian taiga (mixed green and sparse snow)
    base = np.random.normal(0.35, 0.06, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.12
    # Scattered snow patches
    snow_mask = np.random.random((64, 64, 1)) > 0.7
    snow_color = np.array([0.8, 0.82, 0.85]).reshape(1, 1, 3)
    base = np.where(snow_mask, snow_color, base)
    save_img(base, os.path.join(out, "siberian_taiga_snow.png"))

    # 7. California chaparral (golden-brown dry vegetation)
    base = np.random.normal(0.4, 0.05, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] += 0.15  # golden
    base[:, :, 1] += 0.1
    base[:, :, 2] -= 0.05
    save_img(base, os.path.join(out, "california_chaparral.png"))

    print(f"  Generated {len(os.listdir(out))} different geography images")


def generate_resolution_variant_images():
    out = os.path.join(OUTPUT_DIR, "low_resolution")
    os.makedirs(out, exist_ok=True)
    out_hi = os.path.join(OUTPUT_DIR, "high_resolution")
    os.makedirs(out_hi, exist_ok=True)

    # Create a base "forest with fire" image at 64x64
    base = np.random.normal(0.3, 0.05, (64, 64, 3)).astype(np.float32)
    base[:, :, 1] += 0.1  # green
    # Add fire-like area
    base[25:40, 25:40, 0] += 0.4
    base[25:40, 25:40, 1] += 0.15
    base[25:40, 25:40, 2] -= 0.1
    base_64 = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8))

    # Low resolution variants
    for size, label in [(8, "8x8"), (16, "16x16"), (32, "32x32")]:
        img_small = base_64.resize((size, size), Image.BILINEAR)
        # Upscale back to 64x64 (simulates what model sees after preprocessing)
        img_back = img_small.resize((64, 64), Image.BILINEAR)
        img_back.save(os.path.join(out, f"forest_fire_{label}_upscaled.png"))
        # Also save at native tiny size
        img_small.save(os.path.join(out, f"forest_fire_{label}_native.png"))

    # Non-fire low-res variants
    base_nofire = np.random.normal(0.3, 0.05, (64, 64, 3)).astype(np.float32)
    base_nofire[:, :, 1] += 0.12
    base_nofire_64 = Image.fromarray((np.clip(base_nofire, 0, 1) * 255).astype(np.uint8))

    for size, label in [(8, "8x8"), (16, "16x16"), (32, "32x32")]:
        img_small = base_nofire_64.resize((size, size), Image.BILINEAR)
        img_back = img_small.resize((64, 64), Image.BILINEAR)
        img_back.save(os.path.join(out, f"forest_nofire_{label}_upscaled.png"))

    # High resolution variants (simulates high-res satellite imagery downscaled)
    base_large = np.random.normal(0.3, 0.05, (512, 512, 3)).astype(np.float32)
    base_large[:, :, 1] += 0.1
    base_large[200:320, 200:320, 0] += 0.4
    base_large[200:320, 200:320, 1] += 0.15
    base_large[200:320, 200:320, 2] -= 0.1
    img_large = Image.fromarray((np.clip(base_large, 0, 1) * 255).astype(np.uint8))
    img_large.save(os.path.join(out_hi, "forest_fire_512x512.png"))

    # High-res no fire
    base_large_nf = np.random.normal(0.3, 0.05, (512, 512, 3)).astype(np.float32)
    base_large_nf[:, :, 1] += 0.12
    img_large_nf = Image.fromarray((np.clip(base_large_nf, 0, 1) * 255).astype(np.uint8))
    img_large_nf.save(os.path.join(out_hi, "forest_nofire_512x512.png"))

    # Very high resolution with fine detail (1024x1024)
    base_vh = np.random.normal(0.3, 0.04, (1024, 1024, 3)).astype(np.float32)
    base_vh[:, :, 1] += 0.1
    # Fine-grained fire pixels
    for i in range(400, 600):
        for j in range(400, 600):
            if np.random.random() > 0.5:
                base_vh[i, j, 0] += 0.4
                base_vh[i, j, 1] += 0.15
    img_vh = Image.fromarray((np.clip(base_vh, 0, 1) * 255).astype(np.uint8))
    img_vh.save(os.path.join(out_hi, "fine_detail_fire_1024x1024.png"))

    print(f"  Generated {len(os.listdir(out))} low-resolution images")
    print(f"  Generated {len(os.listdir(out_hi))} high-resolution images")


def generate_completely_ood_images():
    out = os.path.join(OUTPUT_DIR, "completely_ood")
    os.makedirs(out, exist_ok=True)

    # 1. Indoor scene (warm indoor lighting)
    base = np.random.normal(0.5, 0.08, (64, 64, 3)).astype(np.float32)
    base[:, :, 0] += 0.1  # warm
    base[:, :, 2] -= 0.05
    save_img(base, os.path.join(out, "indoor_scene_warm.png"))

    # 2. Text/document (mostly white with dark regions)
    base = np.ones((64, 64, 3), dtype=np.float32) * 0.9
    # Simulate text lines
    for i in range(5, 60, 8):
        base[i : i + 2, 5:59, :] = 0.1
    save_img(base, os.path.join(out, "document_text.png"))

    # 3. City/urban (grid-like pattern)
    base = np.random.normal(0.4, 0.05, (64, 64, 3)).astype(np.float32)
    # Grid streets
    for i in range(0, 64, 8):
        base[i : i + 2, :, :] = 0.6
    for j in range(0, 64, 8):
        base[:, j : j + 2, :] = 0.6
    save_img(base, os.path.join(out, "urban_grid.png"))

    # 4. Human face (skin-tone oval)
    base = np.random.normal(0.3, 0.03, (64, 64, 3)).astype(np.float32)
    cx, cy = 32, 32
    for i in range(64):
        for j in range(64):
            if ((i - cx) / 14) ** 2 + ((j - cy) / 10) ** 2 < 1:
                base[i, j] = [0.7, 0.5, 0.35]
    save_img(base, os.path.join(out, "face_like_oval.png"))

    # 5. Solid color (uniform)
    base = np.ones((64, 64, 3), dtype=np.float32) * 0.5
    save_img(base, os.path.join(out, "solid_gray.png"))

    # 6. Random noise (sensor noise / corrupted)
    base = np.random.random((64, 64, 3)).astype(np.float32)
    save_img(base, os.path.join(out, "random_noise.png"))

    # 7. Gradient (smooth transition)
    base = np.zeros((64, 64, 3), dtype=np.float32)
    for i in range(64):
        base[i, :, 0] = i / 63.0
        base[:, i, 1] = i / 63.0
    save_img(base, os.path.join(out, "color_gradient.png"))

    print(f"  Generated {len(os.listdir(out))} completely OOD images")


def main():
    print("Generating synthetic OOD test images...")
    print("=" * 50)
    generate_night_dark_images()
    generate_cloudy_smoky_images()
    generate_different_geography_images()
    generate_resolution_variant_images()
    generate_completely_ood_images()
    print("=" * 50)
    print("Done! All OOD test images generated in tests/ood_images/")


if __name__ == "__main__":
    main()
