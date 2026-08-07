from textual.widgets import Static

class ContextView(Static):
    def on_mount(self):
        self.update(
"""
[bold cyan]📑 Context Manager[/bold cyan]

-------------------
[bold]Active Scope:[/bold] None
[bold]Files Indexed:[/bold] 0

[yellow]Waiting for repository indexing to build context window...[/yellow]
"""
        )