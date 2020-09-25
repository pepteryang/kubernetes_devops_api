# from django.urls import path, include
#
# from apps.account.views import CustomAuthToken
#
#
# urlpatterns = [
#     path(r'api-token-auth/', CustomAuthToken.as_view())
# ]


from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.routers import DefaultRouter
from apps.account.views import login, roles, user, menu, rolemenu, roleuser
urlpatterns = [
    # 系统角色管理接口
    path('systemRoleManager/', roles.SystemRoleManager.as_view()),
    # 系统用户管理接口
    path('systemUserManager/', user.SystemUserManager.as_view()),
    # 系统用户管理接口
    path('systemMenuManager/', menu.SystemMenuManager.as_view()),
    # 系统全部导航条接口
    path('treeSystemMenuList/', menu.TreeSystemMenuList.as_view()),
    # 系统角色和按钮接口
    path('systemRoleMenuManager/', rolemenu.SystemRoleMenuManager.as_view()),
    # 角色、用户管理
    path('systemRoleUserManager/', roleuser.SystemRoleUserManager.as_view()),
    # 用户权限接口
    path('userRolesInfo/', login.UserRolesInfo.as_view()),
    # 登陆接口，后续有时间要改改
    path(r'login/', obtain_jwt_token),
    path(r'logout/', refresh_jwt_token),
    path(r"refresh/", refresh_jwt_token),


] # 路由列表
router = DefaultRouter()  # 可以处理视图的路由器
urlpatterns += router.urls  # 将路由器中的所有路由信息追加到Django的路由列表中