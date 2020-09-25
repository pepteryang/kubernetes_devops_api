# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2020/1/8
# @Site : 
# @File : kubernetesGetClusterInfo
# @Software : PyCharm


from Component.kubernetes.kube import KubernetesApi
from rest_framework.views import APIView
from apps.kubernetes import models
from django.http.response import JsonResponse


class GetKubernetesNamespaces(APIView):
    def post(self, request):
        kubernetes_pk = request.data.get("kubernetes_pk", None)
        queryset_kubernetes = models.OtherResourceInfo.objects.get(pk=kubernetes_pk)
        conn = KubernetesApi(master_host=queryset_kubernetes.address,
                             token=queryset_kubernetes.api_token)
        res = conn.list_namespace()
        ret = []
        # 构建数据
        for item in res["items"]:
            ret.append({"name": item["metadata"]["name"]})

        data = {
            "data": ret,
            "code": 66666,
            "message": "数据获取成功"
        }
        return JsonResponse(data)


class GetPodsInKubernetesNamespaces(APIView):
    def post(self, request):
        kubernetes_cluster = request.data.get("kubernetes_cluster", None)
        kubernetes_namespace = request.data.get("kubernetes_namespace", None)
        queryset_kubernetes = models.OtherResourceInfo.objects.get(name=kubernetes_cluster)
        conn = KubernetesApi(master_host=queryset_kubernetes.address,
                             token=queryset_kubernetes.api_token)
        # 拼接 namespace
        json_data = {
            "metadata": {
                "namespace": kubernetes_namespace,
            },
        }
        res = conn.list_namespace_pod(json_data=json_data)
        ret = []
        # 构建数据
        for item in res["items"]:
            ret.append({
                "name": item["metadata"]["name"],
                "namespace": kubernetes_namespace,
                "kind": item["metadata"]["owner_references"][0]["kind"],
                "phase": item["status"]["phase"],
                "pod_ip": item["status"]["pod_ip"],
                "node_ip": item["status"]["host_ip"],
                "start_time": item["status"]["start_time"],
            })

        data = {
            "data": ret,
            "code": 66666,
            "message": "数据获取成功"
        }
        return JsonResponse(data)


class GetPodsForAllNamespaces(APIView):
    def post(self, request):
        kubernetes_cluster = request.data.get("kubernetes_cluster", None)
        queryset_kubernetes = models.OtherResourceInfo.objects.get(name=kubernetes_cluster)
        conn = KubernetesApi(master_host=queryset_kubernetes.address,
                             token=queryset_kubernetes.api_token)

        res = conn.list_pod_for_all_namespaces()
        ret = []
        # 构建数据
        print(res["items"])
        for item in res["items"]:
            ret.append({
                "name": item["metadata"]["name"],
                "namespace": item["metadata"]["namespace"],
                "kind": item["metadata"]["owner_references"][0]["kind"],
                "pod_ip": item["status"]["pod_ip"],
                "node_ip": item["status"]["host_ip"],
                "start_time": item["status"]["start_time"],
                "phase": item["status"]["phase"],
            })

        data = {
            "data": ret,
            "code": 66666,
            "message": "数据获取成功"
        }
        return JsonResponse(data)


class DeleteNamespacePod(APIView):
    def post(self, request):
        kubernetes_cluster = request.data.get("kubernetes_cluster", None)
        namespace = request.data.get("namespace", None)
        pod_name = request.data.get("pod_name", None)
        queryset_kubernetes = models.OtherResourceInfo.objects.get(name=kubernetes_cluster)
        conn = KubernetesApi(master_host=queryset_kubernetes.address,
                             token=queryset_kubernetes.api_token)

        res = conn.delete_namespace_pod(namespace=namespace, pod_name=pod_name)
        print('kubernetes_name:-{} -namespace:{}-pod_name:{}' .format(kubernetes_cluster,namespace,pod_name))
        print(res)
        data = {
            "data": res,
            "code": 66666,
            "message": "数据获取成功"
        }
        return JsonResponse(data)

