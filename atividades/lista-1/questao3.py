"""
Criar uma função chamada:
calcular_preco_final(valor_produto)
Regras: - Se valor do produto for maior que 100 → aplicar 10% de desconto - Caso contrário → manter
valor original
A função deve retornar o preço final.

"""
def numero_valido(valor_produto: float) -> bool:
    try:
        valor_produto = float(valor_produto)
        return True
    except ValueError:
        return False
    
def calcular_preco_final(valor_produto: float) -> float:
    """
    Calcula o preço final de um produto com base no valor original e um desconto de 10% se o valor for superior a R$ 100,00.

    Args:
        valor_produto (float): O valor original do produto.
    
    Returns:
        float: O preço final do produto após aplicar o desconto.
    """
    
    if not numero_valido(valor_produto):
        raise ValueError("O valor do produto deve ser um número.")
    if valor_produto > 100.0:
        desconto = valor_produto * 0.10
    else:
        desconto = 0.0
    preco_final = valor_produto - desconto
    return preco_final
    

# Exemplo de uso
valor = 150.0
preco_final = calcular_preco_final(valor)
print(f"Preço final: R$ {preco_final:.2f}")

valor = 100.0
preco_final = calcular_preco_final(valor)
print(f"Preço final: R$ {preco_final:.2f}")