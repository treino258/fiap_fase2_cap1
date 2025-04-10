from src.database.login.iniciar_database import iniciar_database
from src.database.models.init_tables import check_or_create_tables
from src.logger.loggers import log_critical
from src.menu.menu_principal import menu_principal
import pandas as pd
import traceback

def main():
    iniciar_database()
    check_or_create_tables()

    #necessário para o pandas não truncar os dados
    pd.options.display.max_rows = 99
    pd.options.display.max_columns = 99
    pd.options.display.width = 200


    while True:

        try:
            sair = menu_principal()

            if sair:
                break
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")
            break

        except SystemExit:
            print("\n\nSaindo do sistema...")
            break

        except Exception as e:
            stacktrace = traceback.format_exc()
            log_critical(f'{e}\n{stacktrace}\nErro inesperado saindo do sistema...')
            raise

main()