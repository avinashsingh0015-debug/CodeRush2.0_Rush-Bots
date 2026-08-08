from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable

class MemoryView(Vertical):
    """Displays the agent's historical memory and past fixes."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold magenta]🧠 Agent Memory Bank[/bold magenta]\n-------------------")
        yield Static("[gray]Historical record of identified bugs, actions, and applied patches.[/gray]\n")
        
        # 2. The Data Table
        yield DataTable(id="memory_table")

    def on_mount(self):
        """Populate the table with historical data when the screen loads."""
        table = self.query_one(DataTable)
        
        # Define the columns
        table.add_columns("Timestamp", "Target File", "Status", "Resolution Notes")
        
        # Add some mock historical data (Great for the hackathon demo!)
        table.add_row("01:15 AM", "app/auth.py", "✅ Fixed", "Patched JWT token expiration bug")
        table.add_row("01:42 AM", "services/api.py", "✅ Fixed", "Resolved rate limiting exception")
        table.add_row("02:09 AM", "app/math_app.py", "❌ Failed", "Max attempts reached on logic error")
        
        # Add the fix we just completed together
        table.add_row("02:20 AM", "app/math_app.py", "✅ Fixed", "Corrected AssertionError (subtraction to addition)")