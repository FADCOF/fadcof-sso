# -*- coding: utf-8 -*-
from fadck.crypto.base import AsymmetricCache


class SM2:
    def __init__(self, n, p, g, a, b):
        pass

    def encrypt(self, contents: bytes):
        pass

    def decrypt(self, contents: bytes):
        pass


class SM2Cache(AsymmetricCache):
    def __init__(self, pub_key: bytes, pri_key: bytes):
        super().__init__(pub_key, pri_key)

    def encrypt(self, contents: bytes):
        pass
