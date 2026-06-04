import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

# Add parent and utils directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))

from utils.ood import is_ood
from utils.preprocess import preprocess_for_model
from config import Config

def test_ood_performance():
    print("=== SmokeSignal AI: OOD & Robustness Testing ===")
    
    # 1. Load Main Model
    model_path = Config.MODEL_PATH
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return
    
    model = load_model(model_path)
    print(f"Main model loaded from {model_path}")
    
    # 2. Setup Test Data
    test_dir = "data/test_ood"
    # Include report figures as OOD examples
    report_figures = [
        "reports/figures/class_distribution.png",
        "reports/figures/confusion_matrix.png"
    ]
    
    test_files = [os.path.join(test_dir, f) for f in os.listdir(test_dir)] + report_figures
    
    results = []
    
    print("\nRunning Predictions on Test Cases...")
    print(f"{'File':<30} | {'OOD Status':<10} | {'Scene Type':<20} | {'Wildfire Conf':<15}")
    print("-" * 85)
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            img = Image.open(file_path).convert('RGB')
            
            # Check OOD
            is_flagged, scene_type, ood_conf = is_ood(img)
            
            # Main Model Prediction
            x = preprocess_for_model(img, model.input_shape[1:])
            preds = model.predict(x, verbose=0)
            wildfire_conf = float(preds[0][0])
            
            status = "OOD ⚠️" if is_flagged else "ID ✅"
            
            print(f"{os.path.basename(file_path):<30} | {status:<10} | {scene_type[:20]:<20} | {wildfire_conf:>14.2%}")
            
            results.append({
                "file": os.path.basename(file_path),
                "is_ood": is_flagged,
                "scene": scene_type,
                "wildfire_conf": wildfire_conf
            })
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    # 3. Summary Analysis
    print("\n=== Summary ===")
    ood_count = sum(1 for r in results if r['is_ood'])
    print(f"Total images tested: {len(results)}")
    print(f"OOD detections: {ood_count}")
    print(f"ID (Satellite) detections: {len(results) - ood_count}")
    
    # Check for potential false positives/negatives in synthetic data
    print("\nFindings:")
    for r in results:
        if "wildfire" in r['file'] and not r['is_ood']:
            if r['wildfire_conf'] > 0.5:
                print(f"- Correctly identified wildfire in {r['file']}")
            else:
                print(f"- FAILED to identify wildfire in {r['file']} (Conf: {r['wildfire_conf']:.2%})")
        
        if r['is_ood']:
            print(f"- Successfully flagged OOD image: {r['file']} as {r['scene']}")

if __name__ == "__main__":
    test_ood_performance()
