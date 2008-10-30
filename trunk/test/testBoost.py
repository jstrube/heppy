from Geometry.geometry import Momentum
from math import sqrt

def testBoost():
    """ Boosts a particle to the rest frame of another particle
    This ensures that the answer is the same as for TLorentzVector
    
    The example is taken from an actual MC decay, so the daughters should add up to the mother
    (modulo bremsstrahlung or FSR that was lost)
    >>> m1 = Momentum(5.279, 1.1, 2.2, 3.3)
    >>> m2 = Momentum(13, 0.0, 2.3, 4.5)
    >>> frame = m1.restFrame
    >>> x = frame.coordinatesOf(m2)
    >>> print x.x, x.y, x.z, x.t
    -3.55408552687 -4.80817105373 -6.1622565806 14.737144872
    """
    def makeP4(mass, *p):
        return Momentum(sqrt(mass*mass+p[0]*p[0]+p[1]*p[1]+p[2]*p[2]), *p)
    theB = makeP4(5.1207628250, 0.3115499020, 0.1814490259, 2.9952230453)
    theLambda = makeP4(1.1199678183, -0.7292688489, -0.6621993780, 1.4447448254)
    theP = makeP4(0.938, 0.7323909402, 1.9576436281, 1.4391242266)
    theGamma = makeP4(0, 0.3084278107, -1.1139951944, 0.1113540083)
    
    theSum = theLambda+theP+theGamma - theB
    assert theSum.e < 1e-4
    assert theSum.x < 1e-4
    assert theSum.y < 1e-4
    assert theSum.z < 1e-4
    
    frame = theB.restFrame
    Lambda_star = frame.coordinatesOf(theLambda)
    Gamma_star = frame.coordinatesOf(theGamma)
    P_star = frame.coordinatesOf(theP)
    B_star = frame.coordinatesOf(theB)
    
    theSum = Lambda_star+Gamma_star+P_star - B_star
    assert theSum.e < 1e-4
    assert theSum.x < 1e-4
    assert theSum.y < 1e-4
    assert theSum.z < 1e-4
    
if __name__ == '__main__':
    testBoost()