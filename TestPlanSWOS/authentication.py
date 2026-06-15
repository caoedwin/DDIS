from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from app01.models import UserInfo, Role


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录认证，使用自有用户表
    """
    username_field = 'username'

    def validate(self, attrs):
        authenticate_kwargs = {'account': attrs[self.username_field], 'password': attrs['password']}
        try:
            user = UserInfo.objects.get(**authenticate_kwargs)
        except Exception as e:
            raise exceptions.NotFound(e.args[0])

        refresh = self.get_token(user)
        # 只有指定 role 的用户才能获取 Token
        if Role.objects.filter(name="API_CQM").first() not in user.role.all() and \
           Role.objects.filter(name="admin").first() not in user.role.all():
            raise AuthenticationFailed("没有权限")
        data = {"userId": user.id, "token": str(refresh.access_token), "refresh": str(refresh)}
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    authentication_classes = []          # 允许未认证访问
    permission_classes = [AllowAny]      # 允许任何用户


class MyJWTAuthentication(JWTAuthentication):
    """
    修改JWT认证类，返回自定义User表对象
    """
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')
        return user