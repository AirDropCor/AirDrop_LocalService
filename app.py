import socket
from flask import Flask
from flask_cors import CORS
import asyncio
import websockets

app = Flask(__name__)
CORS(app)

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


def get_ip_address():
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    matching_ips = [ip for ip in ip_addresses if ip.startswith('192.168')][0]
    print("本机ip为: " + matching_ips)
    return matching_ips

if __name__ == "__main__":
    SERVER_IP = get_ip_address() or 'localhost'
    with open('config.ts', 'w') as f:
        f.write(f"const SERVER_IP = '{SERVER_IP}';\nexport default SERVER_IP;\n")
    start_server = websockets.serve(handle_websocket, get_ip_address(), 5230)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
K