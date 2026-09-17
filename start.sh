#!/bin/sh
set -e

# إنشاء المجلد للبيانات إن لم يكن موجوداً
mkdir -p /data

# توليد إعدادات البروكسي الأولية
python3 /app/genconfig.py

# تشغيل بوت التلكرام في الخلفية
python3 /app/bot.py &

# تشغيل خادم البروكسي الأساسي
exec python3 mtprotoproxy.py
