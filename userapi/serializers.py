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


class UserSerializers(serializers.ModelSerializer):
    """
    用户登录后的，个人主页的详细信息
    """
    password = serializers.CharField(write_only=True)
    is_activate = serializers.CharField(write_only=True)
    is_deletes = serializers.CharField(write_only=True)
    is_staff = serializers.CharField(write_only=True)
    code = serializers.IntegerField(default=400)
    msg = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = "__all__"


class SmsSerializer(serializers.Serializer):
    """
    手机验证码的serializer，
    """
    mobile_phone = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile_phone=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile_phone=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserSignInSerializers(serializers.ModelSerializer):
    """
    用户注册时要用到的字段，用于注册后返回时数据
    """
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile_phone=self.initial_data["mobile_phone"]).order_by("-add_time")

        if verify_records:
            last_record = verify_records[0]
            three_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=3)
            if last_record.add_time.replace(tzinfo=None) < three_minutes_ago:
                raise serializers.ValidationError("验证码过期！！")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误！！")
        else:
            raise serializers.ValidationError("验证码错误！！")

    def validate(self, attrs):
        """
        作用与所有字段上， attrs是你serializer所有的字段，跟validate_code有区别，这个判断函数发生在所有的validate_xxx之后
        :param attrs:
        :return:
        """
        # attrs["mobile"] = attrs["username"]
        del attrs["code"]  # 已经验证过了，没用了
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ("username", "code", "mobile_phone", "password")  # serializer和user字段的合集


class UserLoginSerializer(serializers.Serializer):
    """
    用户详情序列化类， 用户已经注册过后，登录后所需的字段
    """
    verify_code = serializers.CharField(required=True, help_text="验证码")
    username = serializers.CharField(required=True, help_text="用户名")
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            # todo: 需要加强，如验证码
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field='username')
            raise serializers.ValidationError(msg)

    class Meta:
        model = User
        fields = ("username", "password", "verify_code", )


