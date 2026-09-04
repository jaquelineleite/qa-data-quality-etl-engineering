/* Source-to-Target Reconciliation */

proc sql;

create table reconciliation as

select
    coalesce(a.transacao_id, b.transacao_id) as transacao_id,

    a.valor_bruto as valor_origem,
    b.valor_bruto as valor_destino,

    a.taxa as taxa_origem,
    b.taxa as taxa_destino

from source_transacoes a

full join target_transacoes b
    on a.transacao_id = b.transacao_id

where
       a.transacao_id is null
    or b.transacao_id is null
    or a.valor_bruto ne b.valor_bruto
    or a.taxa ne b.taxa;

quit;
