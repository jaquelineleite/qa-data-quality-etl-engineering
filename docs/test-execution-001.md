# Data Quality Test Execution 001

## Escopo

Validacao automatizada dos arquivos de clientes e transacoes antes do processamento ETL.

## Resultado

Total de testes: 12

Passed: 9

Failed: 3

Registros defeituosos unicos: 2

## Achados

### transacao_id 1004

Violacoes:

- valor_bruto deve ser maior que zero
- taxa nao deve superar valor_bruto

Defeito relacionado:

BUG-DATA-001

### transacao_id 1005

Violacao:

- status deve pertencer ao dominio permitido

Defeito relacionado:

BUG-DATA-002

## Conclusao

O Quality Gate identificou dados que nao devem seguir para a camada confiavel do Data Warehouse.

Os registros invalidos devem ser rejeitados ou encaminhados para uma area de quarentena antes da carga no destino.
