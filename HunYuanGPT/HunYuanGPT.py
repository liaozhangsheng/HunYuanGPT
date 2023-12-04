import requests
import json


class ChatBot:
    """
    A class representing a chatbot that interacts with the HunYuan API.
    """

    BASE_URL = "https://hunyuan.tencent.com/api"

    def __init__(
        self,
        cookie: str,
        chatId: str = "new",
        autoCreateConversation: bool = True
    ):
        """
        Initializes a ChatBot instance.

        Args:
            cookie (str): The cookie value used for authentication.
            chatId (str, optional): The ID of the conversation. Defaults to "new".
            autoCreateConversation (bool, optional): Whether to automatically create a new conversation. Defaults to True.
        """
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": cookie
        }

        if chatId == "new":
            self._create_conversation()
        else:
            self._chatId = chatId

        self.autoCreateConversation = autoCreateConversation

    def _create_conversation(self):
        """
        Creates a new conversation and returns its ID.

        Returns:
            str: The ID of the created conversation.

        Raises:
            Exception: If creating the conversation fails.
        """
        url = f"{self.BASE_URL}/generate/id"
        chatId = requests.post(url, headers=self.__headers).text

        if chatId == None:
            raise Exception("Create conversation failed.")

        self._chatId = chatId

        return chatId

    def change_converstation(self, chatId: str):
        """
        Changes the current conversation to the one with the specified ID.

        Args:
            chatId (str): The ID of the conversation to change to.
        """
        self._chatId = chatId

    def set_conversation_name(self, name: str, chatId: str = None):
        """
        Sets the name of the conversation.

        Args:
            name (str): The name to set for the conversation.
            chatId (str, optional): The ID of the conversation. Defaults to None.

        Raises:
            Exception: If setting the conversation name fails.
        """
        if chatId == None:
            chatId = self._chatId

        url = f"{self.BASE_URL}/conv/title/{self._chatId}"
        payload = {
            "title": name
        }

        response = requests.post(url, headers=self.__headers, json=payload)

        if response.status_code != 200:
            raise Exception("Set conversation name failed.")

    def get_conversation(self, chatId: str = None):
        """
        Retrieves the conversation with the specified ID.

        Args:
            chatId (str, optional): The ID of the conversation. Defaults to None.

        Returns:
            requests.Response: The response object containing the conversation data.

        Raises:
            Exception: If getting the conversation fails.
        """
        if chatId == None:
            chatId = self._chatId

        url = f"{self.BASE_URL}/conv/{chatId}"
        response = requests.get(url, headers=self.__headers)

        if response.status_code != 200:
            raise Exception(
                "Get conversation failed, please check your chatId")

        return response.json()

    def get_all_conversations(self):
        """
        Retrieves all conversations.

        Returns:
            str: A JSON string containing the IDs and titles of all conversations.

        Raises:
            Exception: If getting all conversations fails.
        """
        url = f"{self.BASE_URL}/convs?orderBy=last&source=web&limit=40&offset=0&chatType=0"
        response = requests.get(url, headers=self.__headers)

        if response.status_code != 200:
            raise Exception("Get all conversations failed.")

        result = []
        for conversation in response.json():
            result.append(
                {"id": conversation["id"], "title": conversation["title"]})

        return result

    def clear_all_conversations(self):
        """
        Clears all conversations.

        Raises:
            Exception: If clearing all conversations fails.
        """
        url = f"{self.BASE_URL}/convs/clear"
        payload = {"chatType": 0}
        response = requests.post(url, headers=self.__headers, json=payload)

        if response.status_code != 200:
            raise Exception("Clear all conversations failed.")

    def ask_stream(
        self,
        prompt: str,
        chatId: str = None,
        is_skip_history: bool = False
    ):
        """
        Sends a message to the chatbot and receives the streaming response.

        Args:
            prompt (str): The prompt message to send to the chatbot.
            chatId (str, optional): The ID of the conversation. If not provided, the default chatId will be used. Defaults to None.
            is_skip_history (bool, optional): Whether to skip the chat history. Defaults to False.

        Yields:
            str: The response messages from the chatbot.
        """
        if chatId == None:
            chatId = self._chatId

        url = f"{self.BASE_URL}/conv/{chatId}"
        response = requests.get(url, headers=self.__headers)

        if self.autoCreateConversation:
            try:
                if len(response.json()["convs"]) == 40:
                    print("Conversation full, create new conversation.")
                    self._chatId = self._create_conversation()
            except:
                pass

        payload = {
            "model": "gpt_175B_0404",
            "prompt": prompt,
            "display_prompt": prompt,
            "display_prompt_type": 1,
            "plugin": "Adaptive",
            "is_skip_history": is_skip_history
        }
        url = f"{self.BASE_URL}/chat/{chatId}"
        response = requests.post(
            url, headers=self.__headers, json=payload, stream=True)

        if response.status_code != 200:
            print(payload)
            print(url)
            raise Exception("Ask failed.")

        _ = 0
        for line in response.iter_lines():
            if _ <= 3:
                _ += 1
                continue

            if not line:
                continue

            line = line.decode("utf-8")[6:]
            if line == "[plugin: ]":
                break

            rsp = json.loads(line)

            if rsp["type"] == "text":
                yield rsp["msg"]
            elif rsp["type"] == "progress":
                continue
            else:
                yield rsp["imageUrlHigh"]
                break

    def ask(
        self,
        prompt: str,
        chatId: str = None,
        is_skip_history: bool = False
    ):
        """
        Sends a message to the chatbot and receives the response.

        Args:
            prompt (str): The prompt message to send to the chatbot.
            chatId (str, optional): The ID of the conversation. If not provided, the default chatId will be used. Defaults to None.
            is_skip_history (bool, optional): Whether to skip the chat history. Defaults to False.

        Returns:
            str: The response message from the chatbot.
        """
        response = self.ask_stream(
            prompt=prompt, chatId=chatId, is_skip_history=is_skip_history)

        full_response = "".join(response)

        return full_response

    def repeat_last_reply(self, prompt: str = None):
        """
        Repeats the last reply in the conversation.

        Args:
            prompt (str): The prompt message to send to the chatbot.

        Raises:
            Exception: If repeating the last reply fails.
        """
        url = f"{self.BASE_URL}/chat/repeat/{self._chatId}"
        payload = {
            "model": "gpt_175B_0404",
            "prompt": prompt,
            "plugin": "Adaptive",
            "isSkipHistory": False
        }
        response = requests.post(url, headers=self.__headers, json=payload)

        if response.status_code != 200:
            raise Exception("Repeat last reply failed.")
        
        full_response = ""
        _ = 0
        for line in response.iter_lines():
            if _ <= 3:
                _ += 1
                continue

            if not line:
                continue

            line = line.decode("utf-8")[6:]
            if line == "[plugin: ]":
                break

            rsp = json.loads(line)

            if rsp["type"] == "text":
                full_response += rsp["msg"]
            elif rsp["type"] == "progress":
                continue
            else:
                full_response =  rsp["imageUrlHigh"]
                break

        return full_response

    def restart_conversation(self):
        """
        Restarts the conversation.

        Raises:
            Exception: If restarting the conversation fails.
        """
        url = f"{self.BASE_URL}/stop/conversation/{self._chatId}"
        response = requests.post(url, headers=self.__headers)

        if response.status_code != 200:
            raise Exception("Restart conversation failed.")

    def get_image(self, prompt: str,  name: str = None, path: str = "./images"):
        """
        Get an image based on the provided prompt and save it to the specified path with the given name.
        
        Args:
            prompt (str): The prompt used to generate the image.
            path (str): The path where the image will be saved.
            name (str): The name of the image file. If None, an unused index will be used as the name.
        
        Returns:
            str: The link to the image.
        """

        print("Getting image...")
        
        link = self.ask(f"请根据信息绘制一张图片：{prompt}")

        print(
            """
            Successfully get the image. 
            Saving image...
            """
        )

        import contextlib
        import os

        with contextlib.suppress(FileExistsError):
            os.mkdir(path)

        if name is None:
            # Find an unused index for the image name
            index = 0
            while os.path.exists(f"{path}/{index}.png"):
                index += 1
            name = str(index)

        with open(f"{path}/{name}.png", "wb") as f:
            f.write(requests.get(link).content)

        print(f"Image saved to {path}/{name}.png")        

        return link
