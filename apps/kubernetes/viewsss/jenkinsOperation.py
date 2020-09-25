# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2020/1/6
# @Site : 
# @File : jenkinsOperation
# @Software : PyCharm


from Component.jenkins.JenkinsApi import JenkinsApi
from django.http import JsonResponse
from rest_framework.views import APIView
from apps.assets.models import OtherResourceInfo


class GetJenkinsAllJobs(APIView):

    def post(self, request):
        pk = request.data.get("pk", None)
        info = OtherResourceInfo.objects.get(id=pk)
        data = JenkinsApi(
            full_url=info.address,
            username=info.username,
            password=info.password).get_jobs()
        return JsonResponse(data, safe=False)


class GetJenkinsAllViews(APIView):

    def post(self, request):
        pk = request.data.get("pk", None)
        info = OtherResourceInfo.objects.get(id=pk)
        data = JenkinsApi(
            full_url=info.address,
            username=info.username,
            password=info.password).get_views()
        return JsonResponse(data, safe=False)


class GetJenkinsJobInfo(APIView):

    def post(self, request):
        pk = request.data.get("pk", None)
        job_name = request.data.get("job_name", None)
        info = OtherResourceInfo.objects.get(id=pk)
        data = JenkinsApi(
            full_url=info.address,
            username=info.username,
            password=info.password).get_job_info(job_name=job_name)
        return JsonResponse(data, safe=False)


class GetJenkinsBuildJob(APIView):
    def post(self, request):
        pk = request.data.get("pk", None)
        job_name = request.data.get("job_name", None)
        info = OtherResourceInfo.objects.get(id=pk)
        data = JenkinsApi(
            full_url=info.address,
            username=info.username,
            password=info.password).build_job(job_name=job_name)
        return JsonResponse(data, safe=False)


class GetJenkinsBuildInfo(APIView):
    def post(self, request):
        pk = request.data.get("pk", None)
        job_name = request.data.get("job_name", None)
        info = OtherResourceInfo.objects.get(id=pk)
        server = JenkinsApi(full_url=info.address, username=info.username, password=info.password)
        job_number = server.get_job_number(job_name=job_name)
        data = server.get_build_info(job_name=job_name, number=job_number)
        return JsonResponse(data, safe=False)


class GetJenkinsBuildConsoleOutput(APIView):
    def post(self, request):
        pk = request.data.get("pk", None)
        job_name = request.data.get("job_name", None)
        info = OtherResourceInfo.objects.get(id=pk)
        server = JenkinsApi(full_url=info.address, username=info.username, password=info.password)
        job_number = server.get_job_number(job_name=job_name)
        ret = server.get_build_console_output(job_name=job_name, number=job_number)
        data = str(ret).strip("\r").split("\n")
        return JsonResponse(data, safe=False)

