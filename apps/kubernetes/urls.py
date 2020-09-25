#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time :     Created on 七月-12-19 11:45
# @Version :  1.0
# @File :     urels.py
# @author:    Zhiqun.yang
# @Email :    zhiqun.yang@bqrzzl.com
# @License :  (C)Copyright 2019-2020, DevopsGroup-NLPR-CASIA
 @Software :  vscode
'''

from apps.kubernetes import views
from rest_framework.routers import DefaultRouter
from apps.kubernetes.viewsss import harbor, kubernetesCategories, kubernetesResources, jenkinsOperation, \
    kubernetesGetClusterInfo, kubernetesDeployService
from django.urls import path

urlpatterns = [
    # 获取Jenkins中的JOBS列表
    path('jenkins/getJenkinsAllJobs/', jenkinsOperation.GetJenkinsAllJobs.as_view()),
    # 获取Jenkins中的视图列表
    path('jenkins/getJenkinsAllViews/', jenkinsOperation.GetJenkinsAllViews.as_view()),
    # 获取Jenkins中Job的详细信息
    path('jenkins/getJenkinsJobInfo/', jenkinsOperation.GetJenkinsJobInfo.as_view()),
    # 获取Jenkins中Job的详细信息
    path('jenkins/getJenkinsBuildJob/', jenkinsOperation.GetJenkinsBuildJob.as_view()),
    # 获取Jenkins中Job的详细信息
    path('jenkins/getJenkinsBuildInfo/', jenkinsOperation.GetJenkinsBuildInfo.as_view()),
    # 获取Jenkins中Job的详细信息
    path('jenkins/getJenkinsBuildConsoleOutput/', jenkinsOperation.GetJenkinsBuildConsoleOutput.as_view()),

    # 获取Harbor中的项目列表
    path('harbor/listProject/', harbor.HarborListProjectView.as_view()),
    # 获取Harbor中的项目详情
    path('harbor/detailProject/', harbor.HarborDetailProjectView.as_view()),
    # 获取Harbor中的项目标签中的详情
    path('harbor/tagInfo/', harbor.HarborTagInfoView.as_view()),
    # 删除Harbor中的项目标签中的详情
    path('harbor/deleteTag/', harbor.HarborDeleteTagView.as_view()),
    # Kubernetes 资源类型和模板接口
    path('kubernetes/resourcesCategoriesInfo/', kubernetesCategories.ResourcesCategoriesInfo.as_view()),
    # Kubernetes 资源接口
    path('kubernetes/kubernetesResources/', kubernetesResources.ResourcesInfo.as_view()),

    # 获取集群中全部的Namespace
    path('kubernetes/getKubernetesNamespaces/', kubernetesGetClusterInfo.GetKubernetesNamespaces.as_view()),
    # 获取集群Namespace中的PODS
    path('kubernetes/getPodsInKubernetesNamespaces/', kubernetesGetClusterInfo.GetPodsInKubernetesNamespaces.as_view()),
    # 获取集群中的所有PODS
    path('kubernetes/getPodsForAllNamespaces/', kubernetesGetClusterInfo.GetPodsForAllNamespaces.as_view()),
    # 删除集群中的POD
    path('kubernetes/deleteNamespacePod/', kubernetesGetClusterInfo.DeleteNamespacePod.as_view()),


    # path('patchServicesInfo/', views.DeploymentServicesInfoModelView.as_view()),
    # path('deployImagesList/', views.DeployImagesInformationView),
    # path('deployServiceInfo/', views.DeployServiceInfoView.as_view()),
    # path('otherServicesInfo/', views.OtherServicesInfoModelView.as_view()),
    # path('searchApplicationServicesInfo/', views.SearchApplicationServicesInfoView.as_view()),
    # path('listDeploySystemServices/', views.ListDeploySystemServicesInfoView.as_view()),
    # path('deploySystemServiceInfoView/', views.DeploySystemServiceInfoView.as_view()),
    # 部署kubernetes服务器接口
    path('kubernetes/DeployKubernetesServices/', kubernetesDeployService.KubernetesDeployServiceInfoView.as_view()),

]  # 路由列表
router = DefaultRouter()  # 可以处理视图的路由器
# router.register(r'ResourceInfo', views.ResourceInfoView, base_name='ResourceInfo')  # 向路由器中注册视图集
# router.register(r'KubernetesProjectList', views.KubernetesProjectListView, base_name='KubernetesProjectList')  # 向路由器中注册视图集
# router.register(r'KubernetesComponentList', views.KubernetesComponentInfoView, base_name='KubernetesComponentList')  # 向路由器中注册视图集
# router.register(r'ResourcesCategoriesList', views.ResourcesCategoriesList, base_name='ResourcesCategoriesList')  # 向路由器中注册视图集
# router.register(r'ListApplicationServices', views.ApplicationServicesInfoModelList, base_name='ApplicationServicesInfoModelList')  # 向路由器中注册视图集
# router.register(r'ListSystemServices', views.KubernetesSystemServicesList, base_name='KubernetesSystemServicesList')  # 向路由器中注册视图集

urlpatterns += router.urls  # 将路由器中的所有路由信息追加到Django的路由列表中
