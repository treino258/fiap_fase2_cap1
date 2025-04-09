from src.database.models.fazenda import Fazenda
from src.database.utils import input_bool
from src.logger.loggers import log_info
from src.menu.alterar_fazenda import alterar_fazendas
from src.menu.cadastrar_fazenda import cadastrar_fazenda
from src.menu.excluir_fazenda import excluir_fazendas
from src.menu.listar_fazendas import listar_fazendas


def menu_principal() -> None|bool:

    print('Bem-vindo ao sistema de gerenciamento de Fazendas!')

    print('1) Cadastrar Fazenda')
    print('2) Listar Fazendas')
    print('3) Editar Fazenda')
    print('4) Excluir Fazenda')

    escolha = input("Escolha uma opção: ")

    match escolha:
        case '1':
            cadastrar_fazenda()

        case '2':
            listar_fazendas()

        case '3':
            alterar_fazendas()

        case '4':
            excluir_fazendas()
        case _:
            print('Opção inválida. Tente novamente.')


