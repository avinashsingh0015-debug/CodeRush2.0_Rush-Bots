from textual.containers import Vertical
from textual.widgets import Button


class SideBar(Vertical):

    def compose(self):

        yield Button("📂 Repository", id="repo")
        yield Button("🧠 Memory", id="memory")
        yield Button("📑 Context", id="context")
        yield Button("📌 Task Graph", id="task")
        yield Button("⚙ Execute", id="execute")
        yield Button("✅ Verify", id="verify")
        yield Button("📊 Benchmark", id="benchmark")
        yield Button("📄 Evidence", id="evidence")
        yield Button("⚙ Settings", id="settings")
        yield Button("❌ Exit", id="exit")