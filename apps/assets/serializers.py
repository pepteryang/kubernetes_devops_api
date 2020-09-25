# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/11/26
# @Site : 
# @File : serializers
# @Software : PyCharm

from rest_framework import serializers
from apps.assets import models


class AssetsIDCManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IDC
        fields = '__all__'


class AssetsEnvManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Environment
        fields = '__all__'


class AssetsProjectManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class AssetsProjectModuleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectModule
        fields = '__all__'


class AssetsHostManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = '__all__'


class AssetsDatabaseInfoManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatabaseInfo
        fields = '__all__'


class AssetsHostRecordManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HostRecord
        fields = '__all__'


class AssetsOtherResourceManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OtherResourceInfo
        fields = '__all__'


