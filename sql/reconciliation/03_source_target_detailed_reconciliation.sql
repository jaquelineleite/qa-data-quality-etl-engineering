-- Source-to-Target Detailed Reconciliation

SELECT
    COALESCE(s.transacao_id, w.transacao_id) AS transacao_id,

    s.valor_bruto AS valor_bruto_origem,
    w.valor_bruto AS valor_bruto_destino,

    s.taxa AS taxa_origem,
    w.taxa AS taxa_destino,

    s.status AS status_origem,
    w.status AS status_destino,

    CASE
        WHEN s.transacao_id IS NULL THEN 'AUSENTE_NA_ORIGEM'
        WHEN w.transacao_id IS NULL THEN 'AUSENTE_NO_DESTINO'

        WHEN s.valor_bruto <> w.valor_bruto
            THEN 'DIVERGENCIA_VALOR_BRUTO'

        WHEN s.taxa <> w.taxa
            THEN 'DIVERGENCIA_TAXA'

        WHEN UPPER(s.status) <> w.status
            THEN 'DIVERGENCIA_STATUS'

        ELSE 'OK'
    END AS resultado_validacao

FROM staging.transacoes s

FULL OUTER JOIN warehouse.fact_transacao w
    ON s.transacao_id = w.transacao_id

WHERE
    s.transacao_id IS NULL
    OR w.transacao_id IS NULL
    OR s.valor_bruto <> w.valor_bruto
    OR s.taxa <> w.taxa
    OR UPPER(s.status) <> w.status;
