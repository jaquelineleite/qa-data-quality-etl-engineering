CREATE TABLE IF NOT EXISTS source.clientes (
    cliente_id BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    email VARCHAR(150),
    cidade VARCHAR(100),
    estado CHAR(2),
    data_cadastro TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS source.estabelecimentos (
    estabelecimento_id BIGINT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2)
);

CREATE TABLE IF NOT EXISTS source.transacoes (
    transacao_id BIGINT PRIMARY KEY,
    cliente_id BIGINT,
    estabelecimento_id BIGINT,
    data_transacao TIMESTAMP NOT NULL,
    valor_bruto NUMERIC(15,2) NOT NULL,
    taxa NUMERIC(15,2) NOT NULL,
    status VARCHAR(30) NOT NULL,

    CONSTRAINT fk_source_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES source.clientes(cliente_id),

    CONSTRAINT fk_source_estabelecimento
        FOREIGN KEY (estabelecimento_id)
        REFERENCES source.estabelecimentos(estabelecimento_id)
);
