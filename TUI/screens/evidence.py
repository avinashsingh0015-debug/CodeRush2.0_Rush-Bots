from textual.widgets import Static

class EvidenceView(Static):
    def on_mount(self):
        self.update(
"""
[bold green]📄 Evidence & Audit Log[/bold green]

-------------------
[bold]Patch History:[/bold] Clean

[white]>[/white] All AI-generated patches and diffs will be recorded here for human review.
"""
        )