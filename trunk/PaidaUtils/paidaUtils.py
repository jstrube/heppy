import paida.paida_gui.PGuiSelector
paida.paida_gui.PGuiSelector.setGuiEngineName('batch')
from paida import IAnalysisFactory, PTypes
import numpy as N


numpyTypes2PaidaTypes = {
    N.int32  : PTypes.Integer
  , N.int64  : PTypes.Long
  , N.float32: PTypes.Float
  , N.float64: PTypes.Double
  , N.int8   : PTypes.Byte}


def tupleColumn2array(tuple, evaluator, filt=None):
    """ Converts the tuple column to a numpy array.
        tuple: ITuple object
        evaluator: IEvaluator object
        filt: IFilter object
    """
    evaluator.initialize(tuple)
    if filt:
        filt.initialize(tuple)
    tuple.start()
    values = []
    # premature optimization: I can save an if in the loop...
    if filt:
        while tuple.next():
            if filt.accept():
                values.append(evaluator.evaluateDouble())
    else:
        while tuple.next():
            values.append(evaluator.evaluateDouble())
    return N.array(values)


class PAIDA(object):
    """ convenience class to convert numpy arrays to AIDA objects
        This is a prime candidate for a singleton/borg/whatever
    """

    def __init__(self):
        self.af = IAnalysisFactory.create()
        self.treeFactory = self.af.createTreeFactory()
        #self.tree = self.treeFactory.create()
        #self.histogramFactory = self.af.createHistogramFactory(self.tree)
        #self.fitFactory = self.af.createFitFactory()
        #self.tupleFactory = self.af.createTupleFactory(self.tree)
        #self.dataPointSetFactory = self.af.createDataPointSetFactory(self.tree)


    def hist1D(self, data, bins=10, label='data'):
        """ Calculates a histogram much like pylab.hist, only with the Paida methods
            Meant as an in-situ replacement for pylab.hist, because the Paida histogramming methods are much more powerful
            Returns a Paida cloud that has been converted to a histogram
        """
        cloud = self.histogramFactory.createCloud1D(label)
        map(cloud.fill, data)
        cloud.convert(bins)
        return cloud.histogram()


    def hist2D(self, data, xbins=10, ybins=10, label='data'):
        """ creates a IHistogram2D from the given array"""
        cloud = self.histogramFactory.createCloud2D(label)
        for row in data:
            cloud.fill(row[0], row[1])
        cloud.convert(xbins, ybins)
        return cloud.histogram()


    def cloud1D(self, data, label='data'):
        """ Creates a cloud1D from the given array"""
        cloud = self.histogramFactory.createCloud1D(label)
        cloud._entryList[0] = data
        cloud._entryList[1] = N.ones_like(data)
        cloud._sumOfWeights = len(data)
        cloud._sumOfTorques[0] = data
        cloud._sumOfInertials[0] = data**2
        cloud._lowerEdges = [N.min(data), 0.0, 0.0]
        cloud._upperEdges = [N.max(data), 0.0, 0.0]

    
    def open(self, filename, option='r'):
        """ mimicks the file open syntax for ITrees"""
        if option == 'r':
            readOnly = True
            createNew = False
        elif option == 'w':
            readOnly = False
            createNew = True
        elif option == 'a':
            readOnly = False
            createNew = False
        return self.treeFactory.create(filename, readOnly=readOnly, createNew=createNew)

paida = PAIDA()
