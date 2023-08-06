MAX_STACK_SIZE = 30


class MessageService:
    def __init__(self):
        self.message_stack = []

    def get_messages(self):
        return self.message_stack

    def add_message(self, message):
        self.message_stack.insert(0, message)
        if len(self.message_stack) > MAX_STACK_SIZE:
            self.message_stack.pop()
