# -*- coding: utf-8 -*-
def rotl(x: int, n: int):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)


def get_uint32_be(x: bytes) -> int:
    return int.from_bytes(x, 'big')


def put_uint32_be(x: int) -> bytearray:
    return bytearray(x.to_bytes(4, 'big'))
