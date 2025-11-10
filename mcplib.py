import queue

class MCPMessage:
    def __init__(self, sender, receiver, msg_type, payload):
        self.sender = sender
        self.receiver = receiver
        self.msg_type = msg_type      # e.g. 'query', 'context', 'result'
        self.payload = payload

class MCPBus:
    def __init__(self):
        self.queues = {}

    def register_agent(self, name):
        if name not in self.queues:
            self.queues[name] = queue.Queue()

    def send_message(self, message):
        if message.receiver in self.queues:
            self.queues[message.receiver].put(message)

    def get_message(self, agent_name):
        try:
            return self.queues[agent_name].get_nowait()
        except queue.Empty:
            return None

class BaseAgent:
    def __init__(self, name, bus):
        self.name = name
        self.bus = bus
        self.bus.register_agent(name)

    def send(self, receiver, msg_type, payload):
        msg = MCPMessage(sender=self.name, receiver=receiver, msg_type=msg_type, payload=payload)
        self.bus.send_message(msg)

    def receive(self):
        return self.bus.get_message(self.name)