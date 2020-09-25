# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/8/12
# @Site : 
# @File : kube.py
# @Software : PyCharm


from __future__ import print_function
import logging
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from pprint import pprint
import urllib3

urllib3.disable_warnings()


class KubernetesApi:

    def __init__(self, token, master_host):
        self.configuration = kubernetes.client.Configuration()
        self.configuration.host = master_host
        self.configuration.verify_ssl = False
        self.configuration.debug = True
        self.configuration.api_key = {"authorization": "Bearer " + token}
        kubernetes.client.Configuration.set_default(self.configuration)
        self.pretty = "pretty"

    def create_namespace(self, json_data):
        '''
        Creates a namespace with the specified name.
        '''
        metadata = json_data['metadata']
        meta_obj = kubernetes.client.V1ObjectMeta(metadata)
        body = kubernetes.client.V1Namespace(metadata=meta_obj)
        body.metadata.name = metadata['name']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespace(body)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def delete_namespace(self, json_data):
        '''
        Deletes the kubernetes namespace defined by name
        '''
        metadata = json_data['metadata']
        name = metadata['name']
        body = kubernetes.client.V1DeleteOptions(
            api_version="v1",
            grace_period_seconds=50,
            propagation_policy='Background'
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.delete_namespace(
                body=body,
                name=name,
                pretty=self.pretty)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def get_namespace(self, json_data):
        '''
        Return information for a given namespace defined by the specified name
        '''
        name = json_data['metadata']['name']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.read_namespace(name=name)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def patch_namespace(self, json_data):
        force = True
        body = 'NULL'
        name = json_data['metadata']['name']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_namespace(name, body, pretty=self.pretty, force=force)
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespace: %s\n" % e)

    def create_config_map(self, json_data):
        '''
        Creates the kubernetes configmap as defined by the user.
        '''
        print(json_data)
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        api_version = json_data['apiVersion']
        kind = json_data['kind']
        data = json_data['data']
        body = kubernetes.client.V1ConfigMap(
            api_version=api_version,
            kind=kind,
            metadata=metadata,
            data=data)
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_config_map(body=body, namespace=namespace)
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            pprint(exc)
            return exc.body

    def get_config_map(self, json_data):
        '''
        Return the kubernetes configmap defined by name and namespace.
        '''
        name = json_data['metadata']['name']
        namespace = json_data['metadata']['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_namespaced_config_map(
                name,
                namespace)
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def delete_config_map(self, json_data):
        '''
        Deletes the kubernetes configmap defined by name and namespace
        '''

        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        body = kubernetes.client.V1DeleteOptions(orphan_dependents=True)

        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.delete_namespaced_config_map(
                name=name,
                namespace=namespace,
                body=body)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def replace_config_map(self, json_data):
        '''
        Replaces an existing configmap with a new one defined by name and
        namespace, having the specificed data.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        name = metadata['name']

        data = self.__enforce_only_strings_dict(json_data['data'])

        body = kubernetes.client.V1ConfigMap(
            metadata=self.__dict_to_object_meta(metadata=metadata),
            data=data)

        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.replace_namespaced_config_map(
                name=name,
                namespace=namespace,
                body=body,
                pretty=self.pretty)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def patch_config_map(self, json_data):
        '''
        Replaces an existing configmap with a new one defined by name and
        namespace, having the specificed data.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        name = metadata['name']
        data = json_data['data']

        data = self.__enforce_only_strings_dict(data)

        body = kubernetes.client.V1ConfigMap(
            metadata=self.__dict_to_object_meta(metadata),
            data=data)

        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.patch_namespaced_config_map(
                name=name,
                namespace=namespace,
                body=body,
                pretty=self.pretty)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def create_services(self, json_data):
        '''
        Creates the kubernetes service as defined by the user.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        body = kubernetes.client.V1Service(
            kind='Service',
            metadata=json_data['metadata'],
            spec=json_data['spec']
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_service(body=body,
                                                   namespace=namespace,
                                                   pretty=self.pretty)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def get_service(self, json_data):
        '''
        Return the kubernetes service defined by name and namespace
        '''
        name = json_data['metadata']['name']
        namespace = json_data['metadata']['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_namespaced_service(name=name, namespace=namespace)
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def patch_service(self, json_data):
        '''
            Replaces an existing service with a new one defined by name and
            namespace, having the service data.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        spec = json_data['spec']
        name = metadata['name']
        body = kubernetes.client.V1Service(
            metadata=metadata,
            spec=spec,
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_namespaced_service(
                name=name,
                namespace=namespace,
                body=body,
                pretty=self.pretty)

            return '{"status": "200", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def delete_service(self, json_data):
        '''
        Deletes the kubernetes service defined by name and namespace
        '''
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.delete_namespaced_service(name=name, namespace=namespace)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def create_deployment(self, json_data):
        '''
        Creates the kubernetes deployment as defined by the user.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        body = kubernetes.client.V1Deployment(
            kind='Deployment',
            metadata=metadata,
            spec=json_data['spec']
        )
        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.create_namespaced_deployment(
                body=body,
                namespace=namespace,
                pretty=self.pretty)
            return {"status": 200, "code": 66666, "message": "Deployment创建成功", "data": api_response}
        except ApiException as exc:
            return {"status": 200, "code": 60000, "message": exc}

    def get_deployment(self, json_data):
        '''
        Return the kubernetes deployment defined by name and namespace
        '''
        name = json_data['metadata']['name']
        namespace = json_data['metadata']['namespace']
        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.read_namespaced_deployment(name=name, namespace=namespace)
            return {"status": 200, "code": 66666, "message": "Deployment获取成功", "data": api_response}
        except ApiException as exc:
            return {"status": 200, "code": 60000, "message": exc}

    def list_namespace_deployment(self, json_data):
        '''
        Return the kubernetes deployment defined by name and namespace
        '''
        namespace = json_data['metadata']['namespace']
        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_deployment(namespace=namespace)
            return {"status": 200, "code": 66666, "message": "Deployment获取成功", "data": api_response}
        except ApiException as exc:
            return {"status": 200, "code": 60000, "message": exc}

    def delete_deployment(self, json_data):
        '''
        Deletes the kubernetes deployment defined by name and namespace
        '''
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        body = kubernetes.client.V1DeleteOptions(
            api_version="v1",
            grace_period_seconds=50,
            propagation_policy="Background"
        )

        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.delete_namespaced_deployment(
                pretty=self.pretty,
                name=name,
                namespace=namespace,
                body=body)
            return {"status": "201", "message": "服务创建成功", "data": api_response}
        except ApiException as exc:
            return exc.body

    def replace_deployment(self, json_data):
        '''
        Replaces an existing deployment with a new one defined by name and
        namespace, having the specificed metadata and spec.
        '''
        metadata = json_data['metadata']
        namespace = json_data['metadata']['namespace']
        name = json_data['metadata']['name']
        body = kubernetes.client.V1Deployment(
            kind='Deployment',
            metadata=metadata,
            spec=json_data['spec']
        )

        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.replace_namespaced_deployment(
                body=body,
                pretty=self.pretty,
                namespace=namespace,
                name=name)
            return {"code": "201", "message": "更新成功", "data": api_response}
        except ApiException as exc:
            return exc.body

    def create_secret(self, json_data):
        '''
        Creates the kubernetes secret as defined by the user.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        data = json_data['data']
        data_type = json_data['type']
        body = kubernetes.client.V1Secret(
            metadata=metadata,
            data=data,
            type=data_type
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_secret(
                namespace=namespace,
                body=body,
                pretty=self.pretty)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def get_secret(self, json_data):
        '''
        Return the kubernetes secret defined by name and namespace.
        The secrets can be decoded if specified by the user. Warning: this has
        security implications.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        name = metadata['name']
        # encode the secrets using base64 as required by kubernetes
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_namespaced_secret(
                namespace=namespace,
                pretty=self.pretty,
                name=name)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def patch_secret(self, json_data):
        '''
        Return the kubernetes secret defined by name and namespace.
        The secrets can be decoded if specified by the user. Warning: this has
        security implications.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        data = json_data['data']
        data_type = json_data['type']
        name = metadata['name']
        body = kubernetes.client.V1Secret(
            metadata=metadata,
            data=data,
            type=data_type
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_namespaced_secret(
                namespace=namespace,
                name=name,
                pretty=self.pretty,
                body=body)

            return '{"status": "200", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def create_ingress(self, json_data):
        '''
            Creates the kubernetes secret as defined by the user.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        spec = json_data['spec']
        # encode the secrets using base64 as required by kubernetes
        body = kubernetes.client.ExtensionsV1beta1Ingress(
            metadata=metadata,
            spec=spec
        )
        try:
            api_instance = kubernetes.client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_ingress(
                namespace=namespace,
                body=body,
                pretty=self.pretty)

            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def patch_ingress(self, json_data):
        '''
        patch the kubernetes deployment defined by name and namespace
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        spec = json_data['spec']
        name = metadata['name']

        body = kubernetes.client.ExtensionsV1beta1Ingress(
            metadata=metadata,
            spec=spec
        )
        try:
            api_instance = kubernetes.client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.patch_namespaced_ingress(
                pretty=self.pretty,
                body=body,
                name=name,
                namespace=namespace, )

            return api_response
        except ApiException as exc:
            return exc.body

    def delete_ingress(self, json_data):
        '''
        Deletes the kubernetes deployment defined by name and namespace
        '''
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=56,
            propagation_policy="Background"
        )
        try:
            api_instance = kubernetes.client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.delete_namespaced_ingress(
                pretty=self.pretty,
                body=body,
                name=name,
                namespace=namespace, )
            mutable_api_response = api_response.to_dict()

            if mutable_api_response['code'] != 200:
                logging.warning('Reached polling time limit. ingress is not yet '
                                'deleted, but we are backing off. Sorry, but you\'ll '
                                'have to check manually.')
            return mutable_api_response
        except ApiException as exc:
            return exc.body

    def get_ingress(self, json_data):
        '''
        Return the kubernetes secret defined by name and namespace.
        The secrets can be decoded if specified by the user. Warning: this has
        security implications.
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        name = metadata['name']
        # encode the secrets using base64 as required by kubernetes
        try:
            api_instance = kubernetes.client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.list_namespaced_ingress(
                namespace=namespace,
                pretty=self.pretty,
                name=name,
            )
            return '{"status": "200", "message": "服务获取成功"}'
        except ApiException as exc:
            return exc.body

    def create_namespace_endpoints(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        secrets = json_data['secrets']
        api_version = json_data['api_version']
        kind = json_data['kind']

        body = kubernetes.client.V1Endpoints(
            metadata=metadata,
            secrets=secrets,
            api_version=api_version,
            kind=kind
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_endpoints(
                namespace=namespace,
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def create_namespace_service_account(self, json_data):
        '''
        create a ServiceAccount defined by name and namespace
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        secrets = json_data['secrets']
        api_version = json_data['api_version']
        kind = json_data['kind']

        body = kubernetes.client.V1ServiceAccount(
            metadata=metadata,
            secrets=secrets,
            api_version=api_version,
            kind=kind
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_service_account(
                namespace=namespace,
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def read_namespace_service_account(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        name = metadata['name']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_namespaced_service_account(
                namespace=namespace,
                name=name,
                pretty=self.pretty,
            )
            return '{"status": "200", "message": "服务获取成功"}'
        except ApiException as exc:
            return exc.body

    def replace_namespace_service_account(self, json_data):
        '''
        create a ServiceAccount defined by name and namespace
        '''
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        secrets = json_data['secrets']
        api_version = json_data['api_version']
        kind = json_data['kind']
        name = metadata['name']

        body = kubernetes.client.V1ServiceAccount(
            metadata=metadata,
            secrets=secrets,
            api_version=api_version,
            kind=kind
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.replace_namespaced_service_account(
                namespace=namespace,
                pretty=self.pretty,
                body=body,
                name=name,
            )
            return '{"status": "201", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def delete_namespace_service_account(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=56,
            propagation_policy="Background",
            orphan_dependents="true",
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.delete_namespaced_service_account(
                namespace=namespace,
                name=name,
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "200", "message": "服务删除成功"}'
        except ApiException as exc:
            return exc.body

    def create_cluster_role(self, json_data):
        metadata = json_data['metadata']
        rules = json_data['rules']
        aggregation_rule = json_data['aggregation_rule']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1ClusterRole(
            aggregation_rule=aggregation_rule,
            api_version=api_version,
            metadata=metadata,
            kind=kind,
            rules=rules
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_cluster_role(
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def read_cluster_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_cluster_role(
                pretty=self.pretty,
                name=name,
            )
            return '{"status": "200", "message": "服务读取成功"}'
        except ApiException as exc:
            return exc.body

    def patch_cluster_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        rules = json_data['rules']
        aggregation_rule = json_data['aggregation_rule']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1ClusterRole(
            aggregation_rule=aggregation_rule,
            api_version=api_version,
            metadata=metadata,
            kind=kind,
            rules=rules
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_cluster_role(
                pretty=self.pretty,
                name=name,
                body=body,
                force=True
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def replace_cluster_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        rules = json_data['rules']
        aggregation_rule = json_data['aggregation_rule']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1ClusterRole(
            aggregation_rule=aggregation_rule,
            api_version=api_version,
            metadata=metadata,
            kind=kind,
            rules=rules
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.replace_cluster_role(
                pretty=self.pretty,
                name=name,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def delete_cluster_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']

        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=56,
            propagation_policy='Background'
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.delete_cluster_role(
                pretty=self.pretty,
                body=body,
                name=name
            )
            return '{"status": "200", "message": "服务删除成功"}'
        except ApiException as exc:
            return exc.body

    def create_cluster_role_binding(self, json_data):
        metadata = json_data['metadata']
        role_ref = json_data['role_ref']
        subjects = json_data['subjects']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1ClusterRoleBinding(
            api_version=api_version,
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects,
            kind=kind,
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_cluster_role_binding(
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def read_cluster_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_cluster_role_binding(
                pretty=self.pretty,
                name=name,
            )
            return '{"status": "200", "message": "服务读取成功"}'
        except ApiException as exc:
            return exc.body

    def patch_cluster_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        role_ref = json_data['role_ref']
        subjects = json_data['subjects']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1ClusterRoleBinding(
            api_version=api_version,
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects,
            kind=kind,
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_cluster_role_binding(
                pretty=self.pretty,
                name=name,
                force=True,
                body=body,
            )
            return '{"status": "201", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def replace_cluster_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        role_ref = json_data['role_ref']
        subjects = json_data['subjects']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1ClusterRoleBinding(
            api_version=api_version,
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects,
            kind=kind,
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.replace_cluster_role_binding(
                pretty=self.pretty,
                name=name,
                body=body,
            )
            return '{"status": "201", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def delete_cluster_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']

        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=56,
            propagation_policy='Background'
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.delete_cluster_role_binding(
                pretty=self.pretty,
                body=body,
                name=name
            )
            return '{"status": "200", "message": "服务删除成功"}'
        except ApiException as exc:
            return exc.body

    def create_namespace_role(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        rules = json_data['rules']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1Role(
            api_version=api_version,
            metadata=metadata,
            kind=kind,
            rules=rules
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_role(
                namespace=namespace,
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def read_namespace_role(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        name = metadata['name']
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_namespaced_role(
                pretty=self.pretty,
                namespace=namespace,
                name=name,
            )
            return '{"status": "200", "message": "服务读取成功"}'
        except ApiException as exc:
            return exc.body

    def patch_namespace_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['metadata']
        namespace = metadata['namespace']
        rules = json_data['rules']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1Role(
            api_version=api_version,
            metadata=metadata,
            kind=kind,
            rules=rules
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_namespaced_role(
                namespace=namespace,
                pretty=self.pretty,
                body=body,
                name=name,
                force=True
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def replace_namespace_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['metadata']
        namespace = metadata['namespace']
        rules = json_data['rules']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1Role(
            api_version=api_version,
            metadata=metadata,
            kind=kind,
            rules=rules
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.replace_namespaced_role(
                namespace=namespace,
                pretty=self.pretty,
                name=name,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def delete_namespace_role(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']

        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=56,
            propagation_policy='Background'
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.delete_namespaced_role(
                pretty=self.pretty,
                namespace=namespace,
                body=body,
                name=name
            )
            return '{"status": "200", "message": "服务删除成功"}'
        except ApiException as exc:
            return exc.body

    def create_namespace_role_binding(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        role_ref = json_data['role_ref']
        subjects = json_data['subjects']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1RoleBinding(
            api_version=api_version,
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects,
            kind=kind,
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.create_namespaced_role_binding(
                namespace=namespace,
                pretty=self.pretty,
                body=body,
            )
            return '{"status": "201", "message": "服务创建成功"}'
        except ApiException as exc:
            return exc.body

    def patch_namespace_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        role_ref = json_data['role_ref']
        subjects = json_data['subjects']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1RoleBinding(
            api_version=api_version,
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects,
            kind=kind,
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.patch_namespaced_role_binding(
                pretty=self.pretty,
                namespace=namespace,
                name=name,
                force=True,
                body=body,
            )
            return '{"status": "201", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def replace_namespace_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        role_ref = json_data['role_ref']
        subjects = json_data['subjects']
        api_version = json_data['api_version']
        kind = json_data['kind']
        body = kubernetes.client.V1RoleBinding(
            api_version=api_version,
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects,
            kind=kind,
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.replace_namespaced_role_binding(
                pretty=self.pretty,
                name=name,
                body=body,
            )
            return '{"status": "201", "message": "服务更新成功"}'
        except ApiException as exc:
            return exc.body

    def read_namespace_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.read_namespaced_role_binding(
                namespace=namespace,
                pretty=self.pretty,
                name=name,
            )
            return '{"status": "200", "message": "服务读取成功"}'
        except ApiException as exc:
            return exc.body

    def delete_namespace_role_binding(self, json_data):
        metadata = json_data['metadata']
        name = metadata['name']
        namespace = metadata['namespace']
        body = kubernetes.client.V1DeleteOptions(
            grace_period_seconds=56,
            propagation_policy='Background'
        )
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_instance.delete_namespaced_role_binding(
                pretty=self.pretty,
                namespace=namespace,
                body=body,
                name=name
            )
            return '{"status": "200", "message": "服务删除成功"}'
        except ApiException as exc:
            return exc.body

    def list_cluster_role(self):
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_cluster_role(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,

            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_cluster_role_binding(self):
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_cluster_role_binding(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_role(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_role(
                timeout_seconds=56,
                pretty=self.pretty,
                namespace=namespace,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_role_binding(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_role_binding(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_network_policy(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.NetworkingV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_network_policy(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_config_map(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_config_map(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_endpoints(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_endpoints(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_event(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_event(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_limit_range(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_limit_range(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_persistent_volume_claim(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_persistent_volume_claim(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_pod(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_pod(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_pod_template(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_pod_template(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_replication_controller(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_replication_controller(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_resource_quota(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_resource_quota(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_secret(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_secret(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_service(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_service(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace_service_account(self, json_data):
        metadata = json_data['metadata']
        namespace = metadata['namespace']
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespaced_service_account(
                timeout_seconds=56,
                namespace=namespace,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_persistent_volume_claim_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_persistent_volume_claim_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_role_binding_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_role_binding_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_ingress_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_ingress_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_role_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.RbacAuthorizationV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_role_binding_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_network_policy_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.NetworkingV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_network_policy_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_pod_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_pod_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_pod_template_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_pod_template_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_replication_controller_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_replication_controller_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_resource_quota_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_resource_quota_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_secret_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_secret_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_service_account_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_service_account_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_limit_range_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_limit_range_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_service_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_service_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_event_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_event_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_endpoints_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_endpoints_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_config_map_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_config_map_for_all_namespaces(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_deployment_for_all_namespaces(self):
        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_deployment_for_all_namespaces(
                limit=0,
                pretty=self.pretty,
                timeout_seconds=56
            )
            print(api_response.to_dict())
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def get_api_resources(self):
        try:
            api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.get_api_resources()
            print(api_response)
            return api_response
        except ApiException as exc:
            return exc.body

    def list_persistent_volume(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_persistent_volume(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_node(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_node(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            print(api_response)
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    def list_namespace(self):
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.list_namespace(
                timeout_seconds=56,
                pretty=self.pretty,
                limit=0,
            )
            return api_response.to_dict()
        except ApiException as exc:
            return exc.body

    @staticmethod
    def __create_object_body(self, kind, obj_class, spec_creator, json_data):
        '''
        Create a Kubernetes Object body instance.
        '''
        if json_data:
            if (
                    not isinstance(json_data, dict) or
                    'kind' not in json_data or
                    json_data['kind'] != kind):
                raise Exception(
                    'The source file should define only '
                    'a {0} object'.format(kind))

            if 'metadata' in json_data:
                metadata = json_data['metadata']
            if 'spec' in json_data:
                spec = json_data['spec']
            if 'kind' in json_data:
                kind = json_data['kind']
            if 'apiVersion' in json_data:
                api_version = json_data['apiVersion']

        return obj_class(
            metadata=self.__dict_to_object_meta(metadata),
            spec=spec_creator(spec), kind=kind, api_version=api_version)

    @staticmethod
    def __dict_to_object_meta(metadata):
        '''
        Converts a dictionary into kubernetes ObjectMetaV1 instance.
        '''
        meta_obj = kubernetes.client.V1ObjectMeta()
        for key, value in metadata.items():
            if hasattr(meta_obj, key):
                setattr(meta_obj, key, value)
        return meta_obj

    @staticmethod
    def __dict_to_deployment_spec(spec):
        '''
        Converts a dictionary into kubernetes AppsV1beta1DeploymentSpec instance.
        '''
        spec_obj = kubernetes.client.V1DeploymentSpec(selector={}, template={})
        for key, value in spec.items():
            if hasattr(spec_obj, key):
                setattr(spec_obj, key, value)
        return spec_obj

    @staticmethod
    def __dict_to_service_spec(spec):
        '''
        Converts a dictionary into kubernetes V1ServiceSpec instance.
        '''
        spec_obj = kubernetes.client.V1ServiceSpec()
        for key, value in spec.items():
            if key == 'ports':
                spec_obj.ports = []
                for port in value:
                    kube_port = kubernetes.client.V1ServicePort(port=0)  # defalut port
                    if isinstance(port, dict):
                        for port_key, port_value in port.items():
                            if hasattr(kube_port, port_key):
                                setattr(kube_port, port_key, port_value)
                    else:
                        kube_port.port = port
                    spec_obj.ports.append(kube_port)
            elif hasattr(spec_obj, key):
                setattr(spec_obj, key, value)
        return spec_obj

    @staticmethod
    def __enforce_only_strings_dict(data):
        '''
        Returns a dictionary that has string keys and values.
        '''
        ret = {}

        for key, value in data.items():
            ret[str(key)] = str(value)
        return ret

    def pod_exec(self, namespace, pod_name, container=""):
        command = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
            '&& ([ -x /usr/bin/script ] '
            '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
            '|| exec /bin/sh']
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        container_stream = stream(
            api_instance.connect_get_namespaced_pod_exec,
            name=pod_name,
            namespace=namespace,
            container=container,
            command=command,
            stderr=True, stdin=True,
            stdout=True, tty=True,
            _preload_content=False
        )
        return container_stream

    def pod_logs(self, namespace, pod_name, container=""):
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
        log_container_stream = stream(
            api_instance.connect_get_namespaced_pod_attach,
            name=pod_name,
            namespace=namespace,
            container=container,
            stderr=True,
            stdin=True,
            stdout=True,
            tty=True,
            _preload_content=False
        )
        pprint(log_container_stream)
        return log_container_stream

    def delete_namespace_pod(self, pod_name, namespace):
        '''
        Deletes the kubernetes deployment defined by name and namespace
        '''
        name = pod_name
        namespace = namespace
        body = kubernetes.client.V1DeleteOptions(
            api_version="v1",
            grace_period_seconds=50,
            propagation_policy="Background"
        )
        try:
            api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(self.configuration))
            api_response = api_instance.delete_namespaced_pod(
                pretty=self.pretty,
                name=name,
                namespace=namespace,
                body=body)
            return {"status": "200", "message": "后台删除成功，请等待清理完成！", "data": api_response}
        except ApiException as exc:
            return exc.body

if __name__ == "__main__":
    token = """eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJ6aGlodWEueWFuZy10b2tlbi05N3ZnbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJ6aGlodWEueWFuZyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjNlYTFhNjljLWIyNmQtMTFlOS05NmNhLTAwNTA1NmFiNDE0NCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTp6aGlodWEueWFuZyJ9.gZTWBgxGsM8iYOYX5aeaHSnVd0jXdHGurApOC-cZNTFh4YCna38MNhixua42jP-ylIa1IlxWglVFmqH-eKnd-BTCQ6-ldXNi7G_tApZhNfjAJuTLZ1Elj57r2UGhOsL_P_t5UzctMjPXCeuU1XiJVDspexLW9pPlnDrMpJNWFKWk4UoWJVb5yduv7uMk_ugLb4WRF75AVkkHCBKtyNf43foAuw0Ni7Ks-E8f_xgP-AzTeBQzfqO32B-TLU1e6bA1aKMmTZD6w0lZsBOj9KWaRW5tuqBqsCmkdtbgKUlXywQY7NnuyySNKyfTBcfI-qaSCL6HN_YNymJViGmg9k3sug"""
    master_host = "https://10.83.36.68:6443"
    s = KubernetesApi(token=token, master_host=master_host).loglog(namespace="uat",
                                                                   pod_name="rpf-core-5dcc85cf4b-wlqv8")
