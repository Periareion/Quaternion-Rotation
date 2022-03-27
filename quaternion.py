
import math
from math import cos, sin, pi, e

class Quaternion:
    
    def __init__(self, real=0, i=0, j=0, k=0):
        
        # Support for making sure it is a quaternion (Q(q) = q if q already is a Quaternion)
        if isinstance(real, Quaternion):
            real, i, j, k = real.components

        self.real = real
        self.i = i
        self.j = j
        self.k = k

    # Returns a tuple of the quaternion's real and imaginary parts
    @property
    def components(self):
        return (self.real, self.i, self.j, self.k)

    def update(self, other):
        self.real, self.i, self.j, self.k = other.components

    # Only returns imaginary parts
    @property
    def imaginary(self):
        return Q(0, self.i, self.j, self.k)

    @property
    def squareSum(self):
        return sum(x**2 for x in self.components)

    # Returns the norm, or the Euclidian distance to the origin
    @property
    def norm(self):
        return math.sqrt(self.squareSum)

    magnitude = norm

    # Returns normalized quaternion (whose norm = 1)
    @property
    def normalized(self):
        return self/self.norm

    versor = normalized

    # Normalizes the quaternion
    def normalize(self):
        self.update(self.normalized)

    # Support for abs(q), defined to be the same as norm
    def __abs__(self):
        return self.norm

    # Returns the conjugate (changes sign of imaginary parts)
    @property
    def conjugate(self):
        return Q(self.real, -self.i, -self.j, -self.k)

    # Similar to the conjugate (inverse = conjugate when norm = 1)
    @property
    def inverse(self):
        #norm = self.norm
        return self.conjugate/self.squareSum #(norm*norm)

    reciprocal = inverse

    # Rounds each part to n decimals
    def __round__(self, n):
        if isinstance(n, int):
            return Q(round(self.real, n), round(self.i, n), round(self.j, n), round(self.k, n))
        else:
            return NotImplemented

    rnd = __round__

    # Returns imaginary parts
    def vector(self, quaternion=False, normalized=False):
        imag = self.imaginary
        if normalized:
            imag.normalize()
        if quaternion:
            return imag
        else:
            return imag.components[1:4]
    
    # Adds two quaternions
    def __add__(self, other):
        if isinstance(other, (float, int)):
            other = Q(other)
        if isinstance(other, Quaternion):
            return Q(self.real+other.real, self.i+other.i, self.j+other.j, self.k+other.k)
        else:
            return NotImplemented

    __radd__ = __add__

    # Returns negative, useful for subtraction
    def __neg__(self):
        return Q(-self.real, -self.i, -self.j, -self.k)

    # Subtracts by adding the negative
    def __sub__(self, other):
        if isinstance(other, (float, int)):
            other = Q(other)
        if isinstance(other, Quaternion):
            return self+(-other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (float, int)):
            other = Q(other)
        if isinstance(other, Quaternion):
            return other+(-self)
        else:
            return NotImplemented

    # Multiplies two quaternions using the Hamilton product
    def __mul__(self, other):
        if isinstance(other, (float, int)):
            other = Q(other)
        if isinstance(other, Quaternion):
            return Q(
                self.real*other.real - self.i*other.i - self.j*other.j - self.k*other.k,
                self.real*other.i + self.i*other.real + self.j*other.k - self.k*other.j,
                self.real*other.j - self.i*other.k + self.j*other.real + self.k*other.i,
                self.real*other.k + self.i*other.j - self.j*other.i + self.k*other.real,
            )
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            other = Q(other)
        if isinstance(other, Quaternion):
            return other*self
        else:
            return NotImplemented

    # Divides using some fancy inverse-multiplication tricks
    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Q(self.real/other, self.i/other, self.j/other, self.k/other)
        elif isinstance(other, Quaternion):
            return self*other.inverse
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (float, int)):
            other = Q(other)/self
        if isinstance(other, Quaternion):
            return other/self
        else:
            return NotImplemented

    def sandwich(self, q):
        if isinstance(q, (float, int)):
            q = Q(q)
        if isinstance(q, Quaternion):
            return q*self*q.inverse
        else:
            return NotImplemented

    def rotate(self, vector, angle):
        norm = self.norm
        q = math.cos(angle/2) + vector.vector(True, True)*math.sin(angle/2)
        rotated = self.sandwich(q).normalized*norm
        self.update(rotated)
        return rotated

    def axis_transform(self, i_prime, j_prime, k_prime):
        q_prime_i = self.i*i_prime.i + self.j*j_prime.i + self.k*k_prime.i
        q_prime_j = self.i*i_prime.j + self.j*j_prime.j + self.k*k_prime.j
        q_prime_k = self.i*i_prime.k + self.j*j_prime.k + self.k*k_prime.k

        return Q(0, i=q_prime_i, j=q_prime_j, k=q_prime_k)

    def set_norm(self, new_norm):
        if isinstance(new_norm (float, int)):
            self.update(self.normalized*new_norm)
        else:
            return NotImplemented

    # Returns e^q
    def exp(self):
        a = self.real
        v = self.imaginary
        norm = v.norm
        return e**a*(cos(norm)+self.unitVector*sin(norm))

    def __pow__(self, exponent):
        if False and (isinstance(exponent, int) or (isinstance(exponent, float) and exponent == int(exponent))):
            norm = self.norm
            self.normalize()
            exponent = exponent
            product = Q(1)
            for _ in range(int(exponent) % 4):
                product *= self
            product.normalize()
            product *= norm**exponent
            return product
        elif isinstance(exponent, (float, int)):
            print("Running test formula")
            norm = self.norm
            theta = math.acos(self.normalized.real)
            return norm**exponent * (cos(exponent*theta) + self.vector * sin(exponent*theta))
        else:
            return NotImplemented

    @property
    def string(self):
        signs = (('-','+')[self.i >= 0],
                 ('-','+')[self.j >= 0],
                 ('-','+')[self.k >= 0])

        #return str(self.components)
        return f"{self.real} {signs[0]} {abs(self.i)}i {signs[1]} {abs(self.j)}j {signs[2]} {abs(self.k)}k"

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string #f'Q({self.real}, {self.i}, {self.j}, {self.k})'

Q = Quaternion

# Don't change these... don't rotate em, don't redefine em, don't you do no nothin'... it will break math.
origin = Q(0,0,0,0)
i = Q(0,1,0,0)
j = Q(0,0,1,0)
k = Q(0,0,0,1)

#print(i,j,k)
#print(Q(i=1).rotate((i+j+k), 2/3*pi),Q(j=1).rotate((i+j+k), 2/3*pi),Q(k=1).rotate((i+j+k), 2/3*pi))
