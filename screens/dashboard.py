from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Button, ContentSwitcher
from widgets.sidebar import SideBar
from widgets.homepage import HomePage
from widgets.topbar import TopBar
from widgets.footerbar import FooterBar

# --- View Imports ---
from screens.memory import MemoryView
from screens.execution import ExecutionView
from screens.verification import VerificationView
from screens.context import ContextView
from screens.task import TaskGraphView
from screens.benchmark import BenchmarkView
from screens.evidence import EvidenceView
from screens.settings import SettingsView

class Dashboard(Screen):

    def compose(self):
        yield FooterBar()
        yield TopBar()

        with Horizontal():
            with Vertical(id="sidebar"):
                yield SideBar()
            
            with Vertical(id="content"):
                with ContentSwitcher(initial="homepage", id="main-switcher"):
                    yield HomePage(id="homepage")
                    yield MemoryView(id="memory")
                    yield ContextView(id="context")
                    yield TaskGraphView(id="task")
                    yield ExecutionView(id="execute")
                    yield VerificationView(id="verify")
                    yield BenchmarkView(id="benchmark")
                    yield EvidenceView(id="evidence")
                    yield SettingsView(id="settings")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle sidebar button clicks."""
        
        # Grab the switcher once to keep the code clean
        switcher = self.query_one(ContentSwitcher)

        if event.button.id == "exit":
            self.app.exit()
        
        elif event.button.id == "repo":
            switcher.current = "homepage"
            
        elif event.button.id == "memory":
            switcher.current = "memory"

        elif event.button.id == "context":
            switcher.current = "context"
            
        elif event.button.id == "task":
            switcher.current = "task"
            
        elif event.button.id == "execute":
            switcher.current = "execute"
            
        elif event.button.id == "verify":
            switcher.current = "verify"

        elif event.button.id == "benchmark":
            switcher.current = "benchmark"

        elif event.button.id == "evidence":
            switcher.current = "evidence"

        elif event.button.id == "settings":
            switcher.current = "settings"