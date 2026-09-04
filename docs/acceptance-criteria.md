# Acceptance Criteria

## Clientes

1. cliente_id deve ser unico.
2. nome deve ser obrigatorio.
3. cpf deve possuir 11 caracteres.
4. estado deve possuir 2 caracteres.
5. data_cadastro deve possuir formato de data valido.

## Transacoes

1. transacao_id deve ser unico.
2. cliente_id deve existir na base de clientes.
3. estabelecimento_id deve existir na base de estabelecimentos.
4. valor_bruto deve ser maior que zero.
5. taxa deve ser maior ou igual a zero.
6. taxa nao pode ser superior ao valor_bruto.
7. status deve pertencer ao dominio:
   - APROVADA
   - NEGADA
   - CANCELADA

## Data Warehouse

valor_liquido deve ser calculado por:

valor_liquido = valor_bruto - taxa

## Reconciliacao

A quantidade de registros validos carregados no destino deve corresponder a quantidade de registros validos da origem.

Os valores financeiros agregados devem possuir correspondencia entre origem e destino.
