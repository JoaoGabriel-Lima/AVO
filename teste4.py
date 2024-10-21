import matplotlib.pyplot as plt

# Função para carregar os valores de NEAR e FAR de um arquivo .xyz
def load_xyz_data(file_path):
    near_values = []
    far_values = []
    
    with open(file_path, 'r') as file:
        for line in file:
            values = line.split()
            if len(values) == 3:
                near = float(values[0])  # Primeiro valor: NEAR
                far = float(values[1])   # Segundo valor: FAR
                near_values.append(near)
                far_values.append(far)
    
    return near_values, far_values

# Função para plotar os valores
def plot_near_far(near_values, far_values):
    delta_far_near = [far - near for far, near in zip(far_values, near_values)]
    
    plt.figure(figsize=(8, 6))
    plt.scatter(near_values, delta_far_near, color='blue', label='FAR - NEAR')
    plt.title('Plot of NEAR vs (FAR - NEAR)')
    plt.xlabel('NEAR')
    plt.ylabel('FAR - NEAR')
    plt.grid(True)
    plt.legend()
    plt.show()

# Caminhos dos arquivos .xyz
file_path1 = 'CSO-7F_FAR.xyz'
file_path2 = 'CSO-7F_NEAR.xyz'


# Carregar os dados dos dois arquivos
near_values1, far_values1 = load_xyz_data(file_path1)
near_values2, far_values2 = load_xyz_data(file_path2)

# Plotar os dados do primeiro arquivo
plot_near_far(near_values1, far_values1)

# Plotar os dados do segundo arquivo (opcional)
# plot_near_far(near_values2, far_values2)
