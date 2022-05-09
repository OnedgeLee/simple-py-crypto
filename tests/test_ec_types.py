from pycrypto.libs.ec_types import secp256k1


def test_secp256k1_valid():
    assert secp256k1.valid
