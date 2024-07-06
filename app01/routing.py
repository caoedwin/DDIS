# 【channels】（第5步）为应用程序创建一个路由配置，该应用程序具有到消费者的路由
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/msg/(?P<room_name>[^/]+)/$', consumers.SyncConsumer),
    url(r'^ws/msg/(?P<room_name>[^/]+)/$', consumers.AsyncConsumer),
]
