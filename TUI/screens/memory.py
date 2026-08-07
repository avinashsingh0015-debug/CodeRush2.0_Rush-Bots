from textual.widgets import Static

class MemoryView(Static):
    """The panel that displays the agent's memory and context."""

    def on_mount(self):
        self.update(
"""
[bold magenta]🧠 Memory Engine[/bold magenta]

-------------------

[green]System Memory:[/green] Online
[green]Vector Store:[/green] Connected

Recent Context:
- No previous actions recorded in current session.

[yellow]Awaiting repository ingestion...[/yellow]
"""
        )