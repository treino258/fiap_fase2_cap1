from src.database.models.fazenda import Fazenda
from src.database.tipos_base.model import Model
from src.menu.generico.alterar_generico import alterar_generico
from src.menu.generico.cadastrar_generico import cadastrar_generico
from src.menu.generico.excluir_generico import excluir_generico
from src.menu.generico.listar_generico import listar_generico


def menu_generico(model:type[Model]):

    while True:
        print(f'--- Menu manutenção de {model.display_name_plural()} ---')
        print()
        print(f'1) Cadastrar {model.display_name()}')
        print(f'2) Listar {model.display_name_plural()}')
        print(f'3) Editar {model.display_name()}')
        print(f'4) Excluir {model.display_name()}')
        print()
        print('0) Voltar para o menu principal')

        escolha = input("Escolha uma opção: ")

        match escolha:
            case '0':
                return

            case '1':
                cadastrar_generico(model)

            case '2':
                listar_generico(model)

            case '3':
                alterar_generico(model)

            case '4':
                excluir_generico(model)
            case _:
                print('Opção inválida. Tente novamente.')
