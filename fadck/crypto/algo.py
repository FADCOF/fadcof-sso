# -*- coding: utf-8 -*-
from fadck.crypto import aes, sm4, hash

ASYMM_CACHE = {
}

SYMM_CACHE = {
    'aes_ecb': aes.AesEcbCache,
    'aes_cbc': aes.AesCbcCache,
    'aes_ctr': aes.AesCtrCache,
    'sm4_ecb': sm4.Sm4EcbCache,
    'sm4_cbc': sm4.Sm4CbcCache,
}

HASH_CACHE = {
    'sm3': hash.SM3Cache,
    'md5': hash.MD5Cache,
    'sha1': hash.SHA1Cache,
    'sha256': hash.SHA1Cache,
    'sha3-256': hash.SHA3_256Cache,
}


def get_hash_cache(method: str) -> hash.HashCache:
    # Construct the cache.
    if method not in HASH_CACHE:
        raise NotImplementedError('No hash method named "{}".'.format(method))
    return HASH_CACHE[method]()
