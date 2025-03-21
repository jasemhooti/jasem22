import telebot
from telebot import types
import requests

# --- تنظیمات ربات ---
BOT_TOKEN = "6414210268:AAEL-RZiABoMzS_QY922hOQnpXcam9OgiF0"
ADMIN_ID = 5691972852
XUI_PANEL_URL = "http://irancell.jasemhooti1.ir:8443/"
XUI_USERNAME = "jasemhooti"
XUI_PASSWORD = "JasemhootI6906"
BANK_CARD_NUMBER = "6219861934798843"
BANK_CARD_OWNER = "حوتی"

# --- تنظیمات کانفیگ‌ها ---
CONFIGS = {
    "10GB": {"name": "10 گیگابایت", "price": 24000, "type": "vless", "limit": 10 * 1024 * 1024 * 1024},  # بر حسب بایت
    "20GB": {"name": "20 گیگابایت", "price": 48000, "type": "vless", "limit": 20 * 1024 * 1024 * 1024},  # بر حسب بایت
}

# --- متغیرها برای ذخیره وضعیت خرید کاربران ---
user_purchase_data = {}

bot = telebot.TeleBot(BOT_TOKEN)

# --- هندلر دستور /start ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for config_id, config_data in CONFIGS.items():
        button_text = f"{config_data['name']} - {config_data['price']} تومان"
        markup.add(types.InlineKeyboardButton(button_text, callback_data=f"buy_{config_id}"))
    bot.send_message(message.chat.id, "لطفاً حجم مورد نظر خود را انتخاب کنید:", reply_markup=markup)

# --- هندلر انتخاب حجم ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy_selection(call):
    chat_id = call.message.chat.id
    config_id = call.data.split("_")[1]
    if config_id in CONFIGS:
        user_purchase_data[chat_id] = {"selected_config": config_id}
        bot.send_message(chat_id, f"شما حجم {CONFIGS[config_id]['name']} به قیمت {CONFIGS[config_id]['price']} تومان را انتخاب کردید.\n\nلطفاً مبلغ {CONFIGS[config_id]['price']} تومان را به شماره کارت زیر کارت به کارت کنید:\n`{BANK_CARD_NUMBER}`\n\nبه نام: {BANK_CARD_OWNER}\n\nسپس رسید پرداخت (عکس) را برای من ارسال کنید.", parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "کانفیگ مورد نظر یافت نشد.")

# --- هندلر دریافت رسید ---
@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    chat_id = message.chat.id
    if chat_id in user_purchase_data and "selected_config" in user_purchase_data[chat_id]:
        selected_config_id = user_purchase_data[chat_id]["selected_config"]
        config_name = CONFIGS[selected_config_id]["name"]
        config_price = CONFIGS[selected_config_id]["price"]
        user_id = message.from_user.id

        # ایجاد دکمه‌های تایید و رد
        markup_admin = types.InlineKeyboardMarkup(row_width=2)
        btn_confirm = types.InlineKeyboardButton("✅ تایید", callback_data=f"admin_confirm_{user_id}")
        btn_reject = types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{user_id}")
        markup_admin.add(btn_confirm, btn_reject)

        # ارسال پیام به ادمین همراه با عکس و دکمه‌ها
        caption_admin = f"کاربر با آیدی {user_id} درخواست خرید حجم {config_name} به قیمت {config_price} تومان را دارد."
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption_admin, reply_markup=markup_admin)

        # اطلاع رسانی به کاربر
        bot.send_message(chat_id, "رسید شما دریافت شد. منتظر تایید ادمین باشید.")
        user_purchase_data[chat_id]["receipt_received"] = True
    else:
        bot.send_message(chat_id, "لطفاً ابتدا یک حجم را انتخاب کنید.")

