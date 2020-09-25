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


class AssetsProjectInfo(APIView):
    """
        项目管理
    """
    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件
        page_size = request.query_params.get('page_size', None)
        pk = request.query_params.get("uuid", None)
        queryset = models.Project.objects.all()
        if queryset and page_size:
            pg = UsersPagination()
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = serializers.AssetsProjectManagementSerializer(instance=page_roles, many=True)
            return pg.get_paginated_response(serializer.data)
        elif pk:
            queryset = models.Project.objects.filter(id=pk)
            serializer = serializers.AssetsProjectManagementSerializer(instance=queryset, many=True)
            data = {
                "data": serializer.data,
                "code": 66666,
                "message": "数据获取成功"
            }
            return JsonResponse(data)
        elif queryset:
            serializer = serializers.AssetsProjectManagementSerializer(instance=queryset, many=True)
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
        verify_data = serializers.AssetsProjectManagementSerializer(data=request.data)
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
            queryset = models.Project.objects.filter(id=pk).first()
            serializer = serializers.AssetsProjectManagementSerializer(queryset, data=request.data, partial=True)
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
        print(request.data)
        try:
            models.Project.objects.filter(id=request.data.get('uuid')).delete()
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
