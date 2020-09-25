# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/10/24
# @Site : 
# @File : jwt_response_payload_handler
# @Software : PyCharm

import datetime
from apps.account.models import UserRole, MenuRole, Role, Menu


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
        :token  返回的jwt
        :user   当前登录的用户信息[对象]
        :request 当前本次客户端提交过来的数据
        :role 角色
    """
    """
    自定义jwt认证成功返回数据
    """
    # 返回之前记录用户最后登陆时间,django默认只会记录登陆后台管理系统最后时间,JWT不记录
    user.last_login = str(datetime.datetime.today())
    user.save()

    if user.alias:
        name = user.alias
    else:
        name = user.username
    return {
            "name": name,
            "username": user.username,
            "token": token,
    }
