from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Tree

class TaskGraphView(Vertical):
    """Visualizes the agent's step-by-step execution pipeline."""

    def compose(self) -> ComposeResult:
        # 1. The Header
        yield Static("[bold blue]🗺️ Task Execution Graph[/bold blue]\n-------------------")
        yield Static("[gray]Interactive node map of the AI's problem-solving sequence.[/gray]\n")
        
        # 2. The Interactive Tree
        yield Tree("🤖 CodeHarness V2 Agent", id="task_tree")

    def on_mount(self):
        """Populates the tree with our backend phases when the screen loads."""
        tree = self.query_one(Tree)
        tree.root.expand()

        # Phase 1: Analysis
        analysis = tree.root.add("🔍 Phase 1: Context Analysis", expand=True)
        analysis.add_leaf("Read Target File")
        analysis.add_leaf("Scan Repository Architecture")

        # Phase 2: Verification
        verify = tree.root.add("⚙️ Phase 2: Initial Verification", expand=True)
        verify.add_leaf("Initialize Pytest Suite")
        verify.add_leaf("Capture Error Tracebacks")

        # Phase 3: AI Resolution
        ai_res = tree.root.add("🧠 Phase 3: AI Resolution", expand=True)
        ai_res.add_leaf("Construct System & User Prompts")
        ai_res.add_leaf("Query LLM Adapter")
        ai_res.add_leaf("Parse Markdown Code Blocks")

        # Phase 4: Application
        apply = tree.root.add("💉 Phase 4: Patch Application", expand=True)
        apply.add_leaf("Overwrite Target File")
        apply.add_leaf("Trigger Re-Verification Loop")