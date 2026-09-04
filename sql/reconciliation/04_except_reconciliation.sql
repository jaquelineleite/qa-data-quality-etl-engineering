-- Set-based Reconciliation using EXCEPT

SELECT
    transacao_id,
    valor_bruto,
    taxa,
    UPPER(status) AS status
FROM staging.transacoes

EXCEPT

SELECT
    transacao_id,
    valor_bruto,
    taxa,
    status
FROM warehouse.fact_transacao;
