# UI.py

from telebot import TeleBot, types
import Back  # Import the backend module

# Function to show 'Start' button
def show_start_button(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton('Start')
    markup.add(start_button)
    Back.bot.send_message(chat_id, "🚀 Click 'Start' to begin.", reply_markup=markup)

# Function to show 'teacher' and 'student' options
def show_options(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn_teacher = types.KeyboardButton('teacher')
    itembtn_student = types.KeyboardButton('student')
    markup.add(itembtn_teacher, itembtn_student)
    Back.bot.send_message(chat_id, "👩‍🏫 Choose 'teacher' or 👨‍🎓 'student':", reply_markup=markup)

# Function to set up buttons for option 'teacher'
def setup_buttons_teacher(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('upload topic')
    itembtn3 = types.KeyboardButton('/restart')
    markup.add(itembtn1, itembtn3)
    Back.bot.send_message(chat_id, "📋 Choose one:", reply_markup=markup)

# Function to set up buttons for option 'student'
def setup_buttons_student(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('topics')
    itembtn3 = types.KeyboardButton('/restart')
    markup.add(itembtn1, itembtn3)
    Back.bot.send_message(chat_id, "📋 Choose one:", reply_markup=markup)
