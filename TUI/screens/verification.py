from textual.widgets import Static

class VerificationView(Static):
    """The panel that displays the test results and validation metrics."""

    def on_mount(self):
        self.update(
"""
[bold neon_green]✅ Verification Suite[/bold neon_green]

-------------------

[bold]Test Runner:[/bold] PyTest (Sandbox Environment)
[bold]Last Run Status:[/bold] [yellow]Pending Execution...[/yellow]

[bold]Verification Logs:[/bold]
[white]>[/white] Awaiting patch application.
[white]>[/white] Test suite standing by.

[blue]Run the execution engine to generate validation metrics.[/blue]
"""
        )