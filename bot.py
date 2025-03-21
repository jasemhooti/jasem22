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

        # ارسال پیام به ادمین
        caption_admin = f"کاربر با آیدی {chat_id} درخواست خرید حجم {config_name} به قیمت {config_price} تومان را دارد."
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption_admin)
        bot.send_message(ADMIN_ID, f"آیدی کاربر: {chat_id}")

        # اطلاع رسانی به کاربر
        bot.send_message(chat_id, "رسید شما دریافت شد. منتظر تایید ادمین باشید.")
        user_purchase_data[chat_id]["receipt_received"] = True
    else:
        bot.send_message(chat_id, "لطفاً ابتدا یک حجم را انتخاب کنید.")

# --- هندلر دستور تایید خرید برای ادمین ---
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and message.text.startswith("/confirm_"))
def confirm_purchase(message):
    try:
        user_id_to_confirm = int(message.text.split("_")[1])
        if user_id_to_confirm in user_purchase_data and "selected_config" in user_purchase_data[user_id_to_confirm] and "receipt_received" in user_purchase_data[user_id_to_confirm]:
            selected_config_id = user_purchase_data[user_id_to_confirm]["selected_config"]
            config_name = CONFIGS[selected_config_id]["name"]
            config_type = CONFIGS[selected_config_id]["type"]
            config_limit = CONFIGS[selected_config_id]["limit"]

            # --- قسمت ساخت کانفیگ در پنل XUI ---
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
                    "settings": '{"clients": [{"id": "'+str(user_id_to_confirm)+'", "flow": "xtls-rprx-vision", "encryption": "none", "host": "", "port": 443, "path": "/"}], "decryption": "none", "fallbacks":}',
                    "streamSettings": '{"network": "ws", "security": "tls", "tlsSettings": {"alpn": ["h2", "http/1.1"], "serverName": "'+XUI_PANEL_URL.split("//")[1].split(":")[0]+'"}, "wsSettings": {"path": "/"}}',
                    "sniffing": False,
                    "server_id": "1", # ممکن است نیاز به تنظیم داشته باشد
                    "remark": f"{config_name} - UserID: {user_id_to_confirm}",
                    "enable": True
                }
                response = session.post(f"{XUI_PANEL_URL}/panel/api/inbound/addClient", json=add_client_data, verify=False)
                response.raise_for_status()
                result = response.json()

                if result and result["success"]:
                    # --- دریافت اطلاعات کانفیگ ---
                    response = session.get(f"{XUI_PANEL_URL}/panel/api/inbound/list", params={"server_id": "1"}, verify=False)
                    response.raise_for_status()
                    inbounds = response.json()["obj"]
                    inbound_id = None
                    for inbound in inbounds:
                        if inbound["protocol"] == "vless" and inbound["streamSettings"]["network"] == "ws":
                            inbound_id = inbound["id"]
                            break

                    if inbound_id:
                        config_link = f"vless://{user_id_to_confirm}@{XUI_PANEL_URL.split('//')[1]}:443?path=%2F&security=tls&sni={XUI_PANEL_URL.split('//')[1].split(':')[0]}&type=ws# خریداری_شده"
                        bot.send_message(user_id_to_confirm, f"خرید شما تایید شد.\n\nکانفیگ {config_name} شما:\n`{config_link}`\n\nبا تشکر از خرید شما!", parse_mode="Markdown")
                        bot.send_message(ADMIN_ID, f"خرید کاربر {user_id_to_confirm} با حجم {config_name} تایید و کانفیگ برای او ارسال شد.")
                        del user_purchase_data[user_id_to_confirm]
                    else:
                        bot.send_message(user_id_to_confirm, "متاسفانه در دریافت لینک کانفیگ مشکلی پیش آمده است. لطفاً به ادمین پیام دهید.")
                        bot.send_message(ADMIN_ID, f"خطا در دریافت لینک کانفیگ برای کاربر {user_id_to_confirm}")

                else:
                    bot.send_message(user_id_to_confirm, "متاسفانه در ساخت کانفیگ مشکلی پیش آمده است. لطفاً به ادمین پیام دهید.")
                    bot.send_message(ADMIN_ID, f"خطا در ساخت کانفیگ برای کاربر {user_id_to_confirm}: {result.get('msg', 'بدون جزئیات')}")

            except requests.exceptions.RequestException as e:
                bot.send_message(user_id_to_confirm, "متاسفانه در ارتباط با پنل مشکلی پیش آمده است. لطفاً به ادمین پیام دهید.")
                bot.send_message(ADMIN_ID, f"خطا در ارتباط با پنل XUI برای کاربر {user_id_to_confirm}: {e}")
            except Exception as e:
                bot.send_message(user_id_to_confirm, "متاسفانه یک خطای غیرمنتظره رخ داده است. لطفاً به ادمین پیام دهید.")
                bot.send_message(ADMIN_ID, f"خطای غیرمنتظره در تایید خرید برای کاربر {user_id_to_confirm}: {e}")

        else:
            bot.send_message(ADMIN_ID, "اطلاعات خرید این کاربر یافت نشد یا هنوز رسیدی ارسال نکرده است.")
    except ValueError:
        bot.send_message(ADMIN_ID, "فرمت دستور تایید خرید اشتباه است. لطفاً از فرمت `/confirm_آیدی_کاربر` استفاده کنید.")

# --- اجرای ربات ---
if __name__ == '__main__':
    print("ربات در حال اجرا است...")
    bot.polling(none_stop=True)
