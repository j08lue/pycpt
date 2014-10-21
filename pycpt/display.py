import numpy as np
import matplotlib.pyplot as plt

from . import load


def plot_colormap(cmap):
    """Make a demo plot of a given colormap with random data."""
    fig = plt.figure()
    ax = fig.gca()
    img = ax.pcolor(np.random.rand(10,10),cmap=cmap)
    cb = plt.colorbar(img)
    cb.ax.set_ylim(cb.ax.get_ylim()[::-1])
    fig.show()
    return fig

def plot_colormaps(cmap_list):
    """Plot a list of color gradients with their names
    
    Credits
    -------
    http://matplotlib.org/examples/color/colormaps_reference.html
    """
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    fig, axes = plt.subplots(nrows=len(cmap_list))
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)

    for ax, cmap in zip(axes, cmap_list):
        if isinstance(cmap, basestring):
            cmap = plt.get_cmap(cmap)
        ax.imshow(gradient, aspect='auto', cmap=cmap)
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, cmap.name, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()

    plt.show()
    return fig


def show_matplotlib_colormaps():
    cmaps = [m for m in plt.cm.datad if not m.endswith('_r')]
    cmaps.sort()
    return plot_colormaps(cmaps)


def demo_uoregon():
    """Plot a demo of a color map from University of Oregon"""
    cmap = load.cmap_from_geo_uoregon('BuOr_8')
    plot_colormap(cmap)


def demo_gmt():
    """Plot a demo of a .cpt / GMT color map from cptcity"""
    cmap = load.cmap_from_cptcity_url('http://soliton.vm.bytemark.co.uk/pub/cpt-city/ma/gray/grayscale02.cpt')
    plot_colormap(cmap)



if __name__ == 'main':
    
    demo_uoregon()

    demo_gmt()
