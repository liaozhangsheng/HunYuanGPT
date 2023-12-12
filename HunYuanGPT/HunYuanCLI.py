import sys
import argparse
from .rich_messages import MessageBlock


from .HunYuanGPT import ChatBot
from .utils import *
from . import __version__


class ChatBotCLI(ChatBot):
    """
    A class representing a chatbot that interacts with the HunYuanGPT in the command line.
    """

    def print_help(self):
        print(
            """
            Commands:
                /help:              Print this help message.
                /clear:             Clear all conversations.
                /list:              List all conversations.
                /history:           List the chat history of the current conversation.
                /setName:           Set the name of the current conversation.
                /restart:           Restart the current conversation.
                /new:               Create a new conversation.
                /change:            Change the current conversation.
                /exit:              Exit the program.
            """
        )

    def handle_commands(self, prompt: str):
        command, *value = prompt.split(" ")

        if command == "/help":
            self.print_help()
        elif command == "/clear":
            print("Are you sure to clear all conversations? (y/n)")
            if input() == "y":
                self.clear_all_conversations()
                print("All conversations cleared.")
                self._create_conversation()
        elif command == "/list":
            print(self.get_all_conversations())
        elif command == "/history":
            print(self.get_conversation())
        elif command == "/name":
            self.set_conversation_name(" ".join(value[0]))
            print(f"Conversation name set as {value[0]}.")
        elif command == "/restart":
            self.restart_conversation()
            print("Conversation restarted.")
        elif command == "/new":
            self._create_conversation()
            print(f"New conversation created, chatId: {self._chatId}.")
        elif command == "/change":
            self.change_converstation(value[0])
            print(f"Conversation changed to {value[0]}.")
        elif command == "/exit":
            Bye()


def Bye():
    print("\nBye......")
    sys.exit()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cookie_file_path",
        type=str,
        help="The path to the cookie file."
    )
    parser.add_argument(
        "--no_stream",
        action="store_true",
        help="Whether to use streaming mode."
    )

    args = parser.parse_args()

    if args.cookie_file_path == None:
        print("Please specify the path to the cookie file.")
        sys.exit()

    try:
        with open(args.cookie_file_path, "r") as f:
            cookie = f.read()
    except Exception as e:
        print(e)
        sys.exit()

    HunYuanBot = ChatBotCLI(cookie=cookie)

    print(f"""
             _    _         __     __                 _____ _____ _______ 
            | |  | |        \ \   / /                / ____|  __ \__   __|
            | |__| |_   _ _ _\ \_/ /   _  __ _ _ __ | |  __| |__) | | |   
            |  __  | | | | '_ \   / | | |/ _` | '_ \| | |_ |  ___/  | |   
            | |  | | |_| | | | | || |_| | (_| | | | | |__| | |      | |   
            |_|  |_|\__,_|_| |_|_| \__,_|\__,_|_| |_|\_____|_|      |_|   
                                                                        
                                                                        
                            Version: {__version__}
          """)
    print("Type /help for help.")
    print("Alt + Enter to send a message.\n")


    session = create_session()
    completer = create_completer(
        ["/help", "/clear", "/list", "/history", "/name", "/restart", "/new", "/change", "/exit"])
    KeyBindings = create_keybindings()

    while True:
        print()
        try:
            print("User: ")
            user_input = get_input(
                session=session, completer=completer, key_bindings=KeyBindings)
        except KeyboardInterrupt:
            Bye()

        if user_input.startswith("/"):
            try:
                HunYuanBot.handle_commands(user_input)
            except Exception as e:
                print(e)
                continue
            continue

        print("\nHunYuanGPT: ", flush=True)

        active_block = MessageBlock()
        if args.no_stream:
            active_block.update_from_message(HunYuanBot.ask(user_input))
            # print(HunYuanBot.ask(user_input), flush=True)
        else:
            for rsp in HunYuanBot.ask_stream(user_input):
                active_block.update_from_message(rsp)
                # print(rsp, end="", flush=True)

        active_block.end()
        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc)
        Bye()
    except KeyboardInterrupt:
        Bye()
