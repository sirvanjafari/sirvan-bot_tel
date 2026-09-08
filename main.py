from your_keep_alive_file import keep_alive
keep_alive()
import telebot
from telebot import types
from g4f.client import Client
# --- تنظیمات اصلی ---
BOT_TOKEN = "888888888888888888888888888" 
bot = telebot.TeleBot(BOT_TOKEN)
client = Client()

SYSTEM_INSTRUCTION = (
    "نام تو 'سیروان‌بات' است. تو یک دستیار هوشمند بسیار باهوش و مودب هستی. "
    "اگر کسی پرسید چه کسی تو را ساخته، با افتخار بگو: "
    "'من توسط سیروان جعفری کجوری، دانش‌آموز و برنامه‌نویس عالی، ساخته شده‌ام'."
)

user_history = {}

def get_response_from_ai(messages):
    test_models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    for model in test_models:
        try:
            response = client.chat.completions.create(model=model, messages=messages)
            answer = response.choices[0].message.content
            if answer: return answer
        except: continue
    return None

# تابع ساخت دکمه‌های شیشه‌ای
def main_menu_markup():
    markup = types.InlineKeyboardMarkup()
    btn_about = types.InlineKeyboardButton("👨‍💻 درباره سازنده", callback_data='about_dev')
    btn_help = types.InlineKeyboardButton("❓ راهنما", callback_data='help_guide')
    btn_reset = types.InlineKeyboardButton("🧹 شروع بحث جدید", callback_data='reset_chat')
    
    # چیدمان دکمه‌ها
    markup.row(btn_about, btn_help)
    markup.row(btn_reset)
    return markup

@bot.message_handler(commands=['start', 'reset'])
def send_welcome(message):
    user_id = message.from_user.id
    user_history[user_id] = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    
    welcome_text = (
        "سلام! به **سیروان‌بات** خوش آمدی. 🚀\n\n"
        "من یک هوش مصنوعی هستم که توسط **سیروان جعفری** برنامه‌نویسی شده‌ام.\n"
        "چطور می‌توانم بهت کمک کنم؟"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_markup(), parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def about_cmd(message):
    bot.send_message(message.chat.id, "👨‍💻 این ربات توسط سیروان جعفری کجوری، دانش‌آموز و برنامه‌نویس با استعداد ساخته شده است.")

# مدیریت کلیک روی دکمه‌های شیشه‌ای
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    if call.data == "about_dev":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "سازنده من سیروان جعفری کجوری است؛ یک برنامه‌نویس عالی که من را برای کمک به شما طراحی کرده است! 🚀")
    
    elif call.data == "help_guide":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "کافیه هر سوالی داری (درسی، برنامه‌ریزی یا چت دوستانه) برام بنویسی تا جواب بدم. با دستور /reset هم می‌تونی حافظه‌ام رو پاک کنی.")
        
    elif call.data == "reset_chat":
        bot.answer_callback_query(call.id, "حافظه پاک شد! ✅")
        user_history[user_id] = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        bot.send_message(call.message.chat.id, "حافظه من پاک شد. موضوع جدید چیه؟")

@bot.message_handler(func=lambda message: True)
def handle_chat(message):
    user_id = message.from_user.id
    if user_id not in user_history:
        user_history[user_id] = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    
    user_history[user_id].append({"role": "user", "content": message.text})
    if len(user_history[user_id]) > 10:
        user_history[user_id] = [user_history[user_id][0]] + user_history[user_id][-5:]

    bot.send_chat_action(message.chat.id, 'typing')
    answer = get_response_from_ai(user_history[user_id])

    if answer:
        user_history[user_id].append({"role": "assistant", "content": answer})
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, "⚠️ سرورهای من کمی شلوغ هستند. لطفاً دوباره امتحان کن.")

if __name__ == "__main__":
    print("--- SirvanBot is Online with Buttons ---")
    bot.infinity_polling()
