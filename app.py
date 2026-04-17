from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "68"   # 👉 यहाँ अपना BotFather token डालो

# 🔹 Telegram webhook route
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text")

        if text == "/start":
            send_message(chat_id, f"🆔 Your Telegram ID:\n{chat_id}")

        elif text == "/otp":
            import random
            otp = random.randint(100000, 999999)
            send_message(chat_id, f"🔐 Your OTP: {otp}")

    return "ok"


# 🔹 Send message function
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": chat_id,
        "text": text
    })


# 🔹 Home route (important for Render)
@app.route("/")
def home():
    return "Bot is running 🚀"


if __name__ == "__main__":
    app.run(debug=True)
