"""
Criar uma função:
converter_segundos(segundos)
A função deve: - Converter para horas, minutos e segundos - Retornar os três valores
"""
def converter_segundos(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    return horas, minutos, segundos_restantes

# Exemplo de uso
total_segundos = 3665
horas, minutos, segundos = converter_segundos(total_segundos)
print(f"{total_segundos} segundos equivalem a {horas} horas, {minutos} minutos e {segundos} segundos.")
