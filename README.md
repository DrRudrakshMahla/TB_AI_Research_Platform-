---
title: TB AI Research Platform
emoji: "🩺"
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "5.34.2"
python_version: "3.10"
app_file: app.py
pinned: false
---

# TB AI Research Platform

AI-powered Tuberculosis Chest X-ray Detection using DenseNet121.# TB AI Research Platform v3.0

## Sprint 1

### Features
- DenseNet121 TB classifier
- Native-resolution Grad-CAM
- Single image analysis
- PDF report
- JSON export
- Modular architecture

## Folder Structure

```
ai/
controllers/
core/
explainability/
preprocessing/
reports/
ui/
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

or

```bash
python launch.py
```

## Hugging Face

- SDK: Gradio
- Python: 3.10+
- Place `TB_AI_Final_Model.pth` inside the `models/` directory.

## Roadmap

### Sprint 1
- Single image inference
- Grad-CAM
- PDF
- JSON

### Sprint 2
- Lung segmentation
- Image quality assessment

### Sprint 3
- DICOM
- Batch analysis
- Multi-model consensus
