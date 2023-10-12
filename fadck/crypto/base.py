# -*- coding: utf-8 -*-
class Cache:
    pass


class AsymmetricCache(Cache):
    def __init__(self, pub_key: bytes, pri_key: bytes):
        pass

    def decrypt(self, content: bytes) -> bytes:
        pass

    def encrypt(self, content: bytes) -> bytes:
        pass


class SymmetricCache(Cache):
    def __init__(self, key: bytes):
        pass

    def decrypt(self, content: bytes) -> bytes:
        pass

    def encrypt(self, content: bytes) -> bytes:
        pass


class PyCryptoSymmetricCache(SymmetricCache):
    def __init__(self, key: bytes, engine):
        super().__init__(key)
        self.__engine = engine

    def decrypt(self, content: bytes) -> bytes:
        return self.__engine.decrypt(content)

    def encrypt(self, content: bytes) -> bytes:
        return self.__engine.encrypt(content)


class HashCache(Cache):
    def __init__(self):
        pass

    def digest(self, content: bytes) -> bytes:
        pass
