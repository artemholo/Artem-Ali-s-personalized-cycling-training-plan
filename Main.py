import logging
from db_utils import connect_to_db, create_tables, clear_tables
from csv_utils import load_csv

# Logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Function to insert data
def insert_data(cursor, workouts, inside_of_training, workout_segments):
    # Insert data to db
    try:
        cursor.execute("BEGIN TRANSACTION;")

        if workouts:
            cursor.executemany(
                """
                INSERT INTO workouts (date, total_duration, training_type, heart_rate_zone, notes)
                VALUES (?, ?, ?, ?, ?);
                """,
                workouts
            )

        if inside_of_training:
            cursor.executemany(
                """
                INSERT INTO inside_of_training (segment_duration, segment_goal, intensity, notes)
                VALUES (?, ?, ?, ?);
                """,
                inside_of_training
            )

        if workout_segments:
            cursor.executemany(
                """
                INSERT INTO workout_segments (workout_id, template_id)
                VALUES (?, ?);
                """,
                workout_segments
            )

        cursor.execute("COMMIT;")
        logging.info("Data inserted successfully.")
    except Exception as e:
        cursor.execute("ROLLBACK;")
        logging.error(f"Error during data insertion: {e}")


def main():
    # Connect to db
    db_name = 'training_plan.db'
    conn = connect_to_db(db_name)
    cursor = conn.cursor()

    # Create tbl
    create_tables(cursor)

    # Check for the presence of data and clear it if necessary
    clear_tables(cursor)

    # Loading data from CSV
    workouts = load_csv('workouts.csv', 6)
    inside_of_training = load_csv('inside_of_training.csv', 5)
    workout_segments = load_csv('workout_segments.csv', 3)

    # Removing id column before insert
    workouts = [row[1:] for row in workouts]
    inside_of_training = [row[1:] for row in inside_of_training]
    workout_segments = [row[1:] for row in workout_segments]

    # Insert data
    insert_data(cursor, workouts, inside_of_training, workout_segments)

    # Saving changes
    conn.commit()
    logging.info("Database updated successfully.")
    conn.close()


if __name__ == "__main__":
    main()
