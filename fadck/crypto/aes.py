# -*- coding: utf-8 -*-
from fadck.crypto.base import PyCryptoSymmetricCache
from Crypto.Cipher import AES


class AesEcbCache(PyCryptoSymmetricCache):
    def __init__(self, key: bytes):
        super().__init__(key, AES.new(key, AES.MODE_ECB))


class AesCbcCache(PyCryptoSymmetricCache):
    def __init__(self, key: bytes):
        super().__init__(key, AES.new(key, AES.MODE_CBC))


class AesCtrCache(PyCryptoSymmetricCache):
    def __init__(self, key: bytes):
        super().__init__(key, AES.new(key, AES.MODE_CTR))
