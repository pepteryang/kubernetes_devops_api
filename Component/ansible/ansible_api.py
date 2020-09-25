# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/12/4
# @Site : 
# @File : ansible_api
# @Software : PyCharm



from django.conf import settings
import os
import logging
from optparse import Values

from collections import namedtuple
import shutil,requests
from ansible.module_utils.common.collections import ImmutableDict
# 核心类
# 用于读取YAML和JSON格式的文件
from ansible.parsing.dataloader import DataLoader
# 用于存储各类变量信息
from ansible.vars.manager import VariableManager
# 用于导入资产文件
from ansible.inventory.manager import InventoryManager
# 存储执行hosts的角色信息
from ansible.playbook.play import Play
# 底层用到的任务队列
from ansible.executor.task_queue_manager import TaskQueueManager

# 状态回调，各种成功失败的状态
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C

from ansible.inventory.group import Group
from ansible.inventory.host import Host
# 执行Playbook
from ansible.executor.playbook_executor import PlaybookExecutor


logger = logging.basicConfig()

ansible_path = os.path.join(settings.BASE_DIR, 'ansible')

ansible_host = os.path.join(ansible_path, 'hosts')


# 重写callback
class ResultsCollector(CallbackBase):
    """
    通过api调用ac-hoc的时候输出结果很多时候不是很明确或者说不是我们想要的结果，主要它还是输出到STDOUT，而且通常我们是在工程里面执行
    这时候就需要后台的结果前端可以解析，正常的API调用输出前端很难解析。 对比之前的执行 adhoc()查看区别。
    为了实现这个目的就需要重写CallbackBase类，需要重写下面三个方法
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):
    def __init__(self):
        self.options = {
            'verbosity': 0,
            'ask_pass': False,
            'private_key_file': None,
            'remote_user': None,
            'connection': 'smart',
            'timeout': 10,
            'ssh_common_args': '',
            'sftp_extra_args': '',
            'scp_extra_args': '',
            'ssh_extra_args': '',
            'force_handlers': False,
            'flush_cache': None,
            'become': False,
            'become_method': 'sudo',
            'become_user': None,
            'become_ask_pass': False,
            'tags': ['all'],
            'skip_tags': [],
            'check': False,
            'syntax': None,
            'diff': False,
            'inventory': ansible_host,
            'listhosts': None,
            'subset': None,
            'extra_vars': [],
            'ask_vault_pass': False,
            'vault_password_files': [],
            'vault_ids': [],
            'forks': 5,
            'module_path': None,
            'listtasks': None,
            'listtags': None,
            'step': None,
            'start_at_task': None,
            'args': ['fake']}
        self.ops = Values(self.options)

        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultsCollector()
        self.inventory = InventoryManager(loader=self.loader, sources=[self.options['inventory']])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def run_command(self, host_list, module_name, module_args):

        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                # options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
                # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        return results_raw



