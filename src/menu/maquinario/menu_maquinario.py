from src.database.models.maquinario import Maquinario
from src.menu.generico.menu_generico import menu_generico

def menu_maquinario():

    return menu_generico(Maquinario)