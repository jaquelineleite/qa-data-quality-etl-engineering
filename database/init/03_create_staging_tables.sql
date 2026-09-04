CREATE TABLE IF NOT EXISTS staging.clientes (
    cliente_id BIGINT,
    nome VARCHAR(150),
    cpf VARCHAR(11),
    email VARCHAR(150),
    cidade VARCHAR(100),
    estado CHAR(2),
    data_cadastro TIMESTAMP,
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.estabelecimentos (
    estabelecimento_id BIGINT,
    nome VARCHAR(150),
    categoria VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.transacoes (
    transacao_id BIGINT,
    cliente_id BIGINT,
    estabelecimento_id BIGINT,
    data_transacao TIMESTAMP,
    valor_bruto NUMERIC(15,2),
    taxa NUMERIC(15,2),
    status VARCHAR(30),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
