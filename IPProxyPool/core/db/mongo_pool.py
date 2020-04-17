# -*- coding: utf-8 -*-
import pymongo
import random

from domain import Proxy
from settings import MONGODB_URL
from utils.log import logger


class MongoPool(object):
    """实现代理池数据库模块"""

    def __init__(self):
        # 1. 建立数据库连接
        self.client = pymongo.MongoClient(MONGODB_URL)
        # 2. 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 3. 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        """实现代理数据插入功能"""

        # 检测需要插入的代理是否已存在
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            # 使用proxy.ip作为Mongodb中数据的主键：_id
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info('插入新代理：{}'.format(proxy))
        else:
            logger.warning('已存在代理：{}'.format(proxy))

    def update_one(self, proxy):
        """实现修改代理数据功能"""
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        """实现删除代理数据功能"""
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info('删除代理：{}'.format(proxy))

    def find_all(self):
        """查询所有代理数据功能"""
        cursor = self.proxies.find()
        for item in cursor:
            # 删除 `_id` key
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions=None, count=0):
        """
        实现查询功能：根据条件进行查询，可以指定查询数量，先按分数降序，再响应速度升序，保证优秀的代理IP在上面
        :param conditions: 查询条件字典
        :param count: 限制最高取出多少个代理IP
        :return: 返回满足要求代理IP(Proxy对象)列表
        """
        if conditions is None:
            conditions = {}
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)
        ])

        # 准备列表，用于存储查询处理代理IP
        proxy_list = []
        # 遍历cursor
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)

        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        根据协议类型和要访问网站的域名，获取代理IP列表
        :param protocol: 协议：http/https
        :param domain: jd.com
        :param count: 限制最高取出多少个代理IP，默认是获取所有的
        :param nick_type: 匿名程度，默认获取高匿的代理IP
        :return: 满足要求代理IP的列表
        """
        # 定义查询条件
        conditions = {'nick_type': nick_type}
        # 根据协议类型指定查询条件
        if protocol is None:
            # 如果没有传入协议类型，返回支持http和https的代理IP
            conditions['protocol'] = 2
        elif protocol.lower() == "http":
            conditions['protocol'] = {'$in': [0, 2]}
        elif protocol.lower() == "https":
            conditions['protocol'] = {'$in': [1, 2]}
        else:
            logger.info('指定协议类型出错，请校验后重新输入！！！')
            return []

        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}

        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        根据协议类型和要访问网站的域名，随机获取一个代理IP
        :param protocol: 协议：http/https
        :param domain: jd.com
        :param count: 限制最高取出多少个代理IP，默认是获取所有的
        :param nick_type: 匿名程度，默认获取高匿的代理IP
        :return: 从满足要求的随机代理IP列表中随机取出一个代理IP返回
        """
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        # 从 proxy_list 中随机取出一个代理IP返回
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        把指定域名添加到指定IP的disable_domain列表中
        :param ip: IP地址
        :param domain: 域名
        :return: 如果返回True，表示添加成功；返回False，表示添加失败
        """
        # 如果 `disable_domains` 字段中没有这个域名，才添加
        if self.proxies.count_documents({'_id': ip, 'disable_domains': domain}) == 0:
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy('222.85.39.133', '1512')
    # dic = {'ip': '117.92.195.116', 'pory': '35557', 'protocol': 2, 'nick_type': 0, 'speed': 0.42, 'area': None, 'score': 30, 'disable_domains': []}
    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)
    # proxy = Proxy('222.85.39.120', '8888')
    # mongo.update_one(proxy)
    # mongo.delete_one(proxy)

    # for proxy in mongo.find_all():
    #     print(proxy)
    # for proxy in mongo.find():
    #     print(proxy)
    # for proxy in mongo.get_proxies(protocol='htt'):
    #     print(proxy)
    for proxy in mongo.get_proxies(protocol='https', domain='taobao.com'):
        print(proxy)
    mongo.disable_domain('117.92.195.114', 'baidu.com')
