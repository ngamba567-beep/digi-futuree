import os
import telebot
import requests
import phonenumbers
from phonenumbers import geocoder, carrier

# 1. Initialize your bot using your Token
# For security, we look for an environment variable. If missing, paste yours as a string.
BOT_TOKEN = os.environ.get("BOT_TOKEN", "PASTE_YOUR_TELEGRAM_TOKEN_HERE")
bot = telebot.TeleBot(8895397749: AAFN8P4ZS9560jj4P11z_bJ-
BcvQiZTVCtA)

# --- START COMMAND ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🔍 *Welcome to the OSINT Framework Bot* 🔍\n\n"
        "Available modules:\n"
        "▶️ `/ip <address>` - Geolocate an IP address.\n"
        "▶️ `/phone <number>` - Scan a phone number (include country code, e.g., +1234567890).\n\n"
        "*Always perform lookups legally and ethically.*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# --- MODULE 1: IP GEOLOCATION ---
@bot.message_handler(commands=['ip'])
def osint_ip(message):
    # Extract the IP address from the command
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Please provide an IP address. Example: `/ip 8.8.8.8`", parse_mode="Markdown")
        return

    target_ip = args[1]
    bot.reply_to(message, f"📡 Scanning IP: `{target_ip}`... Please wait.", parse_mode="Markdown")

    try:
        # Query the ip-api service (Free, no API key required for basic use)
        response = requests.get(f"http://ip-api.com/json/{target_ip}").json()
        
        if response.get("status") == "fail":
            bot.reply_to(message, f"❌ Failed to resolve IP: {response.get('message', 'Unknown error')}")
            return

        # Format the OSINT intelligence report
        report = (
            f"🌐 *IP OSINT REPORT* 🌐\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📍 *Target:* `{response.get('query')}`\n"
            f"🏢 *ISP:* {response.get('isp')}\n"
            f"🏢 *Organization:* {response.get('org')}\n"
            f"🏳️ *Country:* {response.get('country')} ({response.get('countryCode')})\n"
            f"🏙️ *Region/City:* {response.get('regionName')} / {response.get('city')}\n"
            f"🧭 *Coordinates:* `{response.get('lat')}, {response.get('lon')}`\n"
            f"⏰ *Timezone:* {response.get('timezone')}\n"
        )
        bot.reply_to(message, report, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"💥 An internal error occurred during lookup: {str(e)}")

# --- MODULE 2: PHONE NUMBER VALIDATOR ---
@bot.message_handler(commands=['phone'])
def osint_phone(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Please provide a phone number with country code. Example: `/phone +14155552671`", parse_mode="Markdown")
        return

    target_phone = " ".join(args[1:]) # Combine arguments in case they left spaces
    bot.reply_to(message, f"📱 Analyzing phone record: `{target_phone}`...", parse_mode="Markdown")

    try:
        # Parse number using Google's phonenumbers library
        parsed_number = phonenumbers.parse(target_phone, None)
        
        if not phonenumbers.is_valid_number(parsed_number):
            bot.reply_to(message, "❌ Invalid phone number format or country code.")
            return

        # Gather intelligence strings
        location = geocoder.description_for_number(parsed_number, "en")
        operator = carrier.name_for_number(parsed_number, "en")
        
        report = (
            f"📱 *PHONE OSINT REPORT* 📱\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 *Format International:* {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\n"
            f"🏳️ *Derived Location:* {location if location else 'Unknown'}\n"
            f"📡 *Original Carrier:* {operator if operator else 'Unknown / Landline'}\n"
        )
        bot.reply_to(message, report, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"💥 Failed to parse phone number: {str(e)}")

# --- START POLLING LOOP ---
if __name__ == "__main__":
    print("🤖 Bot is waking up... Press Ctrl+C to stop.")
    bot.infinity_polling()
