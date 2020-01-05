#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/12 0012 10:45
# @Author  : LiangLiang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.contrib import admin
from django.urls import path, include
from userapi.views import *


urlpatterns = [
    path('login', UserSerializersViewSet.as_view())

]