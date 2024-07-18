import telebot
from telebot import types
from dotenv import load_dotenv
import UI
import os
from database import insert_topic, insert_source, fetch_all_topics,fetch_all_sources, fetch_target_source,\
                     create_tables, check_topic,check_if_admin,insert_admin,insert_message,fetch_all_chats,\
                     fetch_all_messages_by_chat,delete_all_message_by_chat
# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN_API = os.getenv("TOKEN_API")
KEY = os.getenv("KEY")
SUPER_ADMIN_ID =os.getenv("SUPER_ADMIN_ID")

# Create tables if they do not exist
create_tables()

# Create an instance of the bot
bot = telebot.TeleBot(TOKEN_API)
chat_id = None
replies_id = []
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
@bot.message_handler(func=lambda message: message.text == '🚀 أبدا')
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
# ============================== #
# ======== Admin =============== # 
# ============================== #
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
# =============================== # 
# ======== Send Question ======== #
# Handler to process the user's message after they click /sendMessage
@bot.message_handler(commands=['sendMessage'])
def handle_send_message_command(message):
    bot.send_message(message.chat.id, "من فضلك أدخل رسالتك:")
    bot.register_next_step_handler(message, save_message)

# Function to save the user's message in the database
def save_message(message):
    try:
        sender_name = f'{message.chat.first_name} {message.chat.last_name}'
        chat_id = message.chat.id
        message_id = message.message_id
        # Insert message into the database
        insert_message(sender_name, chat_id, message_id)
        # Notify user that the message has been saved
        bot.send_message(message.chat.id, "تم حفظ رسالتك في قاعدة البيانات.") 
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Handler for the command that triggers the prompt in Arabic
@bot.message_handler(func=lambda message: message.text == '📩 ارسل سؤال')
def send_question_command(message):
    bot.send_message(message.chat.id, "اضغط هنا لإرسال سؤالك: /sendMessage")

# ================================== # 
# ========= Handle Question ======== # 
# Handler for show all sender to SUPER ADMIN
@bot.message_handler(func=lambda message: message.text == '❓ الأسئلة')
def send_senders_list(message): 
    # check Super admin 
    chat_id = message.chat.id
    if chat_id != int(SUPER_ADMIN_ID) : 
        bot.reply_to(message , "أنت لست المشرف الأعلى.")
        return 
    # fetch all senders 
    chats = fetch_all_chats()
    if chats:
        response = f"chats :\n"
        for chat in chats:
            response += f"{chat[0]} [/chat_{chat[1]}]\n"
    else:
        response =  "لا توجد محادثات."
    bot.send_message(message.chat.id, response)

# Handler for show all message from sender to SUPER ADMIN 
@bot.message_handler(func=lambda message: message.text.startswith('/chat_'))
def send_sender_massage(message):
    chat_id = message.chat.id
    if chat_id != int(SUPER_ADMIN_ID) : 
        bot.reply_to(message , "أنت لست المشرف الأعلى.")
        return  
    # show all message for Super Admin
    sender_chat_id = message.text.split("_")[1]
    sender_messages = fetch_all_messages_by_chat(sender_chat_id)
    if sender_messages : 
        for msg in sender_messages : 
            bot.copy_message(chat_id, from_chat_id=sender_chat_id, message_id=msg)
        # show send reply 
        bot.reply_to(message,f"I you want to reply him click /replay_{sender_chat_id} and to remove chat /remove_chat_{sender_chat_id}")
    else : 
        bot.send_message(chat_id, "لا توجد رسائل.")
    
# Handler to start replying process
@bot.message_handler(func=lambda message: message.text.startswith('/replay_'))
def reply_for_sender(message): 
    global replies_id
    chat_id = message.chat.id
    if chat_id != int(SUPER_ADMIN_ID) : 
        bot.reply_to(message , "أنت لست المشرف الأعلى.")
        return 
    # show message to reploy for user
    sender_chat_id = message.text.split("_")[1] 
    bot.reply_to(message, f'ستبدأ بإرسال الرد للمستخدم. جميع الرسائل لن تُرسل حتى تدخل /send_reply ولإزالة محادثة المستخدم من قاعدة البيانات /remove_chat_{sender_chat_id}')
    replies_id.append(sender_chat_id) # save in first the chat_id for user 
    bot.register_next_step_handler(message, collect_message)

