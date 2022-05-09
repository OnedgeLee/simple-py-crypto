"""Implementation of ECDSA algorithm
"""

from secrets import randbelow

from pycrypto.libs.ec_types import Secp256k1
from pycrypto.libs.ec_types import secp256k1
from pycrypto.libs.ec_utils import EllipticCurvePoint


class ECDSA:
    """ECDSA algorithm"""

    def __init__(self) -> None:
        self.__ec_type: Secp256k1 = secp256k1
        self.__gen_point: EllipticCurvePoint = EllipticCurvePoint(self.__ec_type.gx, self.__ec_type.gy, self.__ec_type)

    @property
    def ec_type(self) -> Secp256k1:
        """Get elliptic curve type, always secp256k1

        Returns:
            Secp256k1: Elliptic curve type of secp256k1
        """
        return self.__ec_type

    @property
    def gen_point(self) -> EllipticCurvePoint:
        """Get generation point

        Returns:
            EllipticCurvePoint: Generation point
        """
        return self.__gen_point

    def keygen_private(self) -> str:
        """Private key generation

        Returns:
            str: Private key hex string
        """
        return hex(randbelow(self.ec_type.p - 1) + 1)

    def keygen_public(self, private_key: str) -> str:
        """Public key generation with given private key

        Args:
            private_key (str): Private key hex string

        Returns:
            str: Public key hex string
        """
        return hex((self.gen_point * int(private_key, 16)).x)
