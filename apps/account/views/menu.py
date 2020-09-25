# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/11/27
# @Site :
# @File : IDC
# @Software : PyCharm
# Create your views here.

from django.http import JsonResponse
from rest_framework.views import APIView
from apps.account import models
from apps.account import serializers
from Component.common.assembly import UsersPagination
from rest_framework.response import Response


class SystemMenuManager(APIView):
    """
        系统按钮管理接口
    """
    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件
        page_size = request.query_params.get('page_size', None)
        queryset = models.Menu.objects.all()
        if queryset and page_size:
            pg = UsersPagination()
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = serializers.AccountMenuListSerializer(instance=page_roles, many=True)
            return pg.get_paginated_response(serializer.data)
        elif queryset:
            serializer = serializers.AccountMenuListSerializer(instance=queryset, many=True)
            data = {
                "data": serializer.data,
                "code": 66666,
                "message": "数据获取成功"
            }
            return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": "数据列表为空，请添加后查询"
            }
            return JsonResponse(data)

    def post(self, request):
        verify_data = serializers.AccountMenuListSerializer(data=request.data)
        if verify_data.is_valid():
            verify_data.save()
            data = {
                "data": verify_data.data,
                "code": 66666,
                "message": "数据保存成功"
            }
            return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": verify_data.errors
            }
            return JsonResponse(data)

    def patch(self, request):
        """
        分为两种情况，
        1、更新是父级菜单，那么需要同步更新其他子菜单的标签，因为这里我没有使用外键关联，后续如果有时间更新，我在修改
        2、更新的不是父级菜单，那么就直接更新
        :param request:
        :return:
        """
        pk = request.data.get('uuid')
        label_value = request.data.get('label', None)
        if pk:
            if label_value:
                queryset = models.Menu.objects.filter(id=pk).first()
                queryset_item = models.Menu.objects.filter(parent_name=queryset)
                for item in queryset_item:
                    models.Menu.objects.filter(label=item).update(parent_name=label_value)
                serializer = serializers.AccountMenuListSerializer(queryset, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.validated_data,
                        "code": 66666,
                        "message": "数据更新成功！"
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        "message": serializer.errors,
                        "code": 60000,
                    }
                    return JsonResponse(data)
            else:
                queryset = models.Menu.objects.filter(id=pk).first()
                serializer = serializers.AccountMenuListSerializer(queryset, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.validated_data,
                        "code": 66666,
                        "message": "数据更新成功！"
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        "message": serializer.errors,
                        "code": 60000,
                    }
                    return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": "没有可用的按钮ID，请核对数据！"
            }
            return JsonResponse(data)


    def delete(self, request):
        pk = request.data.get('uuid', None)
        if pk:
            models.Menu.objects.filter(id=pk).delete()
            data = {
                "status": 200,
                "code": 66666,
                "message": "数据删除成功"
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 200,
                "code": 6000,
                "message": "数据不存在，请核实后操作！"
            }
            return JsonResponse(data)


class TreeSystemMenuList(APIView):
    def get(self, request):
        ret = []
        queryset = list(models.Menu.objects.values(
            'label', 'parent_name', 'id'))

        # 取出一二级菜单
        for item in queryset:
            if item['parent_name']:
                pass
            else:
                children = list(models.Menu.objects.values(
                    'label', 'parent_name', 'id').filter(parent_name=item['label']))
                item['children'] = children
                ret.append(item)

        # 取出三级菜单
        for item in ret:
            if item['children']:
                for i in range(len(item['children'])):
                    subs = list(models.Menu.objects.values(
                        'label', 'parent_name', 'id').filter(parent_name=item['children'][i]['label']))
                    if subs:
                        item['children'][i]['children'] = subs

        # 处理系统首页的特殊情况
        for item in ret:
            if item['label'] == '系统首页':
                item.pop('children')

        data = {
            "data": ret,
            "code": 66666,
            "message": "数据获取成功"
        }
        return JsonResponse(data)
