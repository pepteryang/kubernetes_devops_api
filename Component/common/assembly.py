# -*- coding:utf-8-*-
# @Author : PeterYang
# @Email : snfnvtk@163.com
# @Time : 2019/8/19
# @Site : 
# @File : assembly
# @Software : PyCharm

from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict, namedtuple
from rest_framework.response import Response
import os, subprocess, getpass


class UsersPagination(PageNumberPagination):
    # 默认指定每一页的个数
    page_size = 10
    # 前端来设置page_size参数来指定每页个数
    # 默认每页显示15个，可以通过传入page=2&size=4,改变默认每页显示的个数
    page_size_query_param = 'page_size'
    # 前端设置页码的参数
    page_query_param = 'page'
    # 最大页数不超过10
    # URL中指定查多少条数据的参数
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('page_size', self.page_size),
                ('results', data)
             ])
        )


def files_is_exists(file_path):
        if not os.path.exists(file_path):
            return False
        else:
            return True


def run_system_cmd(command):
    """
    执行命令函数
    :return:
    """
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 获取执行后的标准输出和错误输出
    standard_out, standard_err = res.communicate()
    data = {
        "return_code": res.returncode,
        "standard_out": standard_out,
        "standard_err": standard_err,
        "pid": res.pid
    }
    return data


def ssh_copy_ras(password, sudo_user, host_ip, ssh_port):
    user_name = getpass.getuser()
    if user_name == 'root':
        cmd = "sshpass -p '{0}' ssh-copy-id -f -o StrictHostKeyChecking=no -p {3} -i /{4}/.ssh/id_rsa {1}@{2}".format(password,
                                                                                          sudo_user,
                                                                                          host_ip,
                                                                                          ssh_port,
                                                                                          user_name)
        res = run_system_cmd(command=cmd)
        return res

    else:
        cmd = "sshpass -p '{0}' ssh-copy-id -f -o StrictHostKeyChecking=no -p {3} -i /home/{4}/.ssh/id_rsa {1}@{2}".format(password,
                                                                                               sudo_user,
                                                                                               host_ip,
                                                                                               ssh_port,
                                                                                               user_name)
        res = run_system_cmd(command=cmd)
        return res


def run_service_user_ras_key():
    user_name = getpass.getuser()
    file_path = '/home/{0}/.ssh/id_rsa.pub'.format(user_name)
    cmd = "ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''"
    if not os.path.exists(file_path):
        run_system_cmd(command=cmd)


def ansible_is_active():
    cmd = 'ansible --version'
    res = run_system_cmd(command=cmd)
    return res
