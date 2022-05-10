"""Utility methods for modular operation and elliptic curve
"""

from __future__ import annotations

from functools import reduce

from pycrypto.libs.ec_types import EllipticCurveType


def mod_con(a: int, b: int, m: int) -> bool:
    """Check if a and b are congruent modulo n

    Args:
        a (int): Variable to be check congruency
        b (int): Variable to be check congruency
        m (int): Modulus

    Returns:
        bool: If a and b are congruent modulo n
    """
    return (a - b) % m == 0


def gcd_extended(a: int, b: int) -> tuple:
    """Extended Euclidean algorithm
    From Euclidean algorithm:
    gcd(a, 0) = a
    a = bq + r (0 <= r < b) = gcd(b, r) = gcd(a, b)
    r = a - bq = a%b

    From Bezout's identity:
    gcd(a, b) = ax + by (x and y are integer)
    gcd(b, r) = bx' + ry' (x' and y' are integer)
    bx' + ry' = bx' + (a - bq)y'
    bx' + (a - bq)y' = gcd(b, r) = gcd(a, b)
    ay' + b(x' - qy') = gcd(b, r) = gcd(a, b)
    if b == 0 : gcd(a, b) = ax + by = a, so x = 1, b = 0

    Args:
        a (int): Dividend to apply extended Euclidean algorithm
        b (int): Dividend to apply extended Euclidean algorithm

    Returns:
        tuple: tuple containing:

            gcd (int): GCD of a and b
            x (int): x from ax + by = gcd(a, b)
            y (int): y from ax + by = gcd(a, b)
    """
    if b == 0:
        return a, 1, 0
    gcd, x_t, y_t = gcd_extended(b, a % b)
    return gcd, y_t, x_t - ((a // b) * y_t)


def mod_inv(a: int, m: int) -> int:
    """Modular inverse
    ax = my' + 1 (x is modular inverse of a(mod m))
    ax - my' = 1
    We can apply extended Euclidean algorithm, if a and m are coprime
    ax + my = gcd(a, m)

    Args:
        a (int): Integer to find modular inverse
        m (int): Modulus

    Returns:
        int: Modular inverse of a modulo m
    """
    gcd, x, _ = gcd_extended(a, m)
    if gcd != 1:
        raise ValueError("parameter a and m are not coprime")
    return (x + m) % m


class Point:
    """Point of integer coordinates
    Parent class of EllipticCurvePoint
    """

    def __init__(self, x: int, y: int) -> None:
        """Constructor method

        Args:
            x (int): X coordinate of point
            y (int): Y coordinate of point
        """
        self.x = x
        self.y = y

    @property
    def coord(self):
        """Get coordinate tuple (x, y)

        Returns:
            tuple: tuple containing:

                x (int): X coordinate of point
                y (int): Y coordinate of point
        """
        return self.x, self.y


class EllipticCurvePoint(Point):
    """Point on elliptic curve with finite field modulus y^2 % p = (x^3 + ax + b) % p
    Inherits Point class
    Handles elliptic curve point addition and multiplication
    """

    def __init__(self, x: int, y: int, ec_type: EllipticCurveType) -> None:
        """Constructor method

        Args:
            x (int): X coordinate of point
            y (int): Y coordinate of point
            ec_type (EllipticCurveType): Elliptic curve type

        Raises:
            TypeError: If Elliptic curve type is not the instance of 'EllipticCurveType', raises TypeError
        """
        super().__init__(x, y)
        if not isinstance(ec_type, EllipticCurveType):
            raise TypeError("ec_type have to be instance of 'EllipticCurveType'")
        self.ec_type = ec_type

    def __add__(self, point: EllipticCurvePoint) -> EllipticCurvePoint:
        """Elliptic curve point addition

        Args:
            point (EllipticCurvePoint): Elliptic curve point to be added

        Raises:
            TypeError: If elliptic curve type of point to be added is different from current point instance,
            raises TypeError

        Returns:
            EllipticCurvePoint: Result of elliptic curve point addition
        """
        if not isinstance(point.ec_type, type(self.ec_type)):
            raise TypeError("Type of point is not same with current instance")
        if self.coord == point.coord:
            s = (3 * (self.x**2) + self.ec_type.a) / (2 * self.y)
        else:
            s = (point.y - self.y) / (point.x - self.x)

        x = s**2 - self.x - point.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.ec_type)

    @staticmethod
    def double_and_add(point: EllipticCurvePoint, n: int) -> EllipticCurvePoint:
        """Double and add algorithm for elliptic curve point multiplication

        Args:
            point (EllipticCurvePoint): Elliptic curve point to be multiplied
            n (int): Multiplier

        Returns:
            EllipticCurvePoint: Result of elliptic curve point multiplication
        """
        # TODO: Current code suffers from overflow error or exceed of maximum call stack, have to be reimplemented
        if n == 0:
            return 0
        elif n == 1:
            return point
        elif n % 2 == 1:
            return point + EllipticCurvePoint.double_and_add(point, n - 1)
        else:
            return EllipticCurvePoint.double_and_add(point + point, n / 2)

    def __mul__(self, n: int) -> EllipticCurvePoint:
        """Elliptic curve point multiplication

        Args:
            n (int): Multiplier

        Returns:
            EllipticCurvePoint: Result of elliptic curve point multiplication
        """
        # TODO: Replace multiplication with valid and fast algorithm
        return reduce(lambda x, y: x + y, [self for _ in range(n)])
        # return self.double_and_add(self, n)

    __rmul__ = __mul__
