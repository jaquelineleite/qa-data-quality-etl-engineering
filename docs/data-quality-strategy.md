# Data Quality Strategy

## Objetivo

Garantir a qualidade, consistência, integridade e confiabilidade dos dados processados pelo pipeline ETL.

## Dimensoes de Qualidade

### Completeness
Validar se campos obrigatorios possuem valores preenchidos.

### Accuracy
Validar se os dados representam corretamente as regras de negocio.

### Consistency
Garantir consistencia entre dados de origem, staging e destino.

### Uniqueness
Identificar registros duplicados em campos considerados unicos.

### Validity
Validar formatos, dominios e valores permitidos.

### Referential Integrity
Garantir que relacionamentos entre entidades sejam validos.

### Reconciliation
Comparar quantitativos e valores agregados entre origem e destino.

## Abordagem Shift Left

As regras de qualidade devem ser definidas durante o refinamento dos requisitos.

Para cada requisito devem existir:

- criterio de aceite
- regra de negocio
- regra de qualidade
- risco associado
- evidencia esperada

## Automacao

As validacoes criticas devem ser automatizadas e executadas no pipeline CI/CD.

Categorias:

- schema validation
- null validation
- duplicate validation
- referential integrity
- business rules
- source-to-target reconciliation
- transformation rules
