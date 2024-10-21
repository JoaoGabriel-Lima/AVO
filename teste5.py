import numpy as np
import matplotlib.pyplot as plt

# Função para ler arquivo .xyz e retornar as coordenadas
def read_xyz(file):
    coordinates = []
    with open(file, 'r') as f:
        lines = f.readlines()[14:]  # Ignora as duas primeiras linhas
        for line in lines:
            parts = line.split()
            # Extrai as coordenadas x, y, z (as colunas 2, 3, 4)
            coordinates.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return np.array(coordinates)

# Função para calcular a diferença de coordenadas Z entre FAR e NEAR
def calculate_z_difference(far_coords, near_coords):
    return far_coords[:, 2] - near_coords[:, 2]  # Diferença das coordenadas Z

# Lê os arquivos .xyz
near_file = 'CSO-7F_NEAR.xyz'
far_file = 'CSO-7F_FAR.xyz'


near_coords = read_xyz(near_file)
far_coords = read_xyz(far_file)

# Calcula a diferença nas coordenadas Z
z_difference = calculate_z_difference(far_coords, near_coords)

# Seleciona as coordenadas X e Y
x_coords = near_coords[:, 0]  # Coordenadas X (iguais em ambos os arquivos)
y_coords = near_coords[:, 1]  # Coordenadas Y (iguais em ambos os arquivos)

# Plotar os pontos
plt.figure(figsize=(8, 6))

# Categorizar a diferença Z em três faixas de cores (azul, amarelo, vermelho)
plt.scatter(x_coords, y_coords, c='gray', label='Diferença Z Desprezível')
# for i in range(len(x_coords)):
#     if abs(z_difference[i]) < 1:
#         plt.scatter(x_coords[i], y_coords[i], c='blue', label='Pequena Diferença Z' if i == 0 else "")
#     elif 1 <= abs(z_difference[i]) < 3:
#         plt.scatter(x_coords[i], y_coords[i], c='yellow', label='Diferença Moderada Z' if i == 0 else "")
#     else:
#         plt.scatter(x_coords[i], y_coords[i], c='red', label='Diferença Grande Z' if i == 0 else "")

# Configurações do gráfico
plt.xlim(-10, 10)  # Definir limites do eixo X, ajuste conforme necessário
plt.ylim(-10, 10)  # Definir limites do eixo Y, ajuste conforme necessário
plt.xlabel('Near')
plt.ylabel('Far - Near')
plt.title('Plot 2D das Coordenadas X e Y - Diferença em Z')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()