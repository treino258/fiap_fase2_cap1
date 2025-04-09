from src.database.models.fazenda import Fazenda
from src.menu.generico.menu_generico import menu_generico


def menu_fazenda():

    return menu_generico(Fazenda)