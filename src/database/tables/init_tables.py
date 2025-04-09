from src.database.models.cultura import Cultura
from src.logger.loggers import log_info


def check_or_create_tables():

    log_info("Verificando se as tabelas existem...")

    Cultura.check_or_create_table()