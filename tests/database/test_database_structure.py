from scripts.database_connection import get_connection


def executar_query(query):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def test_schema_source_deve_existir():
    resultado = executar_query(
        """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name = 'source';
        """
    )
    assert resultado == [("source",)]


def test_schema_staging_deve_existir():
    resultado = executar_query(
        """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name = 'staging';
        """
    )
    assert resultado == [("staging",)]


def test_schema_warehouse_deve_existir():
    resultado = executar_query(
        """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name = 'warehouse';
        """
    )
    assert resultado == [("warehouse",)]


def test_fact_transacao_deve_existir():
    resultado = executar_query(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'warehouse'
          AND table_name = 'fact_transacao';
        """
    )
    assert resultado == [("fact_transacao",)]


def test_dim_cliente_deve_existir():
    resultado = executar_query(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'warehouse'
          AND table_name = 'dim_cliente';
        """
    )
    assert resultado == [("dim_cliente",)]


def test_dim_estabelecimento_deve_existir():
    resultado = executar_query(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'warehouse'
          AND table_name = 'dim_estabelecimento';
        """
    )
    assert resultado == [("dim_estabelecimento",)]
