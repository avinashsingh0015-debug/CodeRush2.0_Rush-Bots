from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button, SelectionList
from textual.widgets.selection_list import Selection
from textual import work  # Added work decorator

class MultiFolderSelectModal(ModalScreen[list[Path]]):
    def __init__(self, root_path: str = "."):
        super().__init__()
        self.root_path = Path(root_path).resolve()

    def compose(self) -> ComposeResult:
        IGNORED_MODAL_DIRS = {".git", ".pytest_cache", "__pycache__", "venv", ".venv"}

        subdirs = [
            p for p in sorted(self.root_path.iterdir()) 
            if p.is_dir() and not p.name.startswith(".") and p.name not in IGNORED_MODAL_DIRS
        ]
        selections = [Selection(f"📁 {p.name}", value=p, initial_state=True) for p in subdirs]

        with Container(id="modal-container"):
            yield Static("Select Folders for Verification", id="modal-title")
            if selections:
                yield SelectionList[Path](*selections, id="folder-list")
            else:
                yield Static("[!] No sub-directories found.", id="folder-list")

            with Horizontal():
                yield Button("Select All", id="btn-toggle-all", variant="primary")
                yield Button("Confirm", id="btn-confirm", variant="success")
                yield Button("Cancel", id="btn-cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            try:
                folder_list = self.query_one("#folder-list", SelectionList)
                selected_paths: list[Path] = folder_list.selected
            except Exception:
                selected_paths = []
            self.dismiss(selected_paths)

        elif event.button.id == "btn-toggle-all":
            try:
                folder_list = self.query_one("#folder-list", SelectionList)
                if len(folder_list.selected) == len(folder_list._options):
                    folder_list.deselect_all()
                else:
                    folder_list.select_all()
            except Exception:
                pass

        elif event.button.id == "btn-cancel":
            self.dismiss([])

class HarnessUI(App):
    def __init__(self, run_harness_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.run_harness_callback = run_harness_callback

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-panel"):
            yield Static("Terminal Coding Harness v1.0", id="header-title")
            yield Static("\\[⚡ STEP\\] Ready to run verification...", id="status-box")
            with Vertical():
                yield Button("RUN VERIFICATION", id="btn-run", variant="success")
                yield Button("QUIT", id="btn-quit", variant="error")
        yield Footer()

    def update_status(self, message: str):
        self.query_one("#status-box", Static).update(message)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-run":
            self.push_screen(MultiFolderSelectModal("."), self.handle_folders_selected)
        elif event.button.id == "btn-quit":
            self.exit()

    @work(thread=True)
    def handle_folders_selected(self, selected_folders: list[Path]) -> None:
        if not selected_folders:
            self.call_from_thread(self.update_status, "[⚡ CANCELLED] No folders selected.")
            return

        self.call_from_thread(self.update_status, "⏳ Running verification & calling AI model... Please wait.")

        if self.run_harness_callback:
            summary, cost = self.run_harness_callback(selected_folders)
            self.call_from_thread(self.update_status, f"{summary}\n\nCost: ${cost:.5f}")
        else:
            self.call_from_thread(self.update_status, f"Selected {len(selected_folders)} folder(s). No callback registered.")
