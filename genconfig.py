import json
import os

DATA = "/data/subs.json"


def main():
    try:
        with open(DATA, encoding="utf-8") as file:
            database = json.load(file)
    except (OSError, json.JSONDecodeError):
        database = {}

    users = {"admin": os.environ.get("SECRET", "")}
    expirations = {}
    allowed_ips = {}
    connections = {"admin": 32}

    for name, subscriber in database.get("subscribers", {}).items():
        if not isinstance(subscriber, dict) or not subscriber.get("active", True):
            continue
        secret = str(subscriber.get("secret", ""))
        if len(secret) != 32:
            continue
        users[name] = secret
        connections[name] = 4
        if subscriber.get("expiry"):
            expirations[name] = str(subscriber["expiry"])
        if subscriber.get("ip"):
            allowed_ips[name] = str(subscriber["ip"])

    port = int(os.environ.get("PORT", "443"))
    with open("config.py", "w", encoding="utf-8") as file:
        file.write("PORT = %d\n" % port)
        file.write("USERS = %s\n" % json.dumps(users))
        file.write("USER_EXPIRATIONS = %s\n" % json.dumps(expirations))
        file.write("USER_ALLOWED_IPS = %s\n" % json.dumps(allowed_ips))
        file.write("USER_MAX_TCP_CONNS = %s\n" % json.dumps(connections))
        file.write('MODES = {"classic": False, "secure": False, "tls": True}\n')
        file.write("FAST_MODE = True\nPREFER_IPV6 = False\n")


if __name__ == "__main__":
    main()
