"""
reports/pdf_report.py
Complete replacement
"""
from __future__ import annotations
from pathlib import Path
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class PDFReport:
    @staticmethod
    def _safe(obj,name,default="N/A"):
        return getattr(obj,name,default)
    @staticmethod
    def save(result, output_path:str|Path)->Path:
        output_path=Path(output_path)
        output_path.parent.mkdir(parents=True,exist_ok=True)
        styles=getSampleStyleSheet()
        story=[Paragraph("TB AI Research Platform",styles["Title"]),Spacer(1,12)]
        fields=[
            ("Prediction",PDFReport._safe(result,"prediction")),
            ("Probability",f"{PDFReport._safe(result,'probability',0):.4f}"),
            ("Confidence",f"{PDFReport._safe(result,'confidence',0):.4f}"),
            ("Risk Level",PDFReport._safe(result,"risk_level")),
            ("AI Findings",PDFReport._safe(result,"ai_findings")),
            ("AI Impression",PDFReport._safe(result,"ai_impression")),
            ("Model",PDFReport._safe(result,"model_name")),
            ("Version",PDFReport._safe(result,"model_version")),
            ("Inference Time",f"{PDFReport._safe(result,'inference_time',0):.4f} s"),
        ]
        for k,v in fields:
            story.append(Paragraph(f"<b>{k}:</b> {v}",styles["BodyText"]))
            story.append(Spacer(1,6))
        doc=SimpleDocTemplate(str(output_path))
        doc.build(story)
        return output_path