import json
import os
import secrets
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta

TOKEN = os.environ.get("BOT_TOKEN", "")
PUBLIC_IP = os.environ.get("PUBLIC_IP", "")
EXTERNAL_PORT = os.environ.get("EXTERNAL_PORT", "")
ADMIN_TG_ID = os.environ.get("ADMIN_TG_ID", "")
CONTACT = os.environ.get("SUBSCRIBE_CONTACT", "@fadl22b")
DATA = "/data/subs.json"
API = "https://api.telegram.org/bot%s" % TOKEN
TLS_DOMAIN_HEX = "7777772e676f6f676c652e636f6d"

os.makedirs(os.path.dirname(DATA), exist_ok=True)


def load():
    try:
        with open(DATA, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {"admin_id": None, "subscribers": {}, "free_used": []}


def save(database):
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    temporary = DATA + ".tmp"
    with open(temporary, "w", encoding="utf-8") as file:
        json.dump(database, file, ensure_ascii=False, indent=2)
    os.replace(temporary, DATA)


def api(method, **parameters):
    request = urllib.request.Request(
        API + "/" + method,
        data=urllib.parse.urlencode(parameters).encode(),
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        return json.loads(response.read())


def send(chat_id, text):
    try:
        api("sendMessage", chat_id=chat_id, text=text)
    except Exception:
        pass


def proxy_link(secret):
    if not PUBLIC_IP or not EXTERNAL_PORT:
        return "إعدادات البروكسي غير مكتملة: أضف PUBLIC_IP و EXTERNAL_PORT في Railway."
    return "tg://proxy?server=%s&port=%s&secret=ee%s%s" % (
        PUBLIC_IP, EXTERNAL_PORT, secret, TLS_DOMAIN_HEX
    )


def trial(chat_id, user):
    database = load()
    user_id = user.get("id")
    used = database.setdefault("free_used", [])
    if user_id in used:
        send(chat_id, "استخدمت التجربة المجانية سابقًا. للاشتراك تواصل مع المطور: %s" % CONTACT)
        return

    username = user.get("username") or ("user%s" % user_id)
    name = "trial_" + username
    subscribers = database.setdefault("subscribers", {})
    while name in subscribers:
        name += "_" + str(int(time.time()))

    secret = secrets.token_hex(16)
    subscribers[name] = {
        "secret": secret,
        "active": True,
        "expiry": (date.today() + timedelta(days=2)).strftime("%d/%m/%Y"),
        "tg_id": user_id,
    }
    used.append(user_id)
    save(database)
    send(chat_id, "رابط التجربة لمدة يومين:\n\n%s" % proxy_link(secret))


def handle(update):
    message = update.get("message") or {}
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip().lower()
    user = message.get("from", {})
    if not chat_id:
        return

    database = load()
    if database.get("admin_id") is None:
        database["admin_id"] = chat_id
        save(database)

    if text in ("/start", "/help", "start", "تجربة", "مجانية", "مجاني"):
        trial(chat_id, user)
    else:
        send(chat_id, "أرسل /start للحصول على تجربة مجانية لمدة يومين.")


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is required")
    offset = 0
    while True:
        for update in api("getUpdates", offset=offset, timeout=30).get("result", []):
            offset = update["update_id"] + 1
            handle(update)
        time.sleep(1)


if __name__ == "__main__":
    main()
