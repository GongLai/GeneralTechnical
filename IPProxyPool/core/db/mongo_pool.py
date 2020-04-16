# -*- coding: utf-8 -*-
from pymongo import MongoClient

from settings import MONGODB_URL


class MongoPool(object):
    """实现代理池数据库模块"""

    def __init__(self):
        # 1. 建立数据库连接
        self.client = MongoClient(MONGODB_URL)
        # 2. 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 3. 关闭数据库连接
        self.client.close()
