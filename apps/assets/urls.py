# from django.urls import path, include
#
# from apps.account.views import CustomAuthToken
#
#
# urlpatterns = [
#     path(r'api-token-auth/', CustomAuthToken.as_view())
# ]


from django.urls import path
from apps.assets.views import IDC, environment, host, project, database, resources, projectModule
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # CMDB 机房管理接口
    path('assetsIDCInfo/', IDC.AssetsIDCInfo.as_view()),
    # 系统部署环境
    path('assetsEnvInfo/', environment.AssetsEnvInfo.as_view()),
    # 服务器主机接口
    path('assetsHostInfo/', host.AssetsHostInfo.as_view()),
    # 项目管理
    path('assetsProjectInfo/', project.AssetsProjectInfo.as_view()),
    # 项目模块管理
    path('assetsProjectModuleInfo/', projectModule.AssetsProjectModuleInfo.as_view()),
    # 主机修改记录
    path('assetsHostRecordInfo/', host.AssetsHostRecordInfo.as_view()),
    # 数据库信息
    path('assetsDatabaseInfo/', database.AssetsDatabaseInfo.as_view()),
    # 从ANSIBLE更新主机基本信息
    path('updateHostForAnsible/', host.UpdateHostForAnsible.as_view()),
    # 从ANSIBLE更新主机基本信息
    path('exportHostData/', host.ExportHostData.as_view()),
    # 其他资源接口
    path('assetsOtherResource/', resources.AssetsOtherResource.as_view()),
]
# 路由列表
router = DefaultRouter()  # 可以处理视图的路由器
urlpatterns += router.urls  # 将路由器中的所有路由信息追加到Django的路由列表中