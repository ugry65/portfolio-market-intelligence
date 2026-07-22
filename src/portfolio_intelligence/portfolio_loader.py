from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .engines import PortfolioPosition


@dataclass(frozen=True)
class PortfolioLoadResult:
    positions: tuple[PortfolioPosition, ...]
    warnings: tuple[str, ...] = ()


def _normalise_weight(value: Any) -> float:
    weight = float(value)
    if weight > 1:
        weight /= 100
    if not 0 <= weight <= 1:
        raise ValueError("portfolio weight must be between 0 and 1, or 0 and 100 percent")
    return weight


def _tuple_field(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return tuple(item.strip() for item in value.split("|") if item.strip())
    if isinstance(value, list):
        return tuple(str(item).strip() for item in value if str(item).strip())
    raise ValueError("aliases/themes must be a list or pipe-separated string")


def _position_from_mapping(row: dict[str, Any]) -> PortfolioPosition:
    ticker = str(row.get("ticker", "")).strip()
    name = str(row.get("name", "")).strip()
    if not ticker or not name:
        raise ValueError("each position requires ticker and name")

    raw_weight = row.get("weight", row.get("portfolio_weight"))
    if raw_weight in (None, ""):
        raise ValueError(f"missing weight for {ticker}")

    return PortfolioPosition(
        ticker=ticker,
        name=name,
        weight=_normalise_weight(raw_weight),
        aliases=_tuple_field(row.get("aliases")),
        themes=_tuple_field(row.get("themes")),
    )


def load_portfolio_json(path: str | Path) -> PortfolioLoadResult:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = payload.get("positions", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("portfolio JSON must contain a list or a positions list")
    positions = tuple(_position_from_mapping(dict(row)) for row in rows)
    return PortfolioLoadResult(positions=positions, warnings=_weight_warnings(positions))


def load_portfolio_csv(path: str | Path) -> PortfolioLoadResult:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    positions = tuple(_position_from_mapping(dict(row)) for row in rows)
    return PortfolioLoadResult(positions=positions, warnings=_weight_warnings(positions))


def _weight_warnings(positions: tuple[PortfolioPosition, ...]) -> tuple[str, ...]:
    total = sum(position.weight for position in positions)
    warnings: list[str] = []
    if not positions:
        warnings.append("portfolio contains no positions")
    if positions and abs(total - 1.0) > 0.02:
        warnings.append(f"portfolio weights total {total:.4f}, not approximately 1.0")
    duplicate_tickers = sorted(
        ticker for ticker in {position.ticker for position in positions}
        if sum(position.ticker == ticker for position in positions) > 1
    )
    if duplicate_tickers:
        warnings.append("duplicate tickers: " + ", ".join(duplicate_tickers))
    return tuple(warnings)
