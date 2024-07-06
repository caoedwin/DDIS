from rest_framework.authentication import TokenAuthentication
from app01.models import UserToken, Role, UserInfo
from rest_framework.exceptions import AuthenticationFailed # 用于抛出错误信息

class MyOwnTokenAuthentication(TokenAuthentication):
    model = UserToken

    # def authenticate(self, request):
    #     # """自定义的认证类中必须有此方法以及如下的判断和两个返回值"""
    #     # # 1. 获取token
    #     # # print(request,1)
    #     # # print(request.query_params,2)
    #     # token = request.query_params.get('token')
    #     # # print(token)
    #     # # 2. 判断是否成功获取token
    #     # if not token:
    #     #   raise AuthenticationFailed("缺少token")
    #     # # 3. 判断token是否合法
    #     # try:
    #     #   user_obj = UserInfo.objects.filter(token=token).first()
    #     # except Exception:
    #     #   raise AuthenticationFailed("token不合法")
    #     # # 4. 判断token在数据库中是否存在
    #     # if not user_obj:
    #     #   raise AuthenticationFailed("token不存在")
    #     # # 5. 认证通过
    #     # return (user_obj, token)	# 两个值user_obj赋值给了request.user；token赋值给了request.auth
    #     # # 注意，权限组件会用到这两个返回值
    #
    #     # print(request.query_params)
    #     # username = request.data.get('username', '')
    #     # password = request.data.get('password', '')
    #     username = request.query_params.get('username', '')
    #     password = request.query_params.get('password', '')
    #     token = request.query_params.get('token', '')
    #     # print(token)
    #     # print(username, password)
    #     # if request.session.get('is_login', None):
    #     #     # print('1',request.session.get('account'))
    #     #     user_obj = UserInfo.objects.filter(account=request.session.get('account')).first()
    #     # else:
    #     #     user_obj = UserInfo.objects.filter(account=username, password=password).first()
    #     group = Role.objects.filter(name="API_CQM").first()
    #     user_obj = None
    #     if UserInfo.objects.filter(account=username, password=password).first():
    #         groups = UserInfo.objects.filter(account=username, password=password).first().role.all()
    #         # print(groups)
    #         if group in groups:
    #             user_obj = UserInfo.objects.filter(account=username, password=password).first()
    #     # print(user_obj)
    #     if user_obj:
    #         pass
    #     else:
    #         raise AuthenticationFailed("账户密码不正确")
    #     return (user_obj, token)  # 必须要返回两个值，两个值user_obj赋值给了request.user；token赋值给了request.auth