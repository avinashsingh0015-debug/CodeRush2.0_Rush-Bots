from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button, RichLog
from textual import work

# Import our backend function from main.py
from error_check import run_ai_fixer

class ExecutionView(Vertical):
    """The panel that displays the agent's execution logs and actions."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold cyan]⚙ Execution Engine[/bold cyan]\n-------------------")
        
        # 2. The Trigger Button
        yield Button("Start Autonomous Agent", id="start_agent_btn", variant="success")
        
        # 3. The Live Log Box
        yield RichLog(id="execution_log", highlight=True, markup=True)

    def on_mount(self):
        """Runs when the screen first loads to set up initial text."""
        log_widget = self.query_one(RichLog)
        log_widget.write("[green]Agent Status:[/green] Standby")
        log_widget.write("[green]Target Directory:[/green] app/\n")
        log_widget.write("[yellow]Ready to commence autonomous self-healing sequence...[/yellow]\n")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles the button click event."""
        if event.button.id == "start_agent_btn":
            log_widget = self.query_one(RichLog)
            log_widget.write("[bold yellow]>[/bold yellow] Initiating backend agent...")
            
            # Disable the button so the user doesn't click it twice while it runs
            event.button.disabled = True 
            
            # Launch the backend in a background thread
            self.run_backend_task()

    @work(exclusive=True, thread=True)

    def run_backend_task(self):
        """Runs the AI loop in the background so the UI doesn't freeze."""
        
        # Call the actual backend tool we built earlier!
        result = run_ai_fixer(target_relative_path="app/math_app.py")
        
        # Once it finishes, securely send the results back to the main UI thread
        self.app.call_from_thread(self.update_ui_after_task, result)

    def update_ui_after_task(self, result):
        """Updates the screen with the final results."""
        log_widget = self.query_one(RichLog)
        
        # Print all the logs the backend collected
        log_widget.write(result["logs"])
        
        if result["success"]:
            log_widget.write("\n[bold green]✅ Agent sequence completed successfully![/bold green]")
        else:
            log_widget.write("\n[bold red]❌ Agent sequence failed. Check logs.[/bold red]")
        
        # Turn the button back on
        self.query_one("#start_agent_btn", Button).disabled = False
