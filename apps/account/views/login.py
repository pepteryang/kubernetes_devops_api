# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/12/16
# @Site : 
# @File : roles
# @Software : PyCharm

from django.http import JsonResponse
from rest_framework.views import APIView
from apps.account import models
from rest_framework_jwt.utils import jwt_decode_handler


class UserRolesInfo(APIView):
    """
        用户权限列表
    """
    def post(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件

        # 获取所有数据
        token = request.data.get('token', None)
        if token:
            # 通过JWT的解密拿到用户ID
            toke_user = jwt_decode_handler(token)
            user_id = toke_user["user_id"]
            # 获得一个UserRole的OBJECT对象
            role_id = list(models.UserRole.objects.filter(user_id_id=user_id).values('roles_id'))[0]["roles_id"].hex
            #  通过外键查询用户拥有的全部权限ID
            menu = models.Role.objects.get(id=role_id)
            queryset = menu.menus.all().values(
                'label', 'icon', 'parent_name', 'path', 'order_number', 'componentPath', 'id')
            # print(m)
            # 获得Role ID
            # for role in roles:
            # queryset = list(models.Menu.objects.values(
            #     'label', 'icon', 'parent_name', 'path', 'order_number', 'componentPath', 'hidden', 'id').filter(id__in)

            roles =  []

            # 取出一二级菜单
            for item in queryset:
                if item['parent_name']:
                    pass
                else:
                    children = list(models.Menu.objects.values(
                        'label', 'icon', 'parent_name', 'path', 'order_number', 'componentPath', 'id'
                    ).filter(parent_name=item['label']))
                    item['children'] = children
                    roles.append(item)

            # 取出三级菜单
            for item in roles:
                if item['children']:
                    for i in range(len(item['children'])):
                        subs = list(models.Menu.objects.values(
                            'label', 'icon', 'parent_name', 'path', 'order_number', 'componentPath', 'id'
                        ).filter(parent_name=item['children'][i]['label']))
                        if subs:
                            item['children'][i]['children'] = subs

            # 处理系统首页的特殊情况
            for item in roles:
                if item['label'] == '系统首页':
                    item.pop('children')
            data = {
                "authenticated": True,
                "message": 'ok',
                "code": 6666,
                "roles": roles
            }
            return JsonResponse(data)

