from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
# Create your models here.


# class GroupManager(UserManager):
#     """
#     原生的只支持用户名和密码注册,实际上已经有手机注册,微信等第三方注册了, TODO:  待优化
#     """
#     objects = UserManager()
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#     ahah = models.CharField(max_length=100)
#     django_type = models.IntegerField(default=0, primary_key=True)



class User(AbstractUser):
    id = models.IntegerField(auto_created=True, default=0)
    username = models.CharField(max_length=255, null=True,  verbose_name="用户",
                                help_text="登陆用的用户名", blank=True, db_index=True, unique=True)
    password = models.CharField(max_length=255, null=False, help_text="密码")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    alias = models.CharField(max_length=255, null=True, help_text="昵称")  # 昵称, 可以重复

    nation = models.CharField(null=True, blank=True, max_length=15, verbose_name="汉族", help_text="汉族")
    mobile_phone = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    email = models.EmailField(max_length=255, null=True, blank=True, db_index=True)
    head_picture = models.ImageField(max_length=200, upload_to="users/images/headpicture/%Y/%m", null=True,
                                     blank=True, )

    rel_name = models.CharField(max_length=40, null=True, blank=True)
    total_score = models.FloatField(default=0, null=True, blank=True)

    sign_in_datetime = models.DateTimeField(auto_now=True, null=True)
    sign_in_ip = models.GenericIPAddressField(max_length=255, null=True)
    birthday = models.DateTimeField(null=True)
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=40, null=True)
    school = models.CharField(max_length=255, null=True)
    address = models.CharField(null=True, blank=True, max_length=50, verbose_name="家庭地址", help_text="家庭地址")

    user_id = models.AutoField(primary_key=True, unique=True, null=False, blank=False, auto_created=True)

    # groups = models.CharField()
    is_active = models.BooleanField('已激活', default=True, help_text="是否邮箱验证通过了")
    is_deleted = models.BooleanField(default=False, null=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "用户表"
        verbose_name = "用户表"
        verbose_name_plural = "用户表"
        index_together = ["username", "email", "mobile_phone"]

    def __str__(self):
        return "用户信息表"

    def __unicode__(self):
        return "用户信息表"


class UserSignInfoRecord(models.Model):
    sign_in_way_choice = (
        (1, "mobile_phone"),
        (2, "email"),
        (3, "weixin_auth"),
        (4, "qq_auth"),
        (5, "weibo_auth"),
        (6, "others")

    )
    user = models.ForeignKey(to=User, on_delete=False)
    sign_in_ip = models.GenericIPAddressField(max_length=155, null=False, default="0.0.0.0")
    sign_time = models.DateTimeField(auto_created=True,)
    sign_in_way = models.IntegerField(choices=sign_in_way_choice, null=False, default=1)

    class Meta:
        db_table = "用户注册信息表"
        index_together = ["user", "sign_time"]


class UserLoginRecord(models.Model):
    choice = (
        (1, "登陆"),
        (2, "登出")
    )
    user = models.ForeignKey(User, on_delete=True)
    user_ip = models.GenericIPAddressField(max_length=100, null=True)
    actions_types = models.CharField(max_length=100, choices=choice, null=True)
    action_time = models.DateTimeField(auto_now=True, null=True)
    other_info = models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table = "用户的登陆登出记录表"
        index_together = ["user", "actions_types", "action_time"]


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile_phone = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(auto_now=True,  verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
