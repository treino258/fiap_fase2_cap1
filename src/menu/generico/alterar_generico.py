from src.database.tipos_base.model import Model
from src.database.utils import input_int
from src.logger.loggers import log_warning, log_info
from src.menu.generico.cadastrar_generico import cadastrar_generico


def alterar_generico(
    model: type[Model],
):

    instances = model.fetch_all()

    if len(instances) == 0:
        log_warning(f'Nenhum item {model.display_name()} encontrado na base de dados!')
        return

    data_frame = model.get_dataframes(instances)

    log_info(f"Instâncias de {model.display_name()} obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()

    ids_target = [instance.id for instance in instances]

    id_alterar = None

    while id_alterar not in ids_target:

        try:
            id_alterar = input_int('id', message_override=f'Escolha o ID de {model.display_name()} que deseja alterar ou 0 para voltar: ')
        except ValueError:
            log_warning('ID inválido, tente novamente!')
            id_alterar = None
            continue

        if id_alterar == 0:
            log_info('Voltando para o menu anterior...')
            return

        if id_alterar not in ids_target:
            log_warning(f'{model.display_name()} com ID {id_alterar} não está presente na base de dados, tente novamente!')

    instance = model.fetch_by_id(id_alterar)

    log_info(f'Alterando {model.display_name()} com ID {instance.id}...')

    return cadastrar_generico(model, instance)

