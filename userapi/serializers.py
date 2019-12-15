#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/12 0012 10:42
# @Author  : LiangLiang
# @Site    :
# @File    : serializers.py
# @Software: PyCharm
from .models import *
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

