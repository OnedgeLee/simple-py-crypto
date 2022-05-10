from random import randrange

import pytest

# from pycrypto.libs.ec_utils import EllipticCurvePoint
from pycrypto.libs.ec_utils import gcd_extended
from pycrypto.libs.ec_utils import mod_con

# from pycrypto.libs.ec_utils import mod_inv
# from pycrypto.libs.ec_utils import Point


@pytest.fixture(params=range(100))
def make_mod_con():
    m = randrange(2, 100)
    a_mul = randrange(2, 100)
    b_mul = randrange(2, 100)
    r = randrange(min(m, a_mul, b_mul))
    return m, a_mul, b_mul, r


def test_mod_con(make_mod_con):
    m, a_mul, b_mul, r = make_mod_con
    assert mod_con(m * a_mul + r, m * b_mul + r, m)
    assert not mod_con(m * a_mul + r + 1, m * b_mul + r, m)


@pytest.fixture(params=range(100))
def make_gcd_extended():
    a = randrange(100)
    b = randrange(100)
    return a, b


def test_gcd_extended(make_gcd_extended):
    a, b = make_gcd_extended
    gcd, x, y = gcd_extended(a, b)
    assert gcd == a * x + b * y
