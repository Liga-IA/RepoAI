import argparse
import os
from typing import Any, Dict

import yaml

from .exp.trainer import Trainer
from .algo.utils import update_nested_dict


def parse_overrides(overrides: list[str]) -> Dict[str, Any]:
    parsed: Dict[str, Any] = {}
    for ov in overrides:
        if "=" not in ov:
            continue
        key, value = ov.split("=", 1)
        if value.lower() in {"true", "false"}:
            val: Any = value.lower() == "true"
        else:
            try:
                val = int(value)
            except ValueError:
                try:
                    val = float(value)
                except ValueError:
                    val = value
        update_nested_dict(parsed, key.split("."), val)
    return parsed


def merge_config(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for k, v in overrides.items():
        if isinstance(v, dict) and k in result and isinstance(result[k], dict):
            result[k] = merge_config(result[k], v)
        else:
            result[k] = v
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Train an SAC agent")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default.yaml",
        help="Path to a YAML config file",
    )
    parser.add_argument(
        "overrides",
        type=str,
        nargs="*",
        help="List of key=value pairs to override config entries (dot‑notation)",
    )
    args = parser.parse_args()
    with open(args.config, "r", encoding="utf-8") as f:
        cfg: Dict[str, Any] = yaml.safe_load(f)
    override_dict = parse_overrides(args.overrides or [])
    cfg = merge_config(cfg, override_dict)
    os.makedirs("runs", exist_ok=True)
    trainer = Trainer(cfg)
    trainer.train()


if __name__ == "__main__":
    main()