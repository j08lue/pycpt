"""Tools to modify matplotlib colormaps"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import copy

def cmap_xmap(function, cmap, name=None):
    """Applies function on the indices of colormap cmap. Beware, function
    should map the [0, 1] segment to itself, or you are in for surprises."""
    cmap = copy.deepcopy(cmap)
    cdict = cmap._segmentdata
    for key in cdict:
        cdict[key] = sorted([(function(x[0]), x[1], x[2]) for x in cdict[key]])
    if name is not None: cmap.name = name
    return mcolors.LinearSegmentedColormap(cmap.name, cdict, cmap.N)


def reverse_cmap(cmap, newname=None):
    """Reverse a given matplotlib colormap instance"""
    if newname is None:
        newname = cmap.name + '_r'
    return cmap_xmap(lambda x: -1.*(x-1.), cmap, name=newname)


def generate_cmap_norm(levels, cm, extend='neither', name='from_list', return_dict=False):
    """Generate a color map and norm from levels and a colormap (name)
    
    Parameters
    ----------
    levels : iterable of levels
        data levels
    cm : cmap or name of registered cmap
        color map
    extend : str [ neither | both | min | max ]
        which edge(s) of the color range to extend
    name : str, optional
        new name for colormap
    return_dict : bool
        return dictionary
    """
    if isinstance(cm, str):
        cm = plt.get_cmap(cm)
    nplus = [-1,0,0,1][['neither','min','max','both'].index(extend)]
    N = len(levels) + nplus
    colors = cm(np.linspace(0, 1, N))
    cmap = mcolors.ListedColormap(colors, name=(name or cm.name))
    if extend in ['min', 'both']:
        cmap.set_under(colors[0])
    else:
        cmap.set_under('none')
    if extend in ['max', 'both']:
        cmap.set_over(colors[-1])
    else:
        cmap.set_over('none')
    cmap.colorbar_extend = extend
    norm = mcolors.BoundaryNorm(levels, N)
    if return_dict:
        return dict(cmap=cmap, norm=norm)
    else:
        return cmap, norm



