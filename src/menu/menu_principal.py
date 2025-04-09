from src.menu.fazenda.menu_fazenda import menu_fazenda
from src.menu.insumos.menu_insumos import menu_insumos


def menu_principal() -> None|bool:

    print('Bem-vindo ao sistema de gerenciamento de Fazendas!')
    print()
    print('1) Manutenção de fazendas')
    print('2) Manutenção de insumos')
    print('3) Manutenção de maquinários')
    print('5) Relatórios')
    print()
    print('0) Sair')

    escolha = input("Escolha uma opção: ")

    match escolha:
        case '0':
            return True

        case '1':
            menu_fazenda()

        case '2':
            menu_insumos()

        case '3':
            print('Manutenção de maquinários')

        case '4':
            print('Relatórios')
        case _:
            print('Opção inválida. Tente novamente.')


