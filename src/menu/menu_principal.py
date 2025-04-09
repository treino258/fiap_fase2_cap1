from src.menu.fazenda.menu_fazenda import menu_fazenda
from src.menu.insumos.menu_insumos import menu_insumos
from src.menu.maquinario.menu_maquinario import menu_maquinario


def menu_principal() -> None|bool:

    print('Bem-vindo ao sistema de gerenciamento de Fazendas!')
    print()
    print('1) Manutenção de Fazendas')
    print('2) Manutenção de Insumos')
    print('3) Manutenção de Maquinários')
    print('4) Relatórios')
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
            menu_maquinario()

        case '4':
            print('Relatórios')
        case _:
            print('Opção inválida. Tente novamente.')


