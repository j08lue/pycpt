import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import copy

def cmap_xmap(function,cmap,name=None):
    """Applies function on the indices of colormap cmap. Beware, function
    should map the [0, 1] segment to itself, or you are in for surprises."""
    cmap = copy.deepcopy(cmap)
    cdict = cmap._segmentdata
    function_to_map = lambda x : (function(x[0]), x[1], x[2])
    for key in ('red','green','blue'):
        cdict[key] = map(function_to_map, cdict[key])
        cdict[key].sort()
        assert (cdict[key][0]<0 or cdict[key][-1]>1), "Resulting indices extend out of the [0, 1] segment."
    if name is not None: cmap.name = name
    return mcolors.LinearSegmentedColormap(cmap.name,cdict,cmap.N)


def reverse_cmap(cmap,newname=None):
    """Reverse a given matplotlib colormap instance"""
    if newname is None:
        newname = cmap.name + '_r'
    return cmap_xmap(lambda x: -1.*(x-1.),cmap,name=newname)


def generate_cmap_norm(levels, cm, extend='neither'):
    """Generate a color map and norm from levels and a colormap (name)
    
    Parameters
    ----------
    levels : iterable of levels
        data levels
    cm : cmap or name of registered cmap
        color map
    extend : str [ neither | both | min | max ]
        which edge(s) of the color range to extend
    """
    if isinstance(cm, basestring):
        cm = plt.get_cmap(cm)
    nplus = [-1,0,0,1][['neither','min','max','both'].index(extend)]
    N = len(levels) + nplus
    colors = cm(np.linspace(0, 1, N))
    cmap = mcolors.ListedColormap(colors)
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
    return cmap, norm