# Handler to collect reply for start send replay for user  
def collect_message(message): 
    # check if user Enter /send_reply 
    if message.text == ("/send_reply"): 
        # call  send_reply_for_sender
        send_reply_for_sender(message)
        return # to end here  
    else : 
        replies_id.append(message.message_id) # save message id to send it after 
        bot.register_next_step_handler(message,collect_message)

# Handler for end send reply for user 
def send_reply_for_sender(message): 
    global replies_id
    chat_id = message.chat.id
    # send all message in replies to user 
    if replies_id : 
        sender_chat_id = replies_id[0] 
        for _reply_id in replies_id[1:] :
            bot.copy_message(sender_chat_id,from_chat_id=chat_id,message_id=_reply_id) 
    else : 
         bot.send_message(chat_id, "لا توجد رسائل.")
    bot.reply_to(message, f"إذا كنت ترغب في إزالة هذه المحادثة اضغط على /remove_chat_{sender_chat_id}")
    
# Handle remove message from user chat after reply it 
@bot.message_handler(func=lambda message: message.text.startswith('/remove_chat_'))
def remove_chat(message):
    global replies_id
    chat_id = message.chat.id
    if chat_id != int(SUPER_ADMIN_ID) : 
        bot.reply_to(message , "أنت لست المشرف الأعلى.")
        return # Handler for remove Sender message after reply on it 
    
    sender_chat_id = message.text.split('_')[2]
    # remove all replies for replies 
    replies_id.clear()
    # remove chat_id from database 
    try : 
        delete_all_message_by_chat(sender_chat_id)
        bot.reply_to(message, "تم بنجاح حذف جميع الرسائل من هذه المحادثة")
    except : 
        bot.reply_to(message, "معرف المحادثة غير صالح")

# ================================== #
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
            response += f"{topic_name} [/topic_{topic_id}]\n"
    else:
        response = "لا توجد مواضيع متاحة."
    
    bot.send_message(message.chat.id, response)

# Handler for storing sources with message IDs
@bot.message_handler(content_types=['document', 'audio','video'])
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
            if is_topic:  # if topic does not exist before
                insert_topic(topic_id, topic_name)
            insert_source(topic_id, source_id, source_name, message.message_id, message.chat.id, message.content_type)
            bot.reply_to(message, "✅ تم تحميل وحفظ المصدر.")
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")
    else:
        bot.reply_to(message, "❌ يرجى تضمين #اسم_الموضوع #معرف_الموضوع #معرف_المصدر #اسم_المصدر في رسالتك لحفظ المصدر.")

# Handler for sending sources based on source_id
@bot.message_handler(func=lambda message: message.text.startswith('/source_'))
def send_source(message):
    source_id = message.text.strip().split("_")[1]
    source = fetch_target_source(source_id)
    if source:
        bot.copy_message(chat_id=message.chat.id, from_chat_id=source[5], message_id=source[4], caption='')
    else:
        bot.send_message(message.chat.id, "❌ معرف غير صالح أو لا توجد مصادر.")

# Handler for displaying all sources in a topic based on topic_id
@bot.message_handler(func=lambda message: message.text.startswith('/topic_'))
def show_sources_in_topic(message):
    topic_id = message.text.strip().split('_')[1]
    sources = fetch_all_sources(topic_id)
    
    if sources:
        response = f"📚 مصادر الموضوع {topic_id}:\n"
        for source in sources:
            response += f"{source[1]} [/source_{source[0]}]\n"
    else:
        response = f"لا توجد مصادر للموضوع {topic_id}."
    bot.send_message(message.chat.id, response)

# Run the bot
if __name__ == "__main__":
    bot.polling()
