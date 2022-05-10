from pycrypto import ECDSA


def test_ecdsa_keygen_private():
    ecdsa = ECDSA()
    priv_keys = [ecdsa.keygen_private() for _ in range(10)]
    assert len(set(priv_keys)) == len(priv_keys)
    assert all((1 <= int(priv_key, 16) <= ecdsa.ec_type.p - 1 for priv_key in priv_keys))
