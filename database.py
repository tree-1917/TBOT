import sqlite3

# Function to establish a database connection
def connect_db():
    conn = sqlite3.connect('telegram_bot.db')
    return conn

# Function to close the SQLite connection
def close_connection(conn, cursor):
    cursor.close()
    conn.close()

# Function to create tables if they do not exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY,
            topic_id TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            UNIQUE(topic_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY,
            topic_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            source_name TEXT NOT NULL,
            message_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
            UNIQUE (topic_id, source_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            admin_name TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            UNIQUE(chat_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY, 
            sender_name TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL
        )            
    ''')
    conn.commit()
    close_connection(conn, cursor)

# Function to query Check Topic
def check_topic(topic_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT topic_name FROM topics WHERE topic_id = ?', (topic_id,))
    topic = cursor.fetchone()
    conn.commit() 
    close_connection(conn, cursor)
    return False if topic else True 

# Function to Check Source
def check_source(source_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT source_name FROM sources WHERE source_id = ?', (source_id,))
    source = cursor.fetchone()
    conn.commit() 
    close_connection(conn, cursor)
    return False if source else True 

# Function to insert a new topic into the topics table
def insert_topic(topic_id, topic_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO topics (topic_id, topic_name) VALUES (?, ?)', (topic_id, topic_name))
    conn.commit()
    close_connection(conn, cursor)

# Function to insert a new source into the sources table
def insert_source(topic_id, source_id, source_name, message_id, chat_id, type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sources (topic_id, source_id, source_name, message_id, chat_id, type) VALUES (?, ?, ?, ?, ?, ?)',
                   (topic_id, source_id, source_name, message_id, chat_id, type))
    conn.commit()
    close_connection(conn, cursor)

# Function to insert a new admin into the admins table
def insert_admin(admin_name, chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO admins (admin_name, chat_id) VALUES (?, ?)', (admin_name, chat_id))
    conn.commit()
    close_connection(conn, cursor)

# Function to check if a user is an admin
def check_if_admin(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT admin_name FROM admins WHERE chat_id = ?', (chat_id,))
    admin = cursor.fetchone()
    conn.commit()
    close_connection(conn, cursor)
    return True if admin else False

# Function to fetch all topics
def fetch_all_topics():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT topic_name, topic_id FROM topics')
    topics = cursor.fetchall()
    close_connection(conn, cursor)
    return topics

# Function to fetch all sources for a given topic_id
def fetch_all_sources(topic_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT source_id, source_name FROM sources WHERE topic_id = ?', (topic_id,))
    sources = cursor.fetchall()
    close_connection(conn, cursor)
    return sources

# Function to fetch a specific source by source_id
def fetch_target_source(source_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sources WHERE source_id = ?', (source_id,))
    source = cursor.fetchone()
    close_connection(conn,cursor)
    return source

# Function to insert a new message 
def insert_message(sender_name,chat_id,message_id):
    conn = connect_db() 
    cursor = conn.cursor() 
    cursor.execute('INSERT INTO messages (sender_name, chat_id, message_id) VALUES (?, ?, ?)', (sender_name, chat_id, message_id))
    conn.commit() 
    close_connection(conn,cursor)

# Function to fetch all senders 
def fetch_all_chats():
    conn = connect_db() 
    cursor = conn.cursor() 
    cursor.execute('SELECT sender_name,chat_id FROM messages GROUP BY chat_id')
    chats = cursor.fetchall()
    close_connection(conn,cursor)
    return chats

# Function to fethc All message
def fetch_all_messages_by_chat(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT message_id FROM messages WHERE chat_id = ?",(chat_id,))
    messages = cursor.fetchall()
    close_connection(conn,cursor)
    return messages

# Function to delete All message After reply it 
def delete_all_message_by_chat(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE chat_id = ?',(chat_id,))
    conn.commit() 
    close_connection(conn,cursor) 