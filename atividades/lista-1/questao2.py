"""
Criar uma função chamada:
calcular_media(n1, n2, n3)
A função deve: - Calcular a média aritmética - Retornar o valor da média
No programa principal deve ser exibido: - "Aprovado" se média >= 7 - "Reprovado" caso contrário
"""

def calcular_media(n1: float, n2: float, n3: float) -> float:
    media = (n1 + n2 + n3) / 3
    return media

def verificar_aprovacao(media: float) -> str:
    if media >= 7.0:
        return "Aprovado"
    return "Reprovado"
    
def response_resultado(media: float, resultado: str) -> str:
    return f"Média: {media:.2f} - Resultado: {resultado}"

# Exemplo de uso
nota1 = 8.5
nota2 = 6.0
nota3 = 7.5
media_final = calcular_media(nota1, nota2, nota3)
resultado = verificar_aprovacao(media_final)
print(response_resultado(media_final, resultado))