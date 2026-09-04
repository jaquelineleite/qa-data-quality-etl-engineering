/* Business Rules Validation */

proc sql;

select *
from work.transacoes
where valor_bruto <= 0;

select *
from work.transacoes
where taxa < 0;

select *
from work.transacoes
where status not in (
    'APROVADA',
    'NEGADA',
    'CANCELADA'
);

quit;
