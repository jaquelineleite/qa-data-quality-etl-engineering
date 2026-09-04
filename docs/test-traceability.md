# Test Traceability

Este projeto utiliza uma matriz de rastreabilidade para relacionar requisitos, critérios de qualidade, testes automatizados, evidências e defeitos.

O modelo foi estruturado para representar práticas comuns de gestão de testes utilizadas com ferramentas como Jira, Xray e Octane.

> Este repositório não possui integração real com Jira, Xray ou Octane. A estrutura demonstra como os artefatos podem ser organizados e migrados para essas ferramentas.

## Fluxo de rastreabilidade

Requirement
↓
Acceptance Criteria
↓
Automated Test
↓
CI/CD Execution
↓
Evidence
↓
Defect

## Artefatos

- `docs/traceability-matrix.json`: matriz de rastreabilidade estruturada.
- `docs/acceptance-criteria.md`: critérios de aceite.
- `docs/test-plan.md`: planejamento dos testes.
- `docs/data-mapping.md`: mapeamento Source-to-Target.
- `docs/test-execution-001.md`: evidência de execução.
- `docs/defects/`: defeitos documentados.
- `.github/workflows/data-quality-ci.yml`: execução automatizada no CI/CD.

## Defeitos rastreados

### BUG-DATA-001

Transação com valor bruto inválido detectada pelas validações de Data Quality e Quality Gate.

### BUG-DATA-002

Transação contendo status fora do domínio permitido detectada pelas validações automatizadas.

## Test Management

A matriz pode ser utilizada como base para cadastro em ferramentas de gestão de qualidade:

- Jira: requisito, história e defeito;
- Xray: Test, Test Execution e Test Plan;
- Octane: Requirement, Test, Run e Defect.

A rastreabilidade também é validada automaticamente pelo Pytest para impedir referências a artefatos inexistentes no repositório.
