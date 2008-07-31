import numpy as np

from Histogram import Histogram
"""
This test suit ensures sane properties of the histogram classes.
We start out with a simple comparison with numpy
"""
data = np.random.randn(10000)
bins = np.concatenate([-np.random.random_sample(5), np.random.random_sample(5)])
bins.sort()

#for comparison
npHist = np.histogram(data, bins, new=True)


def test_constructor():
    #empty histogram
    h0 = Histogram(bins)
    assert sum(h0.entries) == 0
    assert sum(h0.weights) == 0.0
    
    #directly filled histogram
    h1 = Histogram(bins, data)
    for i, b in enumerate(h1.entries):
        assert b == npHist[0][i]
    
    for i, b in enumerate(h1.binEdges):
        assert b == bins[i]
        assert b == npHist[1][i]
        

def test_methods():
    h1 = Histogram(bins)
    for d in data:
        h1.fill(d)
    print bins
    print h1.entries
    print npHist[0]
    print sum(h1.entries)
    for i, b in enumerate(h1.entries):
        assert b == npHist[0][i]

    for i, b in enumerate(h1.binEdges):
        assert b == bins[i]
        assert b == npHist[1][i]

