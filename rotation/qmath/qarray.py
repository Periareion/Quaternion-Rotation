
from .quaternion import *

class QArray:

    def __init__(self, quaternions=[]):
        if isinstance(quaternions, (list, tuple)):
            array = list(quaternions)
        elif isinstance(quaternions, QArray):
            array = QArray.array
        else:
            array = []
        
        self.array = array

    def __len__(self):
        return len(self.array)

    def __getitem__(self, index):
        return self.array[index]

    def __add__(self, other):
        return QArray([q+other for q in self.array])

    def __mul__(self, other):
        return QArray([q*other for q in self.array])

    def __rmul__(self, other):
        return QArray([other*q for q in self.array])

    def rotate(self, vector, angle):
        for q in self.array:
            q.rotate(vector, angle)

    @property
    def string(self):
        s = f"Quaternion array of length {len(self)}"
        for q in self.array:
            s += '\n    '+str(tuple((' '*(p >= 0)+f"{p}" for p in q.components))).replace('\'', '')
        return s

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

UNIT_QUATERNIONS = QArray([Q(i=1), Q(j=1), Q(k=1)])

##a = QArray([Q(i=1),Q(k=1)])
##
##import time
##from math import cos, sin, pi
##
##a = QArray([Quaternion(i=1), Q(j=1), Q(k=1)])
##for n in range(360):
##    a.rotate((i+j+k), pi/180)
##    print(a)
