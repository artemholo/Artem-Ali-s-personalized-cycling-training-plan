import csv
import logging
import os
import re

# Regular expressions for validation
ISO_DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}$'
ISO_DURATION_PATTERN = r'^P(T(\d+H)?(\d+M)?(\d+S)?)$'


# Validate date format
def is_valid_date(date_str):
    return bool(re.match(ISO_DATE_PATTERN, date_str))


# Validate duration format
def is_valid_duration(duration_str):
    return bool(re.match(ISO_DURATION_PATTERN, duration_str))


# Loads data from a CSV file and validates rows
def load_csv(filename, expected_columns, validators=None):
    if not os.path.exists(filename):
        logging.error(f"File {filename} not found.")
        return []

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        data = []
        for row in reader:
            if len(row) != expected_columns:
                logging.warning(f"Invalid row length in {filename}: {row}")
                continue

            if validators and not all(validator(value) for validator, value in zip(validators, row)):
                logging.warning(f"Invalid data in {filename}: {row}")
                continue

            data.append(row[1:])  # Skip the "id" column
        return data