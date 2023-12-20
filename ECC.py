# -*- coding: utf-8 -*-
# AUTHOR: Soreat_u (2019-10-30)

'''
Elliptic Curves Cryptography.
'''

from Arithmetic import ModInverse as inverse, ModSquareRoot as mod_sqrt

from Utility import int2bits

class Point(object):
    '''
    Integer point on the xy plane.
    '''
    def __init__(self, x=float('inf'), y=float('inf')):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        if not isinstance(new_x, int):
            raise ValueError("x must be an integer!")
        self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        if not isinstance(new_y, int):
            raise ValueError("x must be an integer!")
        self._y = new_y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Point ({self.x}, {self.y})'


class ECC(object):
    '''
    Elliptic curve over the finite field.
    '''
    def __init__(self, A, B, p):
        self._A = A
        self._B = B
        self._p = p
        # The extra point that lives "at infinity".
        self._O = Point(float('inf'), float('inf'))
        # check
        if 4 * A**3 + 27 * B**2 == 0:
            raise ValueError("Elliptic curves with 4A^3 + 27B^2 == 0 are not allowed.")

    def add(self, P: 'Point object', Q: 'Point object', verbose=True):
        '''
        Addition over the elliptic curve.

        Ref: Theorem 6.6 (Elliptic Curve Addition Algorithm)\
            in book `An Introduction to Mathematical Cryptography`.
        '''
        if verbose:
            print(f'Computing {P} + {Q}:')

        if P == self._O:
            return Point(Q.x, Q.y)
        elif Q == self._O:
            return Point(P.x, P.y)

        x1, x2 = P.x, Q.x
        y1, y2 = P.y, Q.y
        if x1 == x2 and (y1 + y2) % self._p == 0:
            return Point(float('inf'), float('inf'))
        # slope
        if P != Q:
            k = (y2-y1) * inverse(x2-x1, self._p, verbose) % self._p
            if verbose:
                print(f'lambda = ({y2}-{y1})/({x2}-{x1}) mod {self._p} = {k}')
        else:
            k = (3 * x1**2 + self._A) * inverse(2*y1, self._p, verbose) % self._p
            if verbose:
                print(f'lambda = (3*{x1}^2 + {self._A}) / (2*{y1}) mod {self._p} = {k}')
        
        # coordinate
        
        x3 = (k**2 - x1 - x2) % self._p
        print(f'x3 = ({k}**2 - {x1} - {x2}) mod {self._p} = {x3}')

        y3 = (k*(x1-x3) - y1) % self._p
        print(f'y3 = ({k}*({x1}-{x3}) - {y1}) mod {self._p} = {y3}')

        print(f'The result of {P} + {Q} is: ({x3}, {y3})')

        return Point(x3, y3)

    # This mul is nice, but I need to print 2^i * P. So I don't use it.
    # def mul(self, P: 'Point object', n: int):
    #     '''
    #     Multiplication over the elliptic curve.

    #     Ref: Table 6.3: The double-and-add algorithm for elliptic curves in
    #          the book "An Introduction to Mathematical Cryptography".
    #     Note: More efficient way to do this: the ternary expansion of n method
    #           which can compute nP in about 4/3k + 1 steps.
    #     '''
    #     Q = Point(P.x, P.y)
    #     R = Point(float('inf'), float('inf'))
    #     while n:
    #         if n & 1:
    #             R = self.add(R, Q)
    #         Q = self.add(Q, Q)
    #         n >>= 1
    #     return R


    # FIXME: Debug
    def mul(self, P: 'Point object', n: int, verbose=True):
    #     '''
    #     Multiplication over the elliptic curve.

    #     Ref: Table 6.3: The double-and-add algorithm for elliptic curves in
    #          the book "An Introduction to Mathematical Cryptography".
    #     Note: More efficient way to do this: the ternary expansion of n method
    #           which can compute nP in about 4/3k + 1 steps.
    #     '''
        if verbose:
            print(f'Computing {n}*{P}:')
        Q = Point(P.x, P.y)
        R = Point(float('inf'), float('inf'))
        
        power_of_2_Ps = [Q] # list of P, 2P, 4P ...
        bits = int2bits(n)
        for i in range(1, len(bits)):
            Q = self.add(Q, Q)
            power_of_2_Ps.append(Q)
        
        print(f'power_of_2_Ps are: {power_of_2_Ps}')

        for i in range(len(bits)):
            if bits[i] == 1:
                R = self.add(R, power_of_2_Ps[i])

        print(f'The result of {n}*{P} is {R}')
        return R


    def solve_y(self, x):
        '''
        Solve y such that y^2 == x^3 + Ax + B over Fp.
        '''
        y = mod_sqrt(x**3 + self._A*x + self._B, self._p)
        return y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Elliptic Curve defined by y^2 = x^3 {self._A:+d}x {self._B:+d}\
                over Finite Field of size {self._p}"


def test():
    # secp256k1
    # p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    # gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    # gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    # ecc = ECC(0, 7, p)
    # G = Point(gx, gy)

    # h = ecc.mul(G, gy)
    # print(h)

    p = 31
    ecc = ECC(1, 18, p)
    P = Point(10, 6)
    O = ecc.mul(P, 15)
    print(O)

if __name__ == '__main__':
    test()