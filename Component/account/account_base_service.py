#-*-coding:utf-8-*-
# @Author : zhihui
# @Email : zhihui.he@bqrzzl.com
# @Time : 2018/6/28 14:15
# @Site : 
# @File : account_base_service.py
# @Software : PyCharm
from django.contrib.auth.hashers import make_password,check_password
from apps.account.models import KubernetesSystemUser, UserRole, Role
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from Component.common.base_service import BaseService
from Component.common.SystemLog import system_log
from apps.account.auths import Auth
import jwt, datetime, time

class AccountBaseService(BaseService):
    """
    账户
    """

    @classmethod
    def     add_user(cls, request_data_dict):
        """
        用户注册
        :param request_data_dict:
        :return:
        """
        password = make_password(request_data_dict["password"])
        request_data_dict["password"] = password
        user_obj = KubernetesSystemUser.objects.filter(username=request_data_dict["username"]).first()
        if user_obj:
            return "用户名已存在"
        new_user = KubernetesSystemUser.objects.create(**request_data_dict)
        new_user.save()
        if new_user:
            return request_data_dict["username"]
        else:
            return "创建失败"

    @classmethod
    def login_user(cls, request, username, password):
        """
        用户登录
        :param request_data_dict:
        :return:
        """
        user_obj = Auth()
        user_token = user_obj.authenticate(request, username=username, password=password)
        if user_token:
            return user_token[0]
        else:
            return False


    @classmethod
    def get_user_by_username(cls, username):
        """
        获取用户信息
        :param username:
        :return:
        """
        result = KubernetesSystemUser.objects.filter(username=username, is_deleted=False).first()
        if result:
            return result, ''
        else:
            return False, '用户不存在'

    @classmethod
    @system_log
    def get_user_role_id_list(cls, username):
        """
        获取用户角色id list
        :param username:
        :return:
        """
        user_obj = KubernetesSystemUser.objects.filter(username=username, is_deleted=0).first()
        if not user_obj:
            return False, '用户信息不存在'

        user_role_queryset = UserRole.objects.filter(user_id=user_obj.id, is_deleted=0).all()
        user_role_id_list = [user_role.id for user_role in user_role_queryset]
        return user_role_id_list, ''

    @classmethod
    @system_log
    def get_role_by_id(cls, role_id):
        """
        获取角色信息
        :param role_id:
        :return:
        """
        return Role.objects.filter(id=role_id, is_deleted=False).first(), ''

    @classmethod
    @system_log
    def get_role_username_list(cls, role_id):
        """
        获取角色对应的username_list
        :param role_id:
        :return:
        """
        user_role_queryset = UserRole.objects.filter(role_id=role_id).all()
        user_id_list = []
        for user_role in user_role_queryset:
            user_id_list.append(user_role.user_id)
        if not user_id_list:
            return [], ''
        username_queryset = KubernetesSystemUser.objects.filter(id__in=(user_id_list)).all()
        username_list = []
        for username in username_queryset:
            username_list.append(username)
        return username_list, ''





