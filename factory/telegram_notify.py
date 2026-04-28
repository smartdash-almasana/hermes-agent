import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )
    response.raise_for_status()


def poll() -> None:
    offset = None
    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"timeout": 30}
        if offset is not None:
            params["offset"] = offset

        response = requests.get(url, params=params, timeout=40)
        response.raise_for_status()

        for update in response.json().get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message", {})
            text = message.get("text", "")
            if text:
                send_message(f"Hermes recibió: {text}")

        time.sleep(1)


if __name__ == "__main__":
    poll()
