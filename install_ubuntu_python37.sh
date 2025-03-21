#!/bin/bash

# نمایش پیام شروع نصب پایتون 3.7 و pip
echo "شروع تلاش برای نصب پایتون 3.7 و pip در Ubuntu..."

# به‌روزرسانی لیست بسته‌ها
echo "به‌روزرسانی لیست بسته‌ها..."
sudo apt update -y

# تلاش برای نصب پایتون 3.7
echo "تلاش برای نصب پایتون 3.7..."
sudo apt install -y python3.7

# تلاش برای نصب pip برای پایتون 3.7
echo "تلاش برای نصب pip برای پایتون 3.7..."
sudo apt install -y python3.7-pip

# بررسی نصب پایتون 3.7
if command -v python3.7 &> /dev/null; then
    echo "پایتون 3.7 با موفقیت نصب شد."
    python3.7 --version
else
    echo "خطا: پایتون 3.7 نصب نشد. ممکن است این بسته در مخازن شما موجود نباشد."
    echo "توصیه می‌شود از آخرین نسخه پایتون 3 موجود در مخازن استفاده کنید."
fi

# بررسی نصب pip برای پایتون 3.7
if command -v pip3.7 &> /dev/null; then
    echo "pip3.7 با موفقیت نصب شد."
    pip3.7 --version
else
    echo "خطا: pip3.7 نصب نشد."
fi

echo "تلاش برای نصب پایتون 3.7 و pip به پایان رسید."
echo "برای اجرای ربات با پایتون 3.7 از دستور 'python3.7 bot.py' استفاده کنید."

# **تغییر اولویت پایتون 3 (اختیاری و با مسئولیت خودتان):**
echo ""
echo "توجه: تغییر اولویت پایتون 3 می‌تواند باعث مشکلات در سیستم شود."
read -p "آیا می‌خواهید پایتون 3.7 را به عنوان پیش‌فرض برای دستور 'python3' تنظیم کنید؟ (y/N) " answer

if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    if command -v python3.7 &> /dev/null && command -v python3 &> /dev/null; then
        echo "تنظیم اولویت پایتون 3.7..."
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
        sudo update-alternatives --config python3
        echo "اولویت پایتون 3 تغییر کرد."
    else
        echo "خطا: پایتون 3.7 یا پایتون 3 پیدا نشد. امکان تغییر اولویت وجود ندارد."
    fi
else
    echo "تغییر اولویت پایتون 3 انجام نشد."
fi

echo ""
echo "برای اجرای ربات، به جای 'python3 bot.py' از 'python3.7 bot.py' استفاده کنید (مگر اینکه اولویت را تغییر داده باشید)."
