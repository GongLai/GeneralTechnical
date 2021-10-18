import time
import logging

# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
INITIAL = 1634544117117


class WorkerId:
    """
    雪花算法实现：用于生成ID
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 起始序号
        """
        # 请求参数验证
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError("worker_id值越界")

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError("datacenter_id值越界")

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    @staticmethod
    def _get_timestamp():
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return: id编号
        """
        # 获取当前时间戳
        timestamp = self._get_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logging.error(f'时钟回拨。当前时间为：{timestamp}，上次计算的时间戳为：{self.last_timestamp}')
            timestamp = self._calc_timestamp(self.last_timestamp)
        # 如果当前时间的时间戳与上一时间的时间戳相同，序号加1,并判断当前序号是否为0,为0说明当前序号已是最大序号，等待下一毫秒
        elif timestamp == self.last_timestamp:
            timestamp = self._calc_timestamp(timestamp)
        else:  # 重置序号
            self.sequence = 0

        # 重置时间戳
        self.last_timestamp = timestamp
        # 生成id编号并返回
        return ((timestamp - INITIAL) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | (
                self.worker_id << WORKER_ID_SHIFT) | self.sequence

    def _calc_timestamp(self, timestamp):
        """
        计算时间戳
        :param timestamp 时间戳
        :return: 时间戳
        """
        # 获取当前序号并加1，掩码计算
        self.sequence = (self.sequence + 1) & SEQUENCE_MASK
        # 如果计算得到的当前序号为0,说明已经是最大值了，时间戳加1毫秒
        if self.sequence == 0:
            timestamp += 1
        # 返回时间戳
        return timestamp


if __name__ == '__main__':
    worker = WorkerId(1, 1, 0)
    print(worker.get_id())
