import pandas as pd
import logging
import re

# Regular expressions for validation
ISO_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
ISO_DURATION_PATTERN = r"^P(T(\d+H)?(\d+M)?(\d+S)?)?$"
NUMBER_PATTERN = r"^\d+(\.\d+)?$"


# Validate date format
def is_valid_date(date_str):
    return bool(re.match(ISO_DATE_PATTERN, date_str))


# Validate duration format
def is_valid_duration(duration_str):
    return bool(re.match(ISO_DURATION_PATTERN, duration_str))


# Number validation (distance)
def is_valid_number(number_str):
    return bool(re.match(NUMBER_PATTERN, number_str))


# Loads data from a CSV file using Pandas and validates rows
def load_csv_with_pandas(file_path, expected_columns, validators=None):
    try:
        df = pd.read_csv(file_path, dtype=str, encoding="utf-8", on_bad_lines="skip", keep_default_na=False)

        if df.empty:
            logging.warning(f"Файл {file_path} пуст!")
        else:
            logging.info(f"Загружено строк: {len(df)}")

        if len(df.columns) != expected_columns:
            logging.error(f"Ошибка в {file_path}: ожидалось {expected_columns} колонок, найдено {len(df.columns)}.")
            return []

        if validators:
            for i, validator in enumerate(validators):
                if validator is not None:
                    df.iloc[:, i] = df.iloc[:, i].astype(str)  # ✅ Преобразуем все данные в строки перед валидацией
                    df.iloc[:, i] = df.iloc[:, i].apply(lambda x: x if validator(x) else None)

            df.dropna(inplace=True)

        return df.iloc[:, 1:].values.tolist()
    except Exception as e:
        logging.error(f"Ошибка загрузки {file_path}: {e}")
        return []