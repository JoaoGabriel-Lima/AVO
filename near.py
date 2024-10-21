import numpy as np
import matplotlib.pyplot as plt

# Exemplo de dados de GR (Gradiente) e IN (Intercepto) para NEAR e FAR
# Substitua isso pelos seus dados reais
GR_near = np.random.rand(10, 10)  # Gradientes NEAR
GR_far = np.random.rand(10, 10)   # Gradientes FAR
IN_near = np.random.rand(10, 10)  # Interceptos NEAR
IN_far = np.random.rand(10, 10)   # Interceptos FAR

n = GR_near.shape[0]  # Número de elementos em uma dimensão

# Coeficientes para a equação WAVO
a = 0.5  # Substituir pelos valores reais
b = 0.5  # Substituir pelos valores reais

# Função para calcular GRi (equação 1) e INj (equação 2)
def calculate_GRi_INj(GR, IN):
    GRi = np.mean(GR, axis=1)  # Média ao longo de j para cada i
    INj = np.mean(IN, axis=0)  # Média ao longo de i para cada j
    return GRi, INj

# Função para calcular AVOID (equação 3) e AVOGD (equação 4)
def calculate_AVOID_AVOGD(GR, IN, GRi, INj):
    AVOID = IN - INj  # AVOID(i,j)
    AVOGD = GR - GRi[:, None]  # AVOGD(i,j)
    return AVOID, AVOGD

# Função para calcular WAVO (equação 5)
def calculate_WAVO(AVOID, AVOGD, a, b):
    return a * AVOID + b * AVOGD  # WAVO(i,j)

# Calcular GRi e INj para NEAR e FAR
GRi_near, INj_near = calculate_GRi_INj(GR_near, IN_near)
GRi_far, INj_far = calculate_GRi_INj(GR_far, IN_far)

# Calcular AVOID e AVOGD para NEAR
AVOID_near, AVOGD_near = calculate_AVOID_AVOGD(GR_near, IN_near, GRi_near, INj_near)

# Calcular AVOID e AVOGD para FAR
AVOID_far, AVOGD_far = calculate_AVOID_AVOGD(GR_far, IN_far, GRi_far, INj_far)

# Calcular WAVO para NEAR e FAR
WAVO_near = calculate_WAVO(AVOID_near, AVOGD_near, a, b)
WAVO_far = calculate_WAVO(AVOID_far, AVOGD_far, a, b)

# Plotar AVO para NEAR e FAR
plt.figure(figsize=(10, 6))

# Plotar AVOID para NEAR
plt.plot(AVOID_near.flatten(), label='AVOID NEAR', color='blue')

# Plotar AVOID para FAR
plt.plot(AVOID_far.flatten(), label='AVOID FAR', color='red')

# Configurações do gráfico
plt.xlabel('Índice (i, j) flatten')
plt.ylabel('AVOID')
plt.title('Gráfico AVOID para NEAR e FAR')
plt.legend()
plt.grid(True)
plt.show()
