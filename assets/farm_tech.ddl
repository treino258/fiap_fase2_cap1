-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-04-16 16:52:35 BRT
--   site:      Oracle Database 12c
--   tipo:      Oracle Database 12c



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE aplicacao_nutrientes 
    ( 
     id_aplicacao              INTEGER  NOT NULL , 
     plantio_id_plantio        INTEGER  NOT NULL , 
     unidade_medida_id_unidade INTEGER  NOT NULL , 
     nutriente_id_nutriente    INTEGER  NOT NULL , 
     data_hora                 TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL , 
     quantidade_aplicada       NUMBER (10,2)  NOT NULL , 
     observacao                CLOB 
    ) 
;

COMMENT ON COLUMN aplicacao_nutrientes.id_aplicacao IS 'identitadade de registro de uma ação como de irrigação ou aplicação de nutriente para manter os dados guardados' 
;

COMMENT ON COLUMN aplicacao_nutrientes.quantidade_aplicada IS 'quantidade de agua/produto' 
;

ALTER TABLE aplicacao_nutrientes 
    ADD CONSTRAINT aplicacao_nutrientes_PK PRIMARY KEY ( id_aplicacao ) ;

CREATE TABLE campo 
    ( 
     id_campo                   INTEGER  NOT NULL , 
     propriedade_id_propriedade INTEGER  NOT NULL , 
     identificador              VARCHAR2 (100)  NOT NULL , 
     area_hectares              NUMBER , 
     localizacao_geo            MDSYS.SDO_GEOMETRY 
    ) 
;

COMMENT ON COLUMN campo.identificador IS 'Nome do lote, ex: lota A1 ou Campo norte' 
;

COMMENT ON COLUMN campo.area_hectares IS 'tamanho da area' 
;

COMMENT ON COLUMN campo.localizacao_geo IS 'por exemplo coordenada' 
;

ALTER TABLE campo 
    ADD CONSTRAINT campo_PK PRIMARY KEY ( id_campo ) ;

ALTER TABLE campo 
    ADD CONSTRAINT campo_identificador_UN UNIQUE ( identificador ) ;

CREATE TABLE cultura 
    ( 
     id_cultura INTEGER  NOT NULL , 
     nome       VARCHAR2 (255)  NOT NULL 
    ) 
;

COMMENT ON COLUMN cultura.id_cultura IS 'numero de indentificação da cultura' 
;

COMMENT ON COLUMN cultura.nome IS 'ex: milho, soja, cafe, cana' 
;

ALTER TABLE cultura 
    ADD CONSTRAINT cultura_PK PRIMARY KEY ( id_cultura ) ;

CREATE TABLE irrigacao 
    ( 
     id_irrigacao              INTEGER  NOT NULL , 
     unidade_medida_id_unidade INTEGER  NOT NULL , 
     plantio_id_plantio        INTEGER  NOT NULL , 
     quantidade_total          NUMBER (12,3)  NOT NULL , 
     inicio                    TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL , 
     fim                       TIMESTAMP WITH LOCAL TIME ZONE , 
     observacao                CLOB 
    ) 
;

ALTER TABLE irrigacao 
    ADD CONSTRAINT irrigacao_PK PRIMARY KEY ( id_irrigacao ) ;

CREATE TABLE leiturasensor 
    ( 
     id_leitura                INTEGER  NOT NULL , 
     plantio_id_plantio        INTEGER  NOT NULL , 
     sensor_id_sensor          INTEGER  NOT NULL , 
     unidade_medida_id_unidade INTEGER  NOT NULL , 
     data_hora_leitura         TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL , 
     valor_lido                NUMBER (12,4)  NOT NULL 
    ) 
;

COMMENT ON COLUMN leiturasensor.id_leitura IS 'identidade da leitura' 
;

COMMENT ON COLUMN leiturasensor.data_hora_leitura IS 'data e hota que captou a leitura' 
;

COMMENT ON COLUMN leiturasensor.valor_lido IS 'o valor lido como numero, podendo ser ph,humidade e etc' 
;

ALTER TABLE leiturasensor 
    ADD CONSTRAINT leiturasensor_PK PRIMARY KEY ( id_leitura ) ;

CREATE TABLE nutriente 
    ( 
     id_nutriente INTEGER  NOT NULL , 
     nome         VARCHAR2 (255)  NOT NULL , 
     observacao   CLOB 
    ) 
;

ALTER TABLE nutriente 
    ADD CONSTRAINT nutriente_PK PRIMARY KEY ( id_nutriente ) ;

CREATE TABLE plantio 
    ( 
     id_plantio         INTEGER  NOT NULL , 
     campo_id_campo     INTEGER  NOT NULL , 
     cultura_id_cultura INTEGER  NOT NULL , 
     data_inicio        TIMESTAMP WITH LOCAL TIME ZONE  NOT NULL , 
     data_fim           TIMESTAMP WITH LOCAL TIME ZONE , 
     observacoes        CLOB 
    ) 
;

COMMENT ON COLUMN plantio.id_plantio IS 'Associa um cultura a um campo por um periodo' 
;

ALTER TABLE plantio 
    ADD CONSTRAINT plantio_PK PRIMARY KEY ( id_plantio ) ;

