#!/bin/bash
set -euo pipefail

python3 <<'PY'
import json
from collections import defaultdict
from pathlib import Path

INPUT_PATH = Path("/app/input.txt")
OUTPUT_PATH = Path("/app/output.json")

windows_by_service: dict[str, list[tuple[int, int]]] = defaultdict(list)

for entry in json.loads(INPUT_PATH.read_text(encoding="utf-8")):
    if entry["status"] == "approved":
        windows_by_service[entry["service"]].append(
            (entry["start_minute"], entry["end_minute"])
        )

report = []
for service in sorted(windows_by_service):
    merged: list[list[int]] = []

    for start, end in sorted(windows_by_service[service]):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    durations = [end - start for start, end in merged]
    report.append(
        {
            "service": service,
            "windows": merged,
            "total_minutes": sum(durations),
            "longest_minutes": max(durations),
        }
    )

OUTPUT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
PY
