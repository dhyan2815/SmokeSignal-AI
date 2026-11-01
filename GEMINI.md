# GEMINI Memory State

## Changelog

### 2026-11-01
- Issue #12 (branch `feat/12-multiclass-false-positive-reduction`): added 5-class pipeline (`src/curate_dataset.py`, `src/synth.py`, `src/train_multiclass.py`, `src/evaluate_multiclass.py`, `src/ingest_external.py`, `tests/eval_edge_cases.py`). Run 1 failed gates (recall 85.6%); data-layer fixes (smoke label noise, hold-out generator families, real IGNIS eval set) documented in `docs/ISSUE12_RETRAIN_RUNBOOK.md`.

### 2026-06-22
- Explained the concept of Out-of-Distribution (OOD) data, providing examples from the project and detailing the MobileNetV2 keyword-matching mechanism used in SmokeSignal-AI.

### 2026-06-21
- Created `docs/INTERVIEW_QNA_SPECIFIC.md` containing targeted, conversational, and technical answers for the eight core interview questions about SmokeSignal-AI.

### 2026-06-20
- Created `docs/INTERVIEW_PREP.md` containing structured Q&As tailored for a fresher AI/ML developer, covering the model architecture, image preprocessing, OOD detection, robustness failures (black images, sunsets), and system deployment/feedback mechanisms.

### 2026-06-07
- Completed task 6 of issue #10: Deployment/Monitoring Strategy.
- Created `docs/DEPLOYMENT.md` documenting Streamlit Community Cloud hosting, Gmail SMTP alert configuration (App Passwords), local/cloud deployment steps, console-based logging strategy, and live demo link.

### 2026-06-06
- Completed task 5 of issue #10: User Testing/Feedback Documentation.
- Created `docs/TESTING.md` analyzing 6 beta testing responses from Google Forms.
- Documented findings, UI responsiveness metrics, model false alarms (sunsets, non-wildfire images), and future roadmap items based on user suggestions.

### 2026-06-04
- Completed task 4 of issue #10: Robustness & OOD Testing.
- Created `tests/test_ood.py` for automated edge case testing.
- Generated synthetic test data in `data/test_ood`.
- Documented findings in `notebooks/OOD_ROBUSTNESS_REPORT.ipynb`, identifying a critical robustness issue with dark/black images and gaps in OOD scene classification.

### 2026-05-27
- Removed the "Model Development Pipeline" section from `README.md` as the architecture is now fully detailed using various diagrams in the "Technical Architecture" section.

### 2026-05-26
- Added architecture diagrams (`activity_diagram.png`, `sequence_diagram.png`, `dfd_diagram.png`, `er_diagram.png`) to the `README.md` file under the "Technical Architecture" section using expanding details blocks.
