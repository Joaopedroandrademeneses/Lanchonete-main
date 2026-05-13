"""
Criar uma função:
maior_valor(a, b, c)
A função deve: - Retornar o maior número entre os três
"""
def maior_valor(a, b, c):
    return max(a, b, c)

# Exemplo de uso
num1 = 10
num2 = 25
num3 = 15
resultado = maior_valor(num1, num2, num3)
print(f"O maior valor entre {num1}, {num2} e {num3} é: {resultado}")