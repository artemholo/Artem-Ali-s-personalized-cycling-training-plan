import unittest
from csv_utils import load_csv_with_pandas, is_valid_date, is_valid_duration, is_valid_number
from db_utils import connect_to_db, create_tables, clear_tables, insert_data


class TestCSVUtils(unittest.TestCase):
    def test_valid_date(self):
        self.assertTrue(is_valid_date("2021-06-12"))
        self.assertFalse(is_valid_date("2021/06/12"))

    def test_valid_duration(self):
        self.assertTrue(is_valid_duration("PT1H30M"))
        self.assertFalse(is_valid_duration("1:30"))

    def test_valid_number(self):
        self.assertTrue(is_valid_number("50"))
        self.assertTrue(is_valid_number("50.5"))
        self.assertFalse(is_valid_number("abc"))


def db_connection():
    conn = connect_to_db(":memory:")
    cursor = conn.cursor()
    create_tables(cursor)
    yield cursor
    conn.close()


def test_insert_data(db_connection):
    data = [("2021-06-12", "PT1H30M", 50, "Recovery", "2z lower limit", "Getting back")]
    insert_data(db_connection, "workouts", data, """
        INSERT INTO workouts (date, total_duration, distance, training_type, heart_rate_zone, notes)
        VALUES (?, ?, ?, ?, ?, ?);
    """)
    db_connection.execute("SELECT * FROM workouts;")
    assert len(db_connection.fetchall()) == 1
