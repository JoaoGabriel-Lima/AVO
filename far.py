import numpy as np
import matplotlib.pyplot as plt

# Função para ler os arquivos .xyz
def read_xyz(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        coords = []
        for line in lines:
            if len(line.split()) == 3:  # Verifica se a linha tem 4 valores (incluindo x, y, z e valor)
                coords.append([float(value) for value in line.split()])  # Pega apenas os 3 últimos valores
        return np.array(coords)

# Função para calcular o crossplotting
def calculate_crossplotting(far_coords, near_coords, a=1, b=1):
    # n é o número de coordenadas
    n = far_coords.shape[0]

    # Inicializando GR e IN
    GR = far_coords[:, 2]  # Gradiente é o valor z do FAR
    IN = near_coords[:, 2]  # Intercept é o valor z do NEAR

    # Equação 1: GRi = ∑ GR(i,j) / n
    GRi = np.mean(GR)

    # Equação 2: INj = ∑ IN(i,j) / n
    INj = np.mean(IN)

    # Equação 3: AVOID(i,j) = IN(i,j) - INj
    AVOID = IN - INj

    # Equação 4: AVOGD(i,j) = GR(i,j) - GRi
    AVOGD = GR - GRi

    # Equação 5: WAVO(i,j) = a * AVOID(i,j) + b * AVOGD(i,j)
    WAVO = a * AVOID + b * AVOGD

    return IN, GR, WAVO

# Função para plotar Intercept vs Gradient
def plot_intercept_vs_gradient(IN, GR):
    plt.scatter(IN, GR, c='blue', label='Intercept vs Gradient')
    plt.title('Crossplot: Intercept vs Gradient')
    plt.xlabel('Intercept (IN)')
    plt.ylabel('Gradient (GR)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Caminhos dos arquivos .xyz
far_file_path = 'CSO-7F_FAR.xyz'
near_file_path = 'CSO-7F_NEAR.xyz'

# Ler as coordenadas dos arquivos
far_coords = read_xyz(far_file_path)
near_coords = read_xyz(near_file_path)

# Calcular crossplotting
IN, GR, WAVO = calculate_crossplotting(far_coords, near_coords)

# Plotar o gráfico Intercept (x) pelo Gradient (y)
plot_intercept_vs_gradient(IN, GR)
