import sqlite3
import logging


# Connecting to a SQLite db
def connect_to_db(db_name):
    return sqlite3.connect(db_name)


# Creating tbl and indexes in a db
def create_tables(cursor):
    # Tbl training
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            total_duration TEXT,
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_workouts_date ON workouts (date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_workouts_type ON workouts (training_type);")

    logging.info("Tables and indexes created successfully.")


# Stop infinite incrementation of id with each program run
def clear_tables(cursor):
    cursor.executescript("""
        DELETE FROM workouts;
        DELETE FROM inside_of_training;
        DELETE FROM workout_segments;
    """)
    logging.info("Tables cleared successfully.")
