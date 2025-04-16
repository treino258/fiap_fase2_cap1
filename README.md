# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Um mapa do tesouro

## Grupo 28

## 👨‍🎓 Integrantes: 
- Vide arquivo separado na entrega no sistema da FIAP
## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">André Godoi</a>


## 📜 Descrição

Este projeto visa modelar um banco de dados relacional para a FarmTech Solutions. O objetivo é armazenar e analisar dados coletados por sensores em plantações (umidade, pH, nutrientes P e K) para otimizar a aplicação de água e nutrientes, visando aumentar a produção agrícola.

O banco de dados deve permitir responder perguntas como:

* **Qual foi a quantidade total de água aplicada em cada mês, por campo?**  
  A consulta SQL utiliza as tabelas `irrigacao`, `plantio` e `campo`, agrupando os dados por campo e mês para calcular o total de água aplicada:
  ```sql
  SELECT 
      c.identificador AS campo,
      TO_CHAR(i.inicio, 'YYYY-MM') AS mes,
      SUM(i.quantidade_total) AS total_agua
  FROM 
      irrigacao i
  JOIN plantio p ON i.plantio_id_plantio = p.id_plantio
  JOIN campo c ON p.campo_id_campo = c.id_campo
  GROUP BY c.identificador, TO_CHAR(i.inicio, 'YYYY-MM');
  ```

* **Como variou o nível de pH do solo em um campo específico ao longo do ano?**  
  A consulta SQL utiliza as tabelas `leiturasensor`, `sensor`, `plantio` e `campo`, filtrando pelo tipo de sensor "pH" e agrupando por mês:
  ```sql
  SELECT 
      TO_CHAR(ls.data_hora_leitura, 'YYYY-MM') AS mes,
      AVG(ls.valor_lido) AS media_ph
  FROM 
      leiturasensor ls
  JOIN sensor s ON ls.sensor_id_sensor = s.id_sensor
  JOIN plantio p ON ls.plantio_id_plantio = p.id_plantio
  JOIN campo c ON p.campo_id_campo = c.id_campo
  WHERE 
      s.tiposensor_id_tipo_sensor = (SELECT id_tipo_sensor FROM tiposensor WHERE nome = 'pH')
      AND c.identificador = 'Campo Norte'
  GROUP BY TO_CHAR(ls.data_hora_leitura, 'YYYY-MM');
  ```

* **Quais campos apresentaram níveis de nutrientes (P ou K) fora do ideal para a cultura atual?**  
  A consulta SQL utiliza as tabelas `leiturasensor`, `sensor`, `plantio`, `campo` e `cultura`, filtrando pelos sensores de nutrientes P e K e comparando com os níveis ideais:
  ```sql
  SELECT 
      c.identificador AS campo,
      t.nome AS nutriente,
      ls.valor_lido AS valor_atual,
      'Nível fora do ideal' AS status
  FROM 
      leiturasensor ls
  JOIN sensor s ON ls.sensor_id_sensor = s.id_sensor
  JOIN tiposensor t ON s.tiposensor_id_tipo_sensor = t.id_tipo_sensor
  JOIN plantio p ON ls.plantio_id_plantio = p.id_plantio
  JOIN campo c ON p.campo_id_campo = c.id_campo
  JOIN cultura cu ON p.cultura_id_cultura = cu.id_cultura
  WHERE 
      t.nome IN ('Nutriente P', 'Nutriente K')
      AND (ls.valor_lido < 10 OR ls.valor_lido > 50); -- Exemplo de níveis ideais
  ```

* **Qual o histórico de leituras de um sensor específico?**  
  A consulta SQL utiliza a tabela `leiturasensor` e filtra pelo ID ou código do sensor:
  ```sql
  SELECT 
      ls.data_hora_leitura,
      ls.valor_lido,
      um.nome AS unidade_medida
  FROM 
      leiturasensor ls
  JOIN sensor s ON ls.sensor_id_sensor = s.id_sensor
  JOIN unidade_medida um ON ls.unidade_medida_id_unidade = um.id_unidade
  WHERE 
      s.codigo_indetificacao = 'SENSOR123'
  ORDER BY ls.data_hora_leitura;
  ```

* **Quais sensores estão ativos e onde estão instalados?**  
  A consulta SQL utiliza a tabela `sensor` e filtra pelos sensores com localização definida:
  ```sql
  SELECT 
      s.codigo_indetificacao AS sensor,
      s.localizacao AS coordenadas,
      s.data_instalacao
  FROM 
      sensor s
  WHERE 
      s.localizacao IS NOT NULL;
  ```

