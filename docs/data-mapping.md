# Source-to-Target Data Mapping

| Source | Campo Origem | Destino | Campo Destino | Transformacao |
|---|---|---|---|---|
| source.clientes | cliente_id | warehouse.dim_cliente | cliente_id | direta |
| source.clientes | nome | warehouse.dim_cliente | nome | TRIM |
| source.clientes | cpf | warehouse.dim_cliente | cpf | somente numeros |
| source.transacoes | transacao_id | warehouse.fact_transacao | transacao_id | direta |
| source.transacoes | data_transacao | warehouse.fact_transacao | data_transacao | direta |
| source.transacoes | valor_bruto | warehouse.fact_transacao | valor_bruto | direta |
| source.transacoes | taxa | warehouse.fact_transacao | taxa | direta |
| source.transacoes | valor_bruto + taxa | warehouse.fact_transacao | valor_liquido | valor_bruto - taxa |
| source.transacoes | status | warehouse.fact_transacao | status | UPPER |
