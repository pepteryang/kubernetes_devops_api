# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/11/20
# @Site : 
# @File : permissions
# @Software : PyCharm


from rest_framework import permissions # 导入基础的权限类


class MyPermission(permissions.BasePermission):
    """
    必备的属性和方法，基本固定的逻辑
    """
    message = "普通用户无权访问的数据"

    def has_permission(self, request, view):
        """
        注意：
        源码中初始化时的顺序是认证在前，权限在后，所以只要认证通过
        我们这里就可以使用request.user拿到用户信息，request.auth拿到用户对象
        """
        # 获取认证控制的返回值
        user_obj = request.auth
        if user_obj.is_admin == 1:
              # 普通用户
            return False
          # 管理员
        return True

   # 是否可以访问视图， view表示当前视图对象
    def has_object_permission(self, request, view):
        """
        :param request:
        :param view:
        :return:
        """
        if request.method in permissions.SAFE_METHODS:
            return True
