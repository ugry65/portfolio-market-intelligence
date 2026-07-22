from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from .models import Signal, SourceStatus


@dataclass(frozen=True)
class AdapterResult:
    signals: tuple[Signal, ...]
    status: SourceStatus


class SourceAdapter(ABC):
    """Contract for external data-source adapters.

    Adapters fetch and normalize source data only. They must not make portfolio
    decisions, invent missing fields, or silently hide degraded source status.
    """

    source_id: str

    @abstractmethod
    def fetch(self) -> AdapterResult:
        raise NotImplementedError


class StaticSignalAdapter(SourceAdapter):
    """Deterministic adapter for tests, demos, and controlled manual inputs."""

    def __init__(self, source_id: str, signals: Iterable[Signal]) -> None:
        self.source_id = source_id
        self._signals = tuple(signals)

    def fetch(self) -> AdapterResult:
        return AdapterResult(
            signals=self._signals,
            status=SourceStatus(
                source_id=self.source_id,
                status="ok",
                item_count=len(self._signals),
                message="Static controlled input.",
            ),
        )
