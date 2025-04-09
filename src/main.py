from src.database.login.iniciar_database import iniciar_database
from src.database.tables.init_tables import check_or_create_tables
from src.menu.menu_principal import menu_principal


def main():
    iniciar_database()
    check_or_create_tables()


    while True:
        sair = menu_principal()

        if sair:
            break


main()