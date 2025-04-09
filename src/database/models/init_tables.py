from src.database.models.fazenda import Fazenda
from src.database.models.insumo import Insumo
from src.database.models.maquinario import Maquinario
from src.logger.loggers import log_info


def check_or_create_tables():

    log_info("Verificando se as tabelas existem...")

    Fazenda.check_or_create_table()
    Insumo.check_or_create_table()
    Maquinario.check_or_create_table()