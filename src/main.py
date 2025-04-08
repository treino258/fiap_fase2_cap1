from src.database.login.iniciar_database import iniciar_database
from src.menu.menu_principal import menu_principal


def main():
    iniciar_database()


    while True:
        sair = menu_principal()

        if sair:
            break


main()