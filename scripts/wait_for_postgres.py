import time

import psycopg2

from scripts.database_connection import get_connection


MAX_ATTEMPTS = 30
WAIT_SECONDS = 2


def esperar_postgres():
    print("Waiting for PostgreSQL...")

    for tentativa in range(1, MAX_ATTEMPTS + 1):
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1;")
                    resultado = cursor.fetchone()

                    if resultado == (1,):
                        print(
                            f"PostgreSQL ready "
                            f"after {tentativa} attempt(s)."
                        )
                        return True

        except psycopg2.OperationalError:
            print(
                f"Attempt {tentativa}/"
                f"{MAX_ATTEMPTS}: database not ready."
            )

            time.sleep(WAIT_SECONDS)

    raise RuntimeError(
        "PostgreSQL did not become available "
        "within the expected time."
    )


if __name__ == "__main__":
    esperar_postgres()
