import sqlite3
import logging


# Connecting to a SQLite db
def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    logging.info(f"Connected to database {db_name}")
    return conn


# Creating tbl and indexes in a db
def create_tables(cursor):
    # Tbl training
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            total_duration TEXT,
            distance REAL,
            training_type TEXT,
            heart_rate_zone TEXT,
            notes TEXT
        );
    """)
    # Tbl task list
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inside_of_training (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            segment_duration TEXT,
            segment_goal TEXT,
            intensity TEXT,
            notes TEXT
        );
    """)
    # Tbl that links itself to the inside_of_training
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER,
            template_id INTEGER,
            FOREIGN KEY (workout_id) REFERENCES workouts(id),
            FOREIGN KEY (template_id) REFERENCES inside_of_training(id)
        );
    """)
    logging.info("Tables and indexes created successfully.")


# Stop infinite incrementation of id with each program run
def clear_tables(cursor):
    cursor.executescript("""
        DELETE FROM workouts;
        DELETE FROM inside_of_training;
        DELETE FROM workout_segments;
    """)
    logging.info("Tables cleared successfully.")


# Inserting data into the database
def insert_data(cursor, table_name, data, query):
    try:
        cursor.executemany(query, data)
        logging.info(f"Data inserted into {table_name} successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error inserting data into {table_name}: {e}")
        raise
