import numpy as np

class Histogram(object):
    """
    This is a one-dimensional histogram with full outlier handling.
    The convention for numbering the bins is:
    start from 0.
    If you care about all entries,
    set the left edge of the first bin to -inf,
    the right edge of the last bin to +inf
    """
    class Entry(object):
        """
        Each entry has a weight, such that each bin has an error and a height
        """
        entry = 0
        weight = 0
    def __init__(self, binEdges, data=None):
        """
        This is the constructor.
        The histogram must be created with the bins edges. (Left edges + the last right edge)
        """
        self.binEdges = binEdges
        self.entries = np.zeros(len(binEdges)-1, np.int32)
        self.weights = np.zeros(len(binEdges)-1, np.float64)
        self.weights_squared = np.zeros(len(binEdges)-1, np.float64)
        self.torques = np.zeros(len(binEdges)-1, np.float64)
        self.inertials = np.zeros(len(binEdges)-1, np.float64)
        if data is not None:
            self.entries=np.histogram(data, binEdges, new=True)[0]


    def fill(self, x, weight=1.):
        index = self.find_index(x)
        if index is None:
            return
        self.entries[index] += 1
        self.weights[index] += weight
        self.weights_squared[index] += weight*weight
        self.torques[index] += x*weight
        self.inertials[index] += x*x*weight
        
        
    def find_index(self, x):
        """
        Returns the index of the bin that this item would be put into
        """
        if x < self.binEdges[0]:
            return None
        # we shift the index of the binEgdes by starting at 1
        # thats why we return i rather than i-1
        for i, edge in enumerate(self.binEdges[1:]):
            if x < edge:
                return i

    def _compute_rms(self):
        return sum(self.torques)
        
    def _compute_mean(self):
        return sum(self.entries)

    rms = property(_compute_rms, doc="The root mean square is defined as")

    mean = property(_compute_mean, doc="The mean value of all entries")

    def __add__(self, other):
        if not all(self.binEdges == other.binEdges):
            print "ERROR! The bin egdes must be the same for both histograms"
            return
        h = Histogram(self.binEdges)
        h.entries = self.entries + other.entries
        h.weights = self.weights + other.weights
        h.weights_squared = self.weights_squared + other.weights_squared
        raise NotImplementedError, "The weights are not yet dealt with properly"
        return h
        

    def ks_test():
        raise NotImplementedError, "Implementing a KS test may require depending on scipy"

