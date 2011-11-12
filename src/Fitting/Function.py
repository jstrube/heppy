import numpy as np
from scipy.integrate import quadrature, romberg
from numpy import sin, cos, exp, log

class PDF:
    """
    A PDF is a normalized Function, i.e. the integral of a PDF is 1
    This version is one-D only
    """
    def __init__(self, fcn, data):
        a = min(data)
        b = max(data)
        print quadrature(fcn, 0, 1, maxiter=100)
        # not as good
        # print romberg(fcn, 0.00000001, 1)
        

def test1(x):
    return x**2 + sin(x)
    
def test2(x):
    return sin(x) - cos(x)

def test3(x):
    return x*sin(x)*cos(x)
    
def test4(x):
    return exp(x) * log(x)
    
if __name__ == '__main__':
    data = np.random.randn(1000)
    PDF(test1, data)
    PDF(test2, data)
    PDF(test3, data)
    PDF(test4, data)
    
