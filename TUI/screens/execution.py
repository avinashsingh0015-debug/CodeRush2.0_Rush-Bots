from textual.widgets import Static

class ExecutionView(Static):
    """The panel that displays the agent's execution logs and actions."""

    def on_mount(self):
        self.update(
"""
[bold cyan]⚙ Execution Engine[/bold cyan]

-------------------

[green]Agent Status:[/green] Standby
[green]Target Directory:[/green] Not Selected

[bold]Execution Logs:[/bold]
[white]>[/white] Engine initialized.
[white]>[/white] Sandbox environment ready.
[white]>[/white] AI adapter loaded and awaiting instructions.

[yellow]Ready to commence autonomous self-healing sequence...[/yellow]
"""
        )