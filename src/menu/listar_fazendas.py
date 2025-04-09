from src.database.models.fazenda import Fazenda
from src.database.utils import input_bool
from src.logger.loggers import log_warning, log_info


def listar_fazendas():
    fazendas = Fazenda.fetch_all()

    if len(fazendas) == 0:
        log_warning('Nenhuma fazenda encontrada na base de dados!')
        return

    data_frame = Fazenda.get_dataframes(fazendas)

    log_info("Fazendas obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()
    input("Pressione qualquer tecla para continuar...")
