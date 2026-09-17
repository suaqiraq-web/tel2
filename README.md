# Telegram MTProto proxy bot

Railway variables:

- `BOT_TOKEN`
- `SECRET` (32 hexadecimal characters)
- `ADMIN_TG_ID`
- `PUBLIC_IP` (TCP proxy domain)
- `EXTERNAL_PORT` (TCP proxy public port)

Configure Railway TCP Proxy from the public port to internal port `443`, then add a persistent Volume mounted at `/data`.
