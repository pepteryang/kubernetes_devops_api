from django.db import models
import uuid
from apps.assets.models import Project, OtherResourceInfo, ProjectModule
# Create your models here.


class KubernetesResourcesCategoriesInfo(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    resources_name = models.CharField(unique=True, max_length=200, blank=False, null=False, verbose_name="资源名称")
    resources_templates = models.CharField(max_length=5000, blank=False, null=False, verbose_name="资源类型模板")
    create_name = models.CharField(max_length=32, blank=False, null=False, verbose_name="创建人姓名")
    create_time = models.DateTimeField(max_length=32, blank=True, auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "k8s_ResourcesCategoriesInfo"
        verbose_name = "Kubernetes资源类型管理"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.resources_name


class KubernetesResourcesInfo(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    resources_name = models.CharField(max_length=128, unique=True, blank=True, null=False, verbose_name="资源名称")
    resources_type = models.ForeignKey(KubernetesResourcesCategoriesInfo,
                                       to_field='resources_name', on_delete=models.CASCADE)
    resources_content = models.CharField(max_length=5000, blank=False, null=False, verbose_name="资源类型模板")
    create_time = models.DateTimeField(max_length=32, blank=True, auto_now_add=True, verbose_name="创建时间")
    project_name = models.ForeignKey(Project, to_field='name', on_delete=models.CASCADE)
    projectModule_name = models.ForeignKey(ProjectModule, to_field='name', on_delete=models.CASCADE)
    modify_name = models.CharField(max_length=32, blank=True, null=True, verbose_name="修改人姓名")
    create_name = models.CharField(max_length=32, blank=False, null=False, verbose_name="创建人姓名")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_system = models.CharField(choices=(('101', u'容器系统服务'), ('102', u'容器程序服务')),
                                 max_length=12,
                                 default=102,
                                 verbose_name="资源类型")

    class Meta:
        ordering = ['-create_time']
        db_table = "k8s_ResourcesInfo"
        verbose_name = "k8s服务资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.resources_name


class KubernetesDeployInfo(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False,)
    kubernetes_cluster = models.CharField(max_length=200, blank=False, null=False, verbose_name="Kubernetes集群")
    kubernetes_namespace = models.CharField(max_length=200, blank=False, null=False, verbose_name="kubernetes命名空间")
    project_name = models.CharField(max_length=32, blank=False, null=False, verbose_name="项目名称")
    project_models = models.CharField(max_length=32, blank=False, null=False, verbose_name="项目组件名称")
    deploy_name = models.CharField(max_length=32, blank=False, null=False, verbose_name="项目部署人员")
    create_time = models.DateTimeField(max_length=32, blank=True, auto_now_add=True, verbose_name="部署时间")
    deploy_message = models.CharField(max_length=10000, blank=False, null=False, verbose_name="部署返回的消息")
    deploy_content = models.CharField(max_length=5000, blank=False, null=False, verbose_name="部署的内容")
    image_url = models.CharField(max_length=256, blank=True, verbose_name="部署的镜像地址")
    resources_type = models.CharField(max_length=256, blank=True, verbose_name="部署的资源类型")

    class Meta:
        db_table = "k8s_DeployInfo"
        verbose_name = "kubernetes 发布管理"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
