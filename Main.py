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


def clear_tables(cursor):
    cursor.execute("DELETE FROM workouts")
    cursor.execute("DELETE FROM inside_of_training")
    cursor.execute("DELETE FROM workout_segments")


# Function to insert data
def insert_data(cursor, workouts, inside_of_training, workout_segments):
    cursor.executemany("""
    INSERT INTO workouts (date, total_duration, training_type, heart_rate_zone, notes)
    VALUES (?, ?, ?, ?, ?);
    """, workouts)

    cursor.executemany("""
    INSERT INTO inside_of_training (segment_duration, segment_goal, intensity, notes)
    VALUES (?, ?, ?, ?);
    """, inside_of_training)

    cursor.executemany("""
    INSERT INTO workout_segments(workout_id, template_id)
    VALUES(?, ?);
    """, workout_segments)


# Function to display tbl content
def print_table(cursor, table_name):
    print(f"\nContents of the table {table_name}:")
    cursor.execute(f"PRAGMA table_info({table_name})")
    headers = [col[1] for col in cursor.fetchall()]
    print(" | ".join(headers))
    cursor.execute(f"SELECT * FROM {table_name}")
    for row in cursor.fetchall():
        print(row)


# Main code
disk_conn = sqlite3.connect('training_plan.db')
cursor = disk_conn.cursor()

# Create tables
create_tables(cursor)

# Insert data
# into workouts
workouts = [
    ('2021-06-12', 'PT1H30M', 'Recovery', '2z lower limit',
     'Getting back into the training process'),
    ('2021-06-13', 'PT1H30M', 'Recovery - tone', '2z - 3z',
     'Getting back into the training process'),
    ('2021-06-14', 'PT1H30M', 'Recovery', '2z lower limit',
     'Getting back into the training process'),
    ('2021-06-17', 'PT1H30M', 'Recovery', '2z lower limit',
     'Getting back into the training process'),
    ('2021-06-15', 'PT1H30M', 'Recovery - tone', '2z - 6z',
     'Getting back into the training process'),
    ('2021-06-17', 'PT1H30M', 'Recovery', '2z lower limit',
     'Getting back into the training process'),
    ('2021-06-18', 'PT1H30M', 'Recovery', '2z lower limit',
     'Getting back into the training process'),
]

# Entrails of workouts
inside_of_training = [
    # 1
    ('PT15M', 'Softly', '1 zone', 'Spinning '),
    # 2
    ('PT70M', 'Easy', '2 zone', None),
    # 3
    ('PT5M', 'Leg over leg', '1 zone', 'Cool down'),
    # 4
    ('PT45M', 'Easy', '2 zone', None),
    # 5
    ('PT2M', 'Middling', '3 zone', 'Get a little involved'),
    # 6
    ('PT3M', "Easy", '1 zone - 2 zone', None),
    # 7
    ('PT0M15S', 'Speed-up', '6 zone', 'Get involved'),
    # 8
    ('PT1M45S', 'Easy', '1 zone - 2 zone', 'Recovery'),
    # 9
    ('PT30M', "Easy", '2 zone', None)
]

# Description workouts
workout_segments = [
    (1, 1),
    (1, 2),
    (1, 3),

    (2, 1),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 5),
    (2, 6),
    (2, 5),
    (2, 6),
    (2, 5),
    (2, 6),
    (2, 5),
    (2, 6),
    (2, 3),

    (3, 1),
    (3, 2),
    (3, 3),

    (4, 1),
    (4, 2),
    (4, 3),

    (5, 1),
    (5, 9),
    (5, 7),
    (5, 8),
    (5, 7),
    (5, 8),
    (5, 7),
    (5, 8),
    (5, 9),
    (5, 7),
    (5, 8),
    (5, 7),
    (5, 8),
    (5, 7),
    (5, 8),
    (5, 1),

    (6, 1),
    (6, 2),
    (6, 3),

    (7, 1),
    (7, 2),
    (7, 3),
]

create_tables(cursor)
clear_tables(cursor)

insert_data(cursor, workouts, inside_of_training, workout_segments)


def export_to_csv(cursor, table_name, filename):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]

    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)  # Write rows


# Export-save tbl
export_to_csv(cursor, "workouts", "workouts.csv")
export_to_csv(cursor, "inside_of_training", "inside_of_training.csv")
export_to_csv(cursor, "workout_segments", "workout_segments.csv")

# Commit and output
disk_conn.commit()
print_table(cursor, "workouts")
print_table(cursor, "inside_of_training")
print_table(cursor, "workout_segments")

# Close connection
disk_conn.close()