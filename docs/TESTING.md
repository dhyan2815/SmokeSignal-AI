# SmokeSignal-AI Beta Testing Report

This report summarizes the feedback and results collected during the initial beta testing phase of **SmokeSignal-AI**. The goal of this phase was to evaluate model accuracy on real-world inputs, verify user interface responsiveness, and gather feature suggestions from a group of external testers.

---

## 1. Methodology
- **Timeline:** June 5 – June 6, 2026
- **Participants:** 6 beta testers (friends and external reviewers)
- **Deployment Platform:** Web App UI (Streamlit/Python)
- **Feedback Collection:** Structured Google Form + Google Sheets CSV integration
- **Test Cases:** Testers uploaded a variety of images, including actual wildfires, clear skies, and challenging edge cases (clouds, fog, and sunset scenes).

---

## 2. Quantitative Results

### User Interface & Responsiveness
- **Responsiveness Rating (Scale 1–5):** **5.0 / 5.0** (100% of testers rated the UI's ease of use and speed as 5/5)
- **Overall Experience Rating (Scale 1–5):** **4.83 / 5.0** (5 out of 6 rated 5/5, 1 rated 4/5)

### Model Prediction Accuracy
- **Wildfire/Smoke Images (3 tested):** **100% Accuracy** (3/3 correctly identified as containing wildfire/smoke)
- **Other/Edge Case Images (3 tested):** **33% Accuracy** (1/3 correctly identified; 2/3 resulted in false positives/errors)
  - *Success Case:* Correctly identified a non-conventional, close-up image of fire (not standard satellite imagery).
  - *Failure Case 1 (Sunset):* A sunset cloud scene false-alarmed as containing a wildfire (model output showed 33% for dark monsoon clouds but ultimately flagged a wildfire hazard due to red/orange hues).
  - *Failure Case 2 (Non-Wildfire Image):* A non-wildfire landscape image false-alarmed as containing a wildfire.

---

## 3. Findings: What Worked vs. What Didn't

### What Worked
- **High-Quality UI/UX:** Testers praised the clean, intuitive, and responsive layout of the application.
- **Clear Wildfire Identification:** Standard wildfire and smoke satellite images were recognized accurately with zero delay.
- **Robustness on Out-of-Distribution Fire Close-ups:** The model correctly handled close-up fire images that were outside the primary satellite dataset's style.

### What Didn't Work (Model Limitations)
- **Sunset False Alarms:** The model is highly sensitive to red, orange, and golden hues typical of sunset and sunrise skies, misinterpreting them as active wildfires.
- **Cloud/Fog Sensitivity:** Differentiating dark monsoon clouds and thick fog from actual smoke plumes remains a key area for model refinement.

---

## 4. User Suggestions & Future Roadmap

Based on the feedback, we have categorized planned improvements into two main areas. These will be addressed after Issue #10 is closed.

### Model & Detection Enhancements
1. **Distinguish Sunsets from Fire:** Retrain or fine-tune the model with a dataset including sunset and sunrise scenes to reduce false alarms.
2. **Granular Classification:** Transition from a monolithic/binary classification model to a multi-class model that classifies smoke, clouds, and fog separately.

### Platform & UI Features
1. **Location & Map Integration:** Add map functionality to display the coordinates or region of the detected fire.
2. **Notification Pipeline (Email + SMS):** Integrate real-time alerting systems (e.g., SMTP or Twilio API) to send automated alerts when wildfire is detected.
3. **Database Logs:** Save all detection records, timestamps, and confidence scores into a persistent database (e.g., SQLite/PostgreSQL) for history tracking.
4. **Emergency Contact Trigger:** Integrate a one-click button to contact local fire departments or emergency services with the location data.
