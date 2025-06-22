import json
import time
import threading
import schedule
from datetime import datetime
import requests

# === НАСТРОЙКИ ===
TOKEN = "6229491676:AAGkHZ3PU9NjEyCw8zz3qSxxVvPrbYYasrE"
CHAT_ID = 1876664038
PLAN_FILE = "devops_plan.json"

# === ЕВРЕЙСКИЕ ПРАЗДНИКИ ===
HOLIDAYS = {
    "2025-04-12", "2025-04-13", "2025-04-14", "2025-04-15", "2025-04-16", "2025-04-17", "2025-04-18",  # Песах
    "2025-06-02", "2025-06-03",  # Шавуот
    "2025-10-01", "2025-10-02",  # Рош ха-Шана
    "2025-10-10",                # Йом Кипур
    "2025-10-15", "2025-10-16", "2025-10-17", "2025-10-18", "2025-10-19", "2025-10-20", "2025-10-21",  # Суккот
    "2025-10-22"                 # Шмини Ацерет
}

# === ЗАГРУЗКА ПЛАНА ===
def load_plan():
    try:
        with open(PLAN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Ошибка загрузки плана]: {e}")
        return {}

# === ОТПРАВКА СООБЩЕНИЯ ===
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"[Ошибка отправки]: {e}")

# === СБОРКА СООБЩЕНИЯ ===
def format_task(task):
    lines = [f"<b>{task['title']}</b>"]
    for item in task["tasks"]:
        lines.append(f"• {item}")
    return "\n".join(lines)

# === ЗАДАНИЕ НА УТРО ===
def morning_job():
    today = datetime.now().strftime("%Y-%m-%d")
    if today in HOLIDAYS:
        print(f"[{today}] Еврейский праздник – задание не отправлено.")
        return
    plan = load_plan()
    if today in plan and "morning" in plan[today]:
        msg = format_task(plan[today]["morning"])
        send_message(f"🕗 <b>Утреннее задание</b>\n\n{msg}")

# === ЗАДАНИЕ НА ДЕНЬ ===
def afternoon_job():
    today = datetime.now().strftime("%Y-%m-%d")
    if today in HOLIDAYS:
        print(f"[{today}] Еврейский праздник – задание не отправлено.")
        return
    plan = load_plan()
    if today in plan and "afternoon" in plan[today]:
        msg = format_task(plan[today]["afternoon"])
        send_message(f"🕒 <b>Дневное задание</b>\n\n{msg}")

# === РАСПИСАНИЕ ===
schedule.every().day.at("08:00").do(morning_job)
schedule.every().day.at("15:00").do(afternoon_job)

# === ЗАПУСК ===
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    print("DevOps бот запущен.")
    threading.Thread(target=run_scheduler).start()


import time
from flask import Flask, request

app = Flask(__name__)

# === Команды ===
def handle_command(text):
    today = datetime.now().date()
    if text.startswith("/plan"):
        parts = text.split()
        if len(parts) == 1:
            query_date = today
        elif parts[1].lower() == "завтра":
            query_date = today + timedelta(days=1)
        else:
            try:
                query_date = datetime.strptime(parts[1], "%Y-%m-%d").date()
            except ValueError:
                return "❌ Неверный формат даты. Используй: /plan 2025-06-30"

        date_str = query_date.strftime("%Y-%m-%d")
        plan = load_plan()
        if date_str in HOLIDAYS:
            return f"📅 {date_str} — праздничный день. Заданий нет."
        if date_str in plan:
            morning = format_task(plan[date_str]["morning"])
            afternoon = format_task(plan[date_str]["afternoon"])
            return f"📅 План на {date_str}\n\n<b>Утро:</b>\n{morning}\n\n<b>День:</b>\n{afternoon}"
        else:
            return f"❌ На {date_str} задания не запланированы."
    else:
        return "🤖 Я понимаю только команду /plan"

# === Обработка запросов Telegram ===
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        response = handle_command(text)
        if response:
            send_message(response)
    return {"ok": True}

# === Запуск Flask-сервера ===
def run_webhook():
    app.run(host="0.0.0.0", port=5000)

# Если нужен запуск бота и веб-сервера параллельно
if __name__ == "__main__":
    import threading
    print("DevOps бот с вебхуком запущен.")
    threading.Thread(target=run_scheduler).start()
    threading.Thread(target=run_webhook).start()