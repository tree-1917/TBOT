import telebot
from telebot import types

# Create an instance of the bot
bot = telebot.TeleBot("5788483192:AAF56JEcKQRgnquOvJBxzX99bWqY8q51NTU")

# Placeholder for the chat_id
chat_id = None

# Dictionary to store books with message IDs
source_with_message_ids = {}


# Handler for /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    global chat_id
    chat_id = message.chat.id
    remove_keyboard_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Click 'Start' to begin.", reply_markup=remove_keyboard_markup)
    show_start_button(chat_id)

# Handler for handling button 'Start'
@bot.message_handler(func=lambda message: message.text == 'Start')
def handle_start_button(message):
    global chat_id
    chat_id = message.chat.id
    show_options(chat_id)

# Handler for /restart command
@bot.message_handler(commands=['restart'])
def restart_chat(message):
    global chat_id
    chat_id = message.chat.id
    remove_keyboard_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "Chat has been reset. Please click 'Start' to begin again.", reply_markup=remove_keyboard_markup)
    handle_start(message)  # Call handle_start to display the 'Start' button

# Handler for handling button 'teacher'
@bot.message_handler(func=lambda message: message.text == 'teacher')
def handle_teacher(message):
    setup_buttons_teacher(message.chat.id)

# Handler for handling button 'student'
@bot.message_handler(func=lambda message: message.text == 'student')
def handle_student(message):
    setup_buttons_student(message.chat.id)

# Handler for handling button 'upload topic' by teacher
@bot.message_handler(func=lambda message: message.text == 'upload topic' and message.chat.id == chat_id)
def handle_upload_topic_teacher(message):
    bot.reply_to(message, "Please upload a PDF and provide a description with #book in your message.")

# Handler for handling button 'topics' by student
@bot.message_handler(func=lambda message: message.text == 'topics')
def handle_topics_student(message):
    global source_with_message_ids
    if source_with_message_ids:
        response = "Topics :\n"
        for source_id, details in source_with_message_ids.items():
            response += f"{details['name']} [{source_id}]\n"
    else:
        response = "No topics with PDFs available."
    bot.send_message(message.chat.id, response)

# Handler for storing books with message IDs
@bot.message_handler(content_types=['document', 'audio'])
def handle_media(message):
    if message.caption and '#light' in message.caption:
        try:
            # Extract source_id and source_name from the caption
            parts = message.caption.split("#")
            if len(parts) < 4:
                bot.reply_to(message, "Invalid format. Please include #light #Source_id #Source_name in your message.")
                return
            
            source_id = parts[2].strip()
            source_name = parts[3].strip()

            # Store the metadata in the dictionary
            source_with_message_ids[f"source_{source_id}"] = {
                'name': source_name,
                'message_id': message.message_id,
                'chat_id': message.chat.id,
                'type': message.content_type  # Store the type of content (document or audio)
            }

            # Debug print to verify the stored information
            print(source_with_message_ids)

            bot.reply_to(message, "Source uploaded and saved.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {str(e)}")
    else:
        bot.reply_to(message, "Please include #light #Source_id #Source_name in your message to save the source.")

# Handler for sending PDF when user clicks on book ID
@bot.message_handler(func=lambda message: message.text.startswith('source_'))
def send_source(message):
    source_id = message.text.strip()
    if source_id in source_with_message_ids:
        source_details = source_with_message_ids[source_id]
        bot.forward_message(message.chat.id, source_details['chat_id'], source_details['message_id'])
    else:
        bot.send_message(message.chat.id, "Invalid  ID.")

# Function to show 'Start' button
def show_start_button(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton('Start')
    markup.add(start_button)
    bot.send_message(chat_id, "Click 'Start' to begin.", reply_markup=markup)

# Function to show 'teacher' and 'student' options
def show_options(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn_teacher = types.KeyboardButton('teacher')
    itembtn_student = types.KeyboardButton('student')
    markup.add(itembtn_teacher, itembtn_student)
    bot.send_message(chat_id, "Choose 'teacher' or 'student':", reply_markup=markup)

# Function to set up buttons for option 'teacher'
def setup_buttons_teacher(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('upload topic')
    itembtn3 = types.KeyboardButton('/restart')
    markup.add(itembtn1, itembtn3)
    bot.send_message(chat_id, "Choose one:", reply_markup=markup)

# Function to set up buttons for option 'student'
def setup_buttons_student(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('topics')
    itembtn3 = types.KeyboardButton('/restart')
    markup.add(itembtn1, itembtn3)
    bot.send_message(chat_id, "Choose one:", reply_markup=markup)

# Run the bot
bot.infinity_polling()