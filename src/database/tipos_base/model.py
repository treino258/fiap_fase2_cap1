from dataclasses import dataclass, fields, field, asdict, InitVar
from enum import Enum
from typing import get_type_hints, Union, ClassVar
import json
from src.database.tipos_base.query import Query
from src.database.utils import input_bool, input_int, input_str, input_float, input_enum
from src.logger.loggers import log_info, log_success, log_error, log_warning
import pandas as pd


# coloco o frozen = True e eq=True para poder comparar as classe e coloca-las em dicionário/set
@dataclass(frozen=True, eq=True)
class Model(Query):

    id: int | None  = field(kw_only=True, default=None)

    #------------- CONSTRUCTOR ---------------------

    @classmethod
    def from_dict(cls, data: dict) -> 'Model':
        type_hints = get_type_hints(cls)
        converted = {}
        for key, value in data.items():
            expected_type = type_hints.get(key)
            if isinstance(expected_type, type) and issubclass(expected_type, Enum):
                converted[key] = expected_type(value)
            else:
                converted[key] = value
        return cls(**converted)

    @classmethod
    def from_terminal_input(cls, old_data: Union[dict, 'Model', None]=None) -> 'Model':

        """Cria uma nova instância da dataclass com os valores de self, sobrescrevendo os valores de other"""
        # Cria um dicionário com os valores de self
        if isinstance(old_data, dict):
            _old_data = old_data
        elif isinstance(old_data, Model):
            _old_data = old_data.to_dict()
        else:
            _old_data = {}


        new_values = {}

        if old_data is not None and old_data.get('id') is not None:
            new_values['id'] = old_data.get('id')

        for field in fields(cls):
            if field.name == 'id':
                continue

            elif field.type is Enum or issubclass(field.type, Enum):

                valor = None

                while valor is None:

                    try:
                        valor = input_enum(field_name=field.metadata.get('label', field.name.capitalize()),
                                           old_value=_old_data.get(field.name),
                                           enum_class=field.type,
                                           )
                        new_values[field.name] = valor
                    except ValueError as e:
                        log_error(str(e))
                        valor = None

            elif field.type is bool or issubclass(field.type, bool):

                valor = None

                while valor is None:

                    try:
                        valor = input_bool(field_name=field.metadata.get('label', field.name.capitalize()), old_value=_old_data.get(field.name))
                        new_values[field.name] = valor
                    except ValueError as e:
                        log_error(str(e))
                        valor = None

            elif field.type is int or issubclass(field.type, int):

                valor = None

                while valor is None:

                    try:
                        valor = input_int(field_name=field.metadata.get('label', field.name.capitalize()), old_value=_old_data.get(field.name))
                        new_values[field.name] = valor
                    except ValueError as e:
                        log_error(str(e))
                        valor = None

            elif field.type is float or issubclass(field.type, float):

                valor = None

                while valor is None:

                    try:
                        valor = input_float(field_name=field.metadata.get('label', field.name.capitalize()), old_value=_old_data.get(field.name))
                        new_values[field.name] = valor
                    except ValueError as e:
                        log_error(str(e))
                        valor = None

            elif field.type is str or issubclass(field.type, str):

                valor = None

                while valor is None:

                    try:
                        valor = input_str(field_name=field.metadata.get('label', field.name.capitalize()), old_value=_old_data.get(field.name), max_length=field.metadata.get('max_length'))
                        new_values[field.name] = valor
                    except ValueError as e:
                        log_error(str(e))
                        valor = None

            else:
                raise NotImplementedError(f"Tipo {field.type} não implementado")

        return cls.from_dict(new_values)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    #------------- METHODS ---------------------

    def copy_with(self, other: Union['Model', dict]) -> 'Model':
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
        return self.from_dict(self_dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self):
        return  json.dumps(self.to_dict())

    @classmethod
    def fields(cls):
        return fields(cls)

    @classmethod
    def field_names(cls):
        return [f.name for f in cls.fields()]

    def get_value(self, field_name):
        '''Retorna o valor do campo field_name da dataclass'''

        valor = getattr(self, field_name)

        if isinstance(valor, Enum):
            return valor.value

        return valor

    def as_display(self) -> dict:

        fields = self.fields()

        retorno = {}

        for f in fields:

            if f.name == 'id':
                if self.id is None:
                    retorno['id'] = 'Novo'
                else:
                    retorno['id'] = self.id
                continue


            label = f.metadata.get('label', f.name.capitalize())
            value = getattr(self, f.name)

            if isinstance(value, Enum):
                retorno[label] = value.name
            else:
                retorno[label] = value

        return retorno


    def get_dataframe(self):

        data = self.as_display()

        return pd.DataFrame.from_records(
            data=[data],
            columns=data.keys(),
            index='id'
        )
        #          .style.set_properties(**{
        #     'text-align': 'left',
        #     'font-size': '12px'
        # })

    @classmethod
    def get_dataframes(cls, instances:list['Model']) -> pd.DataFrame|None:

        data = []

        for i in instances:
            data.append(i.as_display())

        if len(data) == 0:
            return None

        return pd.DataFrame.from_records(
            data=data,
            columns=data[0].keys(),
            index='id'
        )



    #------------- DATABASE ---------------------
    @classmethod
    def field_from_db(cls, colum_name):
        '''Retorna o nome do campo referente a coluna colum_name da dataclass'''
        for field in cls.field_names():
            if Model.colum_name(field) == colum_name:
                return field
        raise ValueError(f"Coluna {colum_name} não encontrada na dataclass {cls.__name__}")

    @classmethod
    def _create_table_sql(cls) -> str:
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''
        table_name = cls.table_name()
        columns = []

        for field in fields(cls):

            if field.name == 'id':
                columns.append(f"{Model.colum_name(field.name)} NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY")

            elif field.type is bool or issubclass(field.type, bool):
                columns.append(f"{Model.colum_name(field.name)} BOOLEAN")

            elif field.type is int or issubclass(field.type, int):
                columns.append(f"{Model.colum_name(field.name)} INT")

            elif field.type is float or issubclass(field.type, float):
                columns.append(f"{Model.colum_name(field.name)} FLOAT")

            elif field.type is str or issubclass(field.type, str):

                if field.metadata.get('max_length'):
                    columns.append(f"{Model.colum_name(field.name)} VARCHAR({field.metadata.get('max_length')})")
                else:
                    columns.append(f"{Model.colum_name(field.name)} VARCHAR(255)")
            else:
                raise NotImplementedError(f"Tipo {field.type} não implementado")

        return  f"CREATE TABLE {table_name} ({', '.join(columns)})"

    @classmethod
    def check_or_create_table(cls):
        '''Cria a tabela referente a esta dataclass na oracladb'''

        if not cls.check_if_table_exists():
            log_info(f"Tabela não existe, criando tabela {cls.table_name()}")
            sql = cls._create_table_sql()
            cls.execute_sql(sql)
            log_success(f"Tabela criada com sucesso {cls.table_name()}")
        else:
            log_info(f"Tabela já existe, não é necessário criar a tabela {cls.table_name()}")

    @classmethod
    def check_if_table_exists(cls):
        '''Verifica se a tabela existe no banco de dados'''
        table_name = cls.table_name()
        sql = f"SELECT COUNT(*) FROM user_tables WHERE table_name = '{table_name}'"
        cursor = cls.cursor
        cursor.execute(sql)
        fetch = cursor.fetchone()
        result = fetch[0]
        return result > 0

    def _create_save_sql(self):
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''
        table_name = self.table_name()
        columns = []
        values = []
        for field in fields(self):
            if field.name == 'id':
                continue
            columns.append(Model.colum_name(field.name))
            values.append(f"'{self.get_value(field.name)}'")
        return  f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)}) RETURNING id INTO :id"

    def _create_update_sql(self):
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''

        if self.get_value('id') is None:
            raise ValueError("Não é possível atualizar um registro sem id")

        table_name = self.table_name()
        columns = []
        for field in fields(self):
            if field.name == 'id':
                continue
            columns.append(f"{Model.colum_name(field.name)} = '{self.get_value(field.name)}'")

        return  f"UPDATE {table_name} SET {', '.join(columns)} WHERE id ={self.get_value('id')} RETURNING id INTO :id"

    def save(self) -> 'Model':

        if self.id is None:
            log_info("Salvando novo registro")
            sql = self._create_save_sql()
        else:
            log_info("Atualizando registro")
            sql = self._create_update_sql()

        id_var = Model.cursor.var(int)
        try:
            Model.execute_sql(sql, id=id_var)
            log_success(f"Registro salvo com sucesso")
            novo_id = id_var.getvalue()[0]
            return self.copy_with({'id': novo_id})

        except Exception as e:
            log_error(f"Erro ao salvar registro: {e}")
            raise e

    def _create_delete_sql(self):
        '''Retorna o comando sql para criar a table referente a esta dataclass na oracladb'''


        if self.get_value('id') is None:
            raise ValueError("Não é possível excluir um registro sem id")

        table_name = self.table_name()
        return  f"DELETE FROM {table_name} WHERE id ={self.get_value('id')}"

    def delete(self) -> 'Model':
        log_warning("Excluindo registro")
        sql = self._create_delete_sql()
        Model.execute_sql(sql)
        log_success(f"Registro excluído com sucesso")
        return self
