import re
import time
import threading
import collections
from rocketchat_API.rocketchat import RocketChat


class RocketBot(RocketChat):
    def __init__(self, username, password, server_url, proxy_dict=None, threading_updates=False):
        super().__init__()
        self.bot_username = username
        self.session = RocketChat(username, password, server_url=server_url, proxies=proxy_dict)
        self._commands = {}
        self._threading = threading_updates

    def command(self, regex):
        def decorator(d):
            self._commands[regex] = d
        return decorator

    def send_message(self, chat_id, text):
        return self.session.chat_post_message(text, chat_id)

    def get_updates(self):
        return self.session.subscriptions_get().json()['update']

    def run(self, chat_type='', sleep=0):
        ids = collections.deque(maxlen=10000)
        while True:
            updates = self.get_updates()

            if updates:
                for result in updates:
                    chat_type = result['t']
                    room_id = result['rid']

                    # Check if it's a direct message or a channel message
                    if chat_type == "d":
                        # Retrieve message history for direct messages
                        messages = self.session.im_history(room_id).json()['messages']
                    elif chat_type == "c":
                        # Retrieve message history for channels
                        messages = self.session.channels_history(room_id).json()['messages']
                    else:
                        # Handle other types of chats if needed
                        continue

                    try:
                        if result['t'] == chat_type:
                            for message in messages:
                                if message['_id'] in ids or message['u']['username'] == self.bot_username:
                                    continue
                                ids.append(message['_id'])

                                def response_update():
                                    if message.get('unread', False):
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

                                if self._threading:
                                    threading.Thread(target=response_update).start()
                                else:
                                    response_update()
                    except Exception as e:
                        print(e)

            time.sleep(sleep)
