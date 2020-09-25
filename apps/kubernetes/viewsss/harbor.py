# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/12/26
# @Site : 
# @File : harbor
# @Software : PyCharm

from rest_framework.views import APIView
from apps.assets.models import OtherResourceInfo
from django.http.response import JsonResponse
from Component.kubernetes.harborapi import HarborApi


class HarborListProjectView(APIView):
    def post(self, request):
        pk = request.data.get('pk')
        info = OtherResourceInfo.objects.get(id=pk)
        data = HarborApi(password=info.password,
                         username=info.username,
                         url=info.address).list_projects()
        # #组装自己需要的信息
        project_info = []
        if data:
            for res in data:
                mid = {
                    "project_id": res["project_id"],
                    "project_name": res["name"],
                    }
                project_info.append(mid)
        return JsonResponse(project_info, safe=False)


class HarborDetailProjectView(APIView):
    def post(self, request):
        pk = request.data.get('pk')
        project_id = request.data.get('project_id')
        info = OtherResourceInfo.objects.get(id=pk)
        data = HarborApi(password=info.password,
                         username=info.username,
                         url=info.address).detail_project(project_id=project_id)
        # 组装自己需要的信息
        project_info = []
        if data:
            for res in data:
                mid = {
                    "project_id": res["project_id"],
                    "repo_name": res["name"],
                    }
                project_info.append(mid)
        return JsonResponse(project_info, safe=False)


class HarborTagInfoView(APIView):
    def post(self, request):
        pk = request.data.get('pk')
        repo_name = request.data.get('repo_name')
        info = OtherResourceInfo.objects.get(id=pk)
        conn = HarborApi(password=info.password,
                         username=info.username,
                         url=info.address)
        data = conn.tags_info(repo_name=repo_name)
        print(data)
        # 组装自己需要的信息
        repo_info = []
        if data:
            for res in data:
                mid = {
                    "repo_name":  repo_name,
                    "tag_name": info.address + "/" + repo_name + ":" + res['name'],
                    "tag_size": res['size'],
                    "create_time": res['created'],
                }
                repo_info.append(mid)
        return JsonResponse(repo_info, safe=False)


class HarborDeleteTagView(APIView):
    def post(self, request):
        pk = request.data.get('pk')
        repo_name = request.data.get('repo_name')
        tag_name = request.data.get('tag_name')
        info = OtherResourceInfo.objects.get(id=pk)
        data = HarborApi(password=info.password,
                         username=info.username,
                         url=info.address).del_tags(repo_name=repo_name, tag_name=tag_name)
        print(data)
        return JsonResponse({"message": data}, safe=False)
