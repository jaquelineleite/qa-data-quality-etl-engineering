# BUG-DATA-002

## Titulo

Transacao carregada com status fora do dominio permitido.

## Severidade

Medium

## Prioridade

High

## Registro afetado

transacao_id: 1005

## Resultado encontrado

status = STATUS_INVALIDO

## Resultado esperado

O campo status deve aceitar apenas:

- APROVADA
- NEGADA
- CANCELADA

Registros com valores fora do dominio devem ser rejeitados ou enviados para quarentena.

## Impacto

Um status invalido pode gerar:

- classificacao incorreta de transacoes
- divergencias em relatorios
- erros em indicadores
- inconsistencias em conciliacao
- falhas em processos downstream

## Evidencia

Arquivo:

data/raw/json/transacoes.json

Teste automatizado:

tests/data-quality/test_transacoes_quality.py

## Regra violada

status IN ('APROVADA', 'NEGADA', 'CANCELADA')
