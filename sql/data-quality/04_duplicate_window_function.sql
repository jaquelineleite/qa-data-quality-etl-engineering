-- Advanced Data Quality
-- Identificação de duplicidades usando Window Function

WITH registros AS (
    SELECT
        transacao_id,
        cliente_id,
        estabelecimento_id,
        data_transacao,
        valor_bruto,
        taxa,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY transacao_id
            ORDER BY data_carga DESC
        ) AS rn
    FROM staging.transacoes
)

SELECT *
FROM registros
WHERE rn > 1;
