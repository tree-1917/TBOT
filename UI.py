from telebot import types

# Function to show 'Start' button
def show_start_button():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton('🚀 أبدا')
    markup.add(start_button)
    return markup

# Function to show 'teacher' and 'student' options
def show_options():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn_teacher = types.KeyboardButton('👳 شيخ')
    itembtn_student = types.KeyboardButton('🧑‍🎓 طالب')
    return markup.add(itembtn_teacher, itembtn_student)

# Function to set up buttons for option 'teacher'
def setup_buttons_teacher():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🔼 أرفع محتوي')
    itembtn2 = types.KeyboardButton('❓ الأسئلة')
    itembtn3 = types.KeyboardButton('/restart')
    return  markup.add(itembtn1, itembtn2,itembtn3)


# Function to set up buttons for option 'student'
def setup_buttons_student():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('📚المواد')
    itembtn2 = types.KeyboardButton('📩 ارسل سؤال')
    itembtn3 = types.KeyboardButton('/restart')
    return  markup.add(itembtn1,itembtn2,itembtn3)


