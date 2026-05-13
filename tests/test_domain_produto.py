# =============================================================================
# test_domain_produto.py — Testes unitários da classe Produto
# =============================================================================
#
# Testes unitários verificam uma única unidade de código isolada, sem
# depender de banco de dados, API ou qualquer outro componente externo.
#
# Aqui testamos apenas a regra de negócio do método preco_final():
#   - Produto tipo 1: desconto percentual É aplicado.
#   - Produto tipo 2: desconto NÃO é aplicado, independente do valor informado.
# =============================================================================

from domain.produto import Produto


def test_produto_tipo_1_aplica_desconto():
    """Produto do tipo 1 com 10% de desconto deve custar 9.0 (era 10.0).

    Cenário:
        - Valor base: R$ 10,00
        - Desconto: 10%
        - Tipo: 1 (desconto ativo)

    Cálculo esperado: 10 * (1 - 10/100) = 10 * 0.90 = 9.0
    """
    p = Produto(codigo=1, valor=10, tipo=1, desconto_percentual=10)
    assert p.preco_final() == 9.0


def test_produto_tipo_2_nao_aplica_desconto():
    """Produto do tipo 2 nunca recebe desconto, mesmo que um percentual seja informado.

    Cenário:
        - Valor base: R$ 20,00
        - Desconto informado: 10% (deve ser ignorado)
        - Tipo: 2 (sem desconto)

    Resultado esperado: preço final == valor base == 20.0
    """
    p = Produto(codigo=2, valor=20, tipo=2, desconto_percentual=10)
    assert p.preco_final() == 20.0


def test_produto_sem_desconto():
    """Produto do tipo 1 sem desconto configurado retorna o valor base.

    Cenário:
        - Valor base: R$ 15,00
        - Desconto: 0%
        - Tipo: 1

    Resultado esperado: preço final == valor base == 15.0
    """
    p = Produto(codigo=3, valor=15, tipo=1, desconto_percentual=0)
    assert p.preco_final() == 15.0
