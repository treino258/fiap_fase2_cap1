import os

from src.logger.loggers import log_info, log_warning, log_error, log_success
from src.database.login.senha import salvar_senha_arquivo_base64, carregar_senha_arquivo_base64
from src.database.tipos_base.database import Database
from src.database.utils import input_str, input_bool


def iniciar_database():

    log_info("Iniciando o banco de dados...")
    user = os.environ.get('user')
    senha = os.environ.get('senha')

    pegou_ambiente = False
    pegou_b64 = False

    if user is not None and senha is not None:
        pegou_ambiente = True
    else:
        user, senha = carregar_senha_arquivo_base64()

        if user is not None and senha is not None:
            pegou_b64 = True



    iniciou = False

    while not iniciou:

        if user is None:
            log_warning("--- Usuário não encontrado ---", write=False)
            user = input_str('user', message_override="Digite o usuário do banco de dados: ")

        if senha is None:
            log_warning("--- Senha não encontrada ---", write=False)
            senha = input_str('senha', message_override="Digite a senha do banco de dados: ")

        iniciou = Database.init_oracledb(user=user, password=senha)

        if not iniciou:
            user = None
            senha = None
            log_error("--- Erro ao conectar ao banco de dados, tentando novamente. ---")

    log_success("--- Banco de dados conectado com sucesso! ---")

    if not pegou_ambiente and not pegou_b64:
        print("Deseja salvar o usuário e senha?")
        salvar = input_bool('Salvar Senha', modo='S')

        if salvar:
            salvar_senha_arquivo_base64(user, senha)
            log_success("--- Senha salva com sucesso! ---", write=False)



if __name__ == "__main__":
    iniciar_database()