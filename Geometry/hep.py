#-----------------------------------------------------------------------
#
# module hep.lorentz
#
# Copyright 2003 by Alex Samuel.  All rights reserved.
#
#-----------------------------------------------------------------------

"""Lorentz vectors and transformations."""

#-----------------------------------------------------------------------
# imports
#-----------------------------------------------------------------------
from __future__ import division
from math import sqrt, sin, cos, pi, atan2, hypot
from geometry import ThreeVector, LorentzVector, Frame, Momentum
from numpy import eye, zeros, array, asmatrix
import numpy as N

#-----------------------------------------------------------------------
# classes
#-----------------------------------------------------------------------



class LabFrame(Frame):
    """The canonical lab frame.
    This is the frame relative to which all other frames are specified.
    Always use the 'lab' singleton instance of this class."""

    # this makes a singleton
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = Frame.__new__(cls)
        return cls._the_instance
    # The coordinates of four-vectors and the matrix elements of
    # transformations are specified in this frame.  Redefine methods to
    # use these directly.

    def __init__(self):
        Frame.__init__(self, asmatrix(eye(4)))

    def __repr__(self):
        return "<LabFrame>"

    def __str__(self):
        return "lab frame"

    def coordinatesOf(self, vector):
        return self.makeLorentzVector(vector._coordinates)

    def getMomentum(self, *args):
        if len(args) == 2:
            vec = [args[0]]
            vec.extend(args[1]._coordinates)
            return self.makeLorentzVector(vec, cls=Momentum)


"""The lab frame."""
lab = LabFrame()

#-----------------------------------------------------------------------
# functions
#-----------------------------------------------------------------------
def angles(vector):
    """Return the polar and azimuthal angles relative to the z axis."""

    x, y, z = vector
    return atan2(hypot(x, y), z), atan2(y, x)


def cosAngle(vector1, vector2=ThreeVector(0, 0, 1)):
    """Return the cosine of the opening angle between two vectors.

    If only one vector is given, returns the cosine of the angle between
    it and the positive z axis."""

    return (N.dot(vector1._coordinates,  vector2._coordinates)) / (vector1.mag() * vector2.mag())


def openingAngle(vector1, vector2=ThreeVector(0, 0, 1)):
    """Return the opening angle between two vectors.

    If only one vector is given, returns the angle between it and the
    positive z axis."""

    return acos(cosAngle(vector1, vector2))


def twoBodyDecayMomentum(mass_a, mass_b, mass_c):
    """Return the decay momentum for a two-body decay.

    'mass_a' -- The mass of the decaying particle.

    'mass_b', 'mass_c' -- The masses of the decay products.

    returns -- The magnitude of the momentum of each the decay products in
    the rest frame of the decaying particle."""

    if mass_a < mass_b + mass_c:
        raise ValueError, \
              "parent's mass cannot be less than sum of children's"
    return sqrt(  (mass_a - mass_b - mass_c)
                * (mass_a + mass_b - mass_c)
                * (mass_a - mass_b + mass_c)
                * (mass_a + mass_b + mass_c)) / (2 * mass_a)


def azimuth(p4, frame=lab):
    """Returns the 3D azimuthal angle 'arctan(hypot(x, y) / z)'."""

    t, x, y, z = frame.coordinatesOf(p4)
    return atan2(sqrt(x * x + y * y), z)


def cos_azimuth(p4, frame=lab):
    """Returns the cosine of 'azimuth'."""

    t, x, y, z = frame.coordinatesOf(p4)
    return z / sqrt(x * x + y * y + z * z)


#-----------------------------------------------------------------------
# test stuff
#-----------------------------------------------------------------------

if __name__ == "__main__":
    from   random import random

    mass_Ups = 10.575
    mass_B0 = 5.2794

    cm_frame = Frame(lab.Boost(0, 0, 0.56), name="CM")
    p4_Ups = cm_frame.Momentum(mass_Ups, 0, 0, 0)

    decay_angles = random() * 2 * pi, random() * pi, random() * 2 * pi
    decay_rotation = cm_frame.Rotation(*decay_angles)

    momentum_B0 = twoBodyDecayMomentum(mass_Ups, mass_B0, mass_B0)
    energy_B0 = hypot(momentum_B0, mass_B0)
    p4_B0 = decay_rotation \
            ^ cm_frame.Momentum(energy_B0, 0, 0, momentum_B0)
    p4_B0bar = decay_rotation \
               ^ cm_frame.Momentum(energy_B0, 0, 0, -momentum_B0)

    print "B0 and B0bar coordinates in %s:" % lab
    print "(%.4f, %.4f, %.4f, %.4f)" % tuple(lab.coordinatesOf(p4_B0))
    print "(%.4f, %.4f, %.4f, %.4f)" % tuple(lab.coordinatesOf(p4_B0bar))
    print "B0 and B0bar coordinates in %s:" % cm_frame
    print "(%.4f, %.4f, %.4f, %.4f)" % tuple(cm_frame.coordinatesOf(p4_B0))
    print "(%.4f, %.4f, %.4f, %.4f)" % tuple(cm_frame.coordinatesOf(p4_B0bar))
    print "Reconstructed Upsilon(4S) mass =", (p4_B0 + p4_B0bar).mass

