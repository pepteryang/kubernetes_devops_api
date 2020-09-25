#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time :     Created on 七月-10-19 10:08
# @Version :  1.0
# @File :     harborapi.py
# @author:    Zhiqun.yang
# @Email :    zhiqun.yang@bqrzzl.com
# @License :  (C)Copyright 2019-2020, DevopsGroup-NLPR-CASIA
 @Software :  vscode
'''

import urllib3
import requests

urllib3.disable_warnings()


class HarborApi(object):
    """
    Harbor 的版本要求大于1.7
    """
    def __init__(self, url, username, password, protocol="https"):
        '''
        init the request
        :param url: url address or doma
        :param username:
        :param passwd:
        :param protect:
        '''
        self.url = url
        self.username = username
        self.password = password
        self.protocol = protocol
        self.session_id, self.session_id_key = self.login_get_session_id()

    def login_get_session_id(self):
        '''
        by the login api to get the session of id
        :return:
        '''
        harbor_version_url = "%s://%s/api/systeminfo" %(self.protocol, self.url)
        header_dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20190101 Firefox/64.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data_dict = {
            "principal": self.username,
            "password": self.password
        }
        v_req_handle = requests.get(harbor_version_url, verify=False)
        self.harbor_version = v_req_handle.json()["harbor_version"]
        req_url = "%s://%s/c/login" % (self.protocol, self.url)
        self.session_id_key = "sid"
        req_handle = requests.post(req_url, data=data_dict, headers=header_dict, verify=False)
        if 200 == req_handle.status_code:
            self.session_id = req_handle.cookies.get(self.session_id_key)
            return self.session_id, self.session_id_key
        else:
            raise Exception("login error,please check your account info!" + self.harbor_version)


    def list_projects(self):
        project_url = "%s://%s/api/projects" % (self.protocol, self.url)
        req_handle = requests.get(project_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the project info。")

    def detail_project(self, project_id):
        repository_url = '%s://%s/api/repositories?project_id=%s' % (self.protocol, self.url, project_id)
        req_handle = requests.get(repository_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the repository info")

    def check_project(self, project_name):
        """
        Code	Description
        200	    Project name exists.
        401	    User need to login first.
        404	    Project name does not exist.
        500	     Unexpected internal errors.
        """
        project_url = '%s://%s/api/projects?project_name=%s' %(self.protocol, self.url, project_name)
        req_handle = requests.head(project_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return "Project name exists"
        if 401 == req_handle.status_code:
            return "User need to login first"
        if 404 == req_handle.status_code:
            return "Project name does not exist."
        else:
            raise Exception("Failed to get the projects info。")

    def create_project(self, project_name, public="true", enable_content_trust="false", prevent_vul="false", severity="high" , auto_scan="true"):
        """
        Code	Description
        201	    Project created successfully.
        400 	Unsatisfied with constraints of the project creation.
        401	    User need to log in first.
        409	    Project name already exists.
        415	    The Media Type of the request is not supported, it has to be "application/json"
        500	    Unexpected internal errors.
        
            project_name	string      The name of the project.
            metadata    {
                public	string  项目是否公开，默认值True 可选值 "true", "false".
                enable_content_trust	string  仅允许部署通过认证的镜像, 没有通过认证的镜像不能部署.默认值：False ,可用值为 "true", "false".
                prevent_vul	string  是否阻止潜在漏洞镜像运行 可用值为： "true", "false".
                severity	string 阻止危害级别以上的镜像运行  可用值为："negligible", "low", "medium", "high", "critical".
                auto_scan	string 漏洞扫描--自动扫描镜像. 值为："true", "false".
            }
        
        """
        data = {
            "project_name": project_name,
            "metadata": {
                "public": public,
                "enable_content_trust": enable_content_trust,
                "prevent_vul": prevent_vul,
                "severity": severity,
                "auto_scan": auto_scan
                }
            }
        
        headers = {
                'Content-Type': 'application/json',
            }
            
        project_url = "%s://%s/api/projects" % (self.protocol, self.url)
        req_handle = requests.post(project_url, json=data, headers=headers, cookies={self.session_id_key: self.session_id}, verify=False)
        if 201 == req_handle.status_code:
            return "Project created successfully"
        if 400 == req_handle.status_code:
            return "Unsatisfied with constraints of the project creation."
        if 401 == req_handle.status_code:
            return "User need to login first"
        if 404 == req_handle.status_code:
            return "Project name does not exist."
        else:
            raise Exception("Unexpected internal errors.")

    def tags_info(self, repo_name):
        tags_url = '%s://%s/api/repositories/%s/tags' % (self.protocol, self.url, repo_name)
        req_handle = requests.get(tags_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return req_handle.json()
        else:
            raise Exception("Failed to get the tags info。")

    def del_tags(self, repo_name, tag_name):
        """
        删除镜像
        repo_name : 项目名称
        tag_name: 镜像名称
        200	Delete tag successfully.
        400	Invalid repo_name.
        401	Unauthorized.
        403	Forbidden.
        404	Repository or tag not found.
        """
        tags_url = '%s://%s/api/repositories/%s/tags/%s' % (self.protocol, self.url, repo_name, tag_name)
        req_handle = requests.delete(tags_url, cookies={self.session_id_key: self.session_id}, verify=False)
        if 200 == req_handle.status_code:
            return "Delete tag successfully."
        if 400 == req_handle.status_code:
            return "Invalid repo_name."
        if 401 == req_handle.status_code:
            return "Unauthorized"
        if 403 == req_handle.status_code:
            return "Forbidden"
        else:
            raise Exception("Repository or tag not found.")
        
# if __name__ == "__main__":
#     s = HarborApi(url='10.83.36.68', username='admin', passwd='Harbor12345')
#     pprint(s.detail_project(project_id=4))