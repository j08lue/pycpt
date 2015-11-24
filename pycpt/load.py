"""Load colormaps from a variety of sources, mainly .cpt though"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
try:
    from urllib.parse import urljoin
    from urllib.request import urlretrieve, urlopen, Request
except ImportError:
    from urllib2 import urlretrieve, urlopen, Request
    from urlparse import urljoin
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import colorsys
import os
import fnmatch

from . import modify

def _cmap_name_from_path(fpath, root='cpt-city', maxdepth=5):
    """Generates a colormap name from a path
    
    Parameters
    ----------
    fpath : str
        full fpath to cpt file
    root : str, optional
        base path
    maxdepth : int
        max depth of path to include in cmap name

    Function will parse the path down to *root* or until *maxdepth* is reached.
    """
    fpath = os.path.splitext(fpath)[0]
    prename = ''
    end = ''
    for i in range(maxdepth):
        fpath, end = os.path.split(fpath)
        if end == root:
            break
        elif end != '':
            if prename == '':
                prename = end
            else:
                prename = end+'/'+prename
    return prename


def find_cpt_files(cmapdir, **kwargs):
    """Find .cpt files in a given path and generate names
    
    Parameters
    ----------
    cmapdir : str
        directory below which the files are
    kwargs : dict
        keyword arguments passed to _cmap_name_from_path()
    """
    cptcitycmaps = {}
    for root, dirnames, filenames in os.walk(cmapdir):
        for filename in fnmatch.filter(filenames, '*.cpt'):
            cmapfile = os.path.join(root, filename)
            cmapname = _cmap_name_from_path(cmapfile, **kwargs)
            cptcitycmaps[cmapname] = cmapfile
            
    return cptcitycmaps


def register_cptcity_cmaps(cptcitycmaps, urlkw={}, cmapnamekw={}):
    """Register cpt-city colormaps from a list of URLs and/or files to the current plt.cm space
    
    Parameters
    ----------
    cptcitycmaps : str, dict, or list
        str will be interpreted as path to scan for .cpt files
        list over file names or urls to .cpt files
        dict can be used to provide (name : fname/url) mappings
    urlkw : dict
        keyword arguments passed to cmap_from_cptcity_url

    Usage
    -----
    To register a set of color maps, use, e.g.
        
        register_cptcity_cmaps({'ncl_cosam' : "http://soliton.vm.bytemark.co.uk/pub/cpt-city/ncl/cosam.cpt"})

    Retrieve the cmap using,
    
        plt.cm.get_cmap('ncl_cosam')

    """
    def _register_with_reverse(cmap):
        plt.cm.register_cmap(cmap=cmap)
        plt.cm.register_cmap(cmap=modify.reverse_cmap(cmap))

    def _try_reading_methods(cmapfile, cmapname=None):
        try:
            return gmtColormap(cmapfile, name=cmapname)
        except IOError:
            try:
                return cmap_from_cptcity_url(cmapfile, name=cmapname, **urlkw) 
            except:
                raise

    if isinstance(cptcitycmaps, str):
        if cptcitycmaps.endswith('.cpt'):
            cptcitycmaps = [cptcitycmaps]
        else:
            cptcitycmaps = find_cpt_files(cptcitycmaps, **cmapnamekw)

    cmaps = []

    if isinstance(cptcitycmaps, dict):
        for cmapname, cmapfile in cptcitycmaps.items():
            cmap = _try_reading_methods(cmapfile, cmapname)
            _register_with_reverse(cmap)
            cmaps.append(cmap)
    else:
        for cmapfile in cptcitycmaps:
            cmap = _try_reading_methods(cmapfile)
            _register_with_reverse(cmap)
            cmaps.append(cmap)

    return cmaps


def gmtColormap(cptfile, name=None):
    """Read a GMT color map from a cpt file

    Parameters
    ----------
    cptfile : str
        path to .cpt file
    name : str, optional
        name for color map
        if not provided, the file name will be used
    """

    def _gmtColormap_openfile(cptf,name=None):
        """Read a GMT color map from an OPEN cpt file

        Parameters
        ----------
        cptf : open file or url handle
            path to .cpt file
        name : str, optional
            name for color map
            if not provided, the file name will be used
        """
        # generate cmap name
        if name is None:
            name = '_'.join(os.path.basename(cptf.name).split('.')[:-1])

        # process file
        x = []
        r = []
        g = []
        b = []
        for l in cptf.readlines():
            ls = l.split()

            # parse header info
            if l[0] == "#":
                if ls[-1] == "HSV":
                    colorModel = "HSV"
                    continue
                else:
                    colorModel = "RGB"
                    continue

            # skip BFN info
            if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
                pass
            else:
                # parse color vectors
                x.append(float(ls[0]))
                r.append(float(ls[1]))
                g.append(float(ls[2]))
                b.append(float(ls[3]))
                xtemp = float(ls[4])
                rtemp = float(ls[5])
                gtemp = float(ls[6])
                btemp = float(ls[7])
        x.append(xtemp)
        r.append(rtemp)
        g.append(gtemp)
        b.append(btemp)

        x,r,g,b = map(np.array,[x,r,g,b])

        if colorModel == "HSV":
            for i in range(r.shape[0]):
                # convert HSV to RGB
                rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
                r[i] = rr ; g[i] = gg ; b[i] = bb
        elif colorModel == "RGB":
            r = r/255.
            g = g/255.
            b = b/255.

        red = []
        blue = []
        green = []
        xNorm = (x - x[0])/(x[-1] - x[0])
        for i in range(len(x)):
            red.append([xNorm[i],r[i],r[i]])
            green.append([xNorm[i],g[i],g[i]])
            blue.append([xNorm[i],b[i],b[i]])

        # return colormap
        cdict = dict(red=red,green=green,blue=blue)
        return mcolors.LinearSegmentedColormap(name=name,segmentdata=cdict)

    try:
        return _gmtColormap_openfile(cptfile,name=name)
    except:
        with open(cptfile) as cptf:
            return _gmtColormap_openfile(cptf,name=name)


def cmap_from_cptcity_url(url,
        baseurl='http://soliton.vm.bytemark.co.uk/pub/cpt-city/',
        download=False, name=None):
    """Create a colormap from a url at cptcity

    Parameters
    ----------
    url : str
        relative or absolute URL to a .cpt file
    baseurl : str, optional
        main directory at cptcity
    download : bool
        whether to download the colormap file to the current working directory
    name : str, optional
        name for color map
    """

    url = urljoin(baseurl,url)
        
    if download:
        fname = os.path.basename(url)
        urlretrieve(url,fname)

        return gmtColormap(fname,name=name)
    
    else:
        # process file directly from online source
        #req = Request(url)
        response = urlopen(url)
        
        if name is None:
            name = '_'.join(os.path.basename(url).split('.')[:-1])
        
        return gmtColormap(response, name=name)
        

def cmap_from_geo_uoregon(cname,
        baseurl='http://geography.uoregon.edu/datagraphics/color/',
        download=False):
    """Parse an online file from geography.uoregon.edu to create a Python colormap"""
    ext = '.txt'

    url = baseurl + cname + ext
    
    # process file directly from online source
    req = Request(url)
    response = urlopen(req)
    rgb = np.loadtxt(response,skiprows=2)
    
    # save original file
    if download:
        fname = os.path.basename(url) + ext
        urlretrieve (url,fname)
        
    return mcolors.ListedColormap(rgb,cname)



