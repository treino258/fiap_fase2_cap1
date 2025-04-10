from src.database.login.iniciar_database import iniciar_database
from src.database.models.compartilhado import TipoCultura, FormatoArea
from src.database.tipos_base.model import Model
from dataclasses import dataclass, field


@dataclass(frozen=True, eq=True)
class Fazenda(Model):

    nome: str = field(metadata={
        'label': 'Nome da Fazenda',
    })

    tipo:TipoCultura = field(metadata={
        'label': 'Tipo de Cultura',
    })

    formato:FormatoArea
    base: float = field(metadata={
        'label': 'Base (m²)',
    })

    altura: float = field(metadata={
        'label': 'Altura (m²)',
    })

    def area(self) -> float:
        """
        Calcula a área da fazenda com base no formato e nas dimensões fornecidas.
        :return: Área da fazenda em m².
        """
        if self.formato == FormatoArea.RETANGULO:
            return self.base * self.altura
        elif self.formato == FormatoArea.TRIANGULO:
            return (self.base * self.altura) / 2
        else:
            raise ValueError("Formato desconhecido")


if __name__ == "__main__":

    # print(Fazenda._create_table_sql())
    # x = Fazenda.from_dict({
    #     'nome': 'Fazenda Teste',
    #     'tipo': 'cana',
    #     'formato': 'triangulo',
    #     'base': 10.0,
    #     'altura': 5.0
    # })
    # print(x.fields())
    # print(x)
    #
    # y = Fazenda.from_terminal_input()

    iniciar_database()

    instances = Fazenda.filter_by_field('nome', 'fazenda teste 2').fetch()

    print(instances)
