import argparse
import copy
import os
from typing import Any, Dict, List

import yaml

from .exp.trainer import Trainer
from .algo.utils import update_nested_dict


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a hyperparameter sweep")
    parser.add_argument("--config", type=str, required=True, help="Path to the sweep YAML file")
    parser.add_argument(
        "--base_config",
        type=str,
        default="configs/default.yaml",
        help="Base config to merge with sweep overrides",
    )
    args = parser.parse_args()
    with open(args.config, "r", encoding="utf-8") as f:
        sweep_cfg = yaml.safe_load(f)
    with open(args.base_config, "r", encoding="utf-8") as f:
        base_cfg = yaml.safe_load(f)
    runs: List[Dict[str, Any]] = sweep_cfg.get("sweep", [])
    if not runs:
        print("No runs defined in sweep configuration")
        return
    os.makedirs("runs", exist_ok=True)
    for idx, run in enumerate(runs):
        run_name = run.get("name", f"run{idx}")
        overrides: Dict[str, Any] = run.get("overrides", {})
        cfg = copy.deepcopy(base_cfg)
        for k, v in overrides.items():
            update_nested_dict(cfg, k.split("."), v)
        exp_name = cfg.get("log", {}).get("experiment_name", "sweep") + f"_{run_name}"
        cfg.setdefault("log", {})["experiment_name"] = exp_name
        trainer = Trainer(cfg)
        print(f"Starting sweep run '{exp_name}'...")
        trainer.train()


if __name__ == "__main__":
    main()