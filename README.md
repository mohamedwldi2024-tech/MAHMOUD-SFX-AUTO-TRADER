# MAHMOUD SFX AUTO TRADER — starter service

This is the first safe deployment stage for the TradingView → Render workflow.

## What it does
- Hosts a Flask web service on Render.
- Provides `GET /` and `GET /health`.
- Receives authenticated JSON alerts at `POST /webhook`.
- Accepts `BUY` or `SELL` signals and logs a minimal event.

## Important safety limitation
This starter version **does not place trades** and does not connect to Capital.com or any other broker. It is intended to confirm that deployment and TradingView webhook delivery work before adding broker execution.

Do not add broker passwords, API keys, or account identifiers to source code or GitHub.

## Deploy on Render
1. Push these files to the GitHub repository.
2. In Render, choose **New → Web Service** and select this repository.
3. Render can detect `render.yaml`. If configuring manually:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Health check path: `/health`
4. In Render Environment, create `WEBHOOK_SECRET` with a long random value. Keep it private.
5. Deploy. Open `https://YOUR-SERVICE.onrender.com/health`; expected response: `{"ok":true}`.

## TradingView alert message
After deployment, create an alert and use this JSON message, replacing the placeholders:

```json
{
  "secret": "YOUR_WEBHOOK_SECRET",
  "action": "BUY",
  "symbol": "YOUR_SYMBOL",
  "timeframe": "5",
  "source": "TradingView"
}
```

Set the webhook URL to:
`https://YOUR-SERVICE.onrender.com/webhook`

Use `SELL` for a sell signal. Never paste the secret into a public screenshot or share it in chat.

## Before broker execution is added
We must first confirm the exact Pine Script signal format and review the current Capital.com demo API requirements. Broker execution should be added only after successful webhook tests, with demo-only safeguards, duplicate-alert protection, position-size limits, and a kill switch.
