"""
Criar uma função:
eh_primo(numero)
A função deve: - Retornar True se o número for primo - Retornar False caso contrário
No programa principal: - Informar se o número é primo ou não
"""
def eh_primo(numero: int) -> bool:
    #Números menores que 2 (0, 1, negativos) não são primos — retorna False imediatamente.
    if numero < 2:
        return False
    # Verifica se o número é divisível por algum número entre 2 e a raiz quadrada do número. Se for, retorna False (não é primo).
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:
            return False
    # Se o número não for divisível por nenhum desses números, é primo — retorna True.
    return True

# Exemplo de uso
"""
Raiz quadrada de 17 ≈ 4.1 → testa i em [2, 3, 4]
17 % 2 = 1, 17 % 3 = 2, 17 % 4 = 1 → nenhum divide
Retorna True (17 é primo)
"""
numero = 17
if eh_primo(numero):
    print(f"O número {numero} é primo.")
else:
    print(f"O número {numero} não é primo.")