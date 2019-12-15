#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 0014 15:03
# @Author  : LiangLiang
# @Site    :
# @File    : adminx.py
# @Software: PyCharm
import xadmin
from xadmin import views
from .models import *


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    """
    后台修改
    """
    site_title = '志愿平台后台管理系统'
    site_footer = '志愿平台'
    # menu_style = 'accordion'  # 开启分组折叠


class UserAdmin:
    name = "用户1"
    verbose_name = "用户中心"
    list_display = ['username', 'email', 'city']
    list_filter = ['email', 'username', 'school']
    search_fields = ['email']

    # fields = ['total_score']


# xadmin.site.register(User, UserAdmin)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)

