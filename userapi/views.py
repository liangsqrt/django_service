from django.shortcuts import render
from .serializers import UserSerializers, UserSignInSerializers, SmsSerializer, UserLoginSerializer
from .models import User, VerifyCode, UserSignInfoRecord, UserLoginRecord
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from random import choice
from .SMSVerify.verify import QCloudSMS
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, BaseAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import exceptions
from rest_framework_jwt.settings import api_settings
from datetime import datetime


class UserAuthentication(ModelBackend):
    """
    验证用户用的，用于一般访问请求时，确定用户到底可不可以访问.这里边的authenticate方法的调用发生在用户登陆的时候（非xadmin界面）
    """
    def authenticate(self, request, username=None, password=None, **kwargs):  # authenticate() 这个函数中处理认证的逻辑
        """

        :param request:
        :param username: 此时 username 可以是 用户名 或者 手机号
        :param password:
        :param kwargs:
        :return:
        """
        if not username:
            raise exceptions.AuthenticationFailed("用户名不能为空")
        try:
            user = User.objects.get(Q(username=username) | Q(mobile_phone=username) | Q(email=username))
            if user.check_password(password):  # check_password() 时会转化为密文的形式
                return user
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed("用户认证失败")

    def authenticate_header(self, request):
        pass


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'code': 200,
        'data': {
            'username': user.alias if user.alias else "awesome one",
            'avatar': "/user/babalababa.jpg" # user.user_header_picture()
        },

    }


class MyPermisssion(BasePermission):
    def has_permission(self, request, view):
        print(request.data)
        if request.user.username:
            return True
        else:
            return False


class UserSerilizersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'ps'
    page_query_param = 'p'
    max_page_size = 30
    authentication_classes = (UserAuthentication, )


#  业务serializer部分
class UserSerializersViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    获取用户的详细信息用的，记得加验证
    """
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer
    queryset = VerifyCode.objects.all()

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile_phone"]

        tencent_sms = QCloudSMS()

        code = self.generate_code()

        sms_status = tencent_sms.send_msg(phone_num=mobile, verify_data=code)

        if sms_status["result"] != 0:
            return Response({
                "mobile": sms_status["errmsg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile_phone=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserSignInViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册使用的视图
    """
    serializer_class = UserSignInSerializers
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, )  # authentication.SessionAuthentication

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserSerializers
        elif self.action == "create":
            return UserSignInSerializers

        return UserLoginSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user_sign_in = UserSignInfoRecord()
        user_sign_in.sign_in_way = 1
        user_sign_in.sign_in_ip = ""

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class LoginViewSet(APIView):
    """
    用户的登录登出
    """
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)  # todo: 用户登录后信息的获取：用户头像链接！！
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print(request)
        # print(args)
        # return None




