import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import numpy as np


def read_xyz(file):
    coordinates = []
    with open(file, 'r') as f:
        lines = f.readlines()[14:]  # Ignora as 14 primeiras linhas
        for line in lines:
            parts = line.split()
            coordinates.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return np.array(coordinates)

# Caminho para os arquivos Near e Far
near_file = 'CSO-7F_NEAR.xyz'
far_file = 'CSO-7F_FAR.xyz'

# Ler as coordenadas dos arquivos
near_coords = read_xyz(near_file)
far_coords = read_xyz(far_file)

if len(near_coords) != len(far_coords):
    raise ValueError("Os arquivos Near e Far devem ter o mesmo número de coordenadas.")

near = np.array([coord for coord in near_coords if coord[2] != -1.000000e+32])
near_amplitude = np.array([coord[2] for coord in near])  
near_x = [coord[0] for coord in near]  
near_y = [coord[1] for coord in near]   

far = np.array([coord for coord in far_coords if coord[2] != -1.000000e+32])
far_amplitude = np.array([coord[2] for coord in far])  

gradienteFarMinusNear = far_amplitude - near_amplitude
near_amplitude_scaled =  near_amplitude*1000
far_amplitude_scaled =  far_amplitude*1000
gradienteFarMinusNear_scaled = gradienteFarMinusNear*1000

fig, ax = plt.subplots(figsize=(8, 6))

# ! Linha Média Gradiente
bin_count = 40  # Número de bins para suavizar a curva
bins = np.linspace(min(near_amplitude_scaled), max(near_amplitude_scaled), bin_count)
bin_means = []
bin_centers = []

for i in range(len(bins) - 1):
    mask = (near_amplitude_scaled >= bins[i]) & (near_amplitude_scaled < bins[i + 1])
    if np.any(mask):  # Verifica se existem dados no bin
        mean_diff = np.mean(gradienteFarMinusNear_scaled[mask])
        bin_means.append(mean_diff)
        bin_centers.append((bins[i] + bins[i + 1]) / 2)

# Converter para arrays numpy para facilitar o plot
bin_centers = np.array(bin_centers)
bin_means = np.array(bin_means)

# ! Linha Média Intercept
bin_count_vertical = 30
bins_vertical = np.linspace(min(gradienteFarMinusNear_scaled), max(gradienteFarMinusNear_scaled), bin_count_vertical)
bin_means_vertical = []
bin_centers_vertical = []
for i in range(len(bins_vertical) - 1):
    mask = (gradienteFarMinusNear_scaled >= bins_vertical[i]) & (gradienteFarMinusNear_scaled < bins_vertical[i + 1])
    if np.any(mask): 
        mean_diff = np.mean(near_amplitude_scaled[mask])
        bin_means_vertical.append(mean_diff)
        bin_centers_vertical.append((bins_vertical[i] + bins_vertical[i + 1]) / 2)
bin_centers_vertical = np.array(bin_centers_vertical)
bin_means_vertical = np.array(bin_means_vertical)

ponto_azul = (near_amplitude_scaled[159], gradienteFarMinusNear_scaled[159])

data = np.nonzero(near_amplitude == -2.116889)
ponto_azul2 = (near_amplitude_scaled[4316], gradienteFarMinusNear_scaled[4316])

def criar_reta_avogd_avoid(ponto_azul):
    # Encontrar o valor mais próximo da curva média dos gradientes e intercepts
    closest_gradient_y = np.interp(ponto_azul[0], bin_centers, bin_means)
    closest_intercept_x = np.interp(ponto_azul[1], bin_centers_vertical,bin_means_vertical)

    # Vetor do ponto azul para a linha média dos gradientes
    plt.scatter(closest_intercept_x - ponto_azul[0], closest_gradient_y - ponto_azul[1], c='green', marker='o', s=100)
    plt.arrow(ponto_azul[0], ponto_azul[1], 0, closest_gradient_y - ponto_azul[1], 
            color='red', head_width=50, linewidth=3, length_includes_head=True, label='Vetor para média dos gradientes')

    # Vetor do ponto azul para a linha média dos intercepts
    plt.arrow(ponto_azul[0], ponto_azul[1], closest_intercept_x - ponto_azul[0], 0, 
            color='red', head_width=70, linewidth=3, length_includes_head=True, label='Vetor para média dos intercepts')

    # Calcular o vetor resultante (a soma dos dois vetores)
    resultant_vector_x = closest_intercept_x - ponto_azul[0]
    resultant_vector_y = closest_gradient_y - ponto_azul[1]

    # Desenhar o vetor resultante (linha preta diagonal)
    plt.arrow(ponto_azul[0], ponto_azul[1], resultant_vector_x, resultant_vector_y, 
            color='lime', head_width=70, linewidth=3, length_includes_head=True, label='Vetor resultante')

    # desenhe uma bola rosa em cada ponto
    plt.scatter(closest_intercept_x, closest_gradient_y, c='magenta', marker='o', s=100)
    return (closest_intercept_x, closest_gradient_y)

closest_gradient_all = np.interp(near_amplitude_scaled, bin_centers, bin_means) - near_amplitude_scaled
closest_intercept_all = np.interp(gradienteFarMinusNear_scaled, bin_centers_vertical,bin_means_vertical) - gradienteFarMinusNear_scaled

v = np.column_stack((closest_gradient_all, closest_intercept_all))

v_x = [coord[0] for coord in v]
v_y = [coord[1] for coord in v]
value = np.sqrt(np.square(v_x) + np.square(v_y))


norms = np.linalg.norm(v, axis=1, keepdims=True)
normalized_array = v / norms



ax.scatter((near_x), (near_y), c=value, cmap='nipy_spectral', marker='o', picker=True, pickradius=1)

with open('WAVO.xyz', 'w') as f:
    f.write(f'{len(near_x)}\n')
    f.write('WAVO\n')
    for i in range(len(near_x)):
        f.write(f'{np.format_float_scientific(near_x[i])} {np.format_float_scientific(near_y[i])} {np.format_float_scientific(value[i])}\n')




# ! CRIAR RETA ORTOGONAL A MÉDIA DOS GRADIENTES e INTERCEPTS

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot 2D: WAVO Map')
# Mostrar o gráfico
plt.grid(True)
plt.show()