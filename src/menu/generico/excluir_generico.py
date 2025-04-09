from time import sleep
from src.database.tipos_base.model import Model
from src.database.utils import input_int
from src.logger.loggers import log_warning, log_info, log_success


def excluir_generico(
        model:type[Model]
):
    instances = model.fetch_all()

    if len(instances) == 0:
        log_warning(f'Nenhuma instância de {model.display_name()} encontrada na base de dados!')
        return

    data_frame = model.get_dataframes(instances)

    log_info("Fazendas obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()

    ids_target = [instance.id for instance in instances]

    id_excluir = None

    while id_excluir not in ids_target:

        try:
            id_excluir = input_int('id', message_override=f'Escolha o ID da instância de {model.display_name()} que deseja excluir ou 0 para voltar: ')
        except ValueError:
            log_warning('ID inválido, tente novamente!')
            id_alterar = None
            continue

        if id_excluir == 0:
            log_info('Voltando para o menu anterior...')
            return

        if id_excluir not in ids_target:
            log_warning(f'Instância de {model.display_name()} com ID {id_excluir} não encontrada na base de dados, tente novamente!')

    instance = model.fetch_by_id(id_excluir)

    log_info(f'Excluindo {model.display_name()} com ID {instance.id} em...')

    for i in range(3, 0, -1):
        print(i, end='...',)
        sleep(1)
    print()
    instance.delete()
    log_success(f"Instância de {model.display_name()} ID {instance.id} excluída com sucesso!")

