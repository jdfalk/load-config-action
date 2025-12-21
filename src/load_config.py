#!/usr/bin/env python3
# file: src/load_config.py
# version: 1.0.0
# guid: 5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b

"""Load and parse .github/repository-config.yml for GitHub Actions."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("::notice::Installing PyYAML...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "PyYAML"])
    import yaml


def write_output(name: str, value: str) -> None:
    """Write to GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            # Handle multiline outputs
            if "\n" in str(value):
                delimiter = "EOF"
                f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
            else:
                f.write(f"{name}={value}\n")


def write_summary(text: str) -> None:
    """Write to GITHUB_STEP_SUMMARY."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def main() -> None:
    """Load and parse repository configuration."""
    config_file = Path(os.environ.get("CONFIG_FILE", ".github/repository-config.yml"))
    fail_on_missing = os.environ.get("FAIL_ON_MISSING", "false").lower() == "true"

    print(f"Loading config from: {config_file.absolute()}")

    # Check if file exists
    if not config_file.exists():
        write_output("has-config", "false")
        write_output("config", "{}")
        write_output("raw-yaml", "")

        msg = f"⚠️ Config file not found: `{config_file}`"
        print(f"::warning::{msg} (using defaults)")
        write_summary(msg)

        if fail_on_missing:
            print(f"::error::Config file required but not found: {config_file}")
            sys.exit(1)
        else:
            sys.exit(0)

    # Read and parse YAML
    try:
        raw_content = config_file.read_text(encoding="utf-8")
        data = yaml.safe_load(raw_content) or {}

        write_output("has-config", "true")
        write_output("config", json.dumps(data, separators=(",", ":")))
        write_output("raw-yaml", raw_content)

        summary = f"✅ Loaded config from `{config_file}`"
        print(summary)
        write_summary(summary)

        if data:
            keys = list(data.keys())
            write_summary(
                f"\n**Config sections:** {', '.join(f'`{k}`' for k in keys)}"
            )
            print(f"Config sections: {', '.join(keys)}")

    except yaml.YAMLError as e:
        write_output("has-config", "false")
        write_output("config", "{}")
        write_output("raw-yaml", "")

        error_msg = f"Failed to parse YAML: {e}"
        print(f"::error::{error_msg}")
        write_summary(f"❌ {error_msg}")

        if fail_on_missing:
            sys.exit(1)
        else:
            sys.exit(0)
    except Exception as e:
        write_output("has-config", "false")
        write_output("config", "{}")
        write_output("raw-yaml", "")

        error_msg = f"Unexpected error: {e}"
        print(f"::error::{error_msg}")
        write_summary(f"❌ {error_msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
