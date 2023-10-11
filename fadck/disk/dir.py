# -*- coding: utf-8 -*-
import os
import logging
from os.path import dirname, abspath

SDK_ROOT = dirname(dirname(abspath(__file__)))
ROOT = dirname(SDK_ROOT)
STORAGE_ROOT = os.path.join(ROOT, 'storage')
MAIN_POOL_ROOT = os.path.join(STORAGE_ROOT, 'main')
BACKUP_POOL_ROOT = os.path.join(STORAGE_ROOT, 'backup')
MAIN_POOL_VALID = False
BACKUP_POOL_VALID = False
MAINTENANCE_MODE = True

logger = logging.getLogger()


def update_pool_states():
    # Check the main disk pool and backup disk pool.
    global MAINTENANCE_MODE, MAIN_POOL_VALID, BACKUP_POOL_VALID
    MAIN_POOL_VALID = os.path.isdir(MAIN_POOL_ROOT)
    BACKUP_POOL_VALID = os.path.isdir(BACKUP_POOL_ROOT)
    MAINTENANCE_MODE = not (MAIN_POOL_VALID and BACKUP_POOL_VALID)
    if not MAIN_POOL_VALID and not BACKUP_POOL_VALID:
        raise RuntimeError('Both main and backup disk pool failed to work.')
    if MAINTENANCE_MODE:
        logger.warning('Storage pool downgrade, {} pool failed to work, system worked in maintenance mode.'.format(
            'main' if not MAIN_POOL_VALID else 'backup'))


def __pool_path(sub_path: str, pool: str = 'main'):
    return os.path.join(MAIN_POOL_ROOT if pool == 'main' else BACKUP_POOL_ROOT, sub_path)


def __valid_path(sub_path: str):
    if MAIN_POOL_VALID:
        return __pool_path(sub_path, 'main')
    if BACKUP_POOL_VALID:
        return __pool_path(sub_path, 'backup')
    raise RuntimeError('Both main and backup disk pool failed to read.')


class Session:
    def __init__(self):
        self.__ops = []

    def push(self, op, *args):
        self.__ops.append((op, args))

    def rollback(self):
        for op, args in self.__ops:
            op(*args)


def mkdir(*subs):
    sess = Session()

    def rmdir(target_path: str):
        os.rmdir(target_path)

    try:
        sub_path = os.path.join(*subs)
        main_path = __pool_path(sub_path, 'main')
        backup_path = __pool_path(sub_path, 'backup')
        sess.push(rmdir, main_path)
        os.mkdir(main_path)
        sess.push(rmdir, backup_path)
        os.mkdir(backup_path)
    except Exception as e:
        sess.rollback()
        raise e


def ensure(*subs):
    sub_path = os.path.join(*subs)
    target_path = __valid_path(sub_path)
    if os.path.isdir(target_path):
        return
    mkdir(*subs)


def startup():
    # Check whether the disk directory exist.
    if not os.path.isdir(STORAGE_ROOT):
        raise FileNotFoundError('No disk directory mapped under the directory.')
    # Check the disk pool.
    update_pool_states()
