DELIMITING_CHAR = '|'

class Message:
    def __init__(self,sender_id,receiver_id,tag,content):
        self.sender_id = int(sender_id)
        self.receiver_id = int(receiver_id)
        self.tag = tag
        self.content = content

    def match_message(self,other_message):
        return self.sender_id == other_message.sender_id and \
               self.receiver_id == other_message.receiver_id and \
               self.tag == other_message.tag and \
               self.content == other_message.content

    def __str__(self):

        return f'SENDER_ID:{self.sender_id}\nRECEIVER_ID:{self.receiver_id}\nTAG:{self.tag}\nCONTENT:{self.content}\n'

class MessageHandler:
    def __init__(self):
        pass

    def get_decoded_message(self,data):

        decoded_message = data.decode().strip()
        parts = decoded_message.split("|")
        if len(parts) != 4:
            print("Invalid message : f{decoded_message}")
            return None
        return Message(*parts)

    def get_encoded_message(self,message):

        message = str(message.sender_id) + DELIMITING_CHAR + \
                  str(message.receiver_id) + DELIMITING_CHAR + \
                  message.tag + DELIMITING_CHAR + \
                  message.content

        return message.encode()