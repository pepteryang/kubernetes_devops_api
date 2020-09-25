# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/11/27
# @Site : 
# @File : IDC
# @Software : PyCharm

# Create your views here.
import json
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.assets import models
from apps.assets import serializers
from Component.common.assembly import UsersPagination
from Component.common.assembly import ssh_copy_ras, run_system_cmd
from Component.common.openpyxl_service import handle_data_to_excl


class ExportHostData(APIView):
    def _get_response(self, file_io, file_name):

        """得到响应对象"""
        res = HttpResponse()
        res["Content-Type"] = "application/octet-stream"
        res["Content-Disposition"] = 'attachment;filename={}.xlsx'.format(file_name).encode()
        res.write(file_io.getvalue())
        return res

    def post(self, request):
        export_data = {}
        pks = request.data.get('data_list_is')
        head_list = ["主机名",
                     "Idc机房",
                     "内网地址",
                     "远程端口",
                     "CPU",
                     '硬盘',
                     '内存',
                     "系统类型",
                     "系统版本",
                     "主机购买时间",
                     "主机到期时间",
                     "项目名称",
                     "部署环境",
                     "user_root密码",
                     "运维用户名",
                     "运维密码",
                     "程序用户名",
                     "程序密码"]
        if pks:
            data_list = models.Host.objects.all().values_list('name',
                                                              'idc',
                                                              'eth1',
                                                              'remote_port',
                                                              'cpu',
                                                              'hard_disk',
                                                              'host_memory',
                                                              'system',
                                                              'system_cpu_arch',
                                                              'purchasing',
                                                              'expire',
                                                              'project',
                                                              'env',
                                                              'root_password',
                                                              'operation_username',
                                                              'operation_password',
                                                              'application_username',
                                                              'application_password'
                                                              ).filter(id__in=pks)
        else:
            data_list = models.Host.objects.all().values_list('name',
                                                              'idc',
                                                              'eth1',
                                                              'remote_port',
                                                              'cpu',
                                                              'hard_disk',
                                                              'host_memory',
                                                              'system',
                                                              'system_cpu_arch',
                                                              'purchasing',
                                                              'expire',
                                                              'project',
                                                              'env',
                                                              'root_password',
                                                              'operation_username',
                                                              'operation_password',
                                                              'application_username',
                                                              'application_password')

        export_data['head_list'] = head_list
        export_data['data_list'] = list(data_list)
        report_name = "HostDetailsReport"

        file_io = handle_data_to_excl(export_data=export_data, report_name=report_name,)
        file_name = report_name
        # 确定响应
        response = self._get_response(file_io, file_name)
        return response


class UpdateHostForAnsible(APIView):
    """
    用于添加主机成功后调用Ansible接口更新服务器基础信息
    """
    def post(self, request):
        pk = request.data.get('host_id')
        hosts = models.Host.objects.get(id=pk)
        print(hosts)
        ssh_copy_ras(password=hosts.operation_password,
                     sudo_user=hosts.operation_username,
                     host_ip=hosts.eth1,
                     ssh_port=hosts.remote_port)

        cmd = "/usr/bin/ansible all -u {name} -i {ip}:{port}, -m setup".format(
            ip=hosts.eth1,
            name=hosts.operation_username,
            port=hosts.remote_port
        )
        try:
            raw_info = run_system_cmd(command=cmd)
            info = str(raw_info["standard_out"], encoding="utf8")
        except Exception as e:
            # subprocess.CalledProcessError
            data = {
                "message": str(e),
                "code": 60000
            }
            return Response(data)

        base_info = json.loads(info.split('=>')[1])['ansible_facts']
        print(type(base_info))

        mac = base_info["ansible_default_ipv4"]['macaddress']
        cpu = base_info['ansible_processor_vcpus']
        memory = round(int(base_info['ansible_memtotal_mb'])/1024.0, 2)
        disk_info = base_info['ansible_devices']
        disk_volume = round(
            sum(
                [int(disk_info[disk]['sectors'])*int(disk_info[disk]['sectorsize']) for disk in disk_info]
            )/1024**3/2
        )
        ansible_distribution = base_info["ansible_distribution"] + '-' + base_info["ansible_distribution_version"]
        os_machine = base_info["ansible_machine"]
        system_kernel = base_info["ansible_kernel"]
        cpu_info = base_info["ansible_processor"][2] if len("ansible_processor") > 3 else base_info["ansible_processor"][1]
        hosts.cpu = cpu
        hosts.mac_address = mac
        hosts.host_memory = memory
        hosts.hard_disk = disk_volume
        hosts.system_cpu_arch = os_machine
        hosts.system = ansible_distribution
        hosts.system_kernel = system_kernel
        hosts.cpu_info = cpu_info
        hosts.save()

        data = {
            "message": "更新成功",
            "code": 66666
        }
        return JsonResponse(data)


class AssetsHostInfo(APIView):
    """
        CMDB 主机管理
    """

    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件
        queryset = models.Host.objects.all()
        if queryset:
            pg = UsersPagination()
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = serializers.AssetsHostManagementSerializer(instance=page_roles, many=True)
            return pg.get_paginated_response(serializer.data)

        else:
            data = {
                "code": 60000,
                "message": "数据列表为空，请添加后查询"
            }
            return JsonResponse(data)

    def post(self, request):
        verify_data = serializers.AssetsHostManagementSerializer(data=request.data)
        if verify_data.is_valid():
            verify_data.save()
            data = {
                "data": verify_data.data,
                "code": 66666,
                "message": "数据保存成功"
            }
            return JsonResponse(data)
        else:
            data = {
                "code": 60000,
                "message": verify_data.errors
            }
            return JsonResponse(data)

    def patch(self, request):
        pk = request.data.get('id')
        print(pk)
        if pk:
            queryset = models.Host.objects.filter(id=pk).first()
            print(queryset)
            serializer = serializers.AssetsHostManagementSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.validated_data,
                    "code": 66666,
                    "message": "数据保存成功"
                }
                return JsonResponse(data)
            else:
                data = {
                    "data": serializer.errors,
                    "code": 60000,
                    "message": "数据保存错误"
                }
                return JsonResponse(data)
        else:
            data = {
                "data": '',
                "code": 60000,
                "message": "没有找到对应的UUID"
            }
            return JsonResponse(data)

    def delete(self, request):
        try:
            models.Host.objects.filter(id=request.data.get('id')).delete()
            data = {
                "status": 200,
                "code": 66666,
                "message": "数据删除成功"
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                "status": 200,
                "code": 6000,
                "message": e
            }
            return JsonResponse(data)


class AssetsHostRecordInfo(APIView):
    def get(self, request):
        # request是被封装后的request,原生的request在request._request
        # 如果想用原生request中的属性，还是原来的用法，因为Request重写了__getattr__方法
        # 原生django只能处理urlencoded和form_data编码，如果是json格式，原生django是不能处理的，需要自己从body中取出来自行处理
        # request.data 不管前端传数据的编码格式是urlencoded，form_data或者是json，都从里面取值
        # request.query_params  是原来django原生的GET中的数据
        # self.FILES  就是上传的文件
        host = request.data.get('host_ip')
        if host:
            queryset = models.HostRecord.objects.all().filter(host=host)
            serializer = serializers.AssetsHostRecordManagementSerializer(instance=queryset, many=True)
            data = {
                "data": serializer.data,
                "code": 66666,
                "message": "数据查询成功"
            }
            return JsonResponse(data)

        else:
            data = {
                "code": 60000,
                "message": "数据列表为空，请添加后查询"
            }
            return JsonResponse(data)


