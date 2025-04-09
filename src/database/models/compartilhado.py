from enum import StrEnum


class TipoCultura(StrEnum):
    CANA_DE_ACUCAR = "cana"

    @property
    def name(self):

        if self.value == "cana":
            return "Cana-de-Açúcar"

        return super().name

class FormatoArea(StrEnum):
    RETANGULO = "retangulo"
    TRIANGULO = "triangulo"

    @property
    def name(self):

        if self.value == "retangulo":
            return "Retângulo"

        if self.value == "triangulo":
            return "Triângulo"

        return super().name

class UnidadesInsumo(StrEnum):
    TONELADA = "t"
    KILO = "kg"
    LITRO = "l"
    GRAMAS = "g"
    ML = "ml"


    @property
    def name(self):

        if self.value == "t":
            return "Tonelada"

        return super().name.upper()