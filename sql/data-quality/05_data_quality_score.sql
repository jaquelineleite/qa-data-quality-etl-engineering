-- Data Quality Score

WITH total AS (
    SELECT COUNT(*) AS total_registros
    FROM staging.transacoes
),

invalidos AS (
    SELECT COUNT(*) AS total_invalidos
    FROM staging.transacoes
    WHERE
        transacao_id IS NULL
        OR cliente_id IS NULL
        OR estabelecimento_id IS NULL
        OR data_transacao IS NULL
        OR valor_bruto IS NULL
        OR valor_bruto <= 0
        OR taxa IS NULL
        OR taxa < 0
        OR status IS NULL
        OR status NOT IN (
            'APROVADA',
            'NEGADA',
            'CANCELADA'
        )
)

SELECT
    t.total_registros,
    i.total_invalidos,
    t.total_registros - i.total_invalidos AS registros_validos,

    ROUND(
        (
            (t.total_registros - i.total_invalidos)::NUMERIC
            /
            NULLIF(t.total_registros, 0)
        ) * 100,
        2
    ) AS data_quality_score

FROM total t
CROSS JOIN invalidos i;
