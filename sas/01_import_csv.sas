/* Importacao de clientes a partir de CSV */

proc import datafile="data/raw/csv/clientes.csv"
    out=work.clientes
    dbms=csv
    replace;
    getnames=yes;
run;

proc print data=work.clientes(obs=10);
run;
