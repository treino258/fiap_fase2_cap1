-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.347.1153
--   em:        2025-04-14 13:16:02 BRT
--   site:      Oracle Database 12c
--   tipo:      Oracle Database 12c



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE ajusteaplicacao (
    id_ajuste                  INTEGER NOT NULL,
    propriedade_id_propriedade INTEGER NOT NULL,
    tipoajuste_id_tipo_ajuste  INTEGER NOT NULL,
    data_hora_ajuste           TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    quantidade_aplicada        NUMBER(10, 2) NOT NULL
);

COMMENT ON COLUMN ajusteaplicacao.id_ajuste IS
    'identitadade de registro de uma ação como de irrigação ou aplicação de nutriente para manter os dados guardados';

COMMENT ON COLUMN ajusteaplicacao.quantidade_aplicada IS
    'quantidade de agua/produto';

ALTER TABLE ajusteaplicacao ADD CONSTRAINT ajusteaplicacao_pk PRIMARY KEY ( id_ajuste );

CREATE TABLE campo (
    id_campo                    INTEGER NOT NULL,
    identificador               VARCHAR2(100) NOT NULL,
    area_hectares               NUMBER,
    localizacao_geo             mdsys.sdo_geometry,
    propriedade_id_propriedade1 INTEGER NOT NULL
);

COMMENT ON COLUMN campo.identificador IS
    'Nome do lote, ex: lota A1 ou Campo norte';

COMMENT ON COLUMN campo.area_hectares IS
    'tamanho da area';

COMMENT ON COLUMN campo.localizacao_geo IS
    'por exemplo coordenada';

ALTER TABLE campo ADD CONSTRAINT campo_pk PRIMARY KEY ( id_campo );

ALTER TABLE campo ADD CONSTRAINT campo_identificador_un UNIQUE ( identificador );

CREATE TABLE cultura (
    id_cultura INTEGER NOT NULL,
    nome       VARCHAR2(100) NOT NULL
);

COMMENT ON COLUMN cultura.id_cultura IS
    'numero de indentificação da cultura';

COMMENT ON COLUMN cultura.nome IS
    'ex: milho, soja, cafe, cana';

ALTER TABLE cultura ADD CONSTRAINT cultura_pk PRIMARY KEY ( id_cultura );

CREATE TABLE leiturasensor (
    id_leitura        INTEGER NOT NULL,
    sensor_id_sensor  INTEGER NOT NULL,
    data_hora_leitura TIMESTAMP WITH TIME ZONE NOT NULL,
    valor_lido        NUMBER(12, 4) NOT NULL
);

COMMENT ON COLUMN leiturasensor.id_leitura IS
    'identidade da leitura';

COMMENT ON COLUMN leiturasensor.data_hora_leitura IS
    'data e hota que captou a leitura';

COMMENT ON COLUMN leiturasensor.valor_lido IS
    'o valor lido como numero, podendo ser ph,humidade e etc';

ALTER TABLE leiturasensor ADD CONSTRAINT leiturasensor_pk PRIMARY KEY ( id_leitura );

CREATE TABLE plantio (
    id_plantio                 INTEGER NOT NULL,
    propriedade_id_propriedade INTEGER NOT NULL,
    cultura_id_cultura         INTEGER NOT NULL,
    data_inicio_plantio        DATE NOT NULL,
    data_fim_plantio           DATE
);

COMMENT ON COLUMN plantio.id_plantio IS
    'Associa um cultura a um campo por um periodo';

ALTER TABLE plantio ADD CONSTRAINT plantio_pk PRIMARY KEY ( id_plantio );

CREATE TABLE propriedade (
    id_propriedade1  INTEGER NOT NULL,
    nome_propriedade VARCHAR2(100)
);

ALTER TABLE propriedade ADD CONSTRAINT propriedade_pk PRIMARY KEY ( id_propriedade1 );

