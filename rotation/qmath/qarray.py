
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
        for i, q in enumerate(self.array):
            self.array[i].rotate(vector, angle)
        return self


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

    def copy(self):
        return QArray([q.copy() for q in self.array])

UNIT_QUATERNIONS = QArray([Q(i=1), Q(j=1), Q(k=1)])