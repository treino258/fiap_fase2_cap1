from enum import Enum

from src.database.model import Model
from dataclasses import dataclass, field


class TipoCultura(str, Enum):
    CANA_DE_ACUCAR = "cana"

class FormatoArea(str, Enum):
    QUADRADO = "quadrado"
    TRIANGULO = "triangulo"


@dataclass(frozen=True, eq=True)
class Cultura(Model):

    tipo:TipoCultura
    formato:FormatoArea
    base: float
    altura: float


if __name__ == "__main__":

    print(Cultura.create_table_sql(Cultura))
    x = Cultura.from_dict({
        'tipo': 'cana',
        'formato': 'triangulo',
        'base': 10.0,
        'altura': 5.0
    })
    print(x.fields())
    print(x)
