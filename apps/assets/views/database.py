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
from apps.assets import models
from apps.assets import serializers
from Component.common.assembly import UsersPagination


class AssetsDatabaseInfo(APIView):
    """
        CMDB 主机管理
    """
    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件

        # 获取所有数据
        queryset = models.DatabaseInfo.objects.all()
        if queryset:
            # 创建分页对象，这里是自定义的UsersPagination
            pg = UsersPagination()
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = serializers.AssetsDatabaseInfoManagementSerializer(instance=page_roles, many=True)
            return pg.get_paginated_response(serializer.data)
        else:
            data = {
                "code": 60000,
                "message": '数据为空，请添加后再查询！'
            }
            return JsonResponse(data)

    def post(self, request):
        verify_data = serializers.AssetsDatabaseInfoManagementSerializer(data=request.data)
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
        pk = request.data.get('uuid')
        if pk:
            queryset = models.DatabaseInfo.objects.filter(id=pk).first()
            serializer = serializers.AssetsDatabaseInfoManagementSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.validated_data,
                    "code": 66666,
                    "message": "数据保存成功"
                }
                return JsonResponse(data)
            else:
                data = {
                    "data": serializer.errors,
                    "code": 60000,
                    "message": "数据保存错误"
                }
                return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": "没有找到可用的ID号，请确认！"
            }
            return JsonResponse(data)

    def delete(self, request):
        pk = request.data.get('uuid')
        print(pk)
        try:
            models.DatabaseInfo.objects.filter(id=pk).delete()
            data = {
                "status": 200,
                "code": 66666,
                "message": "数据删除成功"
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                "status": 200,
                "code": 6000,
                "message": e
            }
            return JsonResponse(data)
