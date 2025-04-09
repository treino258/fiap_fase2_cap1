from src.database.tipos_base.model import Model
from src.database.utils import input_bool


def cadastrar_generico(model: type[Model], instance: Model = None) -> None:
    old_data = None if instance is None else instance.to_dict()
    alterar = True
    while alterar:
        nova_instance = model.from_terminal_input(old_data)
        print()
        print('Foram digitas as seguintes informações:')
        print(nova_instance.get_dataframe())
        print()
        print('Você gostaria de alterar as informações?')
        alterar = input_bool('Alterar', modo='S')
        if alterar:
            old_data = nova_instance.to_dict()
        else:
            nova_instance.save()
            alterar = False
    input("Pressione enter para continuar...")