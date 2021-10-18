# -*- coding: utf-8 -*-
import json
import time
import requests

from settings import TEST_TIMEOUT
from utils.log import logger
from utils.http import get_request_header
from domain import Proxy


def check_proxy(proxy):
    """
    用于检测指定代理IP响应速度，匿名程度，支持协议类型
    :param proxy: 代理IP数据模型对象
    :return: 检测后的代理IP数据模型对象
    """
    # 准备代理IP字典
    proxies = {
        "http": "http://{}:{}".format(proxy.ip, proxy.pory),
        "https": "https://{}:{}".format(proxy.ip, proxy.pory),
    }
    # 测试该代理IP
    http, http_nick_type, http_speed = _check_http_proxies(proxies)
    https, https_nick_type, https_speed = _check_http_proxies(proxies, False)
    # protocol：代理IP支持的协议类型，http为0，https为1，http/https都支持为2
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1

    return proxy


def _check_http_proxies(proxies, is_http=True):
    # 匿名类型 --> 高匿：0, 匿名:1, 透明:2
    nick_type = -1
    # 响应速度，单位：秒
    speed = -1

    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'

    try:
        # 获取开始时间
        start = time.time()
        # 发送请求，获取响应
        response = requests.get(url=test_url, headers=get_request_header(), proxies=proxies, timeout=TEST_TIMEOUT)

        if response.ok:
            # 计算响应速度
            speed = round(time.time() - start, 2)
            # 匿名程度检测
            # 把响应的json转换为字典
            dic = json.loads(response.text)
            # 获取来源IP
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)

            if ',' in origin:
                # 如果响应的 origin 的中有 ',' 分割的两个IP，就是透明代理
                nick_type = 2
            elif proxy_connection:
                # 如果响应的 headers 中包含 Proxy-Connection，说明是匿名代理
                nick_type = 1
            else:
                # 否则就是高匿代理
                nick_type = 0
            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as e:
        # logger.exception(e)
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy('222.85.39.120', '29445')
    rs = check_proxy(proxy)
    print(rs)
