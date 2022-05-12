"""Implementation of SHA-256 algorithm
"""


class SHA256:
    """Class for SHA-256 algorithm"""

    # Initial hash values
    # First 32 bits of the fractional parts of the square roots of the first 8 primes: 2, 3, 5, 7, 11, 13, 17, 19
    h = [
        0x6A09E667,
        0xBB67AE85,
        0x3C6EF372,
        0xA54FF53A,
        0x510E527F,
        0x9B05688C,
        0x1F83D9AB,
        0x5BE0CD19,
    ]

    # first 32 bits of the fractional parts of the cube roots of the first 64 primes (2 - 311)
    k = [
        0x428A2F98,
        0x71374491,
        0xB5C0FBCF,
        0xE9B5DBA5,
        0x3956C25B,
        0x59F111F1,
        0x923F82A4,
        0xAB1C5ED5,
        0xD807AA98,
        0x12835B01,
        0x243185BE,
        0x550C7DC3,
        0x72BE5D74,
        0x80DEB1FE,
        0x9BDC06A7,
        0xC19BF174,
        0xE49B69C1,
        0xEFBE4786,
        0x0FC19DC6,
        0x240CA1CC,
        0x2DE92C6F,
        0x4A7484AA,
        0x5CB0A9DC,
        0x76F988DA,
        0x983E5152,
        0xA831C66D,
        0xB00327C8,
        0xBF597FC7,
        0xC6E00BF3,
        0xD5A79147,
        0x06CA6351,
        0x14292967,
        0x27B70A85,
        0x2E1B2138,
        0x4D2C6DFC,
        0x53380D13,
        0x650A7354,
        0x766A0ABB,
        0x81C2C92E,
        0x92722C85,
        0xA2BFE8A1,
        0xA81A664B,
        0xC24B8B70,
        0xC76C51A3,
        0xD192E819,
        0xD6990624,
        0xF40E3585,
        0x106AA070,
        0x19A4C116,
        0x1E376C08,
        0x2748774C,
        0x34B0BCB5,
        0x391C0CB3,
        0x4ED8AA4A,
        0x5B9CCA4F,
        0x682E6FF3,
        0x748F82EE,
        0x78A5636F,
        0x84C87814,
        0x8CC70208,
        0x90BEFFFA,
        0xA4506CEB,
        0xBEF9A3F7,
        0xC67178F2,
    ]

    def __init__(self) -> None:
        pass

    @classmethod
    def hash(cls, msg_raw: str) -> bytearray:
        """Hashing with SHA-256

        Args:
            msg_raw (str): Raw string message

        Returns:
            bytearray: Hashed byte array
        """
        pass

    @staticmethod
    def binarize(msg_raw: str) -> bytearray:
        """Decode string into byte array

        Args:
            msg (str): raw message

        Returns:
            bytearray: Byte array of message
        """
        return bytearray(msg_raw, "utf-8")

    @staticmethod
    def preprocessing(msg: bytearray) -> bytearray:
        """Preprocessing method for message
        1. Append single 1 to binary message
        2. Pad 0s until data is a multiple of 512(64 byte), less 64(8 byte) bits
           (512bit * n - 64bit), (64byte * n - 8byte)
        3. Append 64 bits to the end,
           where the 64 bits are a big-endian integer
           representing the length of the original input in binary
        It will always be evenly divisible by 512bit (chunk)

        Args:
            msg (bytearray): Byte array of message

        Returns:
            bytearray: Preprocessed byte array
        """
        msg_len = len(msg)
        msg.append(0b10000000)
        pad_length = -(msg_len + 1 + 8) % 64
        for _ in range(pad_length):
            msg.append(0)
        msg.extend((msg_len * 8).to_bytes(8, "big"))
        return msg

    @staticmethod
    def chunking(msg: bytearray) -> list:
        """Chunking method for preprocessed message
        This will split preprocessed messge with 512bit chunks

        Args:
            msg (bytearray): Preprocessed message bytearray

        Returns:
            list: list containing chunks(bytearray)
        """
        chunks = [msg[i * 64:(i + 1) * 64] for i in range(len(msg) // 64)]
        return chunks

    @staticmethod
    def create_message_schedule(chunk):
        """Create message schedule w
        1. Split chunks into a new array where each entry is a 32bit word (16 words)
        2. Add 48 more words initialized to zero (1536 bit)
           Now we have total 64(16+48) words (512 + 1536 = 2048 bit)
        3. For i in range(16, 64):
             s0 = (w[i-15] rightrotate 7) xor (w[i-15] rightrotate 18) xor (w[i-15] rightshift 3)
             s1 = (w[i- 2] rightrotate 17) xor (w[i- 2] rightrotate 19) xor (w[i- 2] rightshift 10)
             w[i] = w[i-16] + s0 + w[i-7] + s1
             (This addition is calculated modulo 2^32, So number of bits never changes)

        Args:
            chunk (bytearray): Bytearray of chunk

        Returns:
            list: List of message schedule w
        """
        pass

    @classmethod
    def compression(cls, w: list) -> list:
        """Compress chunk
        1. Initialize variables a, b, c, d, e, f, g, h and set them
           equal to the current hash values respectively. h0, h1, h2, h3, h4, h5, h6, h7
        2. for i in range(64):
             S1 = (e rightrotate 6) xor (e rightrotate 11) xor (e rightrotate 25)
             ch = (e and f) xor ((not e) and g)
             temp1 = h + S1 + ch + k[i] + w[i]
             S0 = (a rightrotate 2) xor (a rightrotate 13) xor (a rightrotate 22)
             maj = (a and b) xor (a and c) xor (b and c)
             temp2 := S0 + maj
             h = g
             g = f
             f = e
             e = d + temp1
             d = c
             c = b
             b = a
             a = temp1 + temp2
             (All addition is caculated modulo 2^32)

        Args:
            w (list): List of message schedule

        Returns:
            list: List of value v
        """
        pass

    @classmethod
    def finalize(cls, v: list) -> list:
        """Finalize with adding initial hash with obtained values

        Args:
            v (list): List of value

        Returns:
            list: Final hash
        """
        pass

    @staticmethod
    def concatenate(final_hash: list) -> bytearray:
        """Concatenate final hash to get bytearray of hash

        Args:
            final_hash (list): Final hash

        Returns:
            bytearray: Concatenated bytearray
        """
        pass
