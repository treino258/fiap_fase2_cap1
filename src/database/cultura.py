from enum import Enum, StrEnum

from src.database.model import Model
from dataclasses import dataclass, field


class TipoCultura(StrEnum):
    CANA_DE_ACUCAR = "cana"

    @property
    def name(self):

        if self.value == "cana":
            return "Cana-de-Açúcar"

        return super().name


class FormatoArea(StrEnum):
    QUADRADO = "quadrado"
    TRIANGULO = "triangulo"

    @property
    def name(self):

        if self.value == "quadrado":
            return "Quadrado"

        if self.value == "triangulo":
            return "Triângulo"

        return super().name


@dataclass(frozen=True, eq=True)
class Cultura(Model):

    tipo:TipoCultura
    formato:FormatoArea
    base: float = field(metadata={
        'label': 'Base (m²)',
    })
    altura: float = field(metadata={
        'label': 'Altura (m²)',
    })


if __name__ == "__main__":

    print(Cultura._create_table_sql())
    x = Cultura.from_dict({
        'tipo': 'cana',
        'formato': 'triangulo',
        'base': 10.0,
        'altura': 5.0
    })
    print(x.fields())
    print(x)

    y = Cultura.from_terminal_input()
