# -*- coding: utf-8 -*-
from fadck.crypto.base import AsymmetricCache
from Crypto.PublicKey import RSA


class PyCryptoCache(AsymmetricCache):
    def __init__(self, pub_key: bytes, pri_key: bytes):
        super().__init__(pub_key, pri_key)
        self.__pub_key = RSA.import_key(pub_key)
        self.__pri_key = RSA.import_key(pri_key)

    def decrypt(self, content: bytes) -> bytes:
        return self.__pri_key.decrypt(content)