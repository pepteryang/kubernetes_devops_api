# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/3/21
# @Site : 
# @File : apschedule_setting
# @Software : PyCharm

from pytz import utc
from pytz import UnknownTimeZoneError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore
import logging
import tzlocal
import struct
# 添加日志模块
logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/apscheduler.log',
                    filemode='a',
                    )
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
logging.getLogger('SQLAlchemyJobStore.engine').setLevel(logging.INFO)


# 配置作业存储器
# jobstores = {
#     'default': SQLAlchemyJobStore(url='mysql://root:123456@120.78.189.181:3306/apscheduler_jobs')
# }
# 配置执行器，并设置线程数
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(50)
}
job_defaults = {
    # 默认情况下关闭新的作业
    'coalesce': False,
    # 设置调度程序将同时运行的特定作业的最大实例数3
    'max_instances': 3,
    'misfire_grace_time': 30
}

try:
    timezone = tzlocal.get_localzone()
    logging.info('Local timezone name {}'.format(timezone))
    if timezone.zone == 'local':
        timezone = None
except UnknownTimeZoneError:
    timezone = None
except struct.error as e:
    # Hiding exception that may occur in tzfile.py seen in entware
    logging.warning('Hiding exception from tzlocal: %s', e)
    timezone = None
if not timezone:
    logging.info('Local timezone name could not be determined. Scheduler will display times in UTC for any log'
             'messages. To resolve this set up /etc/timezone with correct time zone name.')
    timezone = utc

scheduler = BackgroundScheduler(executors=executors, timezone=timezone,)
scheduler.add_jobstore(DjangoJobStore(), "default")

