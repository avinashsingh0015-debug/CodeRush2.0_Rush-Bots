from textual.widgets import Static

class BenchmarkView(Static):
    def on_mount(self):
        self.update(
"""
[bold magenta]📊 Benchmark Analytics[/bold magenta]

-------------------
[bold]Performance Score:[/bold] N/A
[bold]Resolution Time:[/bold] N/A

[white]>[/white] Awaiting successful patch verifications to calculate metrics.
"""
        )