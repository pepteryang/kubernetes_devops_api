#/usr/bin/env python
#-*- config=utf-8 -*-
#
# https://github.com/kubernetes-client/python/
#https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
#
from __future__ import print_function
import logging
import yaml
import kubernetes.client
from kubernetes.client.rest import ApiException
from urllib3.exceptions import HTTPError
from pprint import pprint


ApiToken = """eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi1uNmQ2cCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImQyOTk2MWEzLTNkM2QtMTFlOC1iOThhLTAwNTA1NmFiNTRkMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.PD4aMZ9qpNSHo4K-z6rC-30SssPb7s7cUCTHgXxIY6PXuQNNy3O_fN-4BtoIQuL8fIIhDq7Z197IffMmbnhceNVHZ2DI5yI2ZNxMsb-8TR6RQQaRXMeOKaN4pD4WBwbdfYVbJhBY9iutD5SspKwpiFQ3xq8LhyBz1kZAjZ7V7HYgr6tiAc6xyuewPBioWEU8L5AajNLSL9k26fgHbc9Uz_lKq4-GmsBADl3k2OCQN4WTJ7FEAhbFNaeCTD_hSB53DCP2dU02qOBlBHSdNqNI11GHyTE3g5UFvPKM6rSkU1WtdeIKRNE6XXYvM2DM5rftat3qCqTNQpwNAgqCtBmHFg"""
configuration = kubernetes.client.Configuration()
configuration.host = 'https://10.83.38.172:6443'
configuration.verify_ssl = False
configuration.debug = True
configuration.api_key = {"authorization" : "Bearer " + ApiToken }
kubernetes.client.Configuration.set_default(configuration)
pretty = "pretty_example"

def create_secret(source):
    '''
    Creates the kubernetes secret as defined by the user.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    namespace = metadata['namespace']
    data = __enforce_only_strings_dict(src_obj['data'])
    type = src_obj['type']
    # encode the secrets using base64 as required by kubernetes
    body = kubernetes.client.V1Secret(
        metadata=__dict_to_object_meta(metadata),
        data=data,
        type=type
    )
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.create_namespaced_secret(
            namespace=namespace,
            body=body,
            pretty=pretty)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->create_namespaced_secret: {0}'.format(exc)
            )
            raise Exception(exc)

def create_configmap(source):
    '''
    Creates the kubernetes configmap as defined by the user.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    namespace = metadata['namespace']
    data=src_obj['data']

    data = __enforce_only_strings_dict(data)

    body = kubernetes.client.V1ConfigMap(
        metadata=__dict_to_object_meta(metadata),
        data=data)

    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.create_namespaced_config_map(body=body,namespace=namespace)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->create_namespaced_config_map: {0}'.format(exc)
            )
            raise Exception(exc)

def create_services(source):
    '''
    Creates the kubernetes service as defined by the user.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    namespace = metadata['namespace']
    body = __create_object_body(
        kind='Service',
        obj_class=kubernetes.client.V1Service,
        spec_creator=__dict_to_service_spec,
        source=source,
    )
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.create_namespaced_service(body=body,namespace=namespace,pretty=pretty)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->create_namespaced_service: {0}'.format(exc)
            )
            raise Exception(exc)

def create_namespace(source):
    '''
    Creates a namespace with the specified name.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata=src_obj['metadata']
    meta_obj = kubernetes.client.V1ObjectMeta(metadata)
    body = kubernetes.client.V1Namespace(metadata=meta_obj)
    body.metadata.name = metadata['name']
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.create_namespace(body)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->create_namespace: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def create_deployment(source):
    '''
    Creates the kubernetes deployment as defined by the user.
    '''
    src_obj = __read_and_render_yaml_file(source)
    namespace = src_obj['metadata']['namespace']
    body = __create_object_body(
        kind='Deployment',
        obj_class=kubernetes.client.V1Deployment,
        source=source,
        spec_creator=__dict_to_deployment_spec,
        )
    try:
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.create_namespaced_deployment(
            body=body,
            namespace=namespace,
            pretty=pretty)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 409:
            return 409
        else:
            logging.exception(
                'Exception when calling '
                'ExtensionsV1beta1Api->create_namespaced_deployment: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def show_deployment(source):
    '''
    Return the kubernetes deployment defined by name and namespace
    '''
    src_obj = __read_and_render_yaml_file(source)
    name = src_obj['metadata']['name']
    namespace = src_obj['metadata']['namespace']
    try:
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.read_namespaced_deployment(name=name, namespace=namespace)
        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'ExtensionsV1beta1Api->read_namespaced_deployment: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def show_service(source):
    '''
    Return the kubernetes service defined by name and namespace
    '''
    src_obj = __read_and_render_yaml_file(source)
    name = src_obj['metadata']['name']
    namespace = src_obj['metadata']['namespace']
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.read_namespaced_service(name=name, namespace=namespace)
        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->read_namespaced_service: {0}'.format(exc)
            )
            raise Exception(exc)

