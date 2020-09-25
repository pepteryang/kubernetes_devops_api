# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2020/1/8
# @Site :
# @File : consumers.py
# @Software : PyCharm


from channels.generic.websocket import WebsocketConsumer
from Component.kubernetes.kube import KubernetesApi
from apps.assets.models import OtherResourceInfo
from threading import Thread
import time
import json


class K8SStreamThread(Thread):
    def __init__(self, websocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    def run(self):
        while self.stream.is_open():
            time.sleep(0.1)
            if not self.stream.is_open():
                self.websocket.close()
            try:
                if self.stream.peek_stdout():
                    stdout = self.stream.read_stdout()
                    self.websocket.send(stdout)
                if self.stream.peek_stderr():
                    stderr = self.stream.read_stderr()
                    self.websocket.send(stderr)
            except Exception as err:
                self.websocket.close()


class SSHConsumer(WebsocketConsumer):

    def connect(self):
        # 可以在这里根据 用户  要访问的pod 进行 权限控制
        self.name = self.scope["url_route"]["kwargs"]["pod_name"]
        self.pk = self.scope["url_route"]["kwargs"]["kubernetes_id"]
        self.namespace = self.scope["url_route"]["kwargs"]["namespace"]

        self.queryset_kubernetes = OtherResourceInfo.objects.get(id=self.pk)
        self.stream = KubernetesApi(master_host=self.queryset_kubernetes.address,
                                    token=self.queryset_kubernetes.api_token).pod_exec(
            namespace=self.namespace,
            pod_name=self.name
        )
        print(str(self.stream.read_stdout))
        kub_stream = K8SStreamThread(self, self.stream)
        kub_stream.start()

        self.accept()

    def disconnect(self, close_code):
        self.stream.write_stdin('exit\r')

    def receive(self, text_data):
        self.stream.write_stdin(text_data)


class SSHLogConsumer(WebsocketConsumer):

    def connect(self):
        # 可以在这里根据 用户  要访问的pod 进行 权限控制
        self.name = self.scope["url_route"]["kwargs"]["pod_name"]
        self.pk = self.scope["url_route"]["kwargs"]["kubernetes_id"]
        self.namespace = self.scope["url_route"]["kwargs"]["namespace"]

        self.queryset_kubernetes = OtherResourceInfo.objects.get(id=self.pk)
        self.stream = KubernetesApi(master_host=self.queryset_kubernetes.address,
                                    token=self.queryset_kubernetes.api_token).pod_logs(
            namespace=self.namespace,
            pod_name=self.name
        )
        kub_stream = K8SStreamThread(self, self.stream)
        kub_stream.start()

        self.accept()

    def disconnect(self, close_code):
        self.stream.write_stdin('exit\r')