CREATE TABLE sensor (
    id_sensor                 INTEGER NOT NULL,
    tiposensor_id_tipo_sensor INTEGER NOT NULL,
    codigo_identificacao      VARCHAR2(100),
    data_instalacao           DATE NOT NULL,
    status                    VARCHAR2(20) NOT NULL,
    campo_id_campo            INTEGER NOT NULL
);

COMMENT ON COLUMN sensor.id_sensor IS
    'numero de identificação do sensor';

COMMENT ON COLUMN sensor.codigo_identificacao IS
    'numero de serie do sensor( para identificar seu hardware e tudo mais)';

COMMENT ON COLUMN sensor.data_instalacao IS
    'a data de instalaçao do sensor';

COMMENT ON COLUMN sensor.status IS
    'ativo, inativo, manutenção';

ALTER TABLE sensor ADD CONSTRAINT sensor_pk PRIMARY KEY ( id_sensor );

CREATE TABLE tipoajuste (
    id_tipo_ajuste INTEGER NOT NULL,
    descricao      VARCHAR2(100) NOT NULL,
    unidade_medida VARCHAR2(20)
);

COMMENT ON COLUMN tipoajuste.id_tipo_ajuste IS
    'identidade do que foi realizado na plantação';

COMMENT ON COLUMN tipoajuste.descricao IS
    'descrição do que foi feito ex: irrigação, aplicação de P ou aplicação de K';

COMMENT ON COLUMN tipoajuste.unidade_medida IS
    'litros, kg, ml';

ALTER TABLE tipoajuste ADD CONSTRAINT tipoajuste_pk PRIMARY KEY ( id_tipo_ajuste );

CREATE TABLE tiposensor (
    id_tipo_sensor INTEGER NOT NULL,
    nome           VARCHAR2(100) NOT NULL,
    unidade_medida VARCHAR2(20)
);

COMMENT ON COLUMN tiposensor.id_tipo_sensor IS
    'o ID para indentificar do sensor';

COMMENT ON COLUMN tiposensor.nome IS
    'nome do sensor ( umidade, ph, nutriente p, nutriente K )';

COMMENT ON COLUMN tiposensor.unidade_medida IS
    'se é em % ph , litros e etc';

ALTER TABLE tiposensor ADD CONSTRAINT tiposensor_pk PRIMARY KEY ( id_tipo_sensor );

ALTER TABLE ajusteaplicacao
    ADD CONSTRAINT ajusteaplicacao_propriedade_fk FOREIGN KEY ( propriedade_id_propriedade )
        REFERENCES campo ( id_campo );

ALTER TABLE ajusteaplicacao
    ADD CONSTRAINT ajusteaplicacao_tipoajuste_fk FOREIGN KEY ( tipoajuste_id_tipo_ajuste )
        REFERENCES tipoajuste ( id_tipo_ajuste );

ALTER TABLE campo
    ADD CONSTRAINT campo_propriedade_fk FOREIGN KEY ( propriedade_id_propriedade1 )
        REFERENCES propriedade ( id_propriedade1 );

ALTER TABLE leiturasensor
    ADD CONSTRAINT leiturasensor_sensor_fk FOREIGN KEY ( sensor_id_sensor )
        REFERENCES sensor ( id_sensor );

ALTER TABLE sensor
    ADD CONSTRAINT sensor_campo_fk FOREIGN KEY ( campo_id_campo )
        REFERENCES campo ( id_campo );

ALTER TABLE sensor
    ADD CONSTRAINT sensor_tiposensor_fk FOREIGN KEY ( tiposensor_id_tipo_sensor )
        REFERENCES tiposensor ( id_tipo_sensor );

ALTER TABLE plantio
    ADD CONSTRAINT talhao_cultura_fk FOREIGN KEY ( cultura_id_cultura )
        REFERENCES cultura ( id_cultura );

ALTER TABLE plantio
    ADD CONSTRAINT talhao_propriedade_fk FOREIGN KEY ( propriedade_id_propriedade )
        REFERENCES campo ( id_campo );



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             9
-- CREATE INDEX                             0
-- ALTER TABLE                             18
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- TSDP POLICY                              0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
