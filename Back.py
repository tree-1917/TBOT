import telebot
from telebot import types
from dotenv import load_dotenv
import UI
import os
from database import insert_topic, insert_source, fetch_all_topics, fetch_all_sources, fetch_target_source, create_tables, check_topic,check_if_admin,insert_admin
# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN_API = os.getenv("TOKEN_API")
KEY = os.getenv("KEY")

# Create tables if they do not exist
create_tables()

# Create an instance of the bot
bot = telebot.TeleBot(TOKEN_API)
chat_id = None

# Handler for /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    global chat_id
    chat_id = message.chat.id
    remove_keyboard_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "👋 مرحبًا مجددًا", reply_markup=remove_keyboard_markup)
    markup = UI.show_start_button()  # Create UI
    bot.send_message(chat_id, "🚀 اضغط على 'ابدأ' للبدء.", reply_markup=markup)

# Handler for handling button 'Start'
@bot.message_handler(func=lambda message: message.text == 'أبدا')
def handle_start_button(message):
    global chat_id
    chat_id = message.chat.id
    markup = UI.show_options()  # Create UI
    bot.send_message(chat_id, "👳 اختر 'شيخ' أو 👨‍🎓 'طالب':", reply_markup=markup)

# Handler for /restart command
@bot.message_handler(commands=['restart'])
def restart_chat(message):
    global chat_id
    chat_id = message.chat.id
    remove_keyboard_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "🔄 تم إعادة ضبط الدردشة. يرجى الضغط على 'ابدأ' للبدء مجددًا.", reply_markup=remove_keyboard_markup)
    handle_start(message)  # Call handle_start to display the 'Start' button
# Handle Admin Level
@bot.message_handler(commands=['addAdmin'])
def add_admin(message): 
    global chat_id 
    chat_id = message.chat.id
    bot.send_message(chat_id, "🚫 أدخل المفتاح السري لإضافة نفسك كمسؤول:")
    bot.register_next_step_handler(message, ask_for_admin_key)
# Register Admin
def ask_for_admin_key(message):
    if message.text == KEY :
        bot.send_message(message.chat.id, "✅ مفتاح صحيح. أرسل اسمك لإضافتك كمسؤول:")
        bot.register_next_step_handler(message, save_admin)
    else:
        bot.send_message(message.chat.id, "❌ مفتاح غير صحيح. يرجى المحاولة مرة أخرى.")
        handle_start(message)
# Save Admin 
def save_admin(message):
    admin_name = message.text
    chat_id = message.chat.id
    insert_admin(admin_name, chat_id)
    bot.send_message(chat_id, f"✅ تمت إضافتك كمسؤول، {admin_name}.")
    handle_teacher(message)

# Handler for handling button 'teacher'
@bot.message_handler(func=lambda message: message.text == '👳 شيخ')
def handle_teacher(message):
    global chat_id
    chat_id = message.chat.id
    markup = UI.setup_buttons_teacher()  # Create UI
    bot.send_message(chat_id, "📋 اختر واحدًا:", reply_markup=markup)

# Handler for handling button 'student'
@bot.message_handler(func=lambda message: message.text == '🧑‍🎓 طالب')
def handle_student(message):
    global chat_id
    chat_id = message.chat.id
    markup = UI.setup_buttons_student()
    bot.send_message(chat_id, "📋 اختر واحدًا:", reply_markup=markup)

# Handler for handling button 'upload topic' by teacher
@bot.message_handler(func=lambda message: message.text == '🔼 أرفع محتوي' and message.chat.id == chat_id)
def handle_upload_topic_teacher(message):
    bot.reply_to(message, "📄 يرجى تحميل ملف PDF وتقديم وصف مع #اسم_الموضوع #معرف_الموضوع #معرف_المصدر #اسم_المصدر في رسالتك.")

# Handler for handling button 'topics' by student
@bot.message_handler(func=lambda message: message.text == '📚المواد')
def handle_topics_student(message):
    topics = fetch_all_topics()
    
    if topics:
        response = "📚 المواضيع:\n"
        for topic_name, topic_id in topics:
            response += f"{topic_name} [topic_{topic_id}]\n"
    else:
        response = "لا توجد مواضيع متاحة."
    
    bot.send_message(message.chat.id, response)

# Handler for storing sources with message IDs
@bot.message_handler(content_types=['document', 'audio'])
def handle_media(message):
    # == CHECK IF ADMIN === # 
    is_admin = check_if_admin(message.chat.id)
    if not is_admin:
        bot.reply_to(message, "أنت لست مسؤولًا لهذا. يجب أن تكون مسؤولًا للقيام بذلك. يرجى النقر على /addAdmin لبدء العملية.")  # Reply in Arabic
        return
    # ===================== # 
    if message.caption:
        try:
            parts = message.caption.split("#")
            if len(parts) < 5:
                bot.reply_to(message, "❌ تنسيق غير صالح. يرجى تضمين #اسم_الموضوع #معرف_الموضوع #معرف_المصدر #اسم_المصدر في رسالتك.")
                return
            
            topic_name = parts[1].strip()
            topic_id = parts[2].strip()
            source_id = parts[3].strip()
            source_name = parts[4].strip()

            # Insert into SQLite database using database.py functions
            is_topic = check_topic(topic_id)
            if not is_topic:  # if topic does not exist before
                insert_topic(topic_id, topic_name)
            insert_source(topic_id, source_id, source_name, message.message_id, message.chat.id, message.content_type)
            bot.reply_to(message, "✅ تم تحميل وحفظ المصدر.")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")
    else:
        bot.reply_to(message, "❌ يرجى تضمين #اسم_الموضوع #معرف_الموضوع #معرف_المصدر #اسم_المصدر في رسالتك لحفظ المصدر.")

# Handler for sending sources based on source_id
@bot.message_handler(func=lambda message: message.text.startswith('source_'))
def send_source(message):
    source_id = message.text.strip().split("_")[1]
    source = fetch_target_source(source_id)
    if source:
        bot.copy_message(chat_id=message.chat.id, from_chat_id=source[5], message_id=source[4], caption='')
    else:
        bot.send_message(message.chat.id, "❌ معرف غير صالح أو لا توجد مصادر.")

# Handler for displaying all sources in a topic based on topic_id
@bot.message_handler(func=lambda message: message.text.startswith('topic_'))
def show_sources_in_topic(message):
    topic_id = message.text.strip().split('_')[1]
    sources = fetch_all_sources(topic_id)
    
    if sources:
        response = f"📚 مصادر الموضوع {topic_id}:\n"
        for source in sources:
            response += f"{source[1]} [source_{source[0]}]\n"
    else:
        response = f"لا توجد مصادر للموضوع {topic_id}."
    bot.send_message(message.chat.id, response)

# Run the bot
bot.infinity_polling()
