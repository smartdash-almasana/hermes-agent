"""SmartPyme model routing guard.

This plugin blocks long audit/inspection style prompts at the gateway before
Hermes sends them to the active cloud model. It is intentionally conservative:
it does not edit code, does not call providers, and only rewrites inbound
messaging events into a short local-routing instruction.
"""

from __future__ import annotations

import os
import re

AUDIT_KEYWORDS = (
    "AUDIT_REQUEST",
    "PRECHECK",
    "REVIEW",
    "READ",
    "INSPECT",
    "INVENTORY",
    "SUMMARY",
)

DEFAULT_LIMIT = 3500


def _limit() -> int:
    raw = os.environ.get("SMARTPYME_LONG_PROMPT_LIMIT", "")
    try:
        return int(raw) if raw else DEFAULT_LIMIT
    except ValueError:
        return DEFAULT_LIMIT


def _looks_like_audit(text: str) -> bool:
    upper = text.upper()
    if any(token in upper for token in AUDIT_KEYWORDS):
        return True
    return bool(re.search(r"\b(audit|precheck|inspect|review|inventory|summary)\b", text, re.I))


def _handler(event=None, **_kwargs):
    text = getattr(event, "text", "") or ""
    if len(text) <= _limit():
        return None
    if not _looks_like_audit(text):
        return None
    return {
        "action": "rewrite",
        "text": (
            "BLOCKED_LONG_PROMPT_VERTEX_FOR_AUDIT\n\n"
            "This audit/read/precheck prompt is too long for cloud routing. "
            "Route this task through the local Ollama/Gemma auditor, or split "
            "the task into a smaller implementation prompt. Do not retry this "
            "large audit prompt against Vertex/Gemini."
        ),
    }


def register(ctx):
    ctx.register_hook("pre_gateway_dispatch", _handler)
