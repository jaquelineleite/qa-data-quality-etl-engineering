import os

import psycopg2


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "qa_data_quality"),
        user=os.getenv("DB_USER", "qa_user"),
        password=os.getenv("DB_PASSWORD", "qa_password"),
    )
