from textual.app import App
from textual.events import Click
from textual.widgets import DirectoryTree
from screens.dashboard import Dashboard
from widgets.context_menu import ContextMenu

class CodeHarnessApp(App):

    CSS = """
    Screen {
        layout: vertical;
        background: #111111;
        layers: below overlay;
    }

    Horizontal {
        height: 1fr;
    }

    #sidebar {
        width: 28;
        background: #1d1d1d;
        border: round cyan;
        padding: 1;
    }

    #content {
        width: 1fr;
        border: round cyan;
        padding: 1;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }

    Static {
        color: white;
    }

    ContextMenu {
        layer: overlay;
        background: #1d1d1d;
        color: white;
        border: solid cyan;
        width: 16;
        height: 6;
    }

    ContextMenu OptionList {
        background: #1d1d1d;
        border: none;
        height: 4;
        padding: 0;
    }

    ContextMenu OptionList > .option-list--option {
        padding: 0 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.context_menu = None
        self.target_widget = None

    def on_mount(self) -> None:
        self.push_screen(Dashboard())

    def on_click(self, event: Click) -> None:
        if self.context_menu:
            try:
                self.context_menu.remove()
            except Exception:
                pass
            self.context_menu = None
            self.target_widget = None
            event.stop()
            if event.button == 1:
                return

        if event.button == 3:
            self.target_widget = event.widget
            self.context_menu = ContextMenu(event.screen_x, event.screen_y)
            self.mount(self.context_menu)
            event.stop()

    def on_context_menu_selected(self, message: ContextMenu.Selected) -> None:
        action = message.action
        focused = self.target_widget
        self.context_menu = None
        self.target_widget = None
        
        try:
            import pyperclip
        except ImportError:
            pyperclip = None

        if action == "Copy":
            text_to_copy = ""
            
            dir_trees = self.screen.query(DirectoryTree)
            target_tree = None
            if focused and isinstance(focused, DirectoryTree):
                target_tree = focused
            elif dir_trees:
                target_tree = dir_trees.first()

            if target_tree and target_tree.cursor_node:
                node = target_tree.cursor_node
                if hasattr(node, "data") and node.data and hasattr(node.data, "path"):
                    text_to_copy = str(node.data.path)
                elif hasattr(node, "path") and node.path:
                    text_to_copy = str(node.path)

            if not text_to_copy and focused:
                if hasattr(focused, "selected_text") and focused.selected_text:
                    text_to_copy = focused.selected_text
                elif hasattr(focused, "value") and isinstance(focused.value, str):
                    text_to_copy = focused.value
                elif hasattr(focused, "text") and isinstance(focused.text, str):
                    text_to_copy = focused.text

            if text_to_copy:
                try:
                    if pyperclip:
                        pyperclip.copy(text_to_copy)
                    self.copy_to_clipboard(text_to_copy)
                    self.notify(f"Copied: {text_to_copy}", severity="information")
                except Exception as e:
                    self.notify(f"Copy failed: {e}", severity="error")
            else:
                self.notify("No text or file path selected to copy.", severity="warning")

        elif action == "Paste":
            try:
                pasted_text = pyperclip.paste() if pyperclip else ""
                if pasted_text and focused:
                    if hasattr(focused, "insert"):
                        focused.insert(pasted_text)
                        self.notify("Pasted successfully!")
                    elif hasattr(focused, "value") and isinstance(focused.value, str):
                        focused.value += pasted_text
                        self.notify("Pasted successfully!")
                    else:
                        self.notify("Focused field does not accept input.", severity="warning")
                else:
                    self.notify("Clipboard is empty.", severity="warning")
            except Exception as e:
                self.notify(f"Paste failed: {e}", severity="error")

        elif action == "Cut":
            text_to_cut = ""
            if focused and hasattr(focused, "selected_text") and focused.selected_text:
                text_to_cut = focused.selected_text
                if hasattr(focused, "delete_selection"):
                    focused.delete_selection()
                elif hasattr(focused, "action_delete"):
                    focused.action_delete()
                
                if text_to_cut:
                    if pyperclip:
                        pyperclip.copy(text_to_cut)
                    self.copy_to_clipboard(text_to_cut)
                    self.notify("Cut to clipboard!")
                else:
                    self.notify("No text selected to cut.", severity="warning")
            else:
                self.notify("Cut is only supported on text selections.", severity="warning")

        elif action == "Select All":
            if focused:
                if hasattr(focused, "action_select_all"):
                    focused.action_select_all()
                    self.notify("Selected all.")
                elif hasattr(focused, "select_all"):
                    focused.select_all()
                    self.notify("Selected all.")
                else:
                    self.notify("Select All not supported here.", severity="warning")