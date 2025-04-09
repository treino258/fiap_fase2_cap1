from src.database.models.cultura import Cultura
from src.database.utils import input_bool
from src.logger.loggers import log_info


def menu_principal() -> None|bool:

    print('Bem-vindo ao sistema de gerenciamento de Fazendas!')

    print('1) Cadastrar Fazenda')
    print('2) Listar Fazendas')
    print('3) Editar Fazenda')
    print('4) Excluir Fazenda')

    escolha = input("Escolha uma opção: ")

    match escolha:
        case '1':
            nova_cultura = Cultura.from_terminal_input()
            print()
            print('Foram digitas as seguintes informações:')
            print(nova_cultura.get_dataframe())
            print()
            print('Você gostaria de salvar as informações?')
            salvar = input_bool('Salvar', modo='S')

            if salvar:
                nova_cultura.save()
                input("Pressione enter para continuar...")

            # Chamar função para cadastrar fazenda
        case '2':
            print('Listar Fazendas')
            # Chamar função para listar fazendas
        case '3':
            print('Editar Fazenda')
            # Chamar função para editar fazenda
        case '4':
            print('Excluir Fazenda')
            # Chamar função para excluir fazenda
        case _:
            print('Opção inválida. Tente novamente.')


