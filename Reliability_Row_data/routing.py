# 【channels】（第2步）设置默认路由在项目创建routing.py文件

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import app01.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 【channels】（第6步）添加路由配置指向应用的路由模块
    'websocket': SessionMiddlewareStack(  # 使用Session中间件，可以请求中session的值
        URLRouter(
            app01.routing.websocket_urlpatterns
        )
    ),
})
