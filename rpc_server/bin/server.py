# @Time    : 2017/10/24 上午11:24
# @Author  : Obser


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main


if __name__ == '__main__':
    main.run()