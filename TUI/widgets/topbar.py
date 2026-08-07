from textual.widgets import Static
from datetime import datetime


class TopBar(Static):

    def on_mount(self):
        self.set_interval(1, self.update_clock)

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")

        self.update(
            f"[bold cyan]🚀 CODEHARNESS v1.0[/]    "
            f"[green]📂 Repository:[/] None    "
            f"[yellow]🤖 Model:[/] GPT-5    "
            f"[cyan]🟢 READY[/]    "
            f"[magenta]🧠 Memory:[/] Warm    "
            f"[white]🕒 {now}[/]"
        )