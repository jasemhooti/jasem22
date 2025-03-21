#!/bin/bash

# نمایش پیام شروع نصب
echo "شروع نصب پایتون 3 و pip در Ubuntu..."

# به‌روزرسانی لیست بسته‌ها
echo "به‌روزرسانی لیست بسته‌ها..."
sudo apt update -y

# نصب پایتون 3
echo "نصب پایتون 3..."
sudo apt install -y python3

# نصب pip برای پایتون 3
echo "نصب pip برای پایتون 3..."
sudo apt install -y python3-pip

# بررسی نصب پایتون
if command -v python3 &> /dev/null; then
    echo "پایتون 3 با موفقیت نصب شد."
    python3 --version
else
    echo "خطا: پایتون 3 نصب نشد."
fi

# بررسی نصب pip
if command -v pip3 &> /dev/null; then
    echo "pip3 با موفقیت نصب شد."
    pip3 --version
else
    echo "خطا: pip3 نصب نشد."
fi

echo "نصب پایتون 3 و pip به پایان رسید."
