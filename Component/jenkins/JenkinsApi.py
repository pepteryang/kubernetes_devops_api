# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2020/1/6
# @Site : 
# @File : JenkinsApi
# @Software : PyCharm


import jenkins

# coding:utf-8
import jenkins


class JenkinsApi(object):
    def __init__(self, full_url, username, password):
        self._url = full_url
        self._username = username
        self._password = password
        self.server = jenkins.Jenkins(self._url, username=self._username, password=self._password)

    def get_jobs(self):
        return self.server.get_jobs()

    def get_jobs_count(self):
        return self.server.jobs_count()

    def get_job_config(self, job_name):
        return self.server.get_job_config(job_name)

    def create_job(self, job_name, config_xml):
        return self.server.create_job(job_name, config_xml)

    def copy_job(self, job_name, new_job_name):
        return self.server.copy_job(job_name, new_job_name)

    def delete_job(self, job_name):
        return self.server.delete_job(job_name)

    def build_job(self, job_name):
        return self.server.build_job(job_name)

    def get_job_info(self, job_name):
        return self.server.get_job_info(job_name)

    def get_job_number(self, job_name):
        return self.server.get_job_info(job_name)['lastCompletedBuild']['number']

    def get_build_info(self, job_name, number):
        return self.server.get_build_info(job_name, number)

    def get_build_console_output(self, job_name, number):
        return self.server.get_build_console_output(job_name, number)

    def get_views(self):
        return self.server.get_views()

#
# if __name__ == "__main__":
#     s = JenkinsApi(full_url="http://10.10.0.150:8080/jenkins", username="admin", password="HpI5npPuonNs")
#     dd = s.get_views()
#     print(dd)
