from flask import jsonify, request, Blueprint
from Service.MessageService import MessageService


class MessageController:
    def __init__(self):
        self.message_service = MessageService()

    def get_all_messages(self):
        messages = self.message_service.get_messages()
        return jsonify({'messages': messages})

    def add_new_message(self, data):
        message = data.get('message')
        if not message:
            return jsonify({'error': 'Invalid message'}), 400
        self.message_service.add_message(message)
        return jsonify({'message': 'Message added successfully'}), 201


message_app = Blueprint('message_app', __name__)

# 创建 MessageController 实例
message_controller = MessageController()


# 在蓝图中定义路由
@message_app.route('/messages', methods=['GET'])
def get_messages():
    return message_controller.get_all_messages()


@message_app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    return message_controller.add_new_message(data)
