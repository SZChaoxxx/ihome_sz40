from .models import User
from django.contrib.auth.backends import ModelBackend
import re


def get_user_by_account(account):
    """判断account是否为手机号， 返回user对象"""

    try:
        if re.match(r'^1[3-9]\d{9}$',account):
    # account是手机号
    # 根据手机号从数据库获取user对象返回
            user = User.objects.get(mobile=account)
        else:
            # account是用户名
            # 根据用户名从数据库获取user对象返回
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        # 如果account 不存在（既不是用户名也不是手机号）
        return None
    else:
        return user


# 继承自 ModelBackend，重写 authenticate函数
class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法，实现用户名和mobile登录功能
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return user
        """
        # 自定义验证用户是否存在的函数：
        # 根据传入的 username 获取 user对象
        # username可以是手机号也可以是账号
        user = get_user_by_account(account=username)
        # 校验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            # 如果user存在，密码正确，则返回user
            return user
