"""Test-wide fixtures and path setup for the chat project."""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)
