import os
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, RichLog
from textual import work

# Import the scanner from your backend services!
from services.scanner import RepoScanner

class ContextView(Vertical):
    """Displays the repository context that the AI will see."""

    def compose(self) -> ComposeResult:
        yield Static("[bold magenta]🧠 Repository Context Scanner[/bold magenta]\n-------------------")
        yield Static("[gray]This is the raw codebase data the AI reads before making a fix.[/gray]\n")
        yield RichLog(id="context_log", highlight=True, markup=False)

    def on_mount(self):
        """When the user clicks the Context tab, start scanning immediately."""
        log_widget = self.query_one("#context_log", RichLog)
        log_widget.write("Scanning repository files...\n")
        
        # Trigger the backend scanner in a background thread
        self.load_repo_context()

    @work(thread=True)
    def load_repo_context(self):
        """Runs the backend RepoScanner without freezing the UI."""
        # Find the root CodehernessV2 folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # Initialize the backend tool
        scanner = RepoScanner(target_directory=root_dir)
        
        # Gather the python files
        context_data = scanner.gather_context(file_extension=".py")
        
        # Safely send the data back to the UI
        self.app.call_from_thread(self.update_log, context_data)
        
    def update_log(self, data):
        """Prints the backend scanner data directly into the dashboard."""
        log_widget = self.query_one("#context_log", RichLog)
        log_widget.write(data)