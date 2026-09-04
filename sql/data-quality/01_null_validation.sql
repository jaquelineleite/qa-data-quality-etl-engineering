-- Data Quality: Completeness

SELECT *
FROM staging.clientes
WHERE cliente_id IS NULL
   OR nome IS NULL
   OR cpf IS NULL
   OR data_cadastro IS NULL;

SELECT *
FROM staging.transacoes
WHERE transacao_id IS NULL
   OR cliente_id IS NULL
   OR estabelecimento_id IS NULL
   OR data_transacao IS NULL
   OR valor_bruto IS NULL
   OR taxa IS NULL
   OR status IS NULL;
