FROM python:3.11-alpine

# تثبيت الحزم الأساسية
RUN apk add --no-cache git gcc musl-dev libffi-dev build-base

# استنسخ السورس وقم بتثبيت المتطلبات
RUN git clone --depth 1 https://github.com/alexbers/mtprotoproxy.git /app
WORKDIR /app

RUN pip install --no-cache-dir cryptography uvloop

# نسخ ملفاتك الخاصة بعد الاستنسخاخ
COPY genconfig.py /app/genconfig.py
COPY bot.py /app/bot.py
COPY start.sh /app/start.sh

# تحويل صيغة الأسطر وصلاحيات التشغيل
RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

ENV PORT=443
EXPOSE 443

CMD ["/bin/sh", "/app/start.sh"]
