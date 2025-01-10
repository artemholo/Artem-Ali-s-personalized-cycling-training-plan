import logging
from db_utils import connect_to_db, create_tables, clear_tables, insert_data
from csv_utils import load_csv, is_valid_date, is_valid_duration

# Logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    db_name = 'training_plan.db'
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    create_tables(cursor)
    clear_tables(cursor)

    # Load and validate data
    workouts = load_csv('workouts.csv', 6, [None, is_valid_date, is_valid_duration, None, None, None])
    inside_of_training = load_csv('inside_of_training.csv', 5, [None, is_valid_duration, None, None, None])
    workout_segments = load_csv('workout_segments.csv', 3)

    # Insert data
    try:
        cursor.execute("BEGIN TRANSACTION;")
        insert_data(cursor, "workouts", workouts, """
            INSERT INTO workouts (date, total_duration, training_type, heart_rate_zone, notes)
            VALUES (?, ?, ?, ?, ?);
        """)
        insert_data(cursor, "inside_of_training", inside_of_training, """
            INSERT INTO inside_of_training (segment_duration, segment_goal, intensity, notes)
            VALUES (?, ?, ?, ?);
        """)
        insert_data(cursor, "workout_segments", workout_segments, """
            INSERT INTO workout_segments (workout_id, template_id)
            VALUES (?, ?);
        """)
        cursor.execute("COMMIT;")
        logging.info("Transaction committed successfully.")
    except Exception as e:
        cursor.execute("ROLLBACK;")
        logging.error(f"Transaction rolled back: {e}")
    finally:
        conn.close()
