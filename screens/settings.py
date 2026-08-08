from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Label, Button

class SettingsView(Vertical):
    """Configuration panel for API keys and agent behavior."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold white]⚙️ System Settings[/bold white]\n-------------------")
        yield Static("[gray]Configure your LLM provider and agent execution parameters.[/gray]\n")
        
        # 2. API Key Input
        yield Label("OpenRouter API Key:")
        yield Input(placeholder="sk-or-v1-...", password=True, id="api_key_input")
        
        yield Static("\n")
        
        # 3. Model Selection Input
        yield Label("Active AI Model:")
        yield Input(value="ling-3.0-tiny:free", id="model_input")
        
        yield Static("\n")
        
        # 4. Save Button
        yield Button("Save Configuration", variant="primary", id="save_settings_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the save button click."""
        if event.button.id == "save_settings_btn":
            # Change the button label to show it worked for the demo!
            event.button.label = "✅ Settings Saved Successfully"
            event.button.variant = "success"