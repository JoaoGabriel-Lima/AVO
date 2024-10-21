import matplotlib.pyplot as plt
import numpy as np

def read_xyz(file):
    coordinates = []
    with open(file, 'r') as f:
        lines = f.readlines()[14:]  # Ignora as duas primeiras linhas
        for line in lines:
            parts = line.split()
            # Extrai as coordenadas x, y, z (as colunas 2, 3, 4)
            coordinates.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return np.array(coordinates)

# Caminho para os arquivos Near e Far
near_file = 'CSO-7F_NEAR.xyz'
far_file = 'CSO-7F_FAR.xyz'

# Ler as coordenadas dos arquivos
near_coords = read_xyz(near_file)
far_coords = read_xyz(far_file)


# Verificar se os arquivos têm o mesmo número de coordenadas
if len(near_coords) != len(far_coords):
    raise ValueError("Os arquivos Near e Far devem ter o mesmo número de coordenadas.")



# Extrair as coordenadas desejadas (supondo que você queira usar as coordenadas x)
near_x = [coord[0] for coord in near_coords]  # Usando x das coordenadas Near
near_y = [coord[1] for coord in near_coords]    # Usando x das coordenadas Far (pode mudar para y ou z se quiser)
near_z = np.array([coord[2] for coord in near_coords] )   # Usando x das coordenadas Far (pode mudar para y ou z se quiser)

# remove all lines in near_coors where z is -1.e_32
near_coords_NEW = np.array([coord for coord in near_coords if coord[2] != -1.000000e+32])
near_z_scaled = near_z * -10


print(near_coords_NEW)
near_coords_NEW_x = [coord[0] for coord in near_coords_NEW]  
near_coords_NEW_y = [coord[1] for coord in near_coords_NEW]   
near_coords_NEW_z = np.array([coord[2] for coord in near_coords_NEW] )  

# Criar o gráfico 2D
plt.figure(figsize=(8, 6))
plt.scatter(near_coords_NEW_x, near_coords_NEW_y, c=near_coords_NEW_z, cmap='rainbow', marker='o')

# Adicionar rótulos e título
plt.xlabel('Near (x)')
plt.ylabel('Near (y)')
plt.title('Plot 2D: Near vs Far')

# Mostrar o gráfico
plt.grid(True)
plt.show()