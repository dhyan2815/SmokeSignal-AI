import numpy as np
import time
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

MODEL_PATH = "model/wildfire_detector_model.keras"
IMAGE_PATH = "test_image.jpg"
BATCH_SIZES = [1, 4, 8, 16]
NUM_ITERATIONS = 100

def create_dummy_image():
    img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    return img

def preprocess_batch(images, target_size=(64, 64)):
    processed = []
    for img in images:
        img_array = img.astype(np.float32) / 255.0
        processed.append(img_array)
    return np.array(processed)

def run_benchmark(model, batch_size, num_iterations=NUM_ITERATIONS):
    timings = []
    
    for _ in range(num_iterations):
        dummy_images = [create_dummy_image() for _ in range(batch_size)]
        x = preprocess_batch(dummy_images)
        
        start = time.perf_counter()
        _ = model.predict(x, verbose=0)
        end = time.perf_counter()
        
        timings.append(end - start)
    
    timings = np.array(timings)
    
    return {
        "batch_size": batch_size,
        "iterations": num_iterations,
        "mean_ms": float(timings.mean() * 1000),
        "std_ms": float(timings.std() * 1000),
        "min_ms": float(timings.min() * 1000),
        "max_ms": float(timings.max() * 1000),
        "p50_ms": float(np.percentile(timings, 50) * 1000),
        "p95_ms": float(np.percentile(timings, 95) * 1000),
        "p99_ms": float(np.percentile(timings, 99) * 1000),
        "throughput_imgs_per_sec": batch_size / timings.mean()
    }

def main():
    print("Loading model...")
    model = load_model(MODEL_PATH)
    print(f"Model loaded: {MODEL_PATH}")
    print(f"Input shape: {model.input_shape}")
    print(f"Output shape: {model.output_shape}")
    print(f"\nRunning benchmark with {NUM_ITERATIONS} iterations per batch size...")
    print("-" * 80)
    
    results = []
    for bs in BATCH_SIZES:
        print(f"\nTesting batch_size={bs}...")
        result = run_benchmark(model, bs, NUM_ITERATIONS)
        results.append(result)
        print(f"  Mean: {result['mean_ms']:.2f}ms | P95: {result['p95_ms']:.2f}ms | Throughput: {result['throughput_imgs_per_sec']:.1f} imgs/s")
    
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)
    print(f"{'Batch':<8} {'Mean':<10} {'Std':<10} {'P50':<10} {'P95':<10} {'P99':<10} {'Throughput':<15}")
    print("-" * 80)
    for r in results:
        print(f"{r['batch_size']:<8} {r['mean_ms']:<10.2f} {r['std_ms']:<10.2f} {r['p50_ms']:<10.2f} {r['p95_ms']:<10.2f} {r['p99_ms']:<10.2f} {r['throughput_imgs_per_sec']:<15.1f}")
    
    print("\n" + "=" * 80)
    print("SYSTEM INFO")
    print("=" * 80)
    import platform
    print(f"Platform: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    try:
        import tensorflow as tf
        print(f"TensorFlow: {tf.__version__}")
        print(f"GPU: {len(tf.config.list_physical_devices('GPU'))} available")
    except:
        pass

if __name__ == "__main__":
    main()