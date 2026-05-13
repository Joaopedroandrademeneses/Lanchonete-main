
"""
Criar as seguintes funções:
 Função 1
calcular_total(qtd, valor_unitario) - Retorna o total da compra
 Função 2
verificar_frete(total) Regras: - Se total >= 200 → frete grátis - Caso contrário → frete = 20
 Função 3 (principal)
processar_pedido(qtd, valor_unitario) Deve: - Calcular total dos produtos - Calcular frete - Exibir:
Total produtos:
Frete:
Total geral:
"""
def calcular_total(qtd: int, valor_unitario: float) -> float:
    """
    Calcula o total a pagar com base na quantidade e valor unitário.

    Args:
        qtd (int): A quantidade de itens.
        valor_unitario (float): O valor unitário de cada item.
    
    Returns:
        float: O total a pagar.
    """
    if qtd < 0:
        raise ValueError("A quantidade não pode ser negativa.")
    if valor_unitario < 0:
        raise ValueError("O valor unitário não pode ser negativo.")
    
    total = qtd * valor_unitario
    return total


def verificar_frete(total: float) -> str:
    """
    Verifica se o frete é gratuito com base no total a pagar.

    Args:
        total (float): O total a pagar.
    
    Returns:
        str: "Frete gratuito" se o total for maior que R$ 200,00, caso contrário "Frete normal".
    """
    if total > 200.0:
        return "Frete gratuito", 0.0
    return "Frete normal", 20.0

def processar_pedido(qtd: int, valor_unitario: float) -> float:
    """
    Processa o pedido calculando o total e verificando o frete.

    Args:
        qtd (int): A quantidade de itens.
        valor_unitario (float): O valor unitário de cada item.
    
    Returns:
        str: Uma mensagem com o total a pagar e o tipo de frete.
    """
    total = calcular_total(qtd, valor_unitario)
    frete, valor_frete = verificar_frete(total)
    total_com_frete = total + valor_frete
    return total, frete, total_com_frete

# Exemplo de uso
quantidade = 5
valor_unitario = 25.0
total, frete, total_com_frete = processar_pedido(quantidade, valor_unitario)
print(f"Total produtos: R$ {total:.2f}")
print(f"Frete: {frete}")
print(f"Total Geral: R$ {total_com_frete:.2f}")