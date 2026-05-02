#!/usr/bin/env bash
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG="$HERMES_HOME/config.yaml"
ENV_FILE="$HERMES_HOME/.env"
OLLAMA_MODEL="${SMARTPYME_OLLAMA_MODEL:-}"

mkdir -p "$HERMES_HOME"

if ! command -v ollama >/dev/null 2>&1; then
  echo "BLOCKED_PROVIDER: ollama command not found" >&2
  exit 2
fi

if ! curl -fsS http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "BLOCKED_PROVIDER: Ollama is not responding on localhost:11434" >&2
  exit 2
fi

if [[ -z "$OLLAMA_MODEL" ]]; then
  OLLAMA_MODEL="$(ollama list | awk 'NR>1 {print $1}' | grep -Ei 'gemma|gemma3|gemma4' | head -1 || true)"
fi

if [[ -z "$OLLAMA_MODEL" ]]; then
  echo "BLOCKED_PROVIDER: no Gemma model found in ollama list" >&2
  exit 2
fi

python3 - "$CONFIG" "$OLLAMA_MODEL" <<'PY'
from pathlib import Path
import sys
import yaml

config_path = Path(sys.argv[1])
model = sys.argv[2]
config = {}
if config_path.exists():
    config = yaml.safe_load(config_path.read_text()) or {}

config.setdefault("model", {})
config["model"]["provider"] = "ollama"
config["model"]["base_url"] = "http://localhost:11434/v1"
config["model"]["default"] = model

config.setdefault("auxiliary", {})
for key in ("web_extract", "session_search"):
    config["auxiliary"].setdefault(key, {})
    config["auxiliary"][key]["provider"] = "main"
    config["auxiliary"][key]["model"] = model

config.setdefault("plugins", {})
enabled = config["plugins"].get("enabled")
if not isinstance(enabled, list):
    enabled = []
if "smartpyme-model-guard" not in enabled:
    enabled.append("smartpyme-model-guard")
config["plugins"]["enabled"] = enabled

config_path.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
PY

if [[ -f "$ENV_FILE" ]]; then
  python3 - "$ENV_FILE" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
lines = path.read_text().splitlines()
out = []
seen = False
for line in lines:
    if line.startswith("SMARTPYME_LONG_PROMPT_LIMIT="):
        out.append("SMARTPYME_LONG_PROMPT_LIMIT=3500")
        seen = True
    else:
        out.append(line)
if not seen:
    out.append("SMARTPYME_LONG_PROMPT_LIMIT=3500")
path.write_text("\n".join(out) + "\n")
PY
else
  printf 'SMARTPYME_LONG_PROMPT_LIMIT=3500\n' > "$ENV_FILE"
fi

echo "DONE: SmartPyme routing configured"
echo "Provider: ollama"
echo "Model: $OLLAMA_MODEL"
echo "Plugin: smartpyme-model-guard enabled"
echo "Config: $CONFIG"
