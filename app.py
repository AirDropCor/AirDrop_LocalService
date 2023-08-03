import socket
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create a stack to store messages
message_stack = []

# Define the maximum size of the message stack
MAX_STACK_SIZE = 30

# GET请求，获取所有消息
@app.route('/messages', methods=['GET'])
def get_messages():
    global message_stack

    # Return the entire message stack as a JSON response
    return jsonify({'messages': message_stack})

# POST请求，添加新消息
@app.route('/messages', methods=['POST'])
def post_message():
    global message_stack

    # Get the message from the request's JSON data
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Invalid message'}), 400

    # Insert the new message at the beginning of the stack
    message_stack.insert(0, message)

    # Keep the stack size within the limit by popping the oldest message if necessary
    if len(message_stack) > MAX_STACK_SIZE:
        message_stack.pop()

    return jsonify({'message': 'Message added successfully'}), 201  # 使用201状态码表示创建成功


def get_ip_address():
    ip_addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    matching_ips = [ip for ip in ip_addresses if ip.startswith('192.168')][0]
    print("本机ip为: " + matching_ips)
    return matching_ips

if __name__ == "__main__":
    SERVER_IP = get_ip_address() or 'localhost'
    with open('config.ts', 'w') as f:
        f.write(f"const SERVER_IP = '{SERVER_IP}';\nexport default SERVER_IP;\n")
    app.run(host=SERVER_IP, port=5230)