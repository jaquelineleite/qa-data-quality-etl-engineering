-- Data Quality: Validity and Business Rules

-- Valor bruto deve ser maior que zero
SELECT *
FROM staging.transacoes
WHERE valor_bruto <= 0;

-- Taxa não pode ser negativa
SELECT *
FROM staging.transacoes
WHERE taxa < 0;

-- Taxa não pode superar valor bruto
SELECT *
FROM staging.transacoes
WHERE taxa > valor_bruto;

-- Status permitido
SELECT *
FROM staging.transacoes
WHERE status NOT IN (
    'APROVADA',
    'NEGADA',
    'CANCELADA'
);
