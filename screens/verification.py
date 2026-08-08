import os
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button, RichLog
from textual import work

# Import the verifier from your backend services!
from services.verifier import CodeVerifier

class VerificationView(Vertical):
    """Displays the test suite results."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold green]✅ Test Suite Verifier[/bold green]\n-------------------")
        yield Static("[gray]Run the backend test suite to check for bugs before or after AI intervention.[/gray]\n")
        
        # 2. The Trigger Button
        yield Button("Run Pytest Suite", id="run_tests_btn", variant="primary")
        
        # 3. The Live Log Box
        yield RichLog(id="verification_log", highlight=True, markup=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles the button click event."""
        if event.button.id == "run_tests_btn":
            log_widget = self.query_one("#verification_log", RichLog)
            log_widget.write("\n[yellow]⏳ Initializing pytest suite...[/yellow]")
            
            # Disable the button to prevent spam-clicking
            event.button.disabled = True 
            
            # Launch the backend verifier in a background thread
            self.run_tests_backend()

    @work(thread=True)
    def run_tests_backend(self):
        """Runs the backend CodeVerifier without freezing the UI."""
        # Find the root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        
        # Initialize the backend tool
        verifier = CodeVerifier(target_directory=root_dir)
        
        # Run the tests! (This returns a dictionary with 'success' and 'output')
        results = verifier.run_tests()
        
        # Safely send the data back to the UI thread
        self.app.call_from_thread(self.update_log, results)
        
    def update_log(self, results):
        """Prints the test results directly into the dashboard."""
        log_widget = self.query_one("#verification_log", RichLog)
        
        # Print the raw pytest terminal output
        log_widget.write(results["output"])
        
        # Print a clear summary status
        if results["success"]:
            log_widget.write("\n[bold green]🎉 SUCCESS: All tests passed![/bold green]")
        else:
            log_widget.write("\n[bold red]❌ FAILED: Bugs detected in the codebase.[/bold red]")
            
        # Re-enable the button
        self.query_one("#run_tests_btn", Button).disabled = False