#!/bin/bash

# خروج در صورت بروز خطا
set -e

# پیام خوشامدگویی
echo "شروع فرآیند نصب Python 3.7 در سرور اوبونتو..."

# آپدیت پکیج‌ها
sudo apt update -y
sudo apt upgrade -y

# نصب پیش‌نیازها برای کامپایل پایتون
sudo apt install -y build-essential zlib1g-dev \
    libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev curl

# دانلود و اکسترکت سورس پایتون ۳.۷
cd /usr/src
sudo curl -O https://www.python.org/ftp/python/3.7.17/Python-3.7.17.tgz
sudo tar xzf Python-3.7.17.tgz

# کامپایل و نصب Python 3.7
cd Python-3.7.17
sudo ./configure --enable-optimizations
sudo make -j$(nproc)
sudo make altinstall

# بررسی نسخه پایتون نصب شده
python3.7 --version

# نصب pip برای پایتون 3.7
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.7

# بررسی نصب pip
python3.7 -m pip --version

echo "✅ Python 3.7 و pip با موفقیت نصب شدند!"
