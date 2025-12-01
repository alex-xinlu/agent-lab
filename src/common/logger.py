# -*- coding: UTF-8 -*-
import os
import logging
import platform

from logging.handlers import RotatingFileHandler, QueueHandler


def is_osx():
    p = platform.platform()
    return p.find('macOS') >= 0 or p.find('Darwin') >= 0


def get_root_log_dir(config, options):
    action = 'default'
    if is_osx():
        return '/tmp/cdit/ai/{}'.format(action)
    else:
        is_dev = (options.cluster is None) or (options.cluster == 'dev')
        if is_dev:
            return '../log/cdit/ai/{}'.format(action)
        else:
            return '/var/cdit/cdit/ai/{}'.format(action)


class TruncatedFileHandler(RotatingFileHandler):
    '''
    日志文件按固定大小自动分割
    '''

    def __init__(self, filename, mode='a', maxBytes=0, encoding=None, delay=0):
        super(TruncatedFileHandler, self).__init__(
            filename, mode, maxBytes, 0, encoding, delay)

    def doRollover(self):
        """Truncate the file"""
        if self.stream:
            self.stream.close()
        dfn = self.baseFilename + ".1"
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(self.baseFilename, dfn)
        os.remove(dfn)
        self.mode = 'w'
        self.stream = self._open()


errors_channel = None


class HostnameFilter(logging.Filter):
    hostname = platform.node()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True


class EntWeChatHandler(QueueHandler):
    def __init__(self, channel):
        QueueHandler.__init__(self, channel)
        self.level = logging.ERROR


def init_log(config, options):
    # 创建日志目录
    root_log_dir = get_root_log_dir(config, options)
    os.makedirs(root_log_dir, exist_ok=True)
    print('root_log_dir:', root_log_dir)

    # 文件日志控制器
    log_filename = root_log_dir + '/app.log'
    file_handler = RotatingFileHandler(log_filename, maxBytes=100 * 1024 * 1024, backupCount=10, encoding='utf-8')

    # 控制台日志控制器
    console_handler = logging.StreamHandler()

    handlers = [
        file_handler,
        console_handler
    ]

    # 日志配置
    logging.basicConfig(
        # 日志格式
        format="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d at %(funcName)s]: %(message)s",
        # 日期格式
        datefmt='%Y-%m-%d %H:%M:%S',
        # 日志级别
        level=logging.INFO,
        # 输出目标，日志文件+控制台
        handlers=handlers
    )
