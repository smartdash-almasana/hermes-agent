import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hermes_action_bridge")


async def execute_action(proposal_json: str) -> dict:
    try:
        payload = json.loads(proposal_json)

        if not isinstance(payload, dict):
            return {
                "status": "failed",
                "adapter_id": "hermes",
                "action_id": "unknown",
                "message": "Invalid JSON payload: payload must be an object",
            }

        missing = [
            key for key in ("action_id", "title", "recommended_action")
            if not payload.get(key)
        ]

        if missing:
            return {
                "status": "failed",
                "adapter_id": "hermes",
                "action_id": payload.get("action_id") or "unknown",
                "message": f"Missing required fields: {', '.join(missing)}",
            }

        action_id = payload["action_id"]
        recommended_action = payload["recommended_action"]

        return {
            "status": "executed",
            "adapter_id": "hermes",
            "action_id": action_id,
            "message": f"Hermes mock executed action {action_id}: {recommended_action}",
        }

    except Exception as exc:
        return {
            "status": "failed",
            "adapter_id": "hermes",
            "action_id": "unknown",
            "message": f"Invalid JSON payload: {exc}",
        }


mcp.tool()(execute_action)


if __name__ == "__main__":
    mcp.run()