def show_namespace(source):
    '''
    Return information for a given namespace defined by the specified name
    '''
    src_obj = __read_and_render_yaml_file(source)
    name = src_obj['metadata']['name']
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.read_namespace(name=name)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->read_namespace: {0}'.format(exc)
            )
            raise Exception(exc)

def show_secret(source):
    '''
    Return the kubernetes secret defined by name and namespace.
    The secrets can be decoded if specified by the user. Warning: this has
    security implications.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    namespace = metadata['namespace']
    data = __enforce_only_strings_dict(src_obj['data'])
    type = src_obj['type']
    name= metadata['name']
    # encode the secrets using base64 as required by kubernetes
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.read_namespaced_secret(
            namespace=namespace,
            pretty=pretty,
            name=name)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->read_namespaced_secret: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def show_configmap(source):
    '''
    Return the kubernetes configmap defined by name and namespace.
    '''
    src_obj = __read_and_render_yaml_file(source)
    name = src_obj['metadata']['name']
    namespace = src_obj['metadata']['namespace']
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.read_namespaced_config_map(
            name,
            namespace)
        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->read_namespaced_config_map: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def delete_configmap(source):
    '''
    Deletes the kubernetes configmap defined by name and namespace
    '''

    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    name = metadata['name']
    namespace = metadata['namespace']
    body = kubernetes.client.V1DeleteOptions(orphan_dependents=True)

    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.delete_namespaced_config_map(
            name=name,
            namespace=namespace,
            body=body)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->delete_namespaced_config_map: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def delete_service(source):
    '''
    Deletes the kubernetes service defined by name and namespace
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    name = metadata['name']
    namespace = metadata['namespace']
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.delete_namespaced_service(name=name,namespace=namespace)
        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling CoreV1Api->delete_namespaced_service: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def delete_namespace(source):
    '''
    Deletes the kubernetes namespace defined by name
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata=src_obj['metadata']
    name = metadata['name']
    body = kubernetes.client.V1DeleteOptions(
        api_version="v1",
        grace_period_seconds=50,
        propagation_policy='Background'
    )
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.delete_namespace(
            body=body,
            name=name,
            pretty=pretty)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->delete_namespace: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def delete_deployment(source):
    '''
    Deletes the kubernetes deployment defined by name and namespace
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata=src_obj['metadata']
    name = metadata['name']
    namespace =metadata['namespace']
    body = kubernetes.client.V1DeleteOptions(
        api_version="v1",
        grace_period_seconds=50,
        propagation_policy="Background"
    )

    try:
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.delete_namespaced_deployment(
            pretty=pretty,
            name=name,
            namespace=namespace,
            body=body)
        mutable_api_response = api_response.to_dict()

        if mutable_api_response['code'] != 200:
            logging.warning('Reached polling time limit. Deployment is not yet '
                        'deleted, but we are backing off. Sorry, but you\'ll '
                        'have to check manually.')
        return mutable_api_response
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'ExtensionsV1beta1Api->delete_namespaced_deployment: '
                '{0}'.format(exc)
            )
            raise ApiException(exc)

def replace_deployment(source):
    '''
    Replaces an existing deployment with a new one defined by name and
    namespace, having the specificed metadata and spec.
    '''
    src_obj = __read_and_render_yaml_file(source)
    namespace = src_obj['metadata']['namespace']
    name=src_obj['metadata']['name']
    body = __create_object_body(
        kind='Deployment',
        obj_class=kubernetes.client.V1Deployment,
        source=source,
        spec_creator=__dict_to_deployment_spec,
    )

    try:
        api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.replace_namespaced_deployment(
            body=body,
            pretty=pretty,
            namespace=namespace,
            name=name)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'ExtensionsV1beta1Api->replace_namespaced_deployment: '
                '{0}'.format(exc)
            )
            raise Exception(exc)

def replace_service(source):
    '''
    Replaces an existing service with a new one defined by name and namespace,
    having the specificed metadata and spec.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata=src_obj['metadata']
    namespace=metadata['namespace']
    name=metadata['name']
    body=__create_object_body(
        kind='Service',
        obj_class=kubernetes.client.V1Service,
        spec_creator=__dict_to_service_spec,
        source=source)
    # Some attributes have to be preserved
    # otherwise exceptions will be thrown
    old_service = show_service(source)
    body.spec.cluster_ip = old_service['spec']['cluster_ip']
    body.metadata.resource_version = old_service['metadata']['resource_version']

    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.replace_namespaced_service(
            namespace=namespace,
            body=body,
            name=name,
            pretty=pretty)
        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->replace_namespaced_service: {0}'.format(exc)
            )
            raise Exception(exc)

def replace_secret(source,):
    '''
    Replaces an existing secret with a new one defined by name and namespace,
    having the specificed data.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    namespace = metadata['namespace']
    name = metadata['name']
    data = __enforce_only_strings_dict(src_obj['data'])
    type = src_obj['type']

    body = kubernetes.client.V1Secret(
        metadata=__dict_to_object_meta(metadata),
        data=data,
        type=type,
    )
    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.replace_namespaced_secret(
            namespace=namespace,
            body=body,
            pretty=pretty,
            name=name)
        pprint(api_response)
        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->create_namespaced_secret: {0}'.format(exc)
            )
            raise Exception(exc)

