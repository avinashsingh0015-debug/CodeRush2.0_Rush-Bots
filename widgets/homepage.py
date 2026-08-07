import os
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DirectoryTree

class HomePage(Vertical):
    """Displays the active project's file structure."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold yellow]📁 Repository Explorer[/bold yellow]\n-------------------")
        yield Static("[gray]Interactive browser for the active workspace and target files.[/gray]\n")
        
        # 2. Get the root directory of your project
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # 3. The Interactive File Tree
        yield DirectoryTree(root_dir, id="repo_tree")

    def on_mount(self):
        """Expand the root directory when the view loads."""
        tree = self.query_one(DirectoryTree)
        tree.root.expand()