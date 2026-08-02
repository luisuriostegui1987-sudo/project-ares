"""ARES institutional API (FastAPI). The single entry point for all clients."""

from .app import create_app

__all__ = ["create_app"]
