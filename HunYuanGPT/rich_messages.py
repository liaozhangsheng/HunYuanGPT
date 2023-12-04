from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
from rich.box import MINIMAL


class MessageBlock:

    def __init__(self):
        self.live = Live(auto_refresh=False, console=Console())
        self.live.start()
        self.content = ""

    def update_from_message(self, message: str):
        self.content += message
        if self.content:
            self.refresh()

    def end(self):
        self.refresh(cursor=False)
        self.live.stop()
        self.content = ""

    def refresh(self, cursor: bool = True):
        markdown = Markdown(self.content.strip() + ("█" if cursor else ""))
        panel = Panel(markdown, box=MINIMAL)
        self.live.update(panel)
        self.live.refresh()
