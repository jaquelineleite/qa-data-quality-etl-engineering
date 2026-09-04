CREATE TABLE IF NOT EXISTS warehouse.dim_cliente (
    cliente_sk BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    email VARCHAR(150),
    cidade VARCHAR(100),
    estado CHAR(2),
    data_cadastro TIMESTAMP
);

CREATE TABLE IF NOT EXISTS warehouse.dim_estabelecimento (
    estabelecimento_sk BIGSERIAL PRIMARY KEY,
    estabelecimento_id BIGINT NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_transacao (
    transacao_sk BIGSERIAL PRIMARY KEY,
    transacao_id BIGINT NOT NULL UNIQUE,

    cliente_sk BIGINT NOT NULL,
    estabelecimento_sk BIGINT NOT NULL,

    data_transacao TIMESTAMP NOT NULL,

    valor_bruto NUMERIC(15,2) NOT NULL,
    taxa NUMERIC(15,2) NOT NULL,
    valor_liquido NUMERIC(15,2) NOT NULL,

    status VARCHAR(30) NOT NULL,

    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fact_cliente
        FOREIGN KEY (cliente_sk)
        REFERENCES warehouse.dim_cliente(cliente_sk),

    CONSTRAINT fk_fact_estabelecimento
        FOREIGN KEY (estabelecimento_sk)
        REFERENCES warehouse.dim_estabelecimento(estabelecimento_sk)
);
