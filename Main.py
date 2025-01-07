import sqlite3
import logging
import csv

logging.basicConfig(level=logging.INFO)


# Function to create tbl
def create_tables(cursor):
    # Tbl training
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,                 -- Training date
        total_duration TEXT,       -- Total training time (ISO 8601)
        training_type TEXT,        -- Type of training (ex "Recovery", "Interval")
        heart_rate_zone TEXT,      -- Pulse zone
        notes TEXT                 -- additional notes
);
""")

    # Tbl task list
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inside_of_training (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        segment_duration TEXT,     -- Total duration of the training segment (ISO 8601)
        segment_goal TEXT,         -- The goal of training and the abstract effort that the athlete applies
        intensity TEXT,            -- Pulse zone
        notes TEXT                 -- Comments and explanations
);
""")

    # Tbl that links itself to the inside_of_training
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER,
        template_id INTEGER,       -- Link to training task template of the tbl inside_of_training
        FOREIGN KEY (workout_id) REFERENCES workouts(id),
        FOREIGN KEY (template_id) REFERENCES inside_of_training(id)
);
""")


# Stop infinite incrementation of id with each program run
def clear_tables(cursor):
    cursor.execute("DELETE FROM workouts")
    cursor.execute("DELETE FROM inside_of_training")
    cursor.execute("DELETE FROM workout_segments")


def load_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропустить заголовок
        return [row for row in reader]


# Function to insert data
def insert_data(cursor, workouts, inside_of_training, workout_segments):
    cursor.executemany(
        "INSERT INTO workouts (date, total_duration, training_type, heart_rate_zone, notes) VALUES (?, ?, ?, ?, ?);",
        workouts)
    cursor.executemany(
        "INSERT INTO inside_of_training (segment_duration, segment_goal, intensity, notes) VALUES (?, ?, ?, ?);",
        inside_of_training)
    cursor.executemany("INSERT INTO workout_segments(workout_id, template_id) VALUES (?, ?);", workout_segments)


# Main code
disk_conn = sqlite3.connect('training_plan.db')
cursor = disk_conn.cursor()

# Create tables
create_tables(cursor)
clear_tables(cursor)

workouts = load_csv('workouts.csv')
inside_of_training = load_csv('inside_of_training.csv')
workout_segments = load_csv('workout_segments.csv')

insert_data(cursor, workouts, inside_of_training, workout_segments)

disk_conn.commit()
logging.info("Data successfully added and saved.")

disk_conn.close()
