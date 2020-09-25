# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/12/24
# @Site : 
# @File : rolemenu
# @Software : PyCharm

from django.http import JsonResponse
from rest_framework.views import APIView
from apps.account import models
from apps.account import serializers


class SystemRoleMenuManager(APIView):
    """
        角色按钮权限管理
    """
    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件
        pk = request.query_params.get('uuid')
        if pk:
            roles = models.Role.objects.get(id=pk)
            menus = list(roles.menus.all().values("id", "label"))
            if menus:
                data = {
                    "data": menus,
                    "code": 66666,
                    "message": "数据查询成功"
                }
                return JsonResponse(data)

            else:
                data = {
                    "code": 60000,
                    "message": "角色没有绑定权限"
                }
                return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": "没有找到可用的角色ID,请确认"
            }
            return JsonResponse(data)

    def patch(self, request):
        pk = request.data.get('role_id', None)
        menus_id = request.data.get('menus_id', None)
        if pk and menus_id:
            roles = models.Role.objects.get(id=pk)
            if roles:
                roles.menus.set(menus_id)
                data = {
                    "code": 66666,
                    "message": "数据更新成功"
                }
                return JsonResponse(data)
            else:
                data = {
                    "code": 60000,
                    "message": "角色ID不存才，请联系管理员！"
                }
                return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": "没有可用的角色ID，或者没有可以用于更新的菜单ID，请联系管理员！"
            }
            return JsonResponse(data)
