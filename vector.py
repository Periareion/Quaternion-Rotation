
import math

class Vector:

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            elements = list(args[0])
        else:
            elements = list(args)

        self.elements = elements

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return repr(self.elements)

    def __repr__(self):
        return repr(self.elements)

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return Vector([x + other for x in self.elements])
        if isinstance(other, (Vector, iter)):
            if len(self) == len(other):
                return Vector([x1 + x2 for x1, x2 in zip(self.elements, other.elements)])
            else:
                raise IndexError
        else:
            return NotImplemented

    __radd__ = __add__

    def __neg__(self):
        return Vector([-x for x in self.elements])

    def __sub__(self, other):
        if isinstance(other, (Vector, iter, float, int)):
            return self+(-other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (Vector, iter, float, int)):
            return other+(-self)
        else:
            return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (float, int)):
            return Vector([x * scalar for x in self.elements])
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        if isinstance(scalar, (float, int)):
            return Vector([x / scalar for x in self.elements])
        else:
            return NotImplemented

    def __rtruediv__(self, scalar):
        return NotImplemented

    def __getitem__(self, index):
        return self.elements[index]

    def repeat(self, n):
        if isinstance(n, int):
            return Vector(self.elements*n)
        else:
            return NotImplemented

    def product(self, start=0, end=None):
        if False not in [isinstance(x, (float, int)) for x in self.elements]:
            return math.prod(self.elements[start:end])
        else:
            return NotImplemented

    def sum(self, start=0, end=None):
        if False not in [isinstance(x, (float, int)) for x in self.elements]:
            return sum(self.elements[start:end])
        else:
            return NotImplemented

    @property
    def norm(self):
        return math.sqrt(sum([x**2 for x in self.elements]))

    @property
    def normalized(self):
        return self/self.norm

    def normalize(self):
        self.elements = self.normalized.elements
        
Vec = Vector
