from django.shortcuts import render
from .serializers import UserSerializers
from .models import User
from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import IsAuthenticated
from django.http.response import HttpResponse
from django.contrib.auth import get_user_model


class UserSerilizersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'ps'
    page_query_param = 'p'
    max_page_size = 30


class UserSerializersView(mixins.ListModelMixin, viewsets.GenericViewSet):
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
            # user = get_user_model()
            # user.check_password(password)
            if user.check_password(password):  # check_password() 时会转化为密文的形式
                return user
        except Exception as e:
            print(e)
            return None
