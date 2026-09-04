-- ETL Transformation Validation
-- Regra:
-- valor_liquido = valor_bruto - taxa

SELECT
    transacao_id,
    valor_bruto,
    taxa,
    valor_liquido,
    valor_bruto - taxa AS valor_liquido_esperado
FROM warehouse.fact_transacao
WHERE valor_liquido <> valor_bruto - taxa;
