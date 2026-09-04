-- Data Quality: Uniqueness

SELECT
    cliente_id,
    COUNT(*) AS quantidade
FROM staging.clientes
GROUP BY cliente_id
HAVING COUNT(*) > 1;

SELECT
    transacao_id,
    COUNT(*) AS quantidade
FROM staging.transacoes
GROUP BY transacao_id
HAVING COUNT(*) > 1;
