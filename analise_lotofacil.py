import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# URL da API
url = "https://loteriascaixa-api.herokuapp.com/api/lotofacil"

# Função para obter todos os resultados da Lotofácil
def obter_resultados():
    response = requests.get(url)
    
    # Verifica o status da resposta
    if response.status_code == 200:
        resultados = response.json()
        
        # Inspeciona a estrutura completa do primeiro sorteio para verificar onde os números estão
        print("Estrutura completa do primeiro sorteio:", resultados[0])
        return resultados
    else:
        print("Erro ao acessar a API")
        return None

# Função para contar a frequência dos números sorteados
def contar_frequencia(resultados):
    numeros = []
    
    # Iterar sobre cada sorteio
    for sorteio in resultados:
        # Inspecionar todas as chaves e valores de cada sorteio
        print("Sorteio completo:", sorteio)
        
        # Tente acessar "dezenasOrdemSorteio" ou outro campo que contenha as dezenas sorteadas
        dezenas = sorteio.get("dezenasOrdemSorteio")  # Verifica se "dezenasOrdemSorteio" existe
        
        if dezenas:
            numeros.extend(dezenas)  # Adiciona os números sorteados à lista
        else:
            print(f"Nenhuma 'dezenasOrdemSorteio' encontrada para este sorteio: {sorteio}")
    
    # Contar a frequência de cada número
    frequencia = Counter(numeros)
    
    # Verifica se os números foram extraídos corretamente
    print("Números extraídos:", numeros)
    return frequencia

# Função para plotar o gráfico de frequência dos números
def plotar_frequencia(frequencia):
    if not frequencia:  # Verifica se há dados a serem plotados
        print("Nenhum dado para plotar!")
        return
    
    numeros = list(frequencia.keys())
    contagens = list(frequencia.values())
    
    plt.figure(figsize=(10,6))
    sns.barplot(x=numeros, y=contagens, palette="viridis")
    plt.title("Frequência dos Números Sorteados - Lotofácil")
    plt.xlabel("Números")
    plt.ylabel("Frequência")
    plt.show()

# Função principal
def main():
    # Obter os resultados da API
    resultados = obter_resultados()
    
    if resultados:
        # Calcular a frequência dos números sorteados
        frequencia = contar_frequencia(resultados)
        
        # Mostrar a frequência
        print("Frequência dos Números Sorteados:")
        for num, freq in frequencia.items():
            print(f"Número {num}: {freq} vezes")
        
        # Plotar o gráfico de frequência
        plotar_frequencia(frequencia)

if __name__ == "__main__":
    main()
