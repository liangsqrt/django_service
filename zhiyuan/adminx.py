import xadmin
from xadmin import views
from .models import *


# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True


# class GlobalSettings:
#     """
#     后台修改
#     """
#     site_title = '志愿平台找大学功能'
#     site_footer = '志愿平台'
#     # menu_style = 'accordion'  # 开启分组折叠


class SchoolOverView:
    name = "找大学-学校概览"
    verbose_name = "找大学-学校概览"
    list_display = ['name']
    list_filter = ['name', 'province', 'is_985', 'is_211']
    search_fields = ['name', 'address']

    # fields = ['total_score']


xadmin.site.register(SchoolOverViewItem, SchoolOverView)
# xadmin.site.register(views.CommAdminView, GlobalSettings)
# xadmin.site.register(views.BaseAdminView, BaseSetting)

