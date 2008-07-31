# -*- Mode: Python -*-  Not really, but close enough

#cimport definitions
from math import sqrt, sin, cos
from numpy import asmatrix, zeros
import numpy as N
# Numpy must be initialized
#definitions.import_array()

cdef class ThreeVector:
    cdef double _x
    cdef double _y
    cdef double _z
    cdef public _coordinates

    def __init__(self, *args):
        if len(args) == 1 and len(args[0]) == 3:
            # assume we're having an array here
            abc = args[0]
        elif len(args) == 3:
            # Three components are given explicitly
            abc = args
        else:
            raise TypeError, \
                'A ThreeVector must be initialized with a length-3 array or with three components'

        # coordinates are column vectors
        self._coordinates = N.matrix(abc, dtype=N.float64).T
        self._x = abc[0]
        self._y = abc[1]
        self._z = abc[2]


    def mag(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __getitem__(self, index):
        return self._coordinates[index] 

    def __setitem__(self, index, value):
        if index == 0:
            x = value
        elif index == 2:
            y = value
        elif index == 3:
            z = value
        else:
            raise IndexError, 'ThreeVector only has three entries'

    property x:
        def __get__(self):
            return self._x

        def __set__(self, val):
            self._x = val
            self._coordinates[0] = val

    
    property y:
        def __get__(self):
            return self._y

        def __set__(self, val):
            self._y = val
            self._coordinates[1] = val


    property z:
        def __get__(self):
            return self._z

        def __set__(self, val):
            self._z = val
            self._coordinates[2] = val


    def __len__(self):
        return 3

    def asarray(self):
        """ Returns the vector as array, so it can be used with the standard numpy methods
        """
        return self._coordinates.copy()

    def __add__(self, other):
        return self.__class__(self.x+other.x, self.y+other.y, self.z+other.z)

    def __iter__(self):
        """ Returns the iterator over the coordinates. This enables tuple unpacking, e.g. f(*self)
        """
        return self._coordinates.__iter__()



cdef class LorentzVector:
    cdef double _t
    cdef double _x
    cdef double _y
    cdef double _z
    cdef readonly _coordinates
    def __init__(self, *args):
        if len(args) == 1 and len(args[0]) == 4:
            # assume we're having an array here
            abcd = args[0]
        elif len(args) == 4:
            # Four components are given explicitly
            abcd = args
        else:
            raise TypeError, \
                'A LorentzVector must be initialized with a length-4 array or with four components'
        
        # coordinates are a column vector
        self._coordinates = N.matrix(abcd, dtype=N.float64).T
        self._t = abcd[0]
        self._x = abcd[1]
        self._y = abcd[2]
        self._z = abcd[3]


    def norm(self):
        return sqrt(self.t**2 - self.x**2 - self.y**2 - self.z**2)


    property t:
        def __get__(self):
            return self._t

        def __set__(self, val):
            self._t = val
            self._coordinates[0] = val

    property x:
        def __get__(self):
            return self._x

        def __set__(self, val):
            self._x = val
            self._coordinates[1] = val

    property y:
        def __get__(self):
            return self._y

        def __set__(self, val):
            self._y = val
            self._coordinates[2] = val

    property z:
        def __get__(self):
            return self._z

        def __set__(self, val):
            self._z = val
            self._coordinates[3] = val

    def v3(self):
        return ThreeVector(self._coordinates[1:])

    def __add__(self, other):
        return self.__class__(self.t+other.t, self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return self.__class__(self.t-other.t, self.x-other.x, self.y-other.y, self.z-other.z)        

    def __neg__(self):
        self._coordinates = -self._coordinates
        self._t = -self._t
        self._x = -self._x
        self._y = -self._y
        self._z = -self._z
        return self
        

    def __iter__(self):
        """ Returns the iterator over the coordinates. This enables tuple unpacking, e.g. f(*self)
        """
        return self._coordinates.__iter__()
        
    def __repr__(self):
        return "%r" % self._coordinates

    def __str__(self):
        return "%s" % self._coordinates



cdef makeRotationMatrix(double phi, double theta, double psi):
    # Construct a rotation matrix.
    # Returns a 4x4 matrix which rotates the space dimensions in the Euler
    # angles 'phi', 'theta', and 'psi'.

    cdef double cosps
    cdef double cosph
    cdef double sinth
    cdef double costh
    cdef double sinps
    cdef double sinph
    sinph = sin(phi)
    cosph = cos(phi)
    sinth = sin(theta)
    costh = cos(theta)
    sinps = sin(psi)
    cosps = cos(psi)
    mat = asmatrix(zeros((4, 4), dtype=N.float64))
    mat[0, 0] = 1.0
    mat[1, 1] =   cosph * costh * cosps - sinph * sinps
    mat[1, 2] = - cosph * costh * sinps - sinph * cosps
    mat[1, 3] =   cosph * sinth
    mat[2, 1] =   sinph * costh * cosps + cosph * sinps
    mat[2, 2] = - sinph * costh * sinps + cosph * cosps
    mat[2, 3] =   sinph * sinth
    mat[3, 1] = -         sinth * cosps
    mat[3, 2] =           sinth * sinps
    mat[3, 3] =           costh
    return mat


def makeBoostMatrix(double beta_x, double beta_y, double beta_z):
    # Construct a boost matrix.
    # Returns a 4x4 matrix for the boost for a vector beta whose
    # components are 'beta_x', 'beta_y', and 'beta_z'.

    cdef double beta2
    cdef double gamma
    cdef double element
    matrix = asmatrix(zeros((4, 4), dtype=N.float64))

    # Handle the zero-boost case.
    if beta_x == 0 and beta_y == 0 and beta_z == 0:
        matrix[0, 0] = 1
        matrix[1, 1] = 1
        matrix[2, 2] = 1
        matrix[3, 3] = 1
        return matrix

    # Compute beta-squared.
    betas = [beta_x, beta_y, beta_z]
    beta2 = beta_x**2 + beta_y**2 + beta_z**2
    if beta2 > 1:
        raise ValueError, \
            "beta may not have magnitude greater than one, but is %s" % str(betas)
    # Compute gamma.
    gamma = 1.0 / sqrt(1.0 - beta2)
    # Construct the boost matrix.
    matrix[0, 0] = gamma
    for i from 1 <= i <= 3:
        element = -gamma * betas[i - 1]
        matrix[i, 0] = element
        matrix[0, i] = element
    for i from 1 <= i <= 3:
        for j from i <= j <= 3:
            element = (gamma - 1) * betas[i - 1] * betas[j - 1] / beta2
            if i == j:
                element = element + 1
            matrix[i, j] = element
            matrix[j, i] = element
    return matrix



cdef class Frame:
    """A reference frame."""
    cdef readonly __inverse_matrix
    cdef readonly __matrix
    cdef public __name

    def __init__(self, transformation, name=None):
        # Construct a new reference frame.
        #
        #   'transformation' -- The Lorentz transformation from the lab
        #    frame to the new frame.
        #
        #    'name' -- An optional name for this frame.

        # Boosting the coordinate system is contravariant.
        self.__inverse_matrix = transformation
        self.__matrix = self.__inverse_matrix.I
        self.__name = name


    def __repr__(self):
        if self.__name is None:
            name = "at 0x%x" % id(self)
        else:
            name = "" + repr(self.__name)
        return "<Frame %s>" % name


    def __str__(self):
        if self.__name is None:
            return "frame at 0x%x" % id(self)
        else:
            return "frame '%s'" % str(self.__name)


    def coordinatesOf(self, vector):
        """ Return the four coordinates of 'vector' in this frame.
        """
        x = self.__matrix * vector._coordinates
        vec = LorentzVector(x.A1)
        # neat little hack to ensure we return the same type that was passed in
        vec.__class__ == vector.__class__
        return vec


    def boostTo(self, vector):
        return self.coordinatesOf(vector)


    def makeLorentzVector(self, *args, **kwargs):
        """ creates a four vector with the desired coordinates in this frame
        """

        cls = kwargs.get('cls', LorentzVector)
        if len(args) == 1 and len(args[0]) == 4:
            vec = N.array(args[0])
        elif len(args) == 4:
            vec = N.array(args)
        else:
            raise AttributeError, \
                'arguments %s have the wrong shape for %s' % (args, cls.__name__)
        data = self.__inverse_matrix * vec
        # return an array, not a matrix
        return cls(data.A[0])



    def makeTransformation(self, matrix):
        """ Construct a Lorentz transformation.

            returns -- The transformation whose matrix representation in
            this frame is 'matrix'.
        """

        return self.__inverse_matrix * matrix * self.__matrix


    def makeBoost(self, beta_x, beta_y, beta_z):
        """ Construct a Lorentz boost.

            returns -- The transformation consisting of boosting by
            '(beta_x, beta_y, beta_z)' in this frame.
        """

        return self.makeTransformation(makeBoostMatrix(beta_x, beta_y, beta_z))


    def makeRotation(self, phi, theta, psi):
        """ Construct a rotation.

            returns -- The transformation consisting of rotating by the
            Euler angles '(phi, theta, psi)' in this frame.
        """

        return self.makeTransformation(makeRotationMatrix(phi, theta, psi))


cdef class Momentum(LorentzVector):
    """A momentum four-vector."""


    property mass:
        """The invariant mass"""
        def __get__(self):
            return self.norm()


    cdef Frame __get_restFrame(self):
        cdef double en, px, py, pz
        en, px, py, pz = self._coordinates
        return Frame(makeBoostMatrix(-px/en, -py/en, -pz/en))


    property restFrame:
        """The rest frame of a particle with this momentum"""
        def __get__(self):
            return self.__get_restFrame()
    
    property e:
        def __get__(self):
            return self._t

        def __set__(self, val):
            self._t = val
            self._coordinates[0] = val

    property px:
        def __get__(self):
            return self._x

        def __set__(self, val):
            self._x = val
            self._coordinates[1] = val

    property py:
        def __get__(self):
            return self._y

        def __set__(self, val):
            self._y = val
            self._coordinates[2] = val

    property pz:
        def __get__(self):
            return self._z

        def __set__(self, val):
            self._z = val
            self._coordinates[3] = val
            
    
