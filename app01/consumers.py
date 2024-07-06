# 【channels】（第4步）创建应用的消费者
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

# 使用异步时继承自AsyncWebsocketConsumer而不是WebsocketConsumer。
# 所有方法都是async def而不是def。
# await用于调用执行I / O的异步函数。
# 在通道层上调用方法时不再需要async_to_sync。
class AsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):  # 连接时触发
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notice_%s' % self.room_name  # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。

        # 将新的连接加入到群组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):  # 断开时触发
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 信息群发
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'system_message',
                'message': message
            }
        )

    # Receive message from room group
    async def system_message(self, event):
        print(event)
        message = event['message']

        # Send message to WebSocket单发消息
        await self.send(text_data=json.dumps({
            'message': message
        }))


# 同步方式，仅作示例，不使用
class SyncConsumer(WebsocketConsumer):
    def connect(self):
        # 从打开到使用者的WebSocket连接的chat/routing.py中的URL路由中获取'room_name'参数。
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('WebSocket建立连接：', self.room_name)
        # 直接从用户指定的房间名称构造通道组名称
        self.room_group_name = 'msg_%s' % self.room_name

        # 加入房间
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )  # async_to_sync(…)包装器是必需的，因为ChatConsumer是同步WebsocketConsumer，但它调用的是异步通道层方法。(所有通道层方法都是异步的。)

        # 接受WebSocket连接。
        self.accept()
        simple_username = self.scope["session"]["session_simple_nick_name"]  # 获取session中的值

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': '@{} 已加入房间'.format(simple_username)
            }
        )

    def disconnect(self, close_code):
        print('WebSocket关闭连接')
        # 离开房间
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从WebSocket中接收消息
    def receive(self, text_data=None, bytes_data=None):
        print('WebSocket接收消息：', text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 发送消息到房间
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 从房间中接收消息
    def chat_message(self, event):
        message = event['message']

        # 发送消息到WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

def send_group_msg(room_name, message):
    # 从Channels的外部发送消息给Channel
    """
    from assets import consumers
    consumers.send_group_msg('Reliability_Row_data', {'content': '这台机器硬盘故障了', 'level': 1})
    consumers.send_group_msg('Reliability_Row_data', {'content': '正在安装系统', 'level': 2})
    :param room_name:
    :param message:
    :return:
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notice_{}'.format(room_name),  # 构造Channels组名称
        {
            "type": "system_message",
            "message": message,
        }
    )

