import os
import hmac
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("mah​​moud_sfx")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

@app.get("/")
def index():
    return jsonify({
        "service": "MAHMOUD SFX AUTO TRADER",
        "status": "running",
        "mode": "signal-receiver-only",
        "message": "Webhook receiver is online. No trades are executed."
    })

@app.get("/health")
def health():
    return jsonify({"ok": True}), 200

@app.post("/webhook")
def webhook():
    if not WEBHOOK_SECRET:
        logger.error("WEBHOOK_SECRET is not configured")
        return jsonify({"ok": False, "error": "server_not_configured"}), 503

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "JSON object required"}), 400

    received_secret = str(payload.get("secret", ""))
    if not hmac.compare_digest(received_secret, WEBHOOK_SECRET):
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    action = str(payload.get("action", "")).upper()
    symbol = str(payload.get("symbol", "")).strip()
    timeframe = str(payload.get("timeframe", "")).strip()

    if action not in {"BUY", "SELL"}:
        return jsonify({"ok": False, "error": "action must be BUY or SELL"}), 400
    if not symbol or len(symbol) > 40:
        return jsonify({"ok": False, "error": "valid symbol is required"}), 400
    if len(timeframe) > 20:
        return jsonify({"ok": False, "error": "timeframe is too long"}), 400

    event = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "symbol": symbol,
        "timeframe": timeframe or "unspecified",
        "source": str(payload.get("source", "TradingView"))[:40],
        "mode": "signal-receiver-only"
    }

    # Safety: this starter service records/acknowledges signals only.
    # It does NOT place orders or connect to a broker.
    logger.info("Signal received: %s", event)
    return jsonify({"ok": True, "accepted": True, "event": event}), 200

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"ok": False, "error": "not_found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
