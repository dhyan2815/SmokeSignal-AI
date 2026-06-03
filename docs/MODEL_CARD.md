# Model Card — SmokeSignal AI Wildfire Detector

**Model version:** 1.0.0  
**Date:** 2026-06-03  
**Model type:** Binary image classification CNN

---

## Model Architecture

| Property         | Detail |
|------------------|--------|
| Architecture     | Sequential CNN |
| Input size       | 64 × 64 × 3 (RGB) |
| Layers           | Conv2D(32) → MaxPool → Conv2D(64) → MaxPool → Flatten → Dense(128) → Dropout(0.5) → Dense(1) |
| Activation       | ReLU (hidden), Sigmoid (output) |
| Total params     | 4,875,845 |
| Trainable params | 1,625,281 |
| Loss function    | Binary Crossentropy |
| Optimizer        | Adam |
| Framework        | TensorFlow / Keras |

---

## Training Details

| Property       | Value |
|----------------|-------|
| Dataset        | [Wildfire Prediction Dataset](https://www.kaggle.com/datasets/abdelghaniaaba/wildfire-prediction-dataset) (Kaggle) |
| Image source   | Satellite tiles (geotagged, Canada regions) |
| Training split | 30,250 images |
| Validation split | 6,300 images |
| Test split     | 6,300 images |
| Epochs         | 5 |
| Batch size     | 32 |
| Data augmentation | None (rescale 1/255 only) |
| Hardware       | Google Colab (GPU) |
| Training time  | ~17 min (5 epochs) |

---

## Performance

### Test Set

| Metric     | Score  |
|------------|--------|
| Accuracy   | 96.06% |
| Precision  | 96.09% |
| Recall     | 96.81% |
| F1-Score   | 96.45% |
| AUC-ROC    | 99.21% |

### Confusion Matrix (Test)

```
             Pred No Fire    Pred Fire
Actual No Fire   2,683          137
Actual Fire        111        3,369
```

- **FPR** (false alarm rate): 4.86%
- **FNR** (missed fire rate): 3.19%

---

## Known Limitations

| Limitation | Description |
|------------|-------------|
| **Low resolution** | 64×64 tiles may miss small/early-stage fires occupying few pixels |
| **Geographic bias** | Trained on Canada satellite tiles only; performance may degrade in other biomes (deserts, tropics) |
| **No temporal context** | Single-frame inference only; no multi-temporal change detection |
| **Weather artefacts** | Clouds, cloud shadows, and haze can produce false positives |
| **Augmentation gap** | No augmentation used; model may be less robust to rotation/flip/illumination variance |

---

## Intended Use

- **Primary:** Real-time wildfire detection from satellite imagery streams.
- **Secondary:** Early warning flagging for human review before dispatching resources.
- **Out of scope:** Predicting fire spread, severity, or behaviour.

---

## Fairness & Bias Notes

- The dataset is geographically concentrated in Canada (latitudes ~43–49°N, longitudes ~73–80°W). Performance on other regions (Amazon, Australia, California, Siberia) is untested.
- Class distribution is roughly balanced (52% wildfire, 48% no wildfire), so no significant label-bias is expected.
- No demographic or human-centric data is involved; the model operates on geospatial satellite imagery.

---

## Maintainance

- Model file: `/content/wildfire_detector_model.keras` (~18 MB)
- Retraining should be considered when expanding to new geographies or if target accuracy drops below 92%.
- Monitor FNR (missed fires) as the primary production metric — a missed detection is more costly than a false alarm.