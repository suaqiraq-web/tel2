#!/bin/sh

# تشغيل خادم MTProxy في الخلفية على المنفذ 443
# (أو أمر تشغيل خادم البروكسي المعتمد في مشروعك)
./mtproxy -p 443 -s $SECRET -H 443 --tls google.com &

# تشغيل بوت الإدارة
python3 bot.py
