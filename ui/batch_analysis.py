
"""
ui/batch_analysis.py
Version 4 (starter)
HF Spaces compatible
"""

from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path

import gradio as gr
import pandas as pd
from openpyxl import Workbook
import matplotlib.pyplot as plt

from ai.batch_inference import BatchInference
from ai.batch_statistics import BatchStatistics


class BatchAnalysisUI:

    def __init__(self, model_path: str, device):
        self.engine = BatchInference(model_path, device)

    def _prepare_folder(self, images, zip_file):
        work = Path(tempfile.mkdtemp())
        folder = work / "images"
        folder.mkdir()

        if images:
            for f in images:
                src = Path(f)
                (folder / src.name).write_bytes(src.read_bytes())
        elif zip_file:
            with zipfile.ZipFile(zip_file, "r") as z:
                z.extractall(folder)
        else:
            raise gr.Error("Upload images or a ZIP dataset.")

        return work, folder

    def analyze(self, images, zip_file):
        work, folder = self._prepare_folder(images, zip_file)

        results, _ = self.engine.predict_folder(folder)
        summary = BatchStatistics.summarize(results)

        rows = []
        for r in results:
            rows.append([
                r.filename,
                r.prediction,
                round(r.probability, 4),
                round(r.confidence, 4),
            ])

        df = pd.DataFrame(
            rows,
            columns=["Filename", "Prediction", "Probability", "Confidence"],
        )

        csv_file = work / "results.csv"
        df.to_csv(csv_file, index=False)

        wb = Workbook()
        ws = wb.active
        ws.append(list(df.columns))
        for row in df.itertuples(index=False):
            ws.append(list(row))
        xlsx = work / "results.xlsx"
        wb.save(xlsx)

        json_file = work / "results.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": summary,
                    "results": BatchStatistics.to_json(results),
                },
                f,
                indent=2,
            )

        fig = plt.figure(figsize=(4,4))
        plt.pie(
            [summary["tuberculosis_cases"], summary["normal_cases"]],
            labels=["TB", "Normal"],
            autopct="%1.0f%%",
        )
        pie = work / "pie.png"
        plt.savefig(pie, dpi=150, bbox_inches="tight")
        plt.close(fig)

        md = f"""# Batch Summary

- Total Cases: **{summary['total_cases']}**
- Tuberculosis: **{summary['tuberculosis_cases']}**
- Normal: **{summary['normal_cases']}**
- Average Confidence: **{summary['average_confidence']:.3f}**
"""

        return md, df, str(pie), str(csv_file), str(xlsx), str(json_file)

    def build(self):
        gr.Markdown("## Batch Analysis v4")

        images = gr.File(
            label="Upload Chest X-rays",
            file_count="multiple",
            file_types=["image"],
        )

        zip_file = gr.File(
            label="OR Upload ZIP Dataset",
            file_count="single",
            file_types=[".zip"],
        )

        run = gr.Button("Run Batch Analysis", variant="primary")

        summary = gr.Markdown()
        table = gr.Dataframe(interactive=False)
        pie = gr.Image(label="TB vs Normal")
        csv = gr.File(label="CSV")
        excel = gr.File(label="Excel")
        jsn = gr.File(label="JSON")

        run.click(
            self.analyze,
            inputs=[images, zip_file],
            outputs=[summary, table, pie, csv, excel, jsn],
        )