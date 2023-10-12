# -*- coding: utf-8 -*-
from collections import ChainMap


def padding_zero(content: bytes, block_size: int = 16):
    residual = len(content) % block_size
    if residual == 0:
        return content
    return content + b'\x00' * (block_size - residual)


def padding_iso9797(content: bytes, block_size: int = 16):
    content += b'\x80'
    return padding_zero(content, block_size)


def padding_pkcs7(content: bytes):
    item = 16 - len(content) % 16
    return content + item.to_bytes(1, 'little') * item


def padding_pboc(content: bytes):
    # Check the residual bytes.
    residual_size = len(content) % 16
    if residual_size == 0:
        return content
    # Return the bytes.
    return padding_iso9797(content, 16)


PADDING_METHODS = {
    ('zero', 'x99', 'ansi x99', 'x9.19', 'ansi x9.19'): padding_zero,
    ('iso9797m2', 'iso9797'): padding_iso9797,
    ('pkcs7', ): padding_pkcs7,
    ('pboc', ): padding_pboc,
}
PADDING_METHODS = dict(ChainMap(*[dict.fromkeys(ks, PADDING_METHODS[ks]) for ks
                                  in PADDING_METHODS]))


def padding(method: str, content: bytes, *args, **kwargs) -> bytes:
    # Find the method.
    if method not in PADDING_METHODS:
        raise NotImplementedError('No padding method named "{}"'.format(method))
    return PADDING_METHODS[method](content, *args, **kwargs)
