-- Financial Reconciliation

SELECT
    'STAGING' AS camada,
    COUNT(*) AS quantidade,
    SUM(valor_bruto) AS total_valor_bruto,
    SUM(taxa) AS total_taxa
FROM staging.transacoes

UNION ALL

SELECT
    'WAREHOUSE' AS camada,
    COUNT(*) AS quantidade,
    SUM(valor_bruto) AS total_valor_bruto,
    SUM(taxa) AS total_taxa
FROM warehouse.fact_transacao;
