"""
Criar uma função chamada:
saudar(nome)
A função deve: - Receber um nome - Retornar a mensagem:
"Olá, <nome>! Seja bem‑vindo."
"""
def saudar(nome: str) -> str:
    return f"Olá, {nome}! Seja bem-vindo(a)!"

# Exemplo de uso
nome_usuario = "Maria"  
response = saudar(nome_usuario)
print(response) 


