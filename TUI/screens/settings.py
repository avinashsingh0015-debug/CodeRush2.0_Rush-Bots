from textual.widgets import Static

class SettingsView(Static):
    def on_mount(self):
        self.update(
"""
[bold white]⚙ System Settings[/bold white]

-------------------
[bold]LLM Provider:[/bold] OpenRouter
[bold]Fallback Model:[/bold] Gemma-2-9b-it (Free)
[bold]Strict Mode:[/bold] Enabled

[white]>[/white] UI Theme: Dark/HUD
[white]>[/white] Telemetry: Disabled
"""
        )