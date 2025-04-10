from typing import ClassVar
from src.database.tipos_base.database import Database

class _Query(Database):

    def __init__(self, filters: list[str] = None, *,
                 model: type['Model'],
                 table_name: str,
                 ):
        self.filters:ClassVar[list[str]] = filters or []
        self.target_table_name:ClassVar[str] = table_name
        self.model:ClassVar[type['Model']] = model

    def filter_by_field(self, field: str, value) -> '_Query':
        '''Adiciona um filtro à lista de filtros'''
        self.filters.append(f"{field} = '{value}'")
        return self

    def fetch(self) -> list['Model']:
        '''Executa a consulta com os filtros acumulados'''
        table_name = self.target_table_name
        where_clause = " AND ".join(self.filters)
        sql = f"SELECT * FROM {table_name} WHERE {where_clause}"
        cursor = self.cursor
        cursor.execute(sql)
        result = cursor.fetchall()
        return [self.model.from_dict(dict(zip([self.model.field_from_db(col[0]) for col in cursor.description], row))) for row in result]

class Query(Database):
    @classmethod
    def fetch_all(cls) -> list['Model']:
        '''Retorna todos os registros da tabela referente a esta dataclass na oracladb'''
        table_name = cls.table_name()
        sql = f"SELECT * FROM {table_name}"
        cursor = cls.cursor
        cursor.execute(sql)
        result = cursor.fetchall()

        return [cls.from_dict(dict(zip([cls.field_from_db(col[0]) for col in cursor.description], row))) for row in result]

    @classmethod
    def fetch_by_id(cls, id:int) -> 'Model':
        table_name = cls.table_name()
        sql = f"SELECT * FROM {table_name} WHERE id = {id}"
        cursor = cls.cursor
        cursor.execute(sql)
        result = cursor.fetchall()
        return cls.from_dict(dict(zip([cls.field_from_db(col[0]) for col in cursor.description], result[0])))

    @classmethod
    def filter_by_field(cls, field:str, value) -> '_Query':
        return _Query(
            filters= [
                f"{field} = '{value}'"
            ],
            model=cls,
            table_name=cls.table_name(),
        )

