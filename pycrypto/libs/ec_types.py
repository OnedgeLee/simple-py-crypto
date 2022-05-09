"""Definition of elliptic curves
"""

from typing import Any


class EllipticCurveType:
    """Elliptic curve type that parses sextuple T = (p,a,b,G,n,h) to domain parameters"""

    def __setattr__(self, name: str, value: Any) -> None:
        """Overrides __setattr__ method to prevent attribute changes, making instance immutable

        Args:
            name (str): Name of attribute to set
            value (Any): Value of attribute to set

        Raises:
            AttributeError: Any kind of attribute modification is prevented
        """
        raise AttributeError("EllipCurveType attributes cannot be setted")

    def __delattr__(self, name: str) -> None:
        """Overrides __delattr__ method to prevent attribute changes, making instance immutable

        Args:
            name (str): Name of attribute to be deleted

        Raises:
            AttributeError: Any kind of attribute deletion is prevented
        """
        raise AttributeError("EllipCurveType attributes cannot be deleted")

    # TODO: Implement Tonelli-Shanks Algorithm
    # To handle condition that G with 02 or 03 encounters
    # Those G does not have y coordinate, and we have to solve
    # (y^2) % p = (x^3 + ax + b) % p with given x coordinate
    # To do so, we have to solve Tonelli-Shanks Algorithm
    # But generally we can easily find information of y on internet,
    # so I'll left this work as future job
    # @staticmethod
    # def tonelli_shanks(n, p):
    #     if not (n ** ((p - 1) / 2)) % p == 1: # Euler's criterion
    #         raise ValueError("n mod p does not have quadratic residue")
    #     pass

    @classmethod
    @property
    def p(cls) -> int:
        """Get elliptic curve domain parameter p from sextuple T = (p,a,b,G,n,h)

        Returns:
            int: Elliptic curve domain parameter p (modulo prime number)
        """
        return int(cls.hex_str_dict["p"], 16)

    @classmethod
    @property
    def a(cls) -> int:
        """Get elliptic curve domain parameter a from sextuple T = (p,a,b,G,n,h)

        Returns:
            int: Elliptic curve domain parameter a (coefficient of x order 1)
        """
        return int(cls.hex_str_dict["a"], 16)

    @classmethod
    @property
    def b(cls) -> int:
        """Get elliptic curve domain parameter b from sextuple T = (p,a,b,G,n,h)

        Returns:
            int: Elliptic curve domain parameter b (coefficient of x order 0, constant parameter)
        """
        return int(cls.hex_str_dict["b"], 16)

    @classmethod
    @property
    def gx(cls) -> int:
        """Get Gx from elliptic curve domain parameter G of sextuple T = (p,a,b,G,n,h)

        Raises:
            ValueError: If encoded string of G is invalid, raises ValueError

        Returns:
            int: X coordinate of generator point G
        """
        g_hex_str = cls.hex_str_dict["g"]
        if g_hex_str[:2] == "02":
            return int(g_hex_str[2:], 16)
        elif g_hex_str[:2] == "03":
            return int(g_hex_str[2:], 16)
        elif g_hex_str[:2] == "04":
            return int(g_hex_str[2:66], 16)
        else:
            raise ValueError("Invalid ground value")

    @classmethod
    @property
    def gy(cls) -> int:
        """Get Gy from elliptic curve domain parameter G of sextuple T = (p,a,b,G,n,h)

        Raises:
            ValueError: G string starts with 02 does not contain Gy information,
                so Tonelli-Shanks Algorithm is needed (not implemented)
            ValueError: G string starts with 03 does not contain Gy information,
                so Tonelli-Shanks Algorithm is needed (not implemented)
            ValueError: If encoded string of G is invalid, raises ValueError

        Returns:
            int: Y coordinate of generator point G
        """
        g_hex_str = cls.hex_str_dict["g"]
        if g_hex_str[:2] == "02":
            # TODO: Implement this with Tonelli-Shanks Algorithm
            raise ValueError("02 type G is not supported for now")
            # n = cls.gx ** 3 + cls.gx * cls.a + cls.b
        elif g_hex_str[:2] == "03":
            # TODO: Implement this with Tonelli-Shanks Algorithm
            raise ValueError("03 type G is not supported for now")
            # n = cls.gx ** 3 + cls.gx * cls.a + cls.b
        elif g_hex_str[:2] == "04":
            return int(g_hex_str[66:], 16)
        else:
            raise ValueError("Invalid ground value")

    @classmethod
    @property
    def n(cls) -> int:
        """Get elliptic curve domain parameter n from sextuple T = (p,a,b,G,n,h)

        Returns:
            int: Elliptic curve domain parameter n (order of point G)
        """
        return int(cls.hex_str_dict["n"], 16)

    @classmethod
    @property
    def h(cls) -> int:
        """Get elliptic curve domain parameter h from sextuple T = (p,a,b,G,n,h)

        Returns:
            int: Elliptic curve domain parameter h (cofactor, N(Number of points) / n(Order of point G))
        """
        return int(cls.hex_str_dict["h"], 16)

    @classmethod
    @property
    def valid(cls) -> bool:
        """Check if the domain parameters are valid
        Check if generator point G is on given elliptic curve with finite field modulus

        Returns:
            bool: If the domain parameters are valid return True, else return False
        """
        return (cls.gy**2) % cls.p == (cls.gx**3 + cls.gx * cls.a + cls.b) % cls.p


class Secp256k1(EllipticCurveType):
    """secp256k1 with its domain parameters"""

    hex_str_dict = {
        "p":
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F",
        "a":
            "0000000000000000000000000000000000000000000000000000000000000000",
        "b":
            "0000000000000000000000000000000000000000000000000000000000000007",
        "g":
            "04"\
            "79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"\
            "483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8",
        "n":
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141",
        "h":
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F",
    }


secp256k1 = Secp256k1()

if not secp256k1.valid:
    raise ValueError("Elliptic Curve information is incorrect")
