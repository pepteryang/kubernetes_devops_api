# -*- coding:utf-8-*-
# @Author : peteryang
# @Email : snfnvtk@163.com
# @Time : 2019/8/21
# @Site : 
# @File : auths
# @Software : PyCharm

import jwt, datetime, time

from apps.account.models import KubernetesSystemUser
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id:
        :param login_time:
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=7),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(payload, 'secret', algorithm='HS256'), ''
        except Exception as e:
            return False, e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return:
        """
        try:
            secret_key = 'ncX2o7fOQiAPxXRn8bBC1GP7vqwrTMeAtcHRzF4k9jxxQFcEbgjJ39i7DYQCv1ig',
            payload = jwt.decode(auth_token,
                                 secret_key,
                                 options={'verify_exp': False}
                                 )
            if( 'data' in payload and 'id' in payload['data']):
                return payload, ''
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return False, "Token过期"
        except jwt.InvalidTokenError:
            return False, "无效的Token"

    def authenticate(self, request, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param username:
        :param password:
        :return:
        """
        ret = KubernetesSystemUser.objects.filter(username=username, is_deleted=False).first()
        if not ret:
            return JsonResponse({"message": "User Does not exist"})
        # if ret.check_password(password):
        user_obj = authenticate(username=username, password=password)
        print(user_obj)
        if user_obj:
            login(request, username)
            login_time = int(time.time())
            print(login_time)
            token, msg = self.encode_auth_token(username, login_time)
            print(token)
            if token:
                return token,
            else:
                return False,
        else:
            return '{"message":"用户名或密码不正确"}'

    def identify(self, request):
        """
        用户鉴权
        :param request:
        :return:
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_array = auth_header.split(" ")
            # not auth_tokenArr or auth_tokenArr[0] != 'jwt' or
            if (len(auth_token_array) != 2):
                return False, "请传递正确的验证头信息"
            else:
                auth_token = auth_token_array[1]
                payload, msg = self.decode_auth_token(auth_token)
                if payload:
                    if not isinstance(payload, str):
                        username = KubernetesSystemUser.objects.filter(username=payload.id, is_deleted=False).first()
                        if not username:
                            return False, "不存在该用户"
                        else:
                            return username, "请求成功"
                    else:
                        return False, payload
                else:
                    return False, msg
        else:
            return False, "没有提供认证token"

    def get_username(self, token):
        """
        通过token获取用户名
        :param token:
        :return:
        """
        user_token_info, msg = self.decode_auth_token(token)
        if user_token_info:
            username = user_token_info['data']['id']
            return username
        else:
            return msg