## Diagrama Entidade-Relacionamento (DER)

O diagrama visual abaixo representa a estrutura final do banco de dados:

<img src="assets/der.png">

## 📜 Modelo Entidade-Relacionamento (MER)

A imagem abaixo representa o modelo entidade-relacionamento (MER) do banco de dados:

<img src="assets/mer.png">

### Entidades e Atributos

#### **aplicacao_nutrientes**
- **id_aplicacao**: INTEGER PRIMARY KEY NOT NULL - Identificador único da aplicação.
- **plantio_id_plantio**: INTEGER FOREIGN KEY NOT NULL - Referência ao plantio.
- **unidade_medida_id_unidade**: INTEGER FOREIGN KEY NOT NULL - Referência à unidade de medida.
- **nutriente_id_nutriente**: INTEGER FOREIGN KEY NOT NULL - Referência ao nutriente.
- **data_hora**: TIMESTAMP WITH LOCAL TIME ZONE NOT NULL - Data e hora da aplicação.
- **quantidade_aplicada**: NUMBER(10,2) NOT NULL - Quantidade aplicada.
- **observacao**: CLOB - Observações adicionais.

#### **campo**
- **id_campo**: INTEGER PRIMARY KEY NOT NULL - Identificador único do campo.
- **propriedade_id_propriedade**: INTEGER FOREIGN KEY NOT NULL - Referência à propriedade.
- **identificador**: VARCHAR2(100) NOT NULL - Nome do campo (ex: lote A1 ou Campo Norte).
- **area_hectares**: NUMBER - Tamanho da área em hectares.
- **localizacao_geo**: MDSYS.SDO_GEOMETRY - Localização geográfica (ex: coordenadas).

#### **cultura**
- **id_cultura**: INTEGER PRIMARY KEY NOT NULL - Identificador único da cultura.
- **nome**: VARCHAR2(255) NOT NULL - Nome da cultura (ex: milho, soja).

#### **irrigacao**
- **id_irrigacao**: INTEGER PRIMARY KEY NOT NULL - Identificador único da irrigação.
- **unidade_medida_id_unidade**: INTEGER FOREIGN KEY NOT NULL - Referência à unidade de medida.
- **plantio_id_plantio**: INTEGER FOREIGN KEY NOT NULL - Referência ao plantio.
- **quantidade_total**: NUMBER(12,3) NOT NULL - Quantidade total de água aplicada.
- **inicio**: TIMESTAMP WITH LOCAL TIME ZONE NOT NULL - Início da irrigação.
- **fim**: TIMESTAMP WITH LOCAL TIME ZONE - Fim da irrigação.
- **observacao**: CLOB - Observações adicionais.

#### **leiturasensor**
- **id_leitura**: INTEGER PRIMARY KEY NOT NULL - Identificador único da leitura.
- **plantio_id_plantio**: INTEGER FOREIGN KEY NOT NULL - Referência ao plantio.
- **sensor_id_sensor**: INTEGER FOREIGN KEY NOT NULL - Referência ao sensor.
- **unidade_medida_id_unidade**: INTEGER FOREIGN KEY NOT NULL - Referência à unidade de medida.
- **data_hora_leitura**: TIMESTAMP WITH LOCAL TIME ZONE NOT NULL - Data e hora da leitura.
- **valor_lido**: NUMBER(12,4) NOT NULL - Valor lido pelo sensor.

#### **nutriente**
- **id_nutriente**: INTEGER PRIMARY KEY NOT NULL - Identificador único do nutriente.
- **nome**: VARCHAR2(255) NOT NULL - Nome do nutriente.
- **observacao**: CLOB - Observações adicionais.

#### **plantio**
- **id_plantio**: INTEGER PRIMARY KEY NOT NULL - Identificador único do plantio.
- **campo_id_campo**: INTEGER FOREIGN KEY NOT NULL - Referência ao campo.
- **cultura_id_cultura**: INTEGER FOREIGN KEY NOT NULL - Referência à cultura.
- **data_inicio**: TIMESTAMP WITH LOCAL TIME ZONE NOT NULL - Data de início do plantio.
- **data_fim**: TIMESTAMP WITH LOCAL TIME ZONE - Data de fim do plantio.
- **observacoes**: CLOB - Observações adicionais.

