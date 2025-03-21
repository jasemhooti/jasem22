#!/bin/bash

# به‌روزرسانی لیست بسته‌ها
sudo apt update

# تلاش برای نصب پایتون 3 و pip
sudo apt install -y python3 python3-pip

# بررسی نصب
if command -v python3 &> /dev/null; then
    echo "پایتون 3 با موفقیت نصب شد."
    python3 --version
else
    echo "خطا: پایتون 3 نصب نشد."
fi

if command -v pip3 &> /dev/null; then
    echo "pip3 با موفقیت نصب شد."
    pip3 --version
else
    echo "خطا: pip3 نصب نشد."
fi
