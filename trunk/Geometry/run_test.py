#!/usr/bin/env python
from hep.vec import ThreeVector as oldVec
from geometry import ThreeVector, LorentzVector
from geometry import makeBoostMatrix, makeRotationMatrix
from lorentz import makeBoostMatrix as oldBoostMatrix
from lorentz import makeRotationMatrix as oldRotationMatrix
import time
import random
import numpy as N

start = time.time()
for x in xrange(10000):
    a = random.random()
    b = random.random()
    c = random.random()
    vec = ThreeVector(a, b, c)
    vec2 = ThreeVector([a, b, c])

    if not a == vec.x == vec2.x or not b == vec.y == vec2.y or not c == vec.z == vec2.z:
        print 'hey'
    if vec.mag() != vec2.mag():
        print 'ERROR Not Equal'
        print vec, vec2
        print a, b, c
        print vec.x, vec.y, vec.z
        print vec2.x, vec2.y, vec2.z
        break
    if vec <= 0:
        print 'ERROR < 0'
        break
else:
    print time.time() - start
start = time.time()

for x in xrange(10000):
    a = random.random()
    b = random.random()
    c = random.random()
    vec = oldVec(a, b, c).norm
    vec2 = oldVec(a, b, c).norm
    if vec != vec2:
        print 'ERROR Not Equal'
        print vec, vec2
        print a, b, c
        print vec.x, vec.y, vec.z
        print vec2.x, vec2.y, vec2.z
        break
    if vec <= 0:
        print 'ERROR < 0'
        break

else:
    print time.time() - start

start = time.time()

for x in xrange(10000):
    a = random.random()/3
    b = random.random()/3
    c = random.random()/3
    makeBoostMatrix(a, b, c)
print time.time() - start

for x in xrange(10000):
    a = random.random()/3
    b = random.random()/3
    c = random.random()/3
    makeRotationMatrix(a, b, c)
print time.time() - start


for x in xrange(10000):
    a = random.random()/3
    b = random.random()/3
    c = random.random()/3
    oldBoostMatrix(a, b, c)
print time.time() - start

for x in xrange(10000):
    a = random.random()/3
    b = random.random()/3
    c = random.random()/3
    oldRotationMatrix(a, b, c)
print time.time() - start
