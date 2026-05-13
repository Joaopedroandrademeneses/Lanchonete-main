from typing import Dict
from domain.cliente import Cliente
from domain.produto import Produto
from domain.pedido import Pedido


class MemoryDB:
    """Repositório em memória para armazenamento dos dados da lanchonete.

    Substitui um banco de dados durante o desenvolvimento/testes.
    Os dados são perdidos ao reiniciar a aplicação.

    Attributes:
        clientes_por_cpf: Mapeamento de CPF -> Cliente.
        produtos_por_id: Mapeamento de código -> Produto.
        pedidos_por_codigo: Mapeamento de código -> Pedido.
    """

    def __init__(self):
        self.clientes_por_cpf: Dict[str, Cliente] = {}
        self.produtos_por_id: Dict[int, Produto] = {}
        self.pedidos_por_codigo: Dict[int, Pedido] = {}


db = MemoryDB()