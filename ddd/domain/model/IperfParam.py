# coding=utf-8

import abc
from .base.value_object import ValueObject


class Iperf(object):
    def __init__(self, dest_ip, dest_port, report_interval=1,
                 duration=7200, bandwidth="50M",
                 total_size=2000000, src_ip=None):
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.report_interval = report_interval
        self.duration = duration
        self.bandwidth = bandwidth
        self.total_size = total_size
        self.buffer_len = 1024
        self.window_size = "512K"
        self.src_ip = src_ip
        self.parallel = 1

    def send_udp(self):
        cmd_result = self.ueServiceMgr.send_udp(self.__dict__)
        if not cmd_result.result:
            return None
        return self._save_task_id(cmd_result)

    def send_tcp(self):
        cmd_result = self.ueServiceMgr.send_tcp(self.__dict__)
        if not cmd_result.result:
            return None
        return self._save_task_id(cmd_result)

ValueObject.register(Iperf)