# --- هندلر برای دکمه‌های تایید و رد ادمین ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_confirm_") or call.data.startswith("admin_reject_"))
def handle_admin_approval(call):
    admin_id = call.from_user.id
    if admin_id == ADMIN_ID:
        user_id_str = parts[1] + "_" + parts[2]
        user_id_to_process = int(user_id_str)
        print(f"Admin action: {action}, User ID to process: {user_id_to_process}, Current data: {user_purchase_data}") # لاگ اضافه شده

        if action == "admin_confirm":
            if user_id_to_process in user_purchase_data and "selected_config" in user_purchase_data[user_id_to_process] and "receipt_received" in user_purchase_data[user_id_to_process]:
                selected_config_id = user_purchase_data[user_id_to_process]["selected_config"]
                config_name = CONFIGS[selected_config_id]["name"]
                config_type = CONFIGS[selected_config_id]["type"]
                config_limit = CONFIGS[selected_config_id]["limit"]

                try:
                    session = requests.Session()
                    login_data = {"username": XUI_USERNAME, "password": XUI_PASSWORD}
                    session.post(f"{XUI_PANEL_URL}/login", data=login_data, verify=False)

                    add_client_data = {
                        "up": 0,
                        "down": 0,
                        "total": config_limit,
                        "expireDay": 0,
                        "listen": "",
                        "port": "",  # پورت اشتراکی
                        "protocol": "vless",
                        "settings": '{"clients": [{"id": "'+str(user_id_to_process)+'", "flow": "xtls-rprx-vision", "encryption": "none", "host": "", "port": 443, "path": "/"}], "decryption": "none", "fallbacks":}',
                        "streamSettings": '{"network": "ws", "security": "tls", "tlsSettings": {"alpn": ["h2", "http/1.1"], "serverName": "'+XUI_PANEL_URL.split("//")[1].split(":")[0]+'"}, "wsSettings": {"path": "/"}}',
                        "sniffing": False,
                        "server_id": "1", # ممکن است نیاز به تنظیم داشته باشد
                        "remark": f"{config_name} - UserID: {user_id_to_process}",
                        "enable": True
                    }
                    response = session.post(f"{XUI_PANEL_URL}/panel/api/inbound/addClient", json=add_client_data, verify=False)
                    response.raise_for_status()
                    result = response.json()

                    if result and result["success"]:
                        response = session.get(f"{XUI_PANEL_URL}/panel/api/inbound/list", params={"server_id": "1"}, verify=False)
                        response.raise_for_status()
                        inbounds = response.json()["obj"]
                        inbound_id = None
                        for inbound in inbounds:
                            if inbound["protocol"] == "vless" and inbound["streamSettings"]["network"] == "ws":
                                inbound_id = inbound["id"]
                                break

                        if inbound_id:
                            config_link = f"vless://{user_id_to_process}@{XUI_PANEL_URL.split('//')[1]}:443?path=%2F&security=tls&sni={XUI_PANEL_URL.split('//')[1].split(':')[0]}&type=ws# خریداری_شده"
                            bot.send_message(user_id_to_process, f"خرید شما تایید شد.\n\nکانفیگ {config_name} شما:\n`{config_link}`\n\nبا تشکر از خرید شما!", parse_mode="Markdown")
                            bot.answer_callback_query(call.id, f"خرید کاربر {user_id_to_process} با حجم {config_name} تایید و کانفیگ برای او ارسال شد.")
                            del user_purchase_data[user_id_to_process]
                        else:
                            bot.send_message(user_id_to_process, "متاسفانه در دریافت لینک کانفیگ مشکلی پیش آمده است. لطفاً به ادمین پیام دهید.")
                            bot.answer_callback_query(call.id, "خطا در دریافت لینک کانفیگ.")

                    else:
                        bot.send_message(user_id_to_process, "متاسفانه در ساخت کانفیگ مشکلی پیش آمده است. لطفاً به ادمین پیام دهید.")
                        bot.answer_callback_query(call.id, f"خطا در ساخت کانفیگ: {result.get('msg', 'بدون جزئیات')}")

                except requests.exceptions.RequestException as e:
                    bot.send_message(user_id_to_process, "متاسفانه در ارتباط با پنل مشکلی پیش آمده است. لطفاً به ادمین پیام دهید.")
                    bot.answer_callback_query(call.id, f"خطا در ارتباط با پنل XUI: {e}")
                except Exception as e:
                    bot.send_message(user_id_to_process, "متاسفانه یک خطای غیرمنتظره رخ داده است. لطفاً به ادمین پیام دهید.")
                    bot.answer_callback_query(call.id, f"خطای غیرمنتظره در تایید خرید: {e}")
            else:
                bot.answer_callback_query(call.id, "اطلاعات خرید این کاربر یافت نشد یا هنوز رسیدی ارسال نکرده است.")

        elif action == "admin_reject":
            print(f"Reject action for user ID: {user_id_to_process}") # لاگ اضافه شده قبل از شرط
            if user_id_to_process in user_purchase_data:
                print(f"User ID {user_id_to_process} found in user_purchase_data for rejection.") # لاگ اضافه شده
                bot.send_message(user_id_to_process, "متاسفانه خرید شما رد شد. برای اطلاعات بیشتر با ادمین تماس بگیرید.")
                bot.answer_callback_query(call.id, f"خرید کاربر {user_id_to_process} رد شد.")
                del user_purchase_data[user_id_to_process]
                print(f"User data for {user_id_to_process} deleted.") # لاگ اضافه شده بعد از حذف
            else:
                print(f"User ID {user_id_to_process} NOT found in user_purchase_data for rejection.") # لاگ اضافه شده
                bot.answer_callback_query(call.id, "اطلاعات خرید این کاربر یافت نشد.")
    else:
        bot.answer_callback_query(call.id, "شما مجوز انجام این کار را ندارید.")

# --- اجرای ربات ---
if __name__ == '__main__':
    print("ربات در حال اجرا است...")
    bot.polling(none_stop=True)
