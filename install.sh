#!/bin/bash

# خروج در صورت بروز خطا
set -e

echo "به اسکریپت نصب ربات فروش فیلترشکن خوش آمدید!"

# بررسی نسخه پایتون 3
python3_version=$(python3 -V 2>&1 | awk '{print $2}' | cut -d'.' -f1-2)
required_version="3.7"

echo "نسخه پایتون 3 فعلی: ${python3_version}"
echo "نسخه پایتون مورد نیاز: ${required_version}"

# ارتقاء پایتون در صورت نیاز (فقط برای سیستم‌های Debian/Ubuntu)
if [[ $(echo "${python3_version}" "${required_version}" | awk '{print ($1 < $2)}') -eq 1 ]]; then
    echo "نسخه پایتون 3 قدیمی است. در حال تلاش برای ارتقاء به نسخه ${required_version}..."
    sudo apt update
    sudo apt install -y python3.7 python3.7-pip
    echo "ارتقاء پایتون 3 به نسخه ${required_version} با موفقیت انجام شد."

    # تغییر لینک پیش‌فرض python3 (اختیاری و با احتیاط)
    echo "در حال تنظیم لینک پیش‌فرض python3 به نسخه ${required_version}..."
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 10
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 20
    sudo update-alternatives --config python3

    python3_executable="python3"
    pip_executable="pip3"
else
    echo "نسخه پایتون 3 مناسب است."
    python3_executable="python3"
    pip_executable="pip3"
fi

# نصب کتابخانه‌های مورد نیاز
echo "در حال نصب کتابخانه‌های مورد نیاز (telebot و requests)..."
${python3_executable} -m pip install --upgrade pip
${python3_executable} -m pip install telebot requests

echo "نصب کتابخانه‌ها با موفقیت انجام شد."

# دانلود سورس کد ربات از GitHub
echo "در حال دانلود سورس کد ربات از GitHub..."
github_repo="jasemhooti/jasem22"
python_file="bot.py"
github_raw_url="https://raw.githubusercontent.com/${github_repo}/main/${python_file}"
wget -O "${python_file}" "${github_raw_url}"

echo "سورس کد ربات با موفقیت دانلود شد."

# اجرای ربات در پس زمینه
echo "در حال اجرای ربات در پس زمینه..."
nohup ${python3_executable} "${python_file}" &
echo "ربات با موفقیت در پس زمینه اجرا شد."

echo "برای مشاهده خروجی ربات می‌توانید از دستور زیر استفاده کنید:"
echo "tail -f nohup.out"

echo "نصب و راه‌اندازی ربات به پایان رسید!"
