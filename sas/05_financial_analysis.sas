/* Analise financeira */

proc means data=work.transacoes
    n
    sum
    mean
    min
    max;

    var valor_bruto taxa;

run;
