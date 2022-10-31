# RocketPyBot

## Python lib for create rocketchat bot with getupdate like TelegramBots

### Installation

```bash
pip install pyrocketbot
```

### Usage

```python
import os
from rocketpybot import RocketBot

username = os.environ.get('ROCKET_USERNAME')
password = os.environ.get('ROCKET_PASSWORD')
server_url = os.environ.get('ROCKET_SERVER_URL')

proxy_dict = {
    "http"  : "http://127.0.0.1:2080",
    "https" : "https://127.0.0.1:2080",
}

bot = RocketBot(username, password, server_url)
# bot = RocketBot(username, password, server_url, proxy_dict=proxy_dict)


@bot.command(r'/start')
def start(message, match_list):
    bot.send_message(message['rid'], 'hi')

@bot.command(r'/echo (.*)')
def echo(message, match_list):
    bot.send_message(message['rid'], match_list[0])


if __name__ == '__main__':
    print('Bot started')
    bot.run(chat_type='d', sleep=0.5)
```

### Note : 
in run method you can set `chat_type` to 'd' for direct message or 'c' for channel message and set `sleep` for sleep time per update


