import os.path
import numpy as np

try:
    from urllib.parse import urljoin
    from urllib.request import urlretrieve, urlopen, Request
except ImportError:
    from urllib2 import urlretrieve, urlopen, Request
    from urlparse import urljoin

url = 'ngdc/ETOPO1.cpt'

download=True

baseurl='http://soliton.vm.bytemark.co.uk/pub/cpt-city/'

url = urljoin(baseurl, url)
    
fname = os.path.basename(url)
urlretrieve(url, fname)

data = np.genfromtxt(fname, skip_header=10)


print(data)
