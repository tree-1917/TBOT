# Back.py
import telebot
from telebot import types
from dotenv import load_dotenv
import UI
import os
from database import insert_topic, insert_source, fetch_all_topics, fetch_all_sources, fetch_target_source, create_tables, check_topic, check_source

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN_API = os.getenv("TOKEN_API")

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
    bot.send_message(chat_id, "👋 Hello Again", reply_markup=remove_keyboard_markup)
    markup = UI.show_start_button() # Create UI 
    bot.send_message(chat_id, "🚀 Click 'Start' to begin.", reply_markup=markup)

# Handler for handling button 'Start'
@bot.message_handler(func=lambda message: message.text == 'Start')
def handle_start_button(message):
    global chat_id
    chat_id = message.chat.id
    markup = UI.show_options() # Create UI 
    bot.send_message(chat_id, "👩‍🏫 Choose 'teacher' or 👨‍🎓 'student':", reply_markup=markup)
    

# Handler for /restart command
@bot.message_handler(commands=['restart'])
def restart_chat(message):
    global chat_id
    chat_id = message.chat.id
    remove_keyboard_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "🔄 Chat has been reset. Please click 'Start' to begin again.", reply_markup=remove_keyboard_markup)
    handle_start(message)  # Call handle_start to display the 'Start' button

# Handler for handling button 'teacher'
@bot.message_handler(func=lambda message: message.text == 'teacher')
def handle_teacher(message):
    global chat_id
    chat_id = message.chat.id
    markup = UI.setup_buttons_teacher() # Create UI 
    bot.send_message(chat_id, "📋 Choose one:", reply_markup=markup)

# Handler for handling button 'student'
@bot.message_handler(func=lambda message: message.text == 'student')
def handle_student(message):
    global chat_id
    chat_id = message.chat.id
    markup = UI.setup_buttons_student()
    bot.send_message(chat_id, "📋 Choose one:", reply_markup=markup)

# Handler for handling button 'upload topic' by teacher
@bot.message_handler(func=lambda message: message.text == 'upload topic' and message.chat.id == chat_id)
def handle_upload_topic_teacher(message):
    bot.reply_to(message, "📄 Please upload a PDF and provide a description with #topic_name #topic_id #Source_id #Source_name in your message.")

# Handler for handling button 'topics' by student
@bot.message_handler(func=lambda message: message.text == 'topics')
def handle_topics_student(message):
    topics = fetch_all_topics()
    
    if topics:
        response = "📚 Topics:\n"
        for topic_name, topic_id in topics:
            response += f"{topic_name} [topic_{topic_id}]\n"
    else:
        response = "No topics available."
    
    bot.send_message(message.chat.id, response)

# Handler for storing sources with message IDs
@bot.message_handler(content_types=['document', 'audio'])
def handle_media(message):
    if message.caption :
        try:
            parts = message.caption.split("#")
            if len(parts) < 5:
                bot.reply_to(message, "❌ Invalid format. Please include #topic_name #topic_id #source_id #source_name in your message.")
                return
            
            topic_name = parts[1].strip()  
            topic_id = parts[2].strip()
            source_id = parts[3].strip()
            source_name = parts[4].strip()

            # Insert into SQLite database using database.py functions
            is_topic =  check_topic(topic_id)
            if is_topic :  # if topic not exists before 
                insert_topic(topic_id, topic_name)
            insert_source(topic_id, source_id, source_name, message.message_id, message.chat.id, message.content_type) 
            bot.reply_to(message, "✅ Source uploaded and saved.")
        except Exception as e:
            bot.reply_to(message, f"❌ An error occurred: {str(e)}")
    else:
        bot.reply_to(message, "❌ Please include #topic_name #topic_id #source_id #source_name in your message to save the source.")

# Handler for sending sources based on source_id
@bot.message_handler(func=lambda message: message.text.startswith('source_'))
def send_source(message):
    source_id = message.text.strip().split("_")[1]
    source = fetch_target_source(source_id)
    if source:
        bot.forward_message(message.chat.id, source[5], source[4])
    else:
        bot.send_message(message.chat.id, "❌ Invalid ID or no sources found.")

# Handler for displaying all sources in a topic based on topic_id
@bot.message_handler(func=lambda message: message.text.startswith('topic_'))
def show_sources_in_topic(message):
    topic_id = message.text.strip().split('_')[1]
    sources = fetch_all_sources(topic_id)
    
    if sources:
        response = f"📚 Sources for Topic {topic_id}:\n"
        for source in sources:
            response += f"{source[1]} [source_{source[0]}]\n"
    else:
        response = f"No sources found for Topic {topic_id}."
    bot.send_message(message.chat.id, response)

# Run the bot
bot.infinity_polling()

