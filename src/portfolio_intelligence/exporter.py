from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .engines import AlertEngine
from .models import Signal, SourceStatus, utc_now_iso

SCHEMA_VERSION = "0.1.0"


def build_payload(
    signals: Iterable[Signal],
    source_statuses: Iterable[SourceStatus],
) -> dict[str, object]:
    alert_engine = AlertEngine()
    ordered_signals = sorted(signals, key=lambda item: (-item.priority_score, item.signal_id))
    signal_payloads: list[dict[str, object]] = []

    for signal in ordered_signals:
        payload = signal.to_dict()
        payload["alert"] = alert_engine.classify(signal).__dict__
        signal_payloads.append(payload)

    statuses = sorted(source_statuses, key=lambda item: item.source_id)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "data_quality": {
            "source_count": len(statuses),
            "failed_sources": [item.source_id for item in statuses if item.status == "failed"],
            "degraded_sources": [item.source_id for item in statuses if item.status == "degraded"],
        },
        "source_statuses": [item.__dict__ for item in statuses],
        "signals": signal_payloads,
    }


def export_json(
    output_path: str | Path,
    signals: Iterable[Signal],
    source_statuses: Iterable[SourceStatus],
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload(signals, source_statuses)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path
