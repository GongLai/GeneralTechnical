# -*- coding: utf-8 -*-
from settings import MAX_SCORE


class Proxy(object):
    # 代理IP的数据模型类

    def __init__(self, ip, pory, pootocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=None):
        # ip：代理的IP地址
        self.ip = ip
        # pory：代理IP的端口号
        self.pory = pory
        # pootocol：代理IP支持的协议类型，http为0，https为1，http/https都支持为2
        self.pootocol = pootocol
        # nick_type：代理IP的匿名程度，高匿：0，匿名：1，透明：2
        self.nick_type = nick_type
        # speed：代理IP的响应速度，单位：s
        self.speed = speed
        # area：代理IP所在的地区
        self.area = area
        # score:代理IP的评分，用于衡量代理IP的可用性
        # 默认分值可用通过配置文件进行配置。在进行代理可用性检测的时候，每遇到一次请求失败就减1分，减到0的时候就从池中删除。如果检测代理可用就恢复默认分值
        self.score = score
        # disable_domains：不可用域名列表，某些代理IP在某些域名下不可用，但在其他域名下可用
        if disable_domains is None:
            disable_domains = []
        self.disable_domains = disable_domains

    def __str__(self):
        """返回数据的字符串"""
        return str(self.__dict__)
