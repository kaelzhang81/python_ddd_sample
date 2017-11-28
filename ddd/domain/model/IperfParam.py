class IperfParam(object):
    def __init__(self, dest_ip, dest_port, report_interval=1,
                 duration=7200, bandwidth="50M",
                 total_size=2000000, src_ip=None, isKeepAlive=False, numberOfBytes=None):
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.report_interval = report_interval
        self.duration = duration
        self.bandwidth = bandwidth
        self.total_size = total_size
        self.buffer_len = 1024
        self.window_size = "512K"
        self.src_ip = src_ip
        self.isKeepAlive = isKeepAlive
        self.numberOfBytes = numberOfBytes
        self.parallel = 1
