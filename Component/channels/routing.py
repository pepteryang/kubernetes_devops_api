from django.urls import path
from Component.channels.consumers import SSHConsumer, SSHLogConsumer

websocket_urlpatterns = [
    path(r"ws/<slug:namespace>/<slug:pod_name>/<slug:kubernetes_id>", SSHConsumer),
    path(r"wsLog/<slug:namespace>/<slug:pod_name>/<slug:kubernetes_id>", SSHLogConsumer),
]