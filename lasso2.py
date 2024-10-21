import numpy as np
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
import matplotlib.pyplot as plt
from matplotlib import cm

class SelectFromCollection:
    """
    Select indices from a matplotlib collection using `LassoSelector`.

    Selected indices are saved in the `ind` attribute. This tool fades out the
    points that are not part of the selection (i.e., reduces their alpha
    values). If your collection has alpha < 1, this tool will permanently
    alter the alpha values.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : `~matplotlib.axes.Axes`
        Axes to interact with.
    collection : `matplotlib.collections.Collection` subclass
        Collection you want to select from.
    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to *alpha_other*.
    """

    def __init__(self, ax, collection, cmap, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other
        self.cmap = cmap

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Get current color array if exists, or create a default one
        self.colors = collection.get_array()
        if self.colors is None:
            self.colors = np.ones(self.Npts)  # Start with ones (full opacity)

        self.lasso = LassoSelector(ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]

        # Only change colors for the selected points
        new_colors = self.colors.copy()  # Preserve original colors
        new_colors[self.ind] = 1  # Set selected points to max alpha
        self.colors[self.ind] = self.alpha_other  # Fade out selected points

        # Update the colormap and colors for selected points
        self.collection.set_array(new_colors)
        self.collection.set_cmap(self.cmap)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        # Reset colors when done
        self.collection.set_array(self.colors)
        self.canvas.draw_idle()


if __name__ == '__main__':
    np.random.seed(19680801)
    data = np.random.rand(100, 2)

    fig, ax = plt.subplots()
    pts = ax.scatter(data[:, 0], data[:, 1], s=80, cmap=cm.viridis)

    selector = SelectFromCollection(ax, pts, cmap=cm.viridis)

    def accept(event):
        if event.key == "enter":
            print("Selected points:")
            print(selector.xys[selector.ind])
            selector.disconnect()
            ax.set_title("")
            fig.canvas.draw()

    fig.canvas.mpl_connect("key_press_event", accept)
    ax.set_title("Press enter to accept selected points.")

    plt.show()