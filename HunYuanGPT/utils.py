import re

from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()


def create_keybindings(key: str = "c-@"):

    @bindings.add(key)
    def _(event: dict) -> None:
        event.app.exit(result=event.app.current_buffer.text)

    return bindings


def create_session():
    return PromptSession(history=InMemoryHistory())


def create_completer(commands: list, pattern_str: str = "$"):
    return WordCompleter(words=commands, pattern=re.compile(pattern_str))


def get_input(
    session: PromptSession = None,
    completer: WordCompleter = None,
    key_bindings: KeyBindings = None,
):
    """
    Multiline input function.
    """
    return (
        session.prompt(
            completer=completer,
            multiline=True,
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=key_bindings,
        )
        if session
        else prompt(multiline=True)
    )
