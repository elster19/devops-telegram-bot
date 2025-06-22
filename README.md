# DevOps Telegram Bot (Interactive)

A Telegram bot that:
- Sends daily DevOps learning tasks at 08:00 and 15:00
- Responds to /plan commands for today's, tomorrow's, or any specific date's plan
- Skips messages on Jewish holidays
- Runs 24/7 on Railway with webhook support

## Commands

- `/plan` — today's plan
- `/plan завтра` — tomorrow's plan
- `/plan YYYY-MM-DD` — plan for specific date

## Deployment (Railway)

1. Clone this repo or deploy via Railway GitHub integration.
2. Set `TOKEN` as a secret env var (your Telegram Bot Token).
3. Run:

```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://<your-app>.railway.app/<YOUR_TOKEN>
```