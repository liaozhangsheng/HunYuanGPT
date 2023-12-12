<div align="center">

<img src="https://xj-psd-1258344703.cos.ap-guangzhou.myqcloud.com/image/hunyuan/logo/animation/welcome-web-repeat.gif" alt="HunYuanGPT" width="200"/>

# HunYuanGPT

_混元大模型逆向api_

</div>

## 安装模块

```bash
pip install HunYuanGPT --upgrade
```

## 获取cookie

1. 你需要一个拥有腾讯混元大模型体验资格的账号。
2. 打开[腾讯混元助手](https://hunyuan.tencent.com/bot/chat)
3. 打开浏览器开发者模式，切换到`network`选项卡，随便发送一条信息，找到一个有效的的请求，获取`cookie`字段的值。

## 使用聊天机器人

### 从命令行运行

```bash
$ python -m HunYuanGPT -h

             _    _         __     __                 _____ _____ _______ 
            | |  | |        \ \   / /                / ____|  __ \__   __|
            | |__| |_   _ _ _\ \_/ /   _  __ _ _ __ | |  __| |__) | | |   
            |  __  | | | | '_ \   / | | |/ _` | '_ \| | |_ |  ___/  | |   
            | |  | | |_| | | | | || |_| | (_| | | | | |__| | |      | |   
            |_|  |_|\__,_|_| |_|_| \__,_|\__,_|_| |_|\_____|_|      |_|   


Type /help for help.
Alt + Enter to send a message.

usage: __main__.py [-h] [--cookie_file_path COOKIE_FILE_PATH] [--no_stream]

options:
  -h, --help            show this help message and exit
  --cookie_file_path COOKIE_FILE_PATH
                        The path to the cookie file.
  --no_stream           Whether to use streaming mode.
```

### 在代码中运行

```python
from HunYuanGPT import ChatBot

bot = ChatBot(cookie="xxxxxxxx")

# Streaming output
for rsp in bot.ask_stream("你好！你叫什么名字？"):
    print(rsp, end="", flush=True)

# Normal output
print(bot.ask("你好！你叫什么名字？"))

# Generate images
# Images are named numerically by default and are saved in the./images folder.
# Of course, you can specify these parameters.
bot.get_image("赛博朋克风格的上海街头", path="./", name="img")
```

#### 其他用法

```python

# Switch to conversation with chatId "xxxxxx"
bot.change_conversation(chatId="xxxxxx")

# Set the name of conversation with chatId "xxxxxx" to "xxx"
bot.set_conversation_name(name="xxx", chatId="xxxxxx")

# Get the history of conversation with chatId "xxxxxx"
bot.get_conversation(chatId="xxxxxx")

# Get chatId and titles of all conversations
bot.get_all_conversations()

# Clear all conversations
bot.clear_all_conversations()

# Repeat the last reply
bot.repeat_last_reply()

# Forget the history and continue the conversation
bot.restart_conversation()
```