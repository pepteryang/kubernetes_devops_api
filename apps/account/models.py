#-*- coding:utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group
import uuid


class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        """
            Creates and saves a User with the given email, date of
            birth and password.
            """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class KubernetesSystemUser(AbstractUser):
    # AbstractUser,AbstractBaseUser
    """
    用户
    1. AbstractBaseUser已经有password, last_login,所以密码这些就不用费心了
    2. 由于get_username用到了self.USERNAME_FIELD,所以需要指明哪个字段为用户名
    3. get_short_name,get_full_name需要实现,否则会抛异常
    4. 其他就按照自己的业务来写即可
    """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    username = models.CharField(u'用户名', max_length=50, unique=True)
    alias = models.CharField(u'姓名', max_length=50, default='')
    email = models.EmailField(u'邮箱', max_length=255)
    phone = models.CharField(u'电话', max_length=13, default='')
    is_admin = models.BooleanField(u'超级管理员', default=False)
    creator = models.CharField(u'创建人', max_length=50)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    modify_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)
    is_active = models.BooleanField(u'已激活', default=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'  # 必须有一个唯一标识--USERNAME_FIELD
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # 创建superuser时的必须字段

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    # '''用户是否有权限看到app'''
    #     # def has_module_perms(self, app_label):
    #     #     return True
    #
    #     # def is_authenticated(self):
    #     #     """
    #     #     Always return True. This is a way to tell if the user has been
    #     #     authenticated in templates.
    #     #     """
    #     #     return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = "tb_KubernetesSystemUser"
        ordering = ('-create_time',)

class AppToken(models.Model):
    """
    App token,用于api调用方授权
    """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    app_name = models.CharField(u'应用名称', unique=True, max_length=50)
    token = models.CharField(u'签名令牌', max_length=128, help_text='后端自动生成')
    creator = models.CharField('创建人', max_length=50)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '调用token'
        verbose_name_plural = '调用token'
        db_table = "tb_AppToken"


class Menu(models.Model):
    """
    菜单
    """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    path = models.CharField(u'索引', max_length=64, unique=True)
    label = models.CharField(u'菜单名称', max_length=64)
    icon = models.CharField(u'图标', max_length=64)
    parent_name = models.CharField(u'父菜单名称', max_length=128, blank=True, default=None)
    order_number = models.CharField(u'按钮排序', max_length=32)
    componentPath = models.CharField(u'模板路径', max_length=128, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = "tb_menu"
        verbose_name = "菜单"
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


class Role(models.Model):
    """
    角色
    """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(u'名称', unique=True, blank=False, null=False, max_length=150)
    menus = models.ManyToManyField(Menu, through='MenuRole')
    users = models.ManyToManyField(KubernetesSystemUser, through='UserRole')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'
        db_table = "tb_Role"
        ordering = ('-create_time',)


# class UserGroup(models.Model):
#     group_name = models.CharField(u'用户组名称', unique=True, max_length=150)
#     create_time = models.DateTimeField('创建时间', auto_now_add=True)
#
#     class Meta:
#         db_table = "tb_UserGroup"
#         verbose_name = "用户组名称"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.group_name


class UserRole(models.Model):
    """
    用户关联角色
    """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    roles_id = models.ForeignKey(Role, related_name='userRole_to_roleId', to_field='id',
                                 max_length=64,
                                 on_delete=models.CASCADE, default="")
    user_id = models.ForeignKey(KubernetesSystemUser, related_name='userRole_to_userId', to_field='id',
                                max_length=64,
                                on_delete=models.CASCADE, default="")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'
        db_table = "tb_UserRole"
        ordering = ('-create_time',)


class MenuRole(models.Model):
    """
    角色和菜单关联
    """
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    role_id = models.ForeignKey(Role, related_name='menuRole_to_roleId', max_length=64,
                                to_field='id', on_delete=models.CASCADE, default="")
    menu_id = models.ForeignKey(Menu, related_name='menuRole_to_menuId', to_field='id',
                                max_length=64,
                                on_delete=models.CASCADE, default="")
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '角色和菜单关联'
        verbose_name_plural = '角色和菜单关联'
        db_table = "tb_MenuRole"
        ordering = ('-create_time',)

# class RolePermission(models.Model):
#   """
#   权限表
#   """
#   title = models.CharField(verbose_name='标题', max_length=32)
#   url = models.CharField(verbose_name='含正则的URL', max_length=128)
#   pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', related_name='ps', null=True, blank=True,
#               limit_choices_to={'menu__isnull': False})
#   menu = models.ForeignKey(verbose_name='菜单', to='Menu', null=True, blank=True, help_text='null表示非菜单')
#
#   def __str__(self):
#     return self.title