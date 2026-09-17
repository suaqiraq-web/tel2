import os
import json
from datetime import datetime


def load_subs():
    try:
        with open("/data/subs.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def parse_expiry(exp_str):
    """تحويل تاريخ DD/MM/YYYY إلى Unix Timestamp"""
    try:
        dt = datetime.strptime(str(exp_str).strip(), "%d/%m/%Y")
        # نهاية اليوم
        dt = dt.replace(hour=23, minute=59, second=59)
        return int(dt.timestamp())
    except Exception:
        return None


def main():
    subs = load_subs()
    dat = subs.get("subscribers", {})

    users = {}
    exp = {}
    ips = {}
    conns = {"admin": 32}

    for name, s in dat.items():
        if not isinstance(s, dict):
            continue
        secret = str(s.get("secret", ""))
        if len(secret) != 32:
            continue
        if not bool(s.get("active", True)):
            continue

        users[name] = secret

        # تحويل التاريخ إلى Timestamp
        if s.get("expiry"):
            ts = parse_expiry(s["expiry"])
            if ts:
                exp[name] = ts

        if s.get("ip"):
            ips[name] = str(s["ip"])

        conns[name] = 4

    admin = os.environ.get("SECRET", "c7b105c8829e465a542b58d61d1d235f")
    users["admin"] = admin

    port = int(os.environ.get("PORT", "443"))

    cfg = f"""PORT = {port}

USERS = {json.dumps(users, indent=4)}

USER_EXPIRATIONS = {json.dumps(exp, indent=4)}

USER_ALLOWED_IPS = {json.dumps(ips, indent=4)}

USER_MAX_TCP_CONNS = {json.dumps(conns, indent=4)}

MODES = {{
    "classic": False,
    "secure": False,
    "tls": True,
}}

TLS_DOMAIN = "www.google.com"

FAST_MODE = True
PREFER_IPV6 = False

TO_CLT_BUFSIZE = 1048576
TO_TG_BUFSIZE = 1048576

TG_CONNECT_TIMEOUT = 100
TG_READ_TIMEOUT = 100
CLIENT_HANDSHAKE_TIMEOUT = 100
"""

    with open("config.py", "w", encoding="utf-8") as f:
        f.write(cfg)

    print("config.py regenerated: %d subscribers, %d active" % (len(dat), len(users) - 1))


if __name__ == "__main__":
    main()
