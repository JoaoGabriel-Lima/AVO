import numpy as np

from matplotlib.path import Path
from matplotlib.widgets import LassoSelector


class SelectFromCollection:

    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        self.lasso = LassoSelector(ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt

        
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


    closest_gradient_all = np.interp(near_amplitude_scaled, bin_centers, bin_means) - near_amplitude_scaled
    closest_intercept_all = np.interp(gradienteFarMinusNear_scaled, bin_centers_vertical,bin_means_vertical) - gradienteFarMinusNear_scaled

    v = np.column_stack((closest_gradient_all, closest_intercept_all))

    v_x = [coord[0] for coord in v]
    v_y = [coord[1] for coord in v]
    value = np.sqrt(np.square(v_x) + np.square(v_y))


    norms = np.linalg.norm(v, axis=1, keepdims=True)
    normalized_array = v / norms
    subplot_kw = dict( autoscale_on=True)
    fig, (ax2, ax1) = plt.subplots(subplot_kw=subplot_kw, nrows=1, ncols=2, figsize=(8, 6))

    wavomap= ax1.scatter((near_x), (near_y), c=v_x, cmap='nipy_spectral', marker='o')
   


    ax2.plot(bin_centers, bin_means, color='lime', label='Mean Difference Curve', linewidth=3)
    ax2.plot(bin_means_vertical, bin_centers_vertical, color='darkred', label='Mean Difference Curve', linewidth=3)

    pts = ax2.scatter((near_amplitude_scaled), (gradienteFarMinusNear_scaled), c='blue', marker='o')
    selector = SelectFromCollection(ax2, pts)

    def accept(event):
        if event.key == "enter":
            print("Selected points:")
            selected_points = selector.xys[selector.ind]
            selected_xy_wavomap = []

            for point in selected_points:
                near_amplitude_selected = point[0]
                near_index = np.nonzero(near_amplitude_scaled == near_amplitude_selected)

                gradiente_far_minus_near_selected = point[1]
                for index in near_index:
                    ponto_escolhido = near[index][0]
                    far_coordinate = far[np.nonzero((far[:,0] == ponto_escolhido[0]) & (far[:,1] == ponto_escolhido[1]))]

                    if far_coordinate.size > 0:
                        if (far_coordinate[0][2] - ponto_escolhido[2])*1000 == gradiente_far_minus_near_selected:
                            selected_xy_wavomap.append([ponto_escolhido[0], ponto_escolhido[1]])

            print(selected_xy_wavomap)


            x_wavomap = [coord[0] for coord in selected_xy_wavomap]
            y_wavomap = [coord[1] for coord in selected_xy_wavomap]
            ax1.scatter(x_wavomap, y_wavomap, c='black', marker='o')


            selector.disconnect()
            ax2.set_title("")
            fig.canvas.draw()

    fig.canvas.mpl_connect("key_press_event", accept)
    ax2.set_title("Press enter to accept selected points.")



    plt.show()