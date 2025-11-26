class EventHandlerKey:

    def __init__(self,callback,rate_limit,event_type,event_key=None):

        self.last_trigger = 0
        self.callback = callback
        self.event_type = event_type
        self.event_key = event_key
        self.rate_limit = rate_limit

    def check(self,pygame_event,now):
        if (now - self.last_trigger) <= self.rate_limit:
            return
        if pygame_event.type == self.event_type:
            if self.event_key is not None and pygame_event.key != self.event_key:
                return
            self.last_trigger = now
            self.callback()

class EventHandlerNetwork:

    def __init__(self,callback,rate_limit,tx_message):

        self.last_trigger = 0
        self.callback = callback
        self.rate_limit = rate_limit
        self.tx_message = tx_message

    def check(self,message,now):      
        if (now - self.last_trigger) <= self.rate_limit:
            return
        if message.match_message(self.tx_message):
            self.last_trigger = now
            self.callback()
