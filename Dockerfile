FROM python:3.11-alpine

RUN apk add --no-cache git gcc musl-dev libffi-dev build-base
RUN git clone --depth 1 https://github.com/alexbers/mtprotoproxy.git /app
WORKDIR /app
RUN pip install --no-cache-dir cryptography uvloop

COPY genconfig.py /app/genconfig.py
COPY bot.py /app/bot.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV PORT=443
EXPOSE 443
VOLUME /data
CMD ["/bin/sh", "/app/start.sh"]
