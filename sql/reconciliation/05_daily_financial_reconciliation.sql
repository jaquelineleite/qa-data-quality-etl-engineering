-- Daily Financial Reconciliation

WITH origem AS (
    SELECT
        DATE(data_transacao) AS data,
        COUNT(*) AS quantidade,
        SUM(valor_bruto) AS valor_bruto,
        SUM(taxa) AS taxa
    FROM staging.transacoes
    GROUP BY DATE(data_transacao)
),

destino AS (
    SELECT
        DATE(data_transacao) AS data,
        COUNT(*) AS quantidade,
        SUM(valor_bruto) AS valor_bruto,
        SUM(taxa) AS taxa,
        SUM(valor_liquido) AS valor_liquido
    FROM warehouse.fact_transacao
    GROUP BY DATE(data_transacao)
)

SELECT
    COALESCE(o.data, d.data) AS data,

    o.quantidade AS quantidade_origem,
    d.quantidade AS quantidade_destino,

    o.valor_bruto AS bruto_origem,
    d.valor_bruto AS bruto_destino,

    o.taxa AS taxa_origem,
    d.taxa AS taxa_destino,

    d.valor_liquido,

    CASE
        WHEN o.quantidade = d.quantidade
         AND o.valor_bruto = d.valor_bruto
         AND o.taxa = d.taxa
        THEN 'OK'
        ELSE 'DIVERGENCIA'
    END AS resultado

FROM origem o

FULL OUTER JOIN destino d
    ON o.data = d.data

ORDER BY data;
