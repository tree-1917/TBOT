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
            FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
        )
    ''')

    conn.commit()
    close_connection(conn, cursor)

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
    cursor.execute('''
        SELECT source_id, source_name FROM sources WHERE topic_id = ?
    ''', (topic_id,))
    sources = cursor.fetchall()
    close_connection(conn, cursor)
    return sources

# Function to fetch a specific source by source_id
def fetch_target_source(source_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM sources WHERE source_id = ?
    ''', (source_id,))
    source = cursor.fetchone()
    conn.close()
    return source    
