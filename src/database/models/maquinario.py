from src.database.login.iniciar_database import iniciar_database
from src.database.models.compartilhado import FormatoArea
from src.database.models.fazenda import Fazenda
from src.database.tipos_base.model import Model
from dataclasses import dataclass, field
import matplotlib.pyplot as plt

@dataclass(frozen=True, eq=True)
class Maquinario(Model):

    @classmethod
    def display_name(cls) -> str:
        return "Maquinário"

    nome: str = field(metadata={
        'label': 'Nome do Maquinário',
    })

    largura:float = field(metadata={
        'label': 'Largura (m)',
    })

    profundidade:float = field(metadata={
        'label': 'Profundidade (m)',
    })

    valocidademax: float = field(metadata={
        'label': 'Velocidade Máx. (km/h)',
    })

    consumo: float = field(metadata={
        'label': 'Consumo combustível (km/l)',
    })

    def _calcular_rota_retangulo(self, largura: float, altura: float, largura_carro: float) -> list[tuple]:
        """Calcula a rota mais curta para cobrir um retângulo."""
        rota = []
        y = 0
        sentido = 1  # 1 para direita, -1 para esquerda

        while y < altura:
            if sentido == 1:
                rota.append((0, y))
                rota.append((largura, y))
            else:
                rota.append((largura, y))
                rota.append((0, y))

            y += largura_carro
            sentido *= -1  # Inverte o sentido

        return rota

    def _calcular_rota_triangulo(self, base: float, altura: float, largura_carro: float) -> list[tuple]:
        """Calcula a rota mais curta para cobrir um triângulo."""
        rota = []
        y = 0
        sentido = 1  # 1 para direita, -1 para esquerda

        while y < altura:
            largura_atual = (base / altura) * (altura - y)  # Largura do triângulo na altura atual
            if sentido == 1:
                rota.append((0, y))
                rota.append((largura_atual, y))
            else:
                rota.append((largura_atual, y))
                rota.append((0, y))

            y += largura_carro
            sentido *= -1  # Inverte o sentido

        return rota

    def calcular_rota(self, fazenda:Fazenda):

        if fazenda.formato == FormatoArea.TRIANGULO:
            return self._calcular_rota_triangulo(fazenda.base, fazenda.altura, self.largura)
        elif fazenda.formato == FormatoArea.RETANGULO:
            return self._calcular_rota_retangulo(fazenda.base, fazenda.altura, self.largura)
        else:
            raise NotImplementedError(f"Formato {fazenda.formato.name} não implementado")

    def calcular_distancia(cls, rota: list[tuple]) -> float:
        """Calcula a distância total percorrida com base na rota."""
        distancia_total = 0.0
        for i in range(1, len(rota)):
            x1, y1 = rota[i - 1]
            x2, y2 = rota[i]
            distancia_total += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 1/2
        return distancia_total

    def calcular_consumo(cls, distancia: float, consumo_por_km: float) -> float:
        """Calcula o consumo de combustível com base na distância e eficiência."""
        if consumo_por_km <= 0:
            raise ValueError("O consumo por km deve ser maior que zero.")
        return distancia / consumo_por_km

def desenhar_rota(rota, titulo="Rota"):
    """Desenha a rota em um gráfico."""
    x, y = zip(*rota)  # Separa as coordenadas x e y

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, marker='o', linestyle='-', color='blue')  # Desenha a rota
    plt.title(titulo)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    rota_exemplo = [
        (0, 0), (10, 0), (10, 2), (0, 2), (0, 4), (10, 4)
    ]

    print("Rota calculada:")
    for ponto in rota_exemplo:
        print(ponto)

    desenhar_rota(rota_exemplo, titulo="Rota Exemplo")

    iniciar_database()

    fazenda = Fazenda.fetch_by_id(4)
    maquinario = Maquinario.fetch_by_id(1)

    rota = maquinario.calcular_rota(fazenda)

    print("Rota calculada:")
    desenhar_rota(rota)
