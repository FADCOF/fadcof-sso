# -*- coding: utf-8 -*-
import uvicorn
import sys


def main():
    uvicorn.run('main:app', host='localhost', port=8000, log_level="debug")


if __name__ == '__main__':
    sys.exit(main())
