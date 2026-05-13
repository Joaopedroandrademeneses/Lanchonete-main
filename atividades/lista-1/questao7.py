"""
Criar uma função:
calcular_salario(salario_base)
Regras: - Até 1500 → aumento de 15% - 
Até 3000 → aumento de 10% - 
Acima de 3000 → aumento de
5%
A função deve retornar o novo salário.
"""
def calcular_salario(salario_base: float) -> float:
    if salario_base <= 1500:
        aumento = salario_base * 0.15
    elif salario_base <= 3000:
        aumento = salario_base * 0.10
    else:
        aumento = salario_base * 0.05
    novo_salario = salario_base + aumento
    return novo_salario

# Exemplo de uso
salario = 2000.0
novo_salario = calcular_salario(salario)
print(f"Salário base: R$ {salario:.2f}")
print(f"Novo salário: R$ {novo_salario:.2f}")