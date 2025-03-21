#!/bin/bash

# خروج در صورت بروز خطا
set -e

# --- تنظیمات ---
github_repo="jasemhooti/jasem22"
python_file="bot.py"

# --- توابع ---

install_bot() {
    echo "در حال شروع نصب ربات..."

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
        python3_executable="python3.7"
        pip_executable="python3.7 -m pip"
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
    github_raw_url="https://raw.githubusercontent.com/${github_repo}/main/${python_file}"
    wget -O "${python_file}" "${github_raw_url}"

    echo "سورس کد ربات با موفقیت دانلود شد."

    # اجرای ربات در پس زمینه
    echo "در حال اجرای ربات در پس زمینه..."
    nohup ${python3_executable} "${python_file}" &
    echo "ربات با موفقیت در پس زمینه اجرا شد."
    echo "برای مشاهده خروجی ربات می‌توانید از دستور زیر استفاده کنید: tail -f nohup.out"
}

update_bot() {
    echo "در حال بروزرسانی ربات..."
    pid=$(pgrep -f "${python_file}")
    if [ -n "$pid" ]; then
        echo "فرآیند ربات با شناسه ${pid} پیدا شد. در حال توقف..."
        kill -9 "$pid"
        echo "ربات متوقف شد."
    else
        echo "هیچ فرآیندی با نام '${python_file}' در حال اجرا یافت نشد."
    fi
    cd "$(dirname "$0")"
    branch="main"
    echo "در حال دریافت آخرین نسخه کد از GitHub..."
    git init 2>/dev/null # جلوگیری از نمایش پیام init اگر قبلاً انجام شده باشد
    git remote add origin "https://github.com/${github_repo}.git" 2>/dev/null
    git fetch origin 2>/dev/null
    git checkout "${branch}" -- "${python_file}"
    echo "آخرین نسخه کد با موفقیت دریافت شد."
    echo "در حال اجرای مجدد ربات در پس زمینه..."
    nohup python3 "${python_file}" &
    echo "ربات با موفقیت در پس زمینه اجرا شد."
    echo "برای مشاهده خروجی ربات می‌توانید از دستور زیر استفاده کنید: tail -f nohup.out"
}

uninstall_bot() {
    echo "در حال حذف ربات..."
    pid=$(pgrep -f "${python_file}")
    if [ -n "$pid" ]; then
        echo "فرآیند ربات با شناسه ${pid} پیدا شد. در حال توقف..."
        kill -9 "$pid"
        echo "ربات متوقف شد."
    else
        echo "هیچ فرآیندی با نام '${python_file}' در حال اجرا یافت نشد."
    fi
    cd "$(dirname "$0")"
    if [ -f "${python_file}" ]; then
        echo "در حال حذف فایل ربات ('${python_file}')..."
        rm "${python_file}"
        echo "فایل ربات حذف شد."
    else
        echo "فایل ربات ('${python_file}') یافت نشد."
    fi
    log_file="nohup.out"
    if [ -f "${log_file}" ]; then
        echo "در حال حذف فایل خروجی ('${log_file}')..."
        rm "${log_file}"
        echo "فایل خروجی حذف شد."
    else
        echo "فایل خروجی ('${log_file}') یافت نشد."
    fi
    echo "حذف ربات به پایان رسید!"
}

# --- منو ---
while true; do
    echo ""
    echo "لطفاً یک گزینه را انتخاب کنید:"
    echo "1. نصب ربات"
    echo "2. بروزرسانی ربات"
    echo "3. حذف ربات"
    echo "4. خروج"
    read -p "انتخاب شما (1-4): " choice

    case "$choice" in
        1)
            install_bot
            break # پس از نصب معمولاً می‌خواهیم از منو خارج شویم
            ;;
        2)
            update_bot
            echo "بروزرسانی با موفقیت انجام شد."
            break # پس از بروزرسانی معمولاً می‌خواهیم از منو خارج شویم
            ;;
        3)
            uninstall_bot
            echo "حذف با موفقیت انجام شد."
            break # پس از حذف معمولاً می‌خواهیم از منو خارج شویم
            ;;
        4)
            echo "خروج از اسکریپت."
            exit 0
            ;;
        *)
            echo "گزینه نامعتبر. لطفاً از بین 1 تا 4 انتخاب کنید."
            ;;
    esac
done
