from flask import Flask
from flask_cors import CORS
import asyncio
import websockets

app = Flask(__name__)
CORS(app)
ip = "192.168.10.101"

# 用于存储所有客户端的 WebSocket 连接对象
clients = set()

async def handle_websocket(websocket, path):
    try:
        # 添加当前连接的 WebSocket 到 clients 集合
        clients.add(websocket)

        async for message in websocket:
            print('收到消息：', message)

            # 在这里你可以处理收到的消息，并根据需要发送消息给客户端
            response = f"服务器已收到消息：{message}"

            # 将消息发送给所有连接的客户端
            await asyncio.gather(*[client.send(response) for client in clients])
    except websockets.exceptions.ConnectionClosedError:
        print('WebSocket连接已关闭')
        # 移除断开的 WebSocket 连接
        clients.remove(websocket)



if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket, ip, 5230)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
