import unittest

import matplotlib.pyplot as plt
import numpy as np

from pycpt.modify import reverse_cmap

class TestReverse(unittest.TestCase):

    def test_modify_reverse_cmap(self):
    
        cmap = plt.get_cmap('jet')

        cmap_r = reverse_cmap(cmap)
        cmap_r_r = reverse_cmap(cmap_r)

        def _cmdata(cmap):
            return np.array(cmap._segmentdata['red'])

        self.assertTrue(np.allclose(_cmdata(cmap), _cmdata(cmap_r_r)))



if __name__ == '__main__':
    unittest.main()
