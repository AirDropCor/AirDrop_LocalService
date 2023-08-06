import socket
from flask import Flask
from flask_cors import CORS
from Controller.MessageController import message_app  # 从 message_controller.py 中导入蓝图

app = Flask(__name__)
CORS(app)

# 创建一个用于存储消息的栈
message_stack = []

# 定义消息栈的最大大小
MAX_STACK_SIZE = 30


def get_ip_address():
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    matching_ips = [ip for ip in ip_addresses if ip.startswith('192.168')][0]
    print("本机ip为: " + matching_ips)
    return matching_ips


if __name__ == "__main__":
    SERVER_IP = get_ip_address() or 'localhost'
    with open('config.ts', 'w') as f:
        f.write(f"const SERVER_IP = '{SERVER_IP}';\nexport default SERVER_IP;\n")

    # 将 message_app 蓝图注册到主程序中
    app.register_blueprint(message_app)

    app.run(host=SERVER_IP, port=5230)
