#!/bin/sh
set -eu

export PORT="${PORT:-443}"
mkdir -p /data
[ -f /data/subs.json ] || printf '%s\n' '{"admin_id": null, "subscribers": {}, "free_used": []}' > /data/subs.json

python3 /app/genconfig.py
python3 /app/bot.py &
exec python3 /app/mtprotoproxy.py
