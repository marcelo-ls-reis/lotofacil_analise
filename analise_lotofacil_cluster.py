import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.cluster import KMeans

# URL da API
url = "https://loteriascaixa-api.herokuapp.com/api/lotofacil"

# Função para obter todos os resultados da Lotofácil
def obter_resultados():
    response = requests.get(url)
    
    # Verifica o status da resposta
    if response.status_code == 200:
        resultados = response.json()
        return resultados
    else:
        print("Erro ao acessar a API")
        return None

# Função para contar a frequência dos números sorteados
def contar_frequencia(resultados):
    numeros = []
    
    # Iterar sobre cada sorteio
    for sorteio in resultados:
        dezenas = sorteio.get("dezenasOrdemSorteio")  # Acessa as dezenas sorteadas
        
        if dezenas:
            numeros.extend(dezenas)  # Adiciona os números sorteados à lista
        else:
            print(f"Nenhuma 'dezenasOrdemSorteio' encontrada para este sorteio: {sorteio}")
    
    # Contar a frequência de cada número
    frequencia = Counter(numeros)
    
    return frequencia

# Função para realizar a análise de clusters
def analise_clusters(frequencia, n_clusters=3):
    numeros = np.array(list(frequencia.keys())).reshape(-1, 1)
    contagens = np.array(list(frequencia.values())).reshape(-1, 1)
    
    # Aplicar K-Means para agrupar os números de acordo com suas frequências
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(contagens)
    
    # Adiciona os rótulos dos clusters para cada número
    clusters = kmeans.labels_
    
    # Exibir os clusters
    for cluster in range(n_clusters):
        print(f"\nCluster {cluster + 1}:")
        for i, num in enumerate(numeros):
            if clusters[i] == cluster:
                print(f"Número {num[0]}: sorteado {contagens[i][0]} vezes")
    
    # Visualizar os clusters
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=numeros.flatten(), y=contagens.flatten(), hue=clusters, palette="viridis", s=100)
    plt.title("Análise de Clusters dos Números Sorteados - Lotofácil")
    plt.xlabel("Números")
    plt.ylabel("Frequência de Sorteio")
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
        
        # Realizar a análise de clusters
        analise_clusters(frequencia, n_clusters=3)

if __name__ == "__main__":
    main()
