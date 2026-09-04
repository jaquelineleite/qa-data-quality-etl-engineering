/* Data Quality - Completeness */

proc sql;

select *
from work.clientes
where cliente_id is missing
   or nome is missing
   or cpf is missing;

quit;
