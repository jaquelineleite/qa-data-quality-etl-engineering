/* Data Quality - Validacao de duplicidades */

proc sql;

select
    cliente_id,
    count(*) as quantidade
from work.clientes
group by cliente_id
having count(*) > 1;

quit;
