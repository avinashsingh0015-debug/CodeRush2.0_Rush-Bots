from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

class EvidenceView(Vertical):
    """Displays the code diffs (before/after) of applied patches."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold red]🔎 Patch Evidence & Diffs[/bold red]\n-------------------")
        yield Static("[gray]Review the exact code modifications made by the autonomous agent.[/gray]\n")
        
        # 2. The Code Diff
        yield Static("""
[bold]Target File:[/bold] app/math_app.py
[bold]Action:[/bold] Logic Correction (Subtraction to Addition)

[red]-    def add_numbers(a, b):[/red]
[red]-        \"\"\"Adds two numbers together.\"\"\"[/red]
[red]-        return a - b[/red]

[green]+    def add_numbers(a, b):[/green]
[green]+        \"\"\"Adds two numbers together.\"\"\"[/green]
[green]+        return a + b[/green]

-------------------
[bold green]✅ Patch successfully applied and verified by the test suite.[/bold green]
""")