import numpy as np
import matplotlib.colors as mcolors
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


def generate_cmap_norm(levels,cm):
    colors = cm(np.linspace(0, 1, len(levels)+1))
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(levels, cmap.N)
    return cmap,norm



