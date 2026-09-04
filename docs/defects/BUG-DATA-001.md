# BUG-DATA-001

## Titulo

ETL permite transacao com valor bruto negativo.

## Severidade

High

## Prioridade

High

## Registro

transacao_id: 1004

## Resultado encontrado

valor_bruto = -120.00

status = APROVADA

## Resultado esperado

Transacoes financeiras devem possuir valor_bruto maior que zero.

O registro deve ser rejeitado ou direcionado para area de quarentena.

## Impacto

Dados financeiros inconsistentes podem afetar:

- conciliacao
- indicadores financeiros
- relatorios
- faturamento
- analytics

## Evidencia

Arquivo:

data/raw/json/transacoes.json

## Regra violada

valor_bruto > 0
