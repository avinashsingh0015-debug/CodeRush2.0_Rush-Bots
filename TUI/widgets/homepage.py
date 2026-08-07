from textual.widgets import Static

class HomePage(Static):

    def on_mount(self):
        self.update(
"""
Repository Overview

-------------------

Welcome to CodeHarness

[red]✗ Repository not loaded[/red]

[green]✓ Memory Ready[/green]

[green]✓ Context Manager Ready[/green]

[bold yellow]⚠ Awaiting user action...[/bold yellow]
"""
        )