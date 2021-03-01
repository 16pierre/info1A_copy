import json

class Message(object):
    def __init__(self, msg_id, emetteur, contenu, verified):
        self.id = msg_id
        self.emetteur = emetteur
        self.contenu = contenu
        self.verified = verified
    
    def to_dict(self):
        return {
            "id": self.id,
            "emetteur": self.emetteur,
            "contenu": self.contenu,
            "verified": self.verified
        }

class MessageManager(object):
    def __init__(self):
        self.messages = {}
        self.next_msg_id = 0
    
    def add_message(self, emetteur, contenu, verified):
        message = Message(self.next_msg_id, emetteur, contenu, verified)
        self.messages[message.id] = message
        self.next_msg_id += 1
    
    def get_messages(self, count=30):
        messages = []
        idx = self.next_msg_id
        while len(messages) < count and idx >= 0:
            if idx in self.messages:
                messages.append(self.messages[idx].to_dict())
            idx -= 1
        
        return json.dumps(messages)