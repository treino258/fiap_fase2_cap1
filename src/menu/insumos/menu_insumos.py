from src.database.models.insumo import Insumo
from src.menu.generico.menu_generico import menu_generico


def menu_insumos():

    return menu_generico(Insumo)