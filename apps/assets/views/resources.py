# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/12/20
# @Site : 
# @File : resources
# @Software : PyCharm

from django.http import JsonResponse
from rest_framework.views import APIView
from apps.assets import models
from apps.assets import serializers
from Component.common.assembly import UsersPagination


class AssetsOtherResource(APIView):
    """
        Kubernetes其他资源管理
    """
    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件
        page_size = request.query_params.get('page_size', None)
        resource_type = request.query_params.get('type', None)
        
        if resource_type:
            queryset = models.OtherResourceInfo.objects.all().filter(type=resource_type)
            serializer = serializers.AssetsOtherResourceManagementSerializer(instance=queryset, many=True)
            data = {
                "data": serializer.data,
                "code": 66666,
                "message": "数据获取成功"
            }
            return JsonResponse(data)

        elif page_size:
            pg = UsersPagination()
            queryset = models.OtherResourceInfo.objects.all()
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = serializers.AssetsOtherResourceManagementSerializer(instance=page_roles, many=True)
            return pg.get_paginated_response(serializer.data)
        else:
            data = {
                "code": 60000,
                "message": "没有相关数据，请添加后查询！"
            }
            return JsonResponse(data)

    def post(self, request):
        verify_data = serializers.AssetsOtherResourceManagementSerializer(data=request.data)
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
            queryset = models.OtherResourceInfo.objects.filter(id=pk).first()
            serializer = serializers.AssetsOtherResourceManagementSerializer(queryset, data=request.data, partial=True)
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
                    "message": "数据保存成功"
                }
                return JsonResponse(data)

    def delete(self, request):
        data = request.data
        try:
            models.OtherResourceInfo.objects.filter(id=data.get('uuid')).delete()
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