CREATE TABLE propriedade 
    ( 
     id_propriedade INTEGER  NOT NULL , 
     nome           VARCHAR2 (255) , 
     cnpj           VARCHAR2 (14) 
    ) 
;

ALTER TABLE propriedade 
    ADD CONSTRAINT propriedade_PK PRIMARY KEY ( id_propriedade ) ;

CREATE TABLE sensor 
    ( 
     id_sensor                 INTEGER  NOT NULL , 
     tiposensor_id_tipo_sensor INTEGER  NOT NULL , 
     codigo_indetificacao      VARCHAR2 (100)  NOT NULL , 
     data_instalacao           TIMESTAMP WITH LOCAL TIME ZONE , 
     descricao                 CLOB , 
     localizacao               MDSYS.SDO_GEOMETRY 
    ) 
;

ALTER TABLE sensor 
    ADD CONSTRAINT sensor_PK PRIMARY KEY ( id_sensor ) ;

CREATE TABLE tiposensor 
    ( 
     id_tipo_sensor INTEGER  NOT NULL , 
     nome           VARCHAR2 (100)  NOT NULL 
    ) 
;

COMMENT ON COLUMN tiposensor.id_tipo_sensor IS 'o ID para indentificar do sensor' 
;

COMMENT ON COLUMN tiposensor.nome IS 'nome do sensor ( umidade, ph, nutriente p, nutriente K )' 
;

ALTER TABLE tiposensor 
    ADD CONSTRAINT tiposensor_PK PRIMARY KEY ( id_tipo_sensor ) ;

CREATE TABLE unidade_medida 
    ( 
     id_unidade INTEGER  NOT NULL , 
     nome       VARCHAR2 (20) 
    ) 
;

ALTER TABLE unidade_medida 
    ADD CONSTRAINT unidade_medida_PK PRIMARY KEY ( id_unidade ) ;

ALTER TABLE aplicacao_nutrientes 
    ADD CONSTRAINT aplicacao_nutriente_FK FOREIGN KEY 
    ( 
     nutriente_id_nutriente
    ) 
    REFERENCES nutriente 
    ( 
     id_nutriente
    ) 
;

ALTER TABLE aplicacao_nutrientes 
    ADD CONSTRAINT aplicacao_nutrientes_pl_FK FOREIGN KEY 
    ( 
     plantio_id_plantio
    ) 
    REFERENCES plantio 
    ( 
     id_plantio
    ) 
;

ALTER TABLE aplicacao_nutrientes 
    ADD CONSTRAINT aplicacao_unidade_FK FOREIGN KEY 
    ( 
     unidade_medida_id_unidade
    ) 
    REFERENCES unidade_medida 
    ( 
     id_unidade
    ) 
;

ALTER TABLE campo 
    ADD CONSTRAINT campo_propriedade_FK FOREIGN KEY 
    ( 
     propriedade_id_propriedade
    ) 
    REFERENCES propriedade 
    ( 
     id_propriedade
    ) 
;

ALTER TABLE irrigacao 
    ADD CONSTRAINT irrigacao_plantio_FK FOREIGN KEY 
    ( 
     plantio_id_plantio
    ) 
    REFERENCES plantio 
    ( 
     id_plantio
    ) 
;

ALTER TABLE irrigacao 
    ADD CONSTRAINT irrigacao_unidade_FK FOREIGN KEY 
    ( 
     unidade_medida_id_unidade
    ) 
    REFERENCES unidade_medida 
    ( 
     id_unidade
    ) 
;

ALTER TABLE leiturasensor 
    ADD CONSTRAINT leiturasensor_plantio_FK FOREIGN KEY 
    ( 
     plantio_id_plantio
    ) 
    REFERENCES plantio 
    ( 
     id_plantio
    ) 
;

ALTER TABLE leiturasensor 
    ADD CONSTRAINT leiturasensor_sensor_FK FOREIGN KEY 
    ( 
     sensor_id_sensor
    ) 
    REFERENCES sensor 
    ( 
     id_sensor
    ) 
;

ALTER TABLE leiturasensor 
    ADD CONSTRAINT leiturasensor_unidade_FK FOREIGN KEY 
    ( 
     unidade_medida_id_unidade
    ) 
    REFERENCES unidade_medida 
    ( 
     id_unidade
    ) 
;

ALTER TABLE plantio 
    ADD CONSTRAINT plantio_campo_FK FOREIGN KEY 
    ( 
     campo_id_campo
    ) 
    REFERENCES campo 
    ( 
     id_campo
    ) 
;

ALTER TABLE plantio 
    ADD CONSTRAINT plantio_cultura_FK FOREIGN KEY 
    ( 
     cultura_id_cultura
    ) 
    REFERENCES cultura 
    ( 
     id_cultura
    ) 
;

ALTER TABLE sensor 
    ADD CONSTRAINT sensor_tiposensor_FK FOREIGN KEY 
    ( 
     tiposensor_id_tipo_sensor
    ) 
    REFERENCES tiposensor 
    ( 
     id_tipo_sensor
    ) 
;



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            11
-- CREATE INDEX                             0
-- ALTER TABLE                             24
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
