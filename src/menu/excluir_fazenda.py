from time import sleep

from src.database.models.fazenda import Fazenda
from src.database.utils import input_bool, input_int
from src.logger.loggers import log_warning, log_info, log_success
from src.menu.cadastrar_fazenda import cadastrar_fazenda


def excluir_fazendas():
    fazendas = Fazenda.fetch_all()

    if len(fazendas) == 0:
        log_warning('Nenhuma fazenda encontrada na base de dados!')
        return

    data_frame = Fazenda.get_dataframes(fazendas)

    log_info("Fazendas obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()

    ids_target = [fazenda.id for fazenda in fazendas]

    id_excluir = None

    while id_excluir not in ids_target:

        try:
            id_excluir = input_int('id', message_override='Escolha o ID da fazenda que deseja excluir ou 0 para voltar: ')
        except ValueError:
            log_warning('ID inválido, tente novamente!')
            id_alterar = None
            continue

        if id_excluir == 0:
            log_info('Voltando para o menu principal...')
            return

        if id_excluir not in ids_target:
            log_warning(f'Fazenda com ID {id_excluir} não encontrada na base de dados, tente novamente!')

    fazenda = Fazenda.fetch_by_id(id_excluir)

    log_info(f'Excluindo fazenda com ID {fazenda.id} em...')

    for i in range(3, 0, -1):
        print(i, end='...',)
        sleep(1)
    print()
    fazenda.delete()
    log_success(f"Fazenda ID {fazenda.id} excluída com sucesso!")

