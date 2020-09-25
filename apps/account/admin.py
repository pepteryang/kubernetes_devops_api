#-*-coding:utf-8-*-

from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from apps.account.models import KubernetesSystemUser, Role, UserRole, AppToken


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput)

    class Meta:
        model = KubernetesSystemUser
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=("你需要重新设置密码，不要犹豫了，老司机，<a href=\"../password/\">快上车</a>."))

    class Meta:
        model = KubernetesSystemUser
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]

#
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'owner', 'remarks')


class KubernetesSystemUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'alias', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Primary info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'alias', 'phone', 'creator')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        ('Add user', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2', 'is_admin', 'is_active')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    readonly_fields = ['creator']


# class ModelBaseAdmin(admin.ModelAdmin):
#     list_display = ('creator', 'is_deleted', 'create_time', 'modify_time')
#     readonly_fields = ['creator']
#
#     def save_model(self, request, obj, form, change):
#         if not obj.creator:
#             obj.creator = request.user.username
#         obj.save()
#
#
# class LoonKubernetesSystemUserAdmin(ModelBaseAdmin):
#     list_display = ('id',
#                     'username',
#                     'alias',
#                     'email',
#                     'phone',
#                     'is_active',
#                     'is_admin') + ModelBaseAdmin.list_display
#     readonly_fields = ['creator', 'last_login']
#     search_fields = ('username',)
#
#     def save_model(self, request, obj, form, change):
#         if not obj.creator:
#             obj.creator = request.user.username
#             # 可用于生成密码，晚点修改下
#             obj.set_password(form.cleaned_data['password'])
#         obj.save()
#
#
# class LoonRoleAdmin(ModelBaseAdmin):
#     search_fields = ('name',)
#     list_display = ('id', 'name', 'description') + ModelBaseAdmin.list_display
#
#
# class LoonUserRoleAdmin(ModelBaseAdmin):
#     search_fields = ('user_id',)
#     list_display = ('id', 'user_id', 'role_id') + ModelBaseAdmin.list_display
#
#
# class AppTokenAdmin(ModelBaseAdmin):
#     search_fields = ('app_name',)
#     readonly_fields = ['token', 'creator']
#     list_display = ('id', 'app_name', 'token') + ModelBaseAdmin.list_display
#
#     def save_model(self, request, obj, form, change):
#         if not obj.creator:
#             obj.creator = request.user.username
#             import uuid
#             obj.token = uuid.uuid1()
#         obj.save()


# Now register the new UserAdmin...
admin.site.register(KubernetesSystemUser, KubernetesSystemUserAdmin)
# admin.site.register(Role, LoonRoleAdmin)
# admin.site.register(UserRole, LoonUserRoleAdmin)
# admin.site.register(AppToken, AppTokenAdmin)
# unregister the Group model from admin.
admin.site.unregister(Group)

