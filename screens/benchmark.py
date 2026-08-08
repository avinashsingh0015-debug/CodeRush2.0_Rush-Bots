from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

class BenchmarkView(Vertical):
    """Displays AI performance metrics and token usage."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold cyan]📊 Performance Benchmarks[/bold cyan]\n-------------------")
        yield Static("[gray]Metrics for agent execution, token consumption, and system latency.[/gray]\n")
        
        # 2. The Metrics Dashboard (Using formatted Rich text for a clean UI)
        yield Static("""
[bold]Latest Execution Metrics:[/bold]

⏱️  [green]Resolution Time:[/green]    1.24 seconds
🪙  [yellow]Tokens Consumed:[/yellow]    842 (Prompt: 600, Completion: 242)
💸  [magenta]Estimated Cost:[/magenta]     $0.0012
🎯  [cyan]Confidence Score:[/cyan]   98.5%

-------------------
[bold]Session Aggregates:[/bold]

Total Fixes Attempted:   [white]4[/white]
Total Fixes Successful:  [green]3[/green]
Average Latency:         [white]1.45s[/white]
Total Tokens Used:       [white]3,450[/white]
Total API Cost:          [white]$0.0048[/white]
""")