-- Source-to-Target Record Count Reconciliation

SELECT
    (SELECT COUNT(*) FROM staging.transacoes) AS quantidade_origem,
    (SELECT COUNT(*) FROM warehouse.fact_transacao) AS quantidade_destino,
    (SELECT COUNT(*) FROM staging.transacoes)
      -
    (SELECT COUNT(*) FROM warehouse.fact_transacao) AS diferenca;
