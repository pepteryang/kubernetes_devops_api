# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/8/19
# @Site : 
# @File : serializers
# @Software : PyCharm


from rest_framework import serializers
from apps.account import models


class AccountMenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = '__all__'


class SystemKubernetesSystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KubernetesSystemUser
        fields = '__all__'


class SystemRolesManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class SystemRoleMenuManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuRole
        fields = '__all__'


class SystemUserRoleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserRole
        fields = '__all__'
