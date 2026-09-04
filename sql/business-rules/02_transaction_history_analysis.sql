-- Advanced SQL
-- Análise histórica de transações utilizando LAG

WITH historico AS (
    SELECT
        cliente_id,
        transacao_id,
        data_transacao,
        valor_bruto,

        LAG(valor_bruto) OVER (
            PARTITION BY cliente_id
            ORDER BY data_transacao
        ) AS valor_transacao_anterior

    FROM staging.transacoes
)

SELECT
    cliente_id,
    transacao_id,
    data_transacao,
    valor_bruto,
    valor_transacao_anterior,
    valor_bruto - valor_transacao_anterior AS diferenca
FROM historico
ORDER BY cliente_id, data_transacao;
