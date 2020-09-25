# # Create your views here.
#
#
# from rest_framework import viewsets, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from apps.kubernetes import models
# from apps.kubernetes import serializers
# from django.http.response import JsonResponse
# from Component.kubernetes.harborapi import HarborApi
# from Component.kubernetes.kube import KubernetesApi
# from Component.common.assembly import UsersPagination
# import json
#
#
#
# # class ResourceInfoView(viewsets.ModelViewSet):
# #     """
# #     queryset:   指明该视图集在查询数据时使用的查询集
# #     serializer_class:   指明该视图在记性序列化或者反序列化时使用的序列化器
# #     """
# #     # permission_classes = (permissions.IsAuthenticated,)
# #     pagination_class = UsersPagination
# #     queryset = models.KubernetesResourceInfo.objects.all()
# #     serializer_class = serializers.ResourceInfoModelSerializer
# #
# #     def get_queryset(self):
# #         resource_type = self.request.query_params.get("type", None)
# # #         if resource_type:
# # #             return models.KubernetesResourceInfo.objects.filter(type=resource_type)
# # #         return models.KubernetesResourceInfo.objects.all()
# #
# #     def patch(self, request):
# #         pk = request.data.get("id", None)
# #         if pk:
# #             queryset = models.KubernetesResourceInfo.objects.filter(id=pk).first()
# #             serializer = serializers.ResourceInfoModelSerializer(queryset, data=request.data, partial=True)
# #             if serializer.is_valid():
# #                 serializer.save()
# #                 return Response(serializer.validated_data)
# #             else:
# #                 return Response(serializer.errors)
# #         else:
# #             return JsonResponse({"message": "没有获取到数据ID，不能更新数据"})
#
#
# class KubernetesProjectListView(viewsets.ModelViewSet):
#     """
#     queryset:   指明该视图集在查询数据时使用的查询集
#     serializer_class:   指明该视图在记性序列化或者反序列化时使用的序列化器
#     """
#     # permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = UsersPagination
#     queryset = models.KubernetesProjectInfo.objects.all()
#     serializer_class = serializers.ProjectInfoModelSerializer
#
#     def get_queryset(self):
#         kubernetes_cluster = self.request.query_params.get("kubernetes_cluster", None)
#         if kubernetes_cluster:
#             return models.KubernetesProjectInfo.objects.filter(kubernetes_cluster=kubernetes_cluster)
#         return models.KubernetesProjectInfo.objects.all()
#
#     def patch(self, request):
#         pk = request.data.get("id", None)
#         if pk:
#             queryset = models.KubernetesProjectInfo.objects.filter(id=pk).first()
#             serializer = serializers.ProjectInfoModelSerializer(queryset, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.validated_data)
#             else:
#                 return Response(serializer.errors)
#         else:
#             return JsonResponse({"message": "没有获取到数据ID，不能更新数据"})
#
#
# class KubernetesComponentInfoView(viewsets.ModelViewSet):
#     """
#     queryset:   指明该视图集在查询数据时使用的查询集
#     serializer_class:   指明该视图在记性序列化或者反序列化时使用的序列化器
#     """
#     # permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = UsersPagination
#     queryset = models.KubernetesComponentInfo.objects.all()
#     serializer_class = serializers.ComponentInfoModelSerializer
#
#     def get_queryset(self):
#         project_name = self.request.query_params.get("project_name", None)
#         kubernetes_cluster = self.request.query_params.get("kubernetes_cluster", None)
#         if project_name and kubernetes_cluster:
#             return models.KubernetesComponentInfo.objects.filter(
#                 kubernetes_cluster=kubernetes_cluster).filter(
#                 project_name=project_name)
#         elif project_name:
#             return models.KubernetesComponentInfo.objects.filter(project_name=project_name)
#         elif kubernetes_cluster:
#             return models.KubernetesComponentInfo.objects.filter(kubernetes_cluster=kubernetes_cluster)
#         else:
#             return models.KubernetesComponentInfo.objects.all()
#
#     def patch(self, request):
#         pk = request.data.get("id", None)
#         if pk:
#             queryset = models.KubernetesComponentInfo.objects.filter(id=pk).first()
#             serializer = serializers.ComponentInfoModelSerializer(queryset, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.validated_data)
#             else:
#                 return Response(serializer.errors)
#         else:
#             return JsonResponse({"message": "没有获取到数据ID，不能更新数据"})
#
#
# class ResourcesCategoriesList(viewsets.ModelViewSet):
#     """
#         Kubernetes 资源选项控制
#        queryset:   指明该视图集在查询数据时使用的查询集
#        serializer_class:   指明该视图在记性序列化或者反序列化时使用的序列化器
#        """
#     # permission_classes = (permissions.IsAuthenticated,)
#     queryset = models.KubernetesResourcesCategoriesInfo.objects.all()
#     serializer_class = serializers.ResourcesCategoriesInfoSerializer
#
#     def get_queryset(self):
#         is_system = self.request.query_params.get("is_system", None)
#         if is_system:
#             return models.KubernetesResourcesCategoriesInfo.objects.filter(is_system=is_system)
#         return models.KubernetesResourcesCategoriesInfo.objects.all()
#
#
# class ApplicationServicesInfoModelList(viewsets.ModelViewSet):
#     """
#         非系统应用的的服务信息
#         Kubernetes 资源选项控制
#        queryset:   指明该视图集在查询数据时使用的查询集
#        serializer_class:   指明该视图在记性序列化或者反序列化时使用的序列化器
#        """
#
#     # permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = UsersPagination
#     queryset = models.KubernetesApplicationServicesInfo.objects.all()
#     serializer_class = serializers.ApplicationServicesInfoModelSerializer
#
#     def get_queryset(self):
#         project_name = self.request.query_params.get("project_name", None)
#         component_name = self.request.query_params.get("component_name", None)
#         resources_model = self.request.query_params.get("resources_model", None)
#         if project_name and component_name and resources_model:
#             return models.KubernetesApplicationServicesInfo.objects.filter(project_name=project_name,
#                                                                  component_name=component_name,
#                                                                  resources_model=resources_model)
#         return models.KubernetesApplicationServicesInfo.objects.all()
#
#     def patch(self, request):
#         pk = request.data.get("id", None)
#         if pk:
#             queryset = models.KubernetesApplicationServicesInfo.objects.filter(id=pk).first()
#             serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.validated_data)
#             else:
#                 return Response(serializer.errors)
#         else:
#             return JsonResponse({"message": "没有获取到数据ID，不能更新数据"})
#
#
# class KubernetesSystemServicesList(viewsets.ModelViewSet):
#     """
#        queryset:   指明该视图集在查询数据时使用的查询集
#        serializer_class:   指明该视图在记性序列化或者反序列化时使用的序列化器
#        管理用系统服务器列表，提供禁用和开启服务
#        """
#     # permission_classes = (permissions.IsAuthenticated,)
#     pagination_class = UsersPagination
#     queryset = models.KubernetesSystemServicesInfo.objects.all()
#     serializer_class = serializers.KubernetesSystemServicesInfoModelSerializer
#
#     def get_queryset(self):
#         resources_model = self.request.query_params.get("resources_model", None)
#         kubernetes_cluster = self.request.query_params.get("kubernetes_cluster", None)
#         if resources_model and kubernetes_cluster:
#             return models.KubernetesSystemServicesInfo.objects.filter(
#                 kubernetes_cluster=kubernetes_cluster).filter(
#                 resources_model=resources_model)
#         elif kubernetes_cluster:
#             return models.KubernetesSystemServicesInfo.objects.filter(
#                 kubernetes_cluster=kubernetes_cluster)
#         else:
#             return models.KubernetesSystemServicesInfo.objects.all()
#
#     def patch(self, request):
#         pk = request.data.get("id", None)
#         print(pk)
#         print(request.data)
#         if pk:
#             queryset = models.KubernetesSystemServicesInfo.objects.filter(id=pk).first()
#             serializer = serializers.KubernetesSystemServicesInfoModelSerializer(
#                 queryset, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.validated_data)
#             else:
#                 return Response(serializer.errors)
#         else:
#             return JsonResponse({"message": "没有获取到数据ID，不能更新数据"})
#
#
# class ListDeploySystemServicesInfoView(APIView):
#     """
#     部署时使用的列表，排除系统已经禁用的项目
#     """
#     def post(self, request):
#         kubernetes_cluster = request.data.get('kubernetes_cluster', None)
#         resources_model = request.data.get('resources_model', None)
#         if kubernetes_cluster and resources_model:
#             try:
#                 queryset = models.KubernetesSystemServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster).filter(
#                     resources_model=resources_model).exclude(is_active=1)
#                 serializer = serializers.KubernetesSystemServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#         elif kubernetes_cluster:
#             try:
#                 queryset = models.KubernetesSystemServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster).exclude(is_active=1)
#                 serializer = serializers.KubernetesSystemServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#         else:
#             try:
#                 queryset = models.KubernetesSystemServicesInfo.objects.exclude(is_active=1)
#                 serializer = serializers.KubernetesSystemServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#
# class DeploymentServicesInfoModelView(APIView):
#     # 部署服务类型为:Deployment
#     def get(self, request):
#         kubernetes_cluster = request.data.get('kubernetes_cluster', None)
#         if kubernetes_cluster:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster).filter(
#                     resources_model='Deployment').exclude(is_active=1)
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#         else:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.filter(
#                     resources_model='Deployment').exclude(is_active=1)
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#     def patch(self, request):
#         data = request.data
#         queryset = models.KubernetesApplicationServicesInfo.objects.filter(id=data.get('id')).first()
#         serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.validated_data)
#         else:
#             return Response(serializer.errors)
#
#
# class OtherServicesInfoModelView(APIView):
#     # 部署服务类型不为:Deployment
#     def get(self, request):
#         queryset = models.KubernetesApplicationServicesInfo.objects.exclude(is_active=1).exclude(resources_model='Deployment')
#         serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def patch(self, request):
#         data = request.data
#         queryset = models.KubernetesApplicationServicesInfo.objects.filter(id=data.get('id')).first()
#         serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.validated_data)
#         else:
#             return Response(serializer.errors)
#
#
# class SearchApplicationServicesInfoView(APIView):
#     """
#         搜索非Kubernetes系统服务
#     """
#     def post(self, request):
#         kubernetes_cluster = request.data.get('kubernetes_cluster', None)
#         project_name = request.data.get('project_name', None)
#         component_name = request.data.get('component_name', None)
#         resources_model = request.data.get('resources_model', None)
#         if resources_model and kubernetes_cluster and project_name and component_name:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster).filter(
#                     project_name=project_name).filter(
#                     component_name=component_name).filter(
#                     resources_model=resources_model)
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#         elif kubernetes_cluster and project_name and component_name:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster).filter(
#                     project_name=project_name).filter(
#                     component_name=component_name)
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#         elif kubernetes_cluster and project_name:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster).filter(
#                     project_name=project_name)
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#         elif kubernetes_cluster:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.filter(
#                     kubernetes_cluster=kubernetes_cluster)
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#         else:
#             try:
#                 queryset = models.KubernetesApplicationServicesInfo.objects.all()
#                 serializer = serializers.ApplicationServicesInfoModelSerializer(queryset, many=True)
#                 return Response(serializer.data)
#             except Exception as e:
#                 return Response(e)
#
#
# def DeployImagesInformationView(request):
#     harbor_name = request.GET.get('harborName')
#     project_name = request.GET.get('project_name')
#     component_name = request.GET.get('component_name')
#     info = models.KubernetesResourceInfo.objects.get(name=harbor_name)
#     conn = HarborApi(passwd=info.password,
#                      username=info.username,
#                      url=info.url)
#     repo_name = project_name + '/' + component_name
#     print(repo_name)
#     data = conn.tags_info(repo_name=repo_name)
#     print(data)
#     # 组装自己需要的信息
#     repo_info = []
#     if data:
#         for res in data:
#             mid = {
#                 "repo_name": repo_name,
#                 "tag_name": info.access_domain + '/' + repo_name + ':' + res['name'],
#                 "create_time": res['created'],
#             }
#             repo_info.append(mid)
#     print(repo_info)
#     return JsonResponse(repo_info, safe=False)
#
#
# class DeployServiceInfoView(APIView):
#     def get(self, request):
#         project_name = request.data.get('project_name')
#         component_name = request.data.get('component_name')
#         if project_name and component_name:
#             query_set = models.KubernetesDeployInfo.objects.all().filter(
#                 project_name=project_name).filter(component_name=component_name)[:10]
#             serializer = serializers.DeployInfoInfoModelSerializer(query_set, many=True)
#             print(serializer.data)
#             return Response(serializer.data)
#         else:
#             query_set = models.KubernetesDeployInfo.objects.all()[:10]
#             serializer = serializers.DeployInfoInfoModelSerializer(query_set, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         pk = request.data.get('id')
#         resources_model = request.data.get('resources_model')
#         kubernetes_name = request.data.get('kubernetes_name')
#         kubernetes_cluster = request.data.get('kubernetes_cluster')
#         image_name = request.data.get('image_name')
#         deploy_name = request.data.get('deploy_name')
#         # 获取Kubernetes资源信息
#         queryset_kubernetes = models.KubernetesResourceInfo.objects.values().filter(name=kubernetes_name)
#         kube_data = list(queryset_kubernetes)[0]
#         # 连接到选择的kubernetes集群
#         conn = KubernetesApi(master_host=kube_data['network'] + '://' + kube_data['url'] + ':' + str(kube_data['port']),
#                              token=kube_data['api_token'])
#         # 根据ID获取json数据
#         queryset_json_data = models.KubernetesServicesInfo.objects.values('component_name',
#                                                                           'project_name',
#                                                                           'content',
#                                                                           'is_deploy').filter(id=pk)
#         # 获取服务Json串，
#         json_data = list(queryset_json_data)[0]['content']
#         # 拼接Docker镜像地址
#         # 根据服务类型选择Api接口
#         if resources_model == 'Deployment':
#             ret = {}
#             # 替换Image中的地址
#             new_data = json_data.replace('imageur2', image_name)
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] != 1:
#                 res = conn.replace_deployment(json.loads(new_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 ret['image_url'] = image_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_deployment(json.loads(new_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 ret['image_url'] = image_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_active=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif resources_model == 'Namespace':
#             ret = {}
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] != 1:
#                 res = conn.patch_namespace(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 ret['image_url'] = image_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_namespace(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 ret['image_url'] = image_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_active=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif resources_model == 'Service':
#             ret = {}
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] == 1:
#                 res = conn.patch_service(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_services(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 ret['image_url'] = image_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_deploy=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif resources_model == 'Secret':
#             ret = {}
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] != 1:
#                 res = conn.patch_secret(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_secret(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_deploy=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif resources_model == 'ConfigMap':
#             ret = {}
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] != 1:
#                 res = conn.patch_config_map(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_config_map(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_deploy=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         elif resources_model == 'Ingress':
#             ret = {}
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] != 1:
#                 res = conn.patch_ingress(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_ingress(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['component_name'] = queryset_json_data[0]['component_name']
#                 ret['project_name'] = queryset_json_data[0]['project_name']
#                 ret['deploy_name'] = deploy_name
#                 ret['image_url'] = image_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_deploy=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return JsonResponse({"status": 400, "message": "没有你要的类型，请联系管理员"})
#
#
# class DeploySystemServiceInfoView(APIView):
#     def post(self, request):
#         pk = request.data.get('id')
#         resources_model = request.data.get('resources_model')
#         kubernetes_cluster = request.data.get('kubernetes_cluster')
#         deploy_name = request.data.get('deploy_name')
#         # 获取Kubernetes资源信息
#         queryset_kubernetes = models.KubernetesSystemServicesInfo.objects.values().filter(
#             kubernetes_cluster=kubernetes_cluster)
#         kubernetes_data = list(queryset_kubernetes)[0]
#         # 连接到选择的kubernetes集群
#         conn = KubernetesApi(master_host=kubernetes_data['network'] + '://' + kubernetes_data['url'] + ':' + str(kubernetes_data['port']),
#                              token=kubernetes_data['api_token'])
#         # 根据ID获取json数据
#         queryset_json_data = models.KubernetesSystemServicesInfo.objects.values(
#             'kubernetes_cluster',
#             'resources_model',
#             'content',
#             'is_deploy').filter(id=pk)
#         # 获取服务Json串，
#         json_data = list(queryset_json_data)[0]['content']
#         # 拼接Docker镜像地址
#         # 根据服务类型选择Api接口
#         if resources_model == 'Deployment':
#             ret = {}
#             # 构造数据，保存结果
#             if list(queryset_json_data)[0]['is_deploy'] != 1:
#                 res = conn.replace_namespace_service_account(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.DeployInfoInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 res = conn.create_namespace_service_account(json.loads(json_data))
#                 ret['message'] = res
#                 ret['resources_model'] = resources_model
#                 ret['kubernetes_cluster'] = kubernetes_cluster
#                 ret['deploy_name'] = deploy_name
#                 serializer = serializers.KubernetesSystemDeployInfoModelSerializer(data=ret)
#                 if serializer.is_valid():
#                     serializer.save()
#                     models.KubernetesServicesInfo.objects.filter(id=pk).update(is_active=0)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# def HarborListProjectView(request):
#     if request.method == 'GET':
#         pk = request.GET.get('pk')
#         info = models.KubernetesResourceInfo.objects.get(id=pk)
#         data = HarborApi(passwd=info.password,
#                          username=info.username,
#                          url=info.url).list_projects()
#         # #组装自己需要的信息
#         project_info = []
#         if data:
#             for res in data:
#                 mid = {
#                     "project_id": res["project_id"],
#                     "project_name": res["name"],
#                     }
#                 project_info.append(mid)
#         return JsonResponse(project_info, safe=False)
#
#
# def HarborDetailProjectView(request):
#     if request.method == 'GET':
#         pk = request.GET.get('pk')
#         project_id = request.GET.get('project_id')
#         info = models.KubernetesResourceInfo.objects.get(id=pk)
#         data = HarborApi(passwd=info.password,
#                          username=info.username,
#                          url=info.url).detail_project(project_id=project_id)
#         print(data)
#         # 组装自己需要的信息
#         project_info = []
#         if data:
#             for res in data:
#                 mid = {
#                     "project_id": res["project_id"],
#                     "repo_name": res["name"],
#                     }
#                 project_info.append(mid)
#         print(project_info)
#         return JsonResponse(project_info, safe=False)
#
#
# def HarborTagInfoView(request):
#     if request.method == 'GET':
#         pk = request.GET.get('pk')
#         repo_name = request.GET.get('repo_name')
#         info = models.KubernetesResourceInfo.objects.get(id=pk)
#         conn = HarborApi(passwd=info.password,
#                          username=info.username,
#                          url=info.url)
#         data = conn.tags_info(repo_name=repo_name)
#         # 组装自己需要的信息
#         repo_info = []
#         if data:
#             for res in data:
#                 mid = {
#                     "repo_name": repo_name,
#                     "tag_name": res['name'],
#                     "tag_size": res['size'],
#                     "create_time": res['created'],
#                 }
#                 repo_info.append(mid)
#         print(repo_info)
#         return JsonResponse(repo_info, safe=False)
#
#
# def HarborDeleteTagView(request):
#     if request.method == 'GET':
#         id = request.GET.get('pk')
#         repo_name = request.GET.get('repo_name')
#         tag_name = request.GET.get('tag_name')
#         info = models.KubernetesResourceInfo.objects.get(id=id)
#         data = HarborApi(passwd=info.password,
#                          username=info.username,
#                          url=info.url).del_tags(repo_name=repo_name, tag_name=tag_name)
#         print(data)
#         return JsonResponse({"message": data},safe=False )
#
#
#
#
#
