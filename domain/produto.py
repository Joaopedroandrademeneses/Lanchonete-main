from dataclasses import dataclass


@dataclass
class Produto:
    """Representa um produto disponível na lanchonete.

    Attributes:
        codigo: Identificador único do produto.
        valor: Preço base do produto (deve ser >= 0).
        tipo: Categoria do produto.
            - tipo 1: desconto percentual é aplicado no preço final.
            - tipo 2: desconto NÃO é aplicado; preço final = valor base.
        desconto_percentual: Percentual de desconto (deve ser >= 0). Padrão: 0.
    """

    codigo: int
    valor: float
    tipo: int
    desconto_percentual: float = 0.0

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Valor do produto não pode ser negativo")
        if self.desconto_percentual < 0:
            raise ValueError("Desconto não pode ser negativo")

    def preco_final(self) -> float:
        """Calcula o preço final do produto aplicando as regras de desconto.

        Produtos do tipo 2 nunca recebem desconto.
        Demais tipos recebem o desconto percentual configurado.

        Returns:
            Preço final como float.
        """
        if self.tipo == 2:
            return float(self.valor)
        if self.desconto_percentual and self.desconto_percentual > 0:
            return float(self.valor) * (1 - self.desconto_percentual / 100)
        return float(self.valor)