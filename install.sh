#!/bin/bash

# خروج در صورت بروز خطا
set -e

echo "به اسکریپت نصب ربات فروش فیلترشکن خوش آمدید!"

# بروزرسانی لیست بسته‌ها
echo "در حال بروزرسانی لیست بسته‌ها..."
sudo apt update

# نصب پایتون 3 و pip
echo "در حال نصب پایتون 3 و pip..."
sudo apt install -y python3 python3-pip

# نصب کتابخانه telebot
echo "در حال نصب کتابخانه telebot..."
pip3 install --upgrade pip
pip3 install telebot requests

# دانلود سورس کد ربات از GitHub
echo "در حال دانلود سورس کد ربات از GitHub..."
github_repo="jasemhooti/jasem22"
python_file="bot.py"
github_raw_url="https://raw.githubusercontent.com/${github_repo}/main/${python_file}"
wget -O "${python_file}" "${github_raw_url}"

echo "سورس کد ربات با موفقیت دانلود شد."

# اجرای ربات در پس زمینه
echo "در حال اجرای ربات در پس زمینه..."
nohup python3 "${python_file}" &
echo "ربات با موفقیت در پس زمینه اجرا شد."

echo "برای مشاهده خروجی ربات می‌توانید از دستور زیر استفاده کنید:"
echo "tail -f nohup.out"

echo "نصب و راه‌اندازی ربات به پایان رسید!"
