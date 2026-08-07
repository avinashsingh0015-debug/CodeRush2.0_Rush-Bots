from textual.widgets import Static

class TaskGraphView(Static):
    def on_mount(self):
        self.update(
"""
[bold blue]📌 Task Graph[/bold blue]

-------------------
[bold]Current Objective:[/bold] Idle

[white]>[/white] No active tasks in the queue.
[white]>[/white] Dependency tree is empty.

[yellow]Initialize execution sequence to populate task graph...[/yellow]
"""
        )