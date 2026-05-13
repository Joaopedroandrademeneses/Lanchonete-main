


"""
Criar uma função:
eh_par(numero)
A função deve: - 
Retornar True se o número for par - 
Retornar False caso contrário
No programa principal: - 
Informar se o número é PAR ou ÍMPAR
"""
def eh_par(numero):
    return numero % 2 == 0

# Exemplo de uso
numero = 10
if eh_par(numero):
    print(f"O número {numero} é PAR.")
else:
    print(f"O número {numero} é ÍMPAR.")

    
