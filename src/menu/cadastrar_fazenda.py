from src.database.models.fazenda import Fazenda
from src.database.utils import input_bool


def cadastrar_fazenda(fazenda: Fazenda = None) -> None:
    old_data = None if fazenda is None else fazenda.to_dict()
    alterar = True
    while alterar:
        nova_fazenda = Fazenda.from_terminal_input(old_data)
        print()
        print('Foram digitas as seguintes informações:')
        print(nova_fazenda.get_dataframe())
        print()
        print('Você gostaria de alterar as informações?')
        alterar = input_bool('Alterar', modo='S')
        if alterar:
            old_data = nova_fazenda.to_dict()

    nova_fazenda.save()
    input("Pressione enter para continuar...")