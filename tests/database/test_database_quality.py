from scripts.database_connection import get_connection


def consultar_valor(query):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]


def test_source_deve_conter_cinco_transacoes():
    total = consultar_valor(
        "SELECT COUNT(*) FROM source.transacoes;"
    )

    assert total == 5


def test_staging_deve_conter_tres_transacoes_validas():
    total = consultar_valor(
        "SELECT COUNT(*) FROM staging.transacoes;"
    )

    assert total == 3


def test_warehouse_deve_conter_tres_transacoes():
    total = consultar_valor(
        "SELECT COUNT(*) FROM warehouse.fact_transacao;"
    )

    assert total == 3


def test_warehouse_nao_deve_conter_registros_invalidos():
    total = consultar_valor(
        """
        SELECT COUNT(*)
        FROM warehouse.fact_transacao
        WHERE transacao_id IN (1004, 1005);
        """
    )

    assert total == 0


def test_valor_liquido_deve_respeitar_transformacao():
    total = consultar_valor(
        """
        SELECT COUNT(*)
        FROM warehouse.fact_transacao
        WHERE valor_liquido <> valor_bruto - taxa;
        """
    )

    assert total == 0


def test_status_deve_pertencer_ao_dominio():
    total = consultar_valor(
        """
        SELECT COUNT(*)
        FROM warehouse.fact_transacao
        WHERE status NOT IN (
            'APROVADA',
            'NEGADA',
            'CANCELADA'
        );
        """
    )

    assert total == 0


def test_source_e_staging_devem_ter_dois_registros_de_diferenca():
    diferenca = consultar_valor(
        """
        SELECT
            (SELECT COUNT(*) FROM source.transacoes)
            -
            (SELECT COUNT(*) FROM staging.transacoes);
        """
    )

    assert diferenca == 2


def test_staging_e_warehouse_devem_estar_reconciliados():
    diferenca = consultar_valor(
        """
        SELECT
            (SELECT COUNT(*) FROM staging.transacoes)
            -
            (SELECT COUNT(*) FROM warehouse.fact_transacao);
        """
    )

    assert diferenca == 0
