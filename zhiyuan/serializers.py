#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/12 0012 10:42
# @Author  : LiangLiang
# @Site    :
# @File    : serializers.py
# @Software: PyCharm
from .models import *
from rest_framework import serializers
from company_website.settings import REGEX_MOBILE
import re
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


class SchooleOverViewItemSerializer(serializers.ModelSerializer):
    """
    用户登录后的，个人主页的详细信息
    """
    class Meta:
        model = SchoolOverViewItem
        fields = "__all__"


class SchoolFilterSerializer(serializers.Serializer):
    provinces = serializers.ListField()
    is_985 = serializers.BooleanField()
    is_211 = serializers.BooleanField()
    tags = serializers.ListField()

