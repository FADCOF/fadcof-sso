# -*- coding: utf-8 -*-
import hashlib
from fadck.crypto.base import HashCache
from fadck.crypto.gmlib import rotl


class SM3Cache(HashCache):
    IV = [1937774191, 1226093241, 388252375, 3666478592,
          2842636476, 372324522, 3817729613, 2969243214, ]

    T_j = [2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
           2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
           2043430169, 2043430169, 2043430169, 2043430169, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
           2055708042, 2055708042, 2055708042, 2055708042]

    @staticmethod
    def __p_0(x):
        return x ^ (rotl(x, 9)) ^ (rotl(x, 17))

    @staticmethod
    def __p_1(x):
        return x ^ (rotl(x, 15)) ^ (rotl(x, 23))

    @staticmethod
    def __ff_j(x, y, z, j):
        if 0 <= j < 16:
            return x ^ y ^ z
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def __gg_j(x, y, z, j):
        if 0 <= j < 16:
            return x ^ y ^ z
        return (x & y) | ((~ x) & z)

    @staticmethod
    def __cf(v_i, b_i):
        def w_i(i: int):
            b_w = 0x1000000
            w_data = 0
            for k in range(i * 4, (i + 1) * 4):
                w_data = w_data + b_i[k] * b_w
                b_w = int(b_w / 0x100)
            return w_data

        w = [w_i(ii) for ii in range(16)]
        for j in range(16, 68):
            w.append(SM3Cache.__p_1(w[j - 16] ^ w[j - 9] ^ (rotl(w[j - 3], 15))) ^ (rotl(w[j - 13], 7)) ^ w[j - 6])
        w_1 = [w[j] ^ w[j+4] for j in range(64)]

        a, b, c, d, e, f, g, h = v_i
        for j in range(64):
            ss_1 = rotl(
                ((rotl(a, 12 % 32)) +
                 e +
                 (rotl(SM3Cache.T_j[j], j % 32))) & 0xffffffff, 7)
            ss_2 = ss_1 ^ (rotl(a, 12 % 32))
            tt_1 = (SM3Cache.__ff_j(a, b, c, j) + d + ss_2 + w_1[j]) & 0xffffffff
            tt_2 = (SM3Cache.__gg_j(e, f, g, j) + h + ss_1 + w[j]) & 0xffffffff
            d = c
            c = rotl(b, 9)
            b = a
            a = tt_1
            h = g
            g = rotl(f, 19 % 32)
            f = e
            e = SM3Cache.__p_0(tt_2)
            # Ensure 64 bits.
            a, b, c, d, e, f, g, h = map(lambda x: x & 0xFFFFFFFF, [a, b, c, d, e, f, g, h])

        return [x ^ y for x, y in zip([a, b, c, d, e, f, g, h], v_i)]

    @staticmethod
    def __int_to_bytes_le(x):
        return [((x & (0xFF << (ii << 3))) >> (ii << 3)) for ii in range(8)]

    @staticmethod
    def __int_to_bytearray_le(x):
        return bytearray(x.to_bytes(8))

    @staticmethod
    def __int_to_bytearray_be(x):
        return bytearray(x.to_bytes(8, 'big'))

    @staticmethod
    def __hash_data(message: bytes):
        # Get the length of the message.
        size_byte = len(message)
        size_bit = size_byte << 3
        # Calculate the padding content.
        message_tail = bytearray([0x80])
        # Add 0x00 padding.
        residual = (size_byte % 64) + 1
        range_end = 120 if residual > 56 else 56
        # Add bits length at the end.
        message_tail += (bytearray([0x00] * (range_end - residual)) +
                         SM3Cache.__int_to_bytearray_be(size_bit))
        # Loop for each 64 bytes.
        block_start = 0
        block_end = block_start + 64
        v = SM3Cache.IV
        while block_end <= size_byte:
            v = SM3Cache.__cf(v, message[block_start:block_end])
            # Move to next block.
            block_start = block_end
            block_end += 64
        # Residual calculation.
        if block_start < size_byte:
            # Append the residual data to the tail bytes.
            message_tail = bytearray(message[block_start:]) + message_tail
        # Keep process the tail of the message.
        block_start = 0
        block_end = block_start + 64
        size_byte = len(message_tail)
        while block_end <= size_byte:
            v = SM3Cache.__cf(v, message_tail[block_start:block_end])
            # Move to next block.
            block_start = block_end
            block_end += 64
        return b''.join(x.to_bytes(4, 'big') for x in v)

    def digest(self, content: bytes) -> bytes:
        return self.__hash_data(content)


class MD5Cache(HashCache):
    def digest(self, content: bytes) -> bytes:
        return hashlib.md5(content).digest()


class SHA1Cache(HashCache):
    def digest(self, content: bytes) -> bytes:
        return hashlib.sha1(content).digest()


class SHA256Cache(HashCache):
    def digest(self, content: bytes) -> bytes:
        return hashlib.sha256(content).digest()


class SHA3_256Cache(HashCache):
    def digest(self, content: bytes) -> bytes:
        return hashlib.sha3_256(content).digest()
