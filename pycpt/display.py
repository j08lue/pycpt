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


def show_matplotlib_colormaps():
    plt.rc('text', usetex=False)
    a = np.outer(np.arange(0,1,0.01),np.ones(10))
    fig = plt.figure(figsize=(10,5))
    fig.subplots_adjust(top=0.8,bottom=0.05,left=0.01,right=0.99)
    cmaps = [m for m in plt.cm.datad if not m.endswith('_r')]
    cmaps.sort()
    l=len(cmaps)+1
    for i,m in enumerate(cmaps):
        plt.subplot(1,l,i+1)
        plt.axis('off')
        plt.imshow(a,aspect='auto',cmap=plt.get_cmap(m),origin='lower')
        plt.title(m,rotation=90,fontsize=10)
    plt.show(fig)


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
