from time import sleep
from typing import ClassVar
import oracledb
from abc import ABC

class Database(ABC):
    conn: ClassVar[oracledb.Connection | None] = None
    cursor: ClassVar[oracledb.Cursor | None] = None

    @staticmethod
    def init_oracledb(*, user, password, dsn='oracle.fiap.com.br:1521/ORCL') -> bool:
        try:
            conn = oracledb.connect(user=user, password=password, dsn=dsn)
            # Cria as instruções para cada módulo

            if not conn.is_healthy():
                raise Exception("Conexão não está saudável")

            Database.conn = conn
            Database.cursor = conn.cursor()
            return True
        except Exception as e:
            print('Falha ao conectar ao banco de dados')
            print("Erro: ", e)
            return False

    @staticmethod
    def execute_sql(sql: str, *, max_retries: int = 3, commit: bool = True, **kwargs):
        '''Executa um comando sql no banco de dados'''
        if Database.conn is None:
            raise ValueError("Banco de dados não inicializado")

        if Database.cursor is None:
            raise ValueError("Cursor não inicializado")

        retries = 0

        while retries < max_retries:
            try:
                Database.cursor.execute(sql, **kwargs)
                if commit:
                    Database.conn.commit()
                break
            except Exception as e:
                retries += 1
                if retries >= max_retries:
                    raise e

                print("Erro ao executar o comando SQL")
                print("Erro: ", e)
                print(f"Tentando novamente {retries + 1} tentativas...")

                sleep(retries)

    @classmethod
    def table_name(cls) -> str:
        '''Retorna o nome da tabela referente a esta dataclass na oracladb'''
        return cls.__name__.upper()