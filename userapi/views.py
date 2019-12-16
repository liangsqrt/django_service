from django.shortcuts import render
from .serializers import UserSerializers, UserVerifySerializers, SmsSerializer, UserDetailSerializer
from .models import User, VerifyCode
from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from random import choice
# from rest_framework.permissions import IsAuthenticated
# from django.http.response import HttpResponse
# from django.contrib.auth import get_user_model
from .SMSVerify.verify import QCloudSMS
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


class UserSerilizersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'ps'
    page_query_param = 'p'
    max_page_size = 30


class UserSerializersView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    todo: 把所有的用户信息暴露出去，这个记得要删除的
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = UserSerilizersPagination


class UserAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):  # authenticate() 这个函数中处理认证的逻辑
        """

        :param request:
        :param username: 此时 username 可以是 用户名 或者 手机号
        :param password:
        :param kwargs:
        :return:
        """
        try:
            user = User.objects.get(Q(username=username) | Q(mobile_phone=username) | Q(email=username))
            if user.check_password(password):  # check_password() 时会转化为密文的形式
                return user
        except Exception as e:
            print(e)
            return None


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


class UserVerifyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserVerifySerializers
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserVerifySerializers
        elif self.action == "create":
            return UserDetailSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
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



