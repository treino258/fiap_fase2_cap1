from dataclasses import dataclass, fields, field, asdict, InitVar
from enum import Enum
from typing import get_type_hints, Union, ClassVar
import json
import oracledb

# coloco o frozen = True e eq=True para poder comparar as classe e coloca-las em dicionário/set
@dataclass(frozen=True, eq=True)
class Model:

    id: int | None  = field(kw_only=True, default=None)

    def copy_with(self, other: Union['Model', dict]):
        """Cria uma nova instância da dataclass com os valores de self, sobrescrevendo os valores de other"""

        # Cria um dicionário com os valores de self
        self_dict = self.to_dict()
        # Atualiza os valores com os de other

        if isinstance(other, dict):
            self_dict.update(other)
        elif isinstance(other, Model):
            self_dict.update(other.to_dict())
        else:
            raise TypeError(f"Tipo {type(other)} não suportado")
        # Retorna uma nova instância da dataclass com os valores atualizados
        return self.from_dict(**self_dict)

    @classmethod
    def from_dict(cls, data: dict):
        type_hints = get_type_hints(cls)
        converted = {}
        for key, value in data.items():
            expected_type = type_hints.get(key)
            if isinstance(expected_type, type) and issubclass(expected_type, Enum):
                converted[key] = expected_type(value)
            else:
                converted[key] = value
        return cls(**converted)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self):
        return  json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    def fields(self):
        return fields(self)

    @staticmethod
    def create_table_sql(cls) -> str:
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''
        table_name = cls.__name__.lower()
        columns = []

        for field in fields(cls):

            if field.name == 'id':
                columns.append(f"{field.name} NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY")

            elif field.type is bool or issubclass(field.type, bool):
                columns.append(f"{field.name} BOOLEAN")

            elif field.type is int or issubclass(field.type, int):
                columns.append(f"{field.name} INT")

            elif field.type is float or issubclass(field.type, float):
                columns.append(f"{field.name} FLOAT")

            elif field.type is str or issubclass(field.type, str):

                if field.metadata.get('max_length'):
                    columns.append(f"{field.name} VARCHAR({field.metadata.get('max_length')})")
                else:
                    columns.append(f"{field.name} VARCHAR(255)")
            else:
                raise NotImplementedError(f"Tipo {field.type} não implementado")

        return  f"CREATE TABLE {table_name} ({', '.join(columns)})"

    def get_value(self, field_name):
        '''Retorna o valor do campo field_name da dataclass cls'''

        valor = getattr(self, field_name)

        if valor is None:
            return 'null'

        elif isinstance(valor, Enum):
            return valor.value

        return valor

    #------------- DATABASE -------------------

    conn:ClassVar[oracledb.Connection | None] = None
    cursor:ClassVar[oracledb.Cursor | None] = None

    @staticmethod
    def init_oracledb(*, user, password, dsn='oracle.fiap.com.br:1521/ORCL') -> bool:
        try:
            conn = oracledb.connect(user=user, password=password, dsn=dsn)
            # Cria as instruções para cada módulo

            if not conn.is_healthy():
                raise Exception("Conexão não está saudável")

            Model.conn = conn
            Model.cursor = conn.cursor()
            return True
        except Exception as e:
            print('Falha ao conectar ao banco de dados')
            print("Erro: ", e)
            return  False


    def _create_save_sql(self):
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''
        table_name = self.__name__.lower()
        columns = []
        values = []
        for field in fields(self):
            if field.name == 'id':
                continue
            columns.append(field.name)
            values.append(f":{getattr(self, field.name)}")

        return  f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"

    def _create_update_sql(self):
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''

        if self.get_value('id') is None:
            raise ValueError("Não é possível atualizar um registro sem id")

        table_name = self.__name__.lower()
        columns = []
        for field in fields(self):
            if field.name == 'id':
                continue
            columns.append(f"{field.name} = '{self.get_value(field.name)}'")

        return  f"UPDATE {table_name} SET {', '.join(columns)} WHERE id ={self.get_value('id')}"

    def save(self):

        if self.database is None:
            raise ValueError("Banco de dados não inicializado")

        if self.cursor is None:
            raise ValueError("Cursor não inicializado")

        if self.id is None:
            print("Salvando novo registro")
            sql = self._create_save_sql()
        else:
            print("Atualizando registro")
            sql = self._create_update_sql()

        retries = 0

        while retries < 3:
            try:
                retorno = self.cursor.execute(sql)
                print(retorno)
                self.conn.commit()
                break
            except Exception as e:
                if retries >= 2:
                    raise e
                retries += 1
                print("Erro ao executar o comando SQL")
                print("Erro: ", e)
                print(f"Tentando novamente {retries + 1} tentativas...")


    def _create_delete_sql(self):
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''


        if self.get_value('id') is None:
            raise ValueError("Não é possível excluir um registro sem id")

        table_name = self.__name__.lower()
        return  f"DELETE FROM {table_name} WHERE id ={self.get_value('id')}"

    def delete(self):
        if self.database is None:
            raise ValueError("Banco de dados não inicializado")

        if self.cursor is None:
            raise ValueError("Cursor não inicializado")

        sql = self._create_delete_sql()

        retries = 0

        while retries < 3:
            try:
                retorno = self.cursor.execute(sql)
                print(retorno)
                self.conn.commit()
                break
            except Exception as e:
                if retries >= 2:
                    raise e
                retries += 1
                print("Erro ao executar o comando SQL")
                print("Erro: ", e)
                print(f"Tentando novamente {retries + 1} tentativas...")