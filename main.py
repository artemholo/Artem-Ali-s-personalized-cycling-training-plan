import logging
import json
from db_utils import connect_to_db, create_tables, clear_tables, insert_data
from csv_utils import load_csv_with_pandas, is_valid_date, is_valid_duration, is_valid_number  # Добавил is_valid_number

# Load settings from config.json
with open("config.json") as f:
    config = json.load(f)

db_name = config["database"]
workouts_file = config["csv_files"]["workouts"]
inside_of_training_file = config["csv_files"]["inside_of_training"]
workout_segments_file = config["csv_files"]["workout_segments"]

# Logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def clear_tables(cursor):
    cursor.executescript("""
        DROP TABLE IF EXISTS workouts;
        DROP TABLE IF EXISTS inside_of_training;
        DROP TABLE IF EXISTS workout_segments;
    """)
    logging.info("Tables cleared successfully.")


def process_and_insert_data(cursor, table_name, file_path, expected_columns, validators, query):
    # Load, validate, and insert data from CSV into the database
    data = load_csv_with_pandas(file_path, expected_columns, validators)
    if not data:
        logging.warning(f"No valid data found in {file_path}. Skipping insertion.")
        return

    insert_data(cursor, table_name, data, query)


def main():
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    # Using PRAGMA to Speed Up SQLite
    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = WAL;")

    # Clear old tables and recreate them
    clear_tables(cursor)
    create_tables(cursor)

    # Process files
    try:
        cursor.execute("BEGIN TRANSACTION;")

        # Process workouts.csv
        process_and_insert_data(
            cursor,
            "workouts",
            workouts_file,  # variable from config.json
            7,
            [None, is_valid_date, is_valid_duration, is_valid_number, None, None, None],
            """
            INSERT INTO workouts (date, total_duration, distance, training_type, heart_rate_zone, notes)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
        )

        # Process inside_of_training.csv
        process_and_insert_data(
            cursor,
            "inside_of_training",
            inside_of_training_file,  # variable from config.json
            5,
            [None, is_valid_duration, None, None, None],
            """
            INSERT INTO inside_of_training (segment_duration, segment_goal, intensity, notes)
            VALUES (?, ?, ?, ?);
            """,
        )

        # Process workout_segments.csv
        process_and_insert_data(
            cursor,
            "workout_segments",
            workout_segments_file,  # variable from config.json
            3,
            None,
            """
            INSERT INTO workout_segments (workout_id, template_id)
            VALUES (?, ?);
            """,
        )

        cursor.execute("COMMIT;")
        logging.info("Data inserted successfully.")

    except Exception as e:
        cursor.execute("ROLLBACK;")
        logging.error(f"Transaction failed and rolled back: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()