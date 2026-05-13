from pydantic import BaseModel


class ProdutoCreate(BaseModel):
    """Payload para criação de um produto."""

    codigo: int
    valor: float
    tipo: int
    desconto_percentual: float = 0.0


class ProdutoOut(BaseModel):
    """Dados de retorno de um produto."""

    codigo: int
    valor: float
    tipo: int
    desconto_percentual: float = 0.0


class ProdutoAlterarValor(BaseModel):
    """Payload para alteração do valor de um produto."""

    novo_valor: float
