#-*-coding:utf-8-*-
# @Author : zhihui
# @Email : zhihui.he@bqrzzl.com
# @Time : 2018/6/27 18:08
# @Site : 
# @File : log_service.py
# @Software : PyCharm

import functools
import logging
import traceback

logger = logging.getLogger('django')


def system_log(func):
    """
    自动记录日志的装饰器：
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.debug(traceback.format_exc())
            return False, e.__str__()
    return _deco
