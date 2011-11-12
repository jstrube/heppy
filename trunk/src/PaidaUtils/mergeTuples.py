#!/usr/bin/env python
""" 
    mergeTuples.py
    takes a list of tuples to merge and writes them all into the same tree
    similar to the cp and mv commands, the last argument is the name of the targetFile
    TODO: use optparse to allow a list of tuples in each file


    usage: mergeTuples.py <tuplename> <filename1 [, filename2, ...]> <targetname>
"""
import paida.paida_gui.PGuiSelector
paida.paida_gui.PGuiSelector.setGuiEngineName('batch')

from paida import IAnalysisFactory
import os
import sys

def getChain(tupleName, listOfTrees, targetName):
    """ creates a chain from a list of trees and returns the target tree
        
        tupleName: Name of the tuple that has to be available in each file
        listOfTrees: an iterable that contains the filenames of the trees
            that should be merged
        targetName: filename of the tree that contains the merged tuples
    """
    af = IAnalysisFactory.create()
    tf = af.createTreeFactory()
    if os.path.exists(targetName):
        raise SystemError('The target file exists. Bailing out to prevent data loss')
    tree = tf.create(targetName, readOnly=False, createNew=True)
    tupleFactory = af.createTupleFactory(tree)
    allTuples = []
    for treeName in listOfTrees:
        # open file in readonly mode to prevent data loss
        t = tf.create(treeName, readOnly=True)
        allTuples.append(t.find(tupleName))
    tuple = tupleFactory.createChained(tupleName, allTuples[0].title(), allTuples)
    return tree


if __name__ == '__main__':
    tree = getChain(sys.argv[1], sys.argv[2:-1], sys.argv[-1])
    
    tree.commit()
    tree.close()

