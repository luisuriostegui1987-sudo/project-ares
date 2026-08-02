"""Append-only institutional fact storage (Sprint-2 minimal implementation)."""

from .store import FactStoreError, InMemoryFactStore

__all__ = ["FactStoreError", "InMemoryFactStore"]
