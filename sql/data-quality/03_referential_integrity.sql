-- Data Quality: Referential Integrity

SELECT t.*
FROM staging.transacoes t
LEFT JOIN staging.clientes c
    ON t.cliente_id = c.cliente_id
WHERE c.cliente_id IS NULL;

SELECT t.*
FROM staging.transacoes t
LEFT JOIN staging.estabelecimentos e
    ON t.estabelecimento_id = e.estabelecimento_id
WHERE e.estabelecimento_id IS NULL;
