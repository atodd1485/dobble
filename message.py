class RxMessage:
    def __init__(self,data):

        decoded_message = data.decode().strip()
        parts = decoded_message.split("|")
        if len(parts) != 3:
            print(f"Invalid message from{decoded_message}")
            return

        name, tag, content = parts

        self.name = name
        self.tag = tag
        self.content = content

    def match_message(self,other_message):
        return self.name == other_message.name and \
               self.tag == other_message.tag and \
               self.content == other_message.content
    def convert(self):
        return TxMessage(self.name,self.tag,self.content)   

class TxMessage:
    def __init__(self,name,tag,content):

        self.name = name
        self.tag = tag
        self.content = content

        message = self.name + '|' + self.tag + '|' +  self.content
        self.encoded_message = message.encode()

    def match_message(self,other_message):
        return self.name == other_message.name and \
               self.tag == other_message.tag and \
               self.content == other_message.content

    def convert(self):
        return RxMessage(self.encoded_message)
