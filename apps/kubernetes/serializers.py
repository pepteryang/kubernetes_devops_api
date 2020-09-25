# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/7/22
# @Site : 
# @File : serializers
# @Software : PyCharm


from rest_framework import serializers
from apps.kubernetes import models


class ResourcesCategoriesInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KubernetesResourcesCategoriesInfo
        fields = '__all__'
        ordering = ('-modify_time',)


class ResourceInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KubernetesResourcesInfo
        fields = '__all__'
        ordering = ('-create_time',)


class KubernetesDeployInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KubernetesDeployInfo
        fields = '__all__'
        ordering = ('-create_time',)




