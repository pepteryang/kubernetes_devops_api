from django.db import models

# Create your models here.
# -*- coding: UTF-8 -*-
import uuid


class IDC(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True, verbose_name=u'机房名称')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"机房"
        verbose_name_plural = verbose_name
        db_table = "tb_IDC"
        ordering = ['-create_time']


class Project(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True, verbose_name=u'项目名')
    project_code = models.CharField(max_length=60, unique=True, verbose_name=u'业务说明')
    project_leader = models.CharField(max_length=60, unique=True, verbose_name=u'业务负责人')
    description = models.TextField(blank=True, null=True, verbose_name=u'业务说明')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目名称'
        verbose_name_plural = verbose_name
        db_table = "tb_Project"
        ordering = ['-create_time']


class ProjectModule(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True, verbose_name=u'模块名称')
    project_id = models.ForeignKey(Project, max_length=64,  related_name='ProjectModule_to_ProjectId',
                                   to_field='id', on_delete=models.CASCADE, verbose_name=u'项目ID')
    project_name = models.CharField(max_length=128, verbose_name=u'项目名称')

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目模块'
        verbose_name_plural = verbose_name
        db_table = "tb_ProjectModule"
        ordering = ['-create_time']


class Environment(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True, verbose_name=u'环境名称')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"发布环境"
        verbose_name_plural = verbose_name
        db_table = "tb_dev_environment"
        ordering = ['-create_time']


class Host(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name=u"主机名")
    idc = models.CharField(max_length=100, verbose_name=u"Idc机房")
    eth1 = models.GenericIPAddressField(unique=True, verbose_name=u'内网地址1')
    remote_port = models.CharField(max_length=64, verbose_name=u'远程端口')
    mac_address = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'mac地址')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    hard_disk = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'硬盘')
    host_memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    system = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"系统类型",)
    system_cpu_arch = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"系统版本")
    cpu_info = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"cpu信息")
    purchasing = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"主机购买时间")
    expire = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"主机到期时间")
    create_time = models.DateTimeField(auto_now_add=True)
    project = models.CharField(max_length=100, verbose_name=u"项目名称")
    env = models.CharField(max_length=100, verbose_name=u"部署环境")
    root_password = models.CharField(max_length=30, verbose_name=u"user_root密码")
    operation_username = models.CharField(max_length=30, verbose_name=u"运维用户名")
    operation_password = models.CharField(max_length=30, verbose_name=u"运维密码")
    application_username = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"程序用户名")
    application_password = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"程序密码")

    def __str__(self):
        return '%s %s %s %s' % (self.eth1, self.remote_port, self.operation_username, self.operation_password)

    class Meta:
        verbose_name = u"服务器"
        verbose_name_plural = verbose_name
        db_table = "tb_Host"
        ordering = ['-create_time']


class DatabaseInfo(models.Model):
    """数据库信息"""
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    database_label = models.CharField(max_length=64, unique=True, blank=True, verbose_name=u'数据库标签')
    database_type = models.CharField(max_length=64, blank=True, verbose_name=u'数据库类型')
    database_port = models.CharField(max_length=64, blank=True, verbose_name=u'数据库端口')
    database_services_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'数据库服务名称')
    database_url = models.CharField(max_length=64, blank=True, verbose_name=u'连接串')
    database_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'数据库库名')
    database_address = models.GenericIPAddressField(max_length=100, blank=True, null=True, verbose_name=u'数据库IP地址')
    database_user = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"用户名")
    database_password = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"密码")
    project_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"所属项目")
    project_env = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"所属环境")
    database_editor = models.TextField(blank=True, null=True, verbose_name=u'备注')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.database_label

    class Meta:
        verbose_name = u"Database_Info"
        verbose_name_plural = verbose_name
        db_table = "tb_Database_Info"
        ordering = ['-create_time']


class OtherResourceInfo(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(u'资源名称', unique=True, max_length=100, blank=False, null=False)
    address = models.CharField(u'访问地址', max_length=100, blank=False, null=False)
    access_domain = models.CharField(u'访问域名', max_length=100, blank=True)
    port = models.CharField(u'访问端口', max_length=100, blank=False)
    network_protocol = models.CharField(u'网络协议', max_length=100, blank=False, null=False)
    username = models.CharField(u'认证用户', blank=True, max_length=100,)
    password = models.CharField(u'认证密码', blank=True, max_length=100,)
    type = models.CharField(u'资源类型', max_length=100, blank=False)
    api_token = models.CharField(u'认证令牌', blank=True, max_length=1000)
    env = models.CharField(u'资源环境', max_length=100, blank=False, null=False)
    description = models.TextField(u'资源描述', max_length=1000, blank=True, null=False)
    create_time = models.DateTimeField(u'创建时间', max_length=32, blank=True, auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = "tb_other_resource"
        verbose_name = "资源信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class HostRecord(models.Model):
    """ 主机修改记录model """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    host = models.GenericIPAddressField(blank=True, null=True, verbose_name=u'主机')
    user = models.CharField(max_length=30, null=True, verbose_name=u'修改用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'修改的时间')
    content = models.TextField(blank=True, null=True, verbose_name=u'修改详情')
    comment = models.TextField(blank=True, null=True, verbose_name=u'评论,保留字段')

    class Meta:
        verbose_name = u"HostRecord"
        verbose_name_plural = verbose_name
        db_table = "tb_host_record"
        ordering = ('-create_time',)


