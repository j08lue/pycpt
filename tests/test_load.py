import unittest
import matplotlib.colors as mcolors
from pycpt.load import cmap_from_cptcity_url, cmap_from_geo_uoregon

class TestLoad(unittest.TestCase):

    def test_cmap_from_cptcity_url(self):
        cmap = cmap_from_cptcity_url('ngdc/ETOPO1.cpt')
        self.assertIsInstance(cmap, mcolors.LinearSegmentedColormap)

    def test_cmap_from_cptcity_url_download(self):
        cmap = cmap_from_cptcity_url('ngdc/ETOPO1.cpt', download=True)
        self.assertIsInstance(cmap, mcolors.LinearSegmentedColormap)

    def test_cmap_from_geo_uoregon(self):
        cmap = cmap_from_geo_uoregon('BuDRd_12')
        self.assertIsInstance(cmap, mcolors.ListedColormap)


if __name__ == '__main__':
    unittest.main()
