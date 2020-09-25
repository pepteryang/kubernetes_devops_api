# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/12/31
# @Site : 
# @File : kubernetesServices
# @Software : PyCharm
"""
1、 个人想法，所有的服务命名根据环境+项目+加组件+资源类型： test_cai_sms_configMap
2、同一类型的资源可以选择部署在不同的kubernetes集群上面，也可以部署在不同的namespace 中最理想的就可以一次性部署一个项目，
属于规范的命名是不可以缺少的在数据库筛选的时候才好过滤到整个项目
3、在设计的时候，把cluster和namespace做成动态可以配置的。这些记录会保存在发布记录中，方便查询！
"""

from django.http import JsonResponse
from rest_framework.views import APIView
from apps.kubernetes import models
from apps.kubernetes import serializers
from Component.common.assembly import UsersPagination


class ResourcesInfo(APIView):
    """
        系统角色管理 机房管理
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
        resources_type = request.query_params.get("resources_model", None)
        queryset = models.KubernetesResourcesInfo.objects.all()
        if queryset and page_size:
            pg = UsersPagination()
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = serializers.ResourceInfoModelSerializer(instance=page_roles, many=True)
            return pg.get_paginated_response(serializer.data)
        elif pk:
            queryset = models.KubernetesResourcesInfo.objects.filter(id=pk)
            serializer = serializers.ResourceInfoModelSerializer(instance=queryset, many=True)
            data = {
                "data": serializer.data,
                "code": 66666,
                "message": "数据获取成功"
            }
            return JsonResponse(data)
        elif resources_type:
            queryset = models.KubernetesResourcesInfo.objects.filter(resources_type=resources_type)
            serializer = serializers.ResourceInfoModelSerializer(instance=queryset, many=True)
            data = {
                "data": serializer.data,
                "code": 66666,
                "message": "数据获取成功"
            }
            return JsonResponse(data)

        elif queryset:
            serializer = serializers.ResourceInfoModelSerializer(instance=queryset, many=True)
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
        verify_data = serializers.ResourceInfoModelSerializer(data=request.data)
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
        pk = request.data.get('uuid', None)
        if pk:
            queryset = models.KubernetesResourcesInfo.objects.filter(id=pk).first()
            serializer = serializers.ResourceInfoModelSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "code": 66666,
                    "message": "数据更新成功！"
                }
                return JsonResponse(data)
            else:
                data = {
                    "data": serializer.errors,
                    "code": 60000,
                    "message": "数据更新失败，请检查！"
                }
                return JsonResponse(data)

    def delete(self, request):
        pk = request.data.get('uuid', None)
        print(pk)
        try:
            ss = models.KubernetesResourcesInfo.objects.get(id=request.data.get('uuid')).delete()
            print(ss)
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
