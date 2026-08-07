from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import OptionList
from textual.message import Message

class ContextMenu(Container):
    """A popup context menu with Cut, Copy, Paste, and Select All options."""
    
    class Selected(Message):
        def __init__(self, action: str) -> None:
            super().__init__()
            self.action = action

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.offset_x = x
        self.offset_y = y

    def compose(self) -> ComposeResult:
        yield OptionList(
            "Cut",
            "Copy",
            "Paste",
            "Select All",
            id="context-options"
        )

    def on_mount(self) -> None:
        self.styles.offset = (self.offset_x, self.offset_y)
        self.styles.width = 16
        self.styles.height = 6
        self.styles.layer = "overlay"

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        action = str(event.option.prompt)
        self.post_message(self.Selected(action))
        self.remove()