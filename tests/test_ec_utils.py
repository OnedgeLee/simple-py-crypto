from random import randrange

import pytest

from pycrypto.libs.ec_types import secp256k1
from pycrypto.libs.ec_utils import EllipticCurvePoint
from pycrypto.libs.ec_utils import gcd_extended
from pycrypto.libs.ec_utils import mod_con
from pycrypto.libs.ec_utils import mod_inv
from pycrypto.libs.ec_utils import Point


@pytest.fixture(params=range(100))
def case_mod_con():
    m = randrange(2, 100)
    a_mul = randrange(2, 100)
    b_mul = randrange(2, 100)
    r = randrange(min(m, a_mul, b_mul))
    return m, a_mul, b_mul, r


def test_mod_con(case_mod_con):
    m, a_mul, b_mul, r = case_mod_con
    assert mod_con(m * a_mul + r, m * b_mul + r, m)
    assert not mod_con(m * a_mul + r + 1, m * b_mul + r, m)


@pytest.fixture(params=range(100))
def case_gcd_extended():
    a = randrange(100)
    b = randrange(100)
    return a, b


def test_gcd_extended(case_gcd_extended):

    def euclidean_algorithm(m, n):
        if m < n:
            m, n = n, m
        if n == 0:
            return m
        if m % n == 0:
            return n
        return euclidean_algorithm(n, m % n)

    a, b = case_gcd_extended
    gcd, x, y = gcd_extended(a, b)
    assert gcd == a * x + b * y
    assert gcd == euclidean_algorithm(a, b)


def coprimes():
    n = 100
    coprime_list = []
    (a, b, c, d) = (0, 1, 1, n)
    while c <= n:
        k = (n + b) // d
        (a, b, c, d) = (c, d, k * c - a, k * d - b)
        if (a * b != 0) and a != 1 and b != 1:
            coprime_list.append([a, b])
    return coprime_list


@pytest.fixture(params=coprimes())
def case_mod_inv(request):
    a = request.param[0]
    m = request.param[1]
    return a, m


def test_mod_inv(case_mod_inv):
    a, m = case_mod_inv
    assert (a * mod_inv(a, m)) % m == 1


@pytest.mark.parametrize("x, y", [(1, 3), (4, 2), (3, 7)])
def test_point(x, y):
    point = Point(x, y)
    assert point.coord == (point.x, point.y)


def test_elliptic_curve_point():
    ec_point = EllipticCurvePoint(secp256k1.gx, secp256k1.gy, secp256k1)
    slope = (3 * (ec_point.x**2) + ec_point.ec_type.a) / (2 * ec_point.y)
    x = slope**2 - ec_point.x * 2
    y = slope * (ec_point.x - x) - ec_point.y
    assert x, y == (ec_point + ec_point).coord
    assert (ec_point + ec_point + ec_point).coord == (ec_point * 3).coord