#### **propriedade**
- **id_propriedade**: INTEGER PRIMARY KEY NOT NULL - Identificador único da propriedade.
- **nome**: VARCHAR2(255) - Nome da propriedade.
- **cnpj**: VARCHAR2(14) - CNPJ da propriedade.

#### **sensor**
- **id_sensor**: INTEGER PRIMARY KEY NOT NULL - Identificador único do sensor.
- **tiposensor_id_tipo_sensor**: INTEGER FOREIGN KEY NOT NULL - Referência ao tipo de sensor.
- **codigo_indetificacao**: VARCHAR2(100) NOT NULL - Código de identificação do sensor.
- **data_instalacao**: TIMESTAMP WITH LOCAL TIME ZONE - Data de instalação do sensor.
- **descricao**: CLOB - Descrição do sensor.
- **localizacao**: MDSYS.SDO_GEOMETRY - Localização geográfica do sensor.

#### **tiposensor**
- **id_tipo_sensor**: INTEGER PRIMARY KEY NOT NULL - Identificador único do tipo de sensor.
- **nome**: VARCHAR2(100) NOT NULL - Nome do tipo de sensor (ex: umidade, pH).

#### **unidade_medida**
- **id_unidade**: INTEGER PRIMARY KEY NOT NULL - Identificador único da unidade de medida.
- **nome**: VARCHAR2(20) - Nome da unidade de medida.

### Relacionamentos Principais

* **propriedade** (1) -- (1,N) **campo**  
  Uma propriedade pode ter um ou mais campos, mas cada campo pertence a exatamente uma propriedade.

* **campo** (1) -- (0,N) **plantio**  
  Um campo pode ter zero ou mais plantios, mas cada plantio ocorre em exatamente um campo.

* **cultura** (1) -- (0,N) **plantio**  
  Uma cultura pode estar associada a zero ou mais plantios, mas cada plantio está associado a exatamente uma cultura.

* **plantio** (1) -- (0,N) **aplicacao_nutrientes**  
  Um plantio pode ter zero ou mais aplicações de nutrientes, mas cada aplicação de nutrientes está associada a exatamente um plantio.

* **plantio** (1) -- (0,N) **irrigacao**  
  Um plantio pode ter zero ou mais irrigações, mas cada irrigação está associada a exatamente um plantio.

* **plantio** (1) -- (0,N) **leiturasensor**  
  Um plantio pode ter zero ou mais leituras de sensores, mas cada leitura de sensor está associada a exatamente um plantio.

* **sensor** (1) -- (0,N) **leiturasensor**  
  Um sensor pode gerar zero ou mais leituras, mas cada leitura está associada a exatamente um sensor.

* **tiposensor** (1) -- (1,N) **sensor**  
  Um tipo de sensor pode estar associado a um ou mais sensores, mas cada sensor pertence a exatamente um tipo de sensor.

* **unidade_medida** (1) -- (0,N) **aplicacao_nutrientes**  
  Uma unidade de medida pode ser usada em zero ou mais aplicações de nutrientes, mas cada aplicação de nutrientes utiliza exatamente uma unidade de medida.

* **unidade_medida** (1) -- (0,N) **irrigacao**  
  Uma unidade de medida pode ser usada em zero ou mais irrigações, mas cada irrigação utiliza exatamente uma unidade de medida.

* **unidade_medida** (1) -- (0,N) **leiturasensor**  
  Uma unidade de medida pode ser usada em zero ou mais leituras de sensores, mas cada leitura de sensor utiliza exatamente uma unidade de medida.

* **nutriente** (1) -- (0,N) **aplicacao_nutrientes**  
  Um nutriente pode ser usado em zero ou mais aplicações de nutrientes, mas cada aplicação de nutrientes utiliza exatamente um nutriente.

## 

## Script SQL (DDL)

O script para criação das tabelas no banco de dados Oracle, pode ser encontrado neste arquivo:
[FarmTech_Schema.ddl](assets/FarmTech_Schema.ddl)

Casos precise do arquivo dmd:
[FarmTech.dmd](assets/FarmTech.dmd)
## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

*Importar o arquivo [FarmTech_Schema.ddl](assets/FarmTech_Schema.ddl) no Oracle Data Modeler.*


## 🗃 Histórico de lançamentos

* 0.1.1 - 16/04/2024

* 0.1.0 - 14/04/2024

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
