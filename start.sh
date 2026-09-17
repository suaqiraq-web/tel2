#!/bin/sh

# 1. توليد ملف config.py الخاص بالبروكسي من المتغيرات
python3 genconfig.py

# 2. تشغيل خادم mtprotoproxy في الخلفية
python3 mtprotoproxy.py config.py &

# 3. تشغيل بوت الإدارة
python3 bot.py
