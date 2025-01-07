import csv
import logging
import os


# Loads data from a CSV file and validates the number of columns
def load_csv(filename, expected_columns):
    if not os.path.exists(filename):
        logging.error(f"File {filename} not found.")
        return []

    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header


        for row in reader:
            if len(row) == expected_columns:
                data.append(row)  # Skip the "id" column
            else:
                logging.warning(f"Invalid row in {filename}: {row}")
    return data
