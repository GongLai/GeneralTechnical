# -*- coding: utf-8 -*-
import logging

# 代理IP默认最高分值：50
MAX_SCORE = 50

# 日志信息的默认配置
LOG_LEVEL = logging.INFO  # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件名称

# 检测代理IP的超时时间
TEST_TIMEOUT = 10


# 配置MongoDB
USER = 'King'
PASSWORD = '1314156'
SERVER = '127.0.0.1'
PORT = '27017'
MONGODB_URL = 'mongodb://{USER}:{PASSWORD}@{SERVER}:{PORT}'.format(USER=USER, PASSWORD=PASSWORD,
                                                                   SERVER=SERVER, PORT=PORT)
