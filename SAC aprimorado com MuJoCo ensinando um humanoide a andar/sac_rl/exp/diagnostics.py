from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd
from tensorboard.backend.event_processing import event_accumulator


def _safe_tag(tag: str) -> str:
    return tag.replace("/", "_").replace(" ", "_")

def export_plots(run_dir: str, output_dir: str) -> None:
    if not os.path.exists(run_dir):
        raise FileNotFoundError(f"Run directory '{run_dir}' does not exist")
    os.makedirs(output_dir, exist_ok=True)
    event_files = [
        os.path.join(run_dir, f)
        for f in os.listdir(run_dir)
        if f.startswith("events.out.tfevents")
    ]
    if not event_files:
        raise RuntimeError(f"No tensorboard event files found in {run_dir}")
    ea = event_accumulator.EventAccumulator(run_dir)
    ea.Reload()
    for tag in ea.Tags().get("scalars", []):
        events = ea.Scalars(tag)
        steps = [e.step for e in events]
        values = [e.value for e in events]
        df = pd.DataFrame({"step": steps, tag: values})
        safe = _safe_tag(tag)
        csv_path = os.path.join(output_dir, f"{safe}.csv")
        df.to_csv(csv_path, index=False)
        plt.figure()
        plt.plot(steps, values)
        plt.xlabel("Step")
        plt.ylabel(tag)
        plt.title(tag)
        plt.tight_layout()
        png_path = os.path.join(output_dir, f"{safe}.png")
        plt.savefig(png_path)
        plt.close()