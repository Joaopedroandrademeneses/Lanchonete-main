# =============================================================================
# test_domain_pedido.py — Testes unitários da classe Pedido
# =============================================================================
#
# Estes testes verificam as regras de negócio da entidade Pedido sem passar
# pela API. Criamos os objetos diretamente e chamamos seus métodos,
# validando comportamento esperado em diferentes situações.
# =============================================================================

from domain.cliente import Cliente
from domain.produto import Produto
from domain.pedido import Pedido


def test_pedido_limite_itens():
    """O pedido deve recusar novos produtos quando o limite máximo for atingido.

    Cenário:
        - Pedido com limite de 1 produto
        - Tentativa de adicionar 2 produtos

    Comportamento esperado:
        - Primeiro produto: adicionado com sucesso (retorna True)
        - Segundo produto: recusado pois o limite já foi atingido (retorna False)

    Por que isso importa?
        Garante que a regra de negócio de limite por pedido está sendo
        respeitada, evitando pedidos maiores do que o permitido.
    """
    c = Cliente(cpf="111", nome="X")
    pedido = Pedido(cliente=c, qtd_max_produtos=1)
    p1 = Produto(codigo=1, valor=10, tipo=1, desconto_percentual=0)
    p2 = Produto(codigo=2, valor=20, tipo=1, desconto_percentual=0)
    assert pedido.adicionar_produto(p1) is True
    assert pedido.adicionar_produto(p2) is False


def test_pedido_total_se_nao_finalizado_retorna_0():
    """Um pedido ainda não finalizado deve retornar total zero.

    Cenário:
        - Pedido com um produto adicionado
        - Pedido ainda não foi finalizado (esta_entregue = False)

    Comportamento esperado:
        - total_se_finalizado() retorna 0.0

    Por que isso importa?
        Impede que o sistema exiba um total antes do pedido ser confirmado,
        evitando cobranças indevidas ou inconsistências na interface.
    """
    c = Cliente(cpf="111", nome="X")
    pedido = Pedido(cliente=c, qtd_max_produtos=10)
    p1 = Produto(codigo=1, valor=10, tipo=1, desconto_percentual=10)
    pedido.adicionar_produto(p1)
    assert pedido.total_se_finalizado() == 0.0


def test_pedido_finalizar_calcula_total_com_regras():
    """Ao finalizar, o total deve aplicar as regras de desconto de cada produto.

    Cenário:
        - p1: tipo 1, valor R$10, desconto 10% → preço final = R$9,00
        - p2: tipo 2, valor R$20, desconto 10% → preço final = R$20,00 (ignorado)

    Comportamento esperado:
        - total = 9.0 + 20.0 = 29.0
        - pedido.esta_entregue passa a ser True após finalizar()

    Por que isso importa?
        Valida que a composição de regras diferentes (por tipo de produto)
        funciona corretamente ao calcular o valor final do pedido.
    """
    c = Cliente(cpf="111", nome="X")
    pedido = Pedido(cliente=c, qtd_max_produtos=10)
    p1 = Produto(codigo=1, valor=10, tipo=1, desconto_percentual=10)
    p2 = Produto(codigo=2, valor=20, tipo=2, desconto_percentual=10)
    pedido.adicionar_produto(p1)
    pedido.adicionar_produto(p2)
    total = pedido.finalizar()
    assert total == 29.0
    assert pedido.esta_entregue is True
