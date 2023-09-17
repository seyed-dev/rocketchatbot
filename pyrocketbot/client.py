import re
import time
import threading
import collections
from rocketchat_API.rocketchat import RocketChat
from datetime import datetime, timezone


class RocketBot(RocketChat):
    _commands = {}
    
    def __init__(self, username, password, server_url, proxy_dict=None, threading_updates=False):
        super().__init__()
        self.bot_username = username
        self.session = RocketChat(username, password, server_url=server_url, proxies=proxy_dict)
        self._threading = threading_updates
        self.last_processed_timestamp = self.get_current_utc_timestamp()

    @staticmethod
    def get_current_utc_timestamp():
        """Get the current UTC timestamp in the same format as the messages."""
        return datetime.now(timezone.utc).isoformat()
        
    @classmethod
    def command(cls, regex):
        def decorator(d):
            print(f"Registering command: {regex}")  # Add this print statement
            cls._commands[regex] = d  # Use the class-level attribute here
        return decorator

    def send_message(self, chat_id, text):
        return self.session.chat_post_message(text, chat_id)

    def get_updates(self):
        response = self.session.subscriptions_get().json()
        return response.get('update')

    def run(self, chat_type='', sleep=0):
        print(f"Registered commands: {self._commands.keys()}")
        ids = collections.deque(maxlen=10000)
        while True:
            updates = self.get_updates()

            if updates:
                for result in updates:
                    try:
                        chat_type = result['t']
                        room_id = result['rid']
                       # room_id = '65076c815118b3aefcbd7e77'
                        
                        if chat_type == "d":
                            response = self.session.im_history(room_id).json()
                            messages = response.get('messages', [])
                        elif chat_type == "c":
                            response = self.session.channels_history(room_id).json()
                            messages = response.get('messages', [])
                        elif chat_type == "p":
                            response = self.session.groups_history(room_id).json()
                            messages = response.get('messages', [])
                        else:
                            continue

                        if result['t'] == chat_type:
                            for message in messages:
                                #print(f"Processing message: {message['msg']}")
                                if message['_id'] in ids or message['u']['username'] == self.bot_username:
                                    continue
                                ids.append(message['_id'])

                                # if not message.get('unread', False):
                                #     continue

                                message_timestamp = message['ts']
                                if self.last_processed_timestamp and message_timestamp <= self.last_processed_timestamp:
                                    continue

                                for k, v in self._commands.items():
                                    regex = re.compile(k, flags=re.MULTILINE | re.DOTALL)
                                    m = regex.match(message['msg'])

                                    if m:
                                        match_list = []
                                        for x in m.groups():
                                            match_list.append(x)
                                        try:
                                            v(message, match_list)
                                        except TypeError:
                                            v(message)

                    except Exception as e:
                        print(f'Error: {e} in {result}')

            time.sleep(sleep)
