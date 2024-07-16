from telebot import TeleBot, types

# Function to show 'Start' button
def show_start_button():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton('Start')
    markup.add(start_button)
    return markup

# Function to show 'teacher' and 'student' options
def show_options():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn_teacher = types.KeyboardButton('teacher')
    itembtn_student = types.KeyboardButton('student')
    return markup.add(itembtn_teacher, itembtn_student)

# Function to set up buttons for option 'teacher'
def setup_buttons_teacher():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('upload topic')
    itembtn3 = types.KeyboardButton('/restart')
    return  markup.add(itembtn1, itembtn3)


# Function to set up buttons for option 'student'
def setup_buttons_student():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('topics')
    itembtn3 = types.KeyboardButton('/restart')
    return  markup.add(itembtn1, itembtn3)

