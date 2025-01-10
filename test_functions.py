import unittest
from csv_utils import load_csv, is_valid_date, is_valid_duration
from db_utils import connect_to_db, create_tables, clear_tables, insert_data

class TestCSVUtils(unittest.TestCase):
    def test_valid_date(self):
        self.assertTrue(is_valid_date("2021-06-12"))
        self.assertFalse(is_valid_date("2021/06/12"))

    def test_valid_duration(self):
        self.assertTrue(is_valid_duration("PT1H30M"))
        self.assertFalse(is_valid_duration("1:30"))

    def test_load_csv(self):
        data = load_csv('workouts.csv', 6)
        self.assertGreater(len(data), 0)

class TestDBUtils(unittest.TestCase):
    def setUp(self):
        self.conn = connect_to_db(":memory:")
        self.cursor = self.conn.cursor()
        create_tables(self.cursor)

    def tearDown(self):
        self.conn.close()

    def test_insert_data(self):
        data = [("2021-06-12", "PT1H30M", "Recovery", "2z lower limit", "Getting back")]
        insert_data(self.cursor, "workouts", data, """
            INSERT INTO workouts (date, total_duration, training_type, heart_rate_zone, notes)
            VALUES (?, ?, ?, ?, ?);
        """)
        self.cursor.execute("SELECT * FROM workouts;")
        self.assertEqual(len(self.cursor.fetchall()), 1)