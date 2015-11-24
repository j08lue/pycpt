"""Display matplotlib colormaps"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colorbar import ColorbarBase

from . import load


def colormap_demo(cmap):
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

    fig, axes = plt.subplots(
            nrows=len(cmap_list), 
            figsize=(6,.5*len(cmap_list)))
    fig.subplots_adjust(top=1, bottom=0, left=0, right=0.9)

    for ax, cmap in zip(axes, cmap_list):
        if isinstance(cmap, basestring):
            cmap = plt.get_cmap(cmap)
        ax.imshow(gradient, aspect='auto', cmap=cmap)
        pos = list(ax.get_position().bounds)
        x_text = pos[0] + pos[2] + 0.02
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, cmap.name, va='center', ha='left', fontsize=12)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()

    return fig


def plot_colormap(cmap, continuous=True, discrete=True, ndisc=9):
    """Make a figure displaying the color map in continuous and/or discrete form
    """
    nplots = int(continuous) + int(discrete)
    fig, axx = plt.subplots(figsize=(6,.5*nplots), nrows=nplots, frameon=False)
    axx = np.asarray(axx)
    i=0
    if continuous:
        norm = mcolors.Normalize(vmin=0, vmax=1)
        ColorbarBase(axx.flat[i], cmap=cmap, norm=norm, orientation='horizontal') ; i+=1
    if discrete:
        colors = cmap(np.linspace(0, 1, ndisc))
        cmap_d = mcolors.ListedColormap(colors, name=cmap.name)
        norm = mcolors.BoundaryNorm(np.linspace(0, 1, ndisc+1), len(colors))
        ColorbarBase(axx.flat[i], cmap=cmap_d, norm=norm, orientation='horizontal')
    for ax in axx.flat:
        ax.set_axis_off()
    fig.text(0.95, 0.5, cmap.name, va='center', ha='left', fontsize=12)


def show_matplotlib_colormaps():
    """Plot a list of all colormaps distributed with matplotlib"""
    cmaps = [m for m in plt.cm.datad if not m.endswith('_r')]
    cmaps.sort()
    return plot_colormaps(cmaps)


def demo_uoregon():
    """Plot a demo of a color map from University of Oregon"""
    cmap = load.cmap_from_geo_uoregon('BuOr_8')
    colormap_demo(cmap)


def demo_gmt():
    """Plot a demo of a .cpt / GMT color map from cptcity"""
    cmap = load.cmap_from_cptcity_url('http://soliton.vm.bytemark.co.uk/pub/cpt-city/ma/gray/grayscale02.cpt')
    colormap_demo(cmap)



if __name__ == 'main':
    
    demo_uoregon()

    demo_gmt()
