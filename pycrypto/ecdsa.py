"""Implementation of ECDSA algorithm
"""

from secrets import randbelow
from typing import Optional

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
        private_key_int = int(private_key, 16)  # Doesn't need explicit exception

        if not 1 <= private_key_int <= self.ec_type.p - 1:
            raise ValueError("Private key is not in the proper range")

        return hex((self.gen_point * int(private_key, 16)).x)

    def keygen(self, private_key: Optional[str] = None) -> str:
        """Key pair generation

        Args:
            private_key (Union[NoneType, str], optional): If private key is specified,
            it will work just as method 'keygen_public',
            or it will generate new private key. Defaults to None.

        Returns:
            tuple: tuple containing:

                private_key (str): Private key hex string
                public_key (str): Public key hex string
        """
        if private_key is None:
            private_key = self.keygen_private()
        return private_key, self.keygen_public(private_key)

    def gen_message_hash(self, message: str) -> str:
        """Message hash generation with given message and SHA-2 algorithm
        Its first proposal was to use SHA-1, but it has some vulnerabilities,
        Adopting SHA-2 would be better. (Chose SHA-256)

        Args:
            message (str): Message to be hashed

        Returns:
            str: Message hash hex string (256 bit)
        """
        # TODO: To be implemented
        pass

    def gen_signature(self, private_key: str, message: str) -> str:
        """Signature generation with given private key and message
        d : private key
        Q : public key
        G : generator point

        1. Generate k (random number)
        2. Generate r (Px where P = k * G)
        3. Generate z (message hash)
        4. Generate s (s = k^-1 * (z + d * r) mod p)
        5. Generate signature with DER(r, s)

        DER :
            1. 0x30 byte: header byte to indicate compound structure
            2. one byte to encode the length of the following data
            3. 0x02: header byte indicating an integer
            4. one byte to encode the length of the following r value
            5. the r value as a big-endian integer
            6. 0x02: header byte indicating an integer
            7. one byte to encode the length of the following s value
            8. the s value as a big-endian integer

        Args:
            private_key (str): Private key hex string
            message (str): Message string

        Returns:
            str : Signature
        """
        # TODO: To be implemented
        pass

    def validate(self, message: str, signature: str, public_key: str) -> bool:
        """Message validation
        Q : public key
        G : generator point
        z : message hash
        r : signature r
        s : signature s

        1. Parse signature (r, s) = DECODE(signature)
        2. Generate z(message hash) from message z = SHA-256(message)
        3. Compute r == Px where P = s^-1 * z * G + s^-1 * r * Q

        Args:
            message (str): Message
            signature (str): Signature
            public_key (str): Public key

        Returns:
            bool: If valid return True, else return False
        """
        # TODO: To be implemented
        pass
