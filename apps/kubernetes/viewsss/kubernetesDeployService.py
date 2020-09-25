# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2020/1/2
# @Site : 
# @File : kubernetesDeployService
# @Software : PyCharm

from rest_framework.views import APIView
from apps.assets.models import OtherResourceInfo
from apps.kubernetes.models import KubernetesResourcesInfo
from apps.kubernetes.serializers import KubernetesDeployInfoModelSerializer
from django.http.response import JsonResponse
from Component.kubernetes.kube import KubernetesApi
import json


class KubernetesDeployServiceInfoView(APIView):
    def post(self, request):
        kubernetes_cluster_name = request.data.get('deploy_kubernetes_cluster_name', None)
        deploy_harbor_id = request.data.get('deploy_harbor_id', None)
        deploy_resources_type = request.data.get('deploy_resources_type', None)
        image_name = request.data.get('deploy_image_name', None)
        deploy_name = request.data.get('deploy_name', None)
        resources_id = request.data.get('deploy_resources_id', None)
        deploy_project_code = request.data.get('deploy_project_code', None)
        deploy_project_module = request.data.get('deploy_project_module', None)
        deploy_namespace = request.data.get('deploy_namespace', None)

        # 获取Kubernetes资源信息
        deploy_kubernetes_info = OtherResourceInfo.objects.get(name=kubernetes_cluster_name)
        # 连接到选择的kubernetes集群
        conn = KubernetesApi(master_host=deploy_kubernetes_info.address, token=deploy_kubernetes_info.api_token)

        # 根据服务类型选择Api接口
        if deploy_resources_type == 'Deployment':
            # 获取其他资源信息
            deploy_harbor_info = OtherResourceInfo.objects.get(id=deploy_harbor_id)
            deploy_resources_info = KubernetesResourcesInfo.objects.get(id=resources_id)
            # 获取服务Json串，
            json_data = deploy_resources_info.resources_content

            # 拼接Docker镜像地址
            ret = {}
            # 替换Image中的地址
            new_data = json_data.replace(
                'kubernetes_deploy_image', image_name
            ).replace("kubernetes_deploy_namespace", deploy_namespace)
            # 构造数据，保存结果
            is_deploy = conn.get_deployment(json.loads(new_data))
            # 判断是否已经创建过，则更新，如果没有就创建它，
            if is_deploy["code"] == 60000 and is_deploy["status"] == 200:
                api_response = conn.create_deployment(json.loads(new_data))
                print(api_response)
                ret['deploy_message'] = api_response["message"]
                ret['resources_type'] = deploy_resources_type
                ret['kubernetes_cluster'] = kubernetes_cluster_name
                ret['project_models'] = deploy_project_module
                ret['project_name'] = deploy_project_code
                ret['deploy_name'] = deploy_name
                ret['image_url'] = image_name
                ret['kubernetes_namespace'] = deploy_namespace
                ret['deploy_content'] = new_data
                serializer = KubernetesDeployInfoModelSerializer(data=ret)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.data,
                        "code": 66666,
                        "message": "服务创建成功！"
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        "data": serializer.errors,
                        "code": 60000,
                        "message": "数据错误！请核对！"
                    }
                    return JsonResponse(data)

            else:
                api_response = conn.replace_deployment(json.loads(new_data))
                print(api_response)
                ret['deploy_message'] = api_response["message"]
                ret['resources_type'] = deploy_resources_type
                ret['kubernetes_cluster'] = kubernetes_cluster_name
                ret['project_models'] = deploy_project_module
                ret['project_name'] = deploy_project_code
                ret['deploy_name'] = deploy_name
                ret['image_url'] = image_name
                ret['kubernetes_namespace'] = deploy_namespace
                ret['deploy_content'] = new_data
                serializer = KubernetesDeployInfoModelSerializer(data=ret)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.data,
                        "code": 66666,
                        "message": "服务更新成功！"
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        "data": serializer.errors,
                        "code": 60000,
                        "message": "数据错误！请核对！"
                    }
                    return JsonResponse(data)
