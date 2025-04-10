from src.database.models.fazenda import Fazenda
from src.database.tipos_base.model import Model
from src.database.utils import input_bool
from src.logger.loggers import log_warning, log_info


def listar_generico(model:type[Model]):
    try:
        instances = model.fetch_all()
    except Exception as e:
        log_warning(f'Erro ao buscar instâncias de {model.display_name()} na base de dados: {e}\nTente novamente mais tarde!')
        return

    if len(instances) == 0:
        log_warning(f'Nenhuma instância de {model.display_name()} encontrada na base de dados!')
        return

    data_frame = model.get_dataframes(instances)

    log_info(f"Instâncias de {model.display_name_plural()} obtidas da database com sucesso!")
    print()
    print(data_frame)
    print()
    input("Pressione qualquer ENTER para continuar...")
