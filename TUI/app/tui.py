from textual.app import App
from screens.dashboard import Dashboard

class CodeHarnessApp(App):

    CSS = """
    Screen {
        layout: vertical;
        background: #111111;
    }

    Horizontal {
        height: 1fr;
    }

    #sidebar {
        width: 28;
        background: #1d1d1d;
        border: round cyan;
        padding: 1;
    }

    #content {
        width: 1fr;
        border: round cyan;
        padding: 1;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }

    Static {
        color: white;
    }
    """

    def on_mount(self):
        self.push_screen(Dashboard())