def replace_configmap(source):
    '''
    Replaces an existing configmap with a new one defined by name and
    namespace, having the specificed data.
    '''
    data = __read_and_render_yaml_file(source)
    metadata = data['metadata']
    namespace = metadata['namespace']
    name = metadata['name']

    data = __enforce_only_strings_dict(data)

    body = kubernetes.client.V1ConfigMap(
        metadata=__dict_to_object_meta(metadata=metadata),
        data=data)

    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.replace_namespaced_config_map(
            name=name,
            namespace=namespace,
            body=body,
            pretty=pretty)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->replace_namespaced_configmap: {0}'.format(exc)
            )
            raise Exception(exc)

def patch_configmap(source):
    '''
    Replaces an existing configmap with a new one defined by name and
    namespace, having the specificed data.
    '''
    src_obj = __read_and_render_yaml_file(source)
    metadata = src_obj['metadata']
    namespace = metadata['namespace']
    name = metadata['name']
    data=src_obj['data']

    data = __enforce_only_strings_dict(data)

    body = kubernetes.client.V1ConfigMap(
        metadata=__dict_to_object_meta(metadata),
        data=data)

    try:
        api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
        api_response = api_instance.patch_namespaced_config_map(
            name=name,
            namespace=namespace,
            body=body,
            pretty=pretty)

        return api_response.to_dict()
    except (ApiException, HTTPError) as exc:
        if isinstance(exc, ApiException) and exc.status == 404:
            return None
        else:
            logging.exception(
                'Exception when calling '
                'CoreV1Api->replace_namespaced_configmap: {0}'.format(exc)
            )
            raise Exception(exc)

def __create_object_body(kind,obj_class,spec_creator,source):
    '''
    Create a Kubernetes Object body instance.
    '''
    if source:
        src_obj = __read_and_render_yaml_file(source)
        if (
            not isinstance(src_obj, dict) or
                'kind' not in src_obj or
            src_obj['kind'] != kind):
            raise Exception(
                'The source file should define only '
                'a {0} object'.format(kind))

        if 'metadata' in src_obj:
            metadata = src_obj['metadata']
        if 'spec' in src_obj:
            spec = src_obj['spec']
        if 'kind' in src_obj:
            kind=src_obj['kind']
        if 'apiVersion' in src_obj:
            apiVersion=src_obj['apiVersion']

    return obj_class(
        metadata=__dict_to_object_meta(metadata),
        spec=spec_creator(spec),kind=kind,api_version=apiVersion)

def __read_and_render_yaml_file(source):
    '''
    Read a yaml file and, if needed, renders that using the specifieds
    templating. Returns the python objects defined inside of the file.
    '''
    try:
        with open(source, encoding="utf-8") as f:
            contents = f.read().encode('utf-8')
        return yaml.load(contents)
    except Exception as e:
        return "Not find this yaml files".format(e)

def __dict_to_object_meta(metadata):
    '''
    Converts a dictionary into kubernetes ObjectMetaV1 instance.
    '''
    meta_obj = kubernetes.client.V1ObjectMeta()
    for key, value in metadata.items():
        if hasattr(meta_obj, key):
           setattr(meta_obj, key, value)
    return meta_obj

def __dict_to_deployment_spec(spec):
    '''
    Converts a dictionary into kubernetes AppsV1beta1DeploymentSpec instance.
    '''
    spec_obj = kubernetes.client.V1DeploymentSpec(selector={}, template={})
    for key, value in spec.items():
        if hasattr(spec_obj, key):
           setattr(spec_obj, key, value)
    return spec_obj

def __dict_to_service_spec(spec):
    '''
    Converts a dictionary into kubernetes V1ServiceSpec instance.
    '''
    spec_obj = kubernetes.client.V1ServiceSpec()
    for key, value in spec.items():
        if key == 'ports':
            spec_obj.ports = []
            for port in value:
                kube_port = kubernetes.client.V1ServicePort(port=0) #defalut port
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

def __enforce_only_strings_dict(data):
    '''
    Returns a dictionary that has string keys and values.
    '''
    ret = {}

    for key, value in data.items():
        ret[str(key)] = str(value)
    return ret
