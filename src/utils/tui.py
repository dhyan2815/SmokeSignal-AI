import os
import time
from datetime import datetime
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress_bar import ProgressBar
from git import Repo
from src.core.config import settings

class StatusLine:
    """
    A persistent status line component for the terminal, 
    inspired by the Claude Code footer with model usage progress.
    """
    def __init__(self, console: Console = None):
        self.console = console or Console()
        self.repo = self._get_repo()
        self.start_time = time.time()
        # Mocking context usage for the wildfire model
        # In a real app, this could be tokens used vs model limits
        self.current_usage = 0.0 
        self.total_limit = 100.0

    def _get_repo(self):
        try:
            return Repo(search_parent_directories=True)
        except Exception:
            return None

    def _get_git_info(self):
        if not self.repo:
            return "[no git]"
        try:
            branch = self.repo.active_branch.name
            return f" {branch}"
        except Exception:
            return "[detached]"

    def _get_status_content(self, status: str = "Idle"):
        # Create a table for the status line components
        table = Table.grid(expand=True)
        table.add_column(justify="left", ratio=2)
        table.add_column(justify="center", ratio=1)
        table.add_column(justify="right", ratio=1)

        # Left side: Model info, Branch, CWD
        cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
        model_name = os.path.basename(settings.model_path)
        
        left_text = Text()
        left_text.append(" 󰚩 ", style="bold cyan")
        left_text.append(f"{model_name} ", style="bold white")
        left_text.append(" | ", style="dim white")
        left_text.append(f"{self._get_git_info()} ", style="bold green")
        left_text.append(" | ", style="dim white")
        left_text.append(f"󰉋 {cwd} ", style="dim cyan")

        # Middle side: Progress Bar & Percentage
        percentage = (self.current_usage / self.total_limit) * 100
        progress_bar = ProgressBar(
            total=self.total_limit,
            completed=self.current_usage,
            width=20,
            pulse=False,
            animation_time=0.5,
            style="grey37",
            complete_style="cyan",
            finished_style="bold green"
        )
        
        middle_group = Group(
            Text.assemble(
                "Usage: ", 
                (f"{percentage:.1f}% ", "bold cyan"),
                progress_bar
            )
        )

        # Right side: Status, Time
        right_text = Text()
        status_style = "bold green" if status == "Idle" else "bold yellow"
        right_text.append(f" {status} ", style=status_style)
        right_text.append(" | ", style="dim white")
        right_text.append(f"{datetime.now().strftime('%H:%M:%S')} ", style="dim white")

        table.add_row(left_text, middle_group, right_text)

        # Return a Panel for that 'bottom line' look
        return Panel(
            table,
            style="on grey11",
            box=None,
            padding=(0, 1),
        )

    def update_usage(self, usage: float):
        """Updates the usage metric shown in the progress bar."""
        self.current_usage = min(usage, self.total_limit)

    def run_interactive(self, task_func):
        """
        Runs a function while maintaining the status line at the bottom.
        """
        with Live(self._get_status_content(), console=self.console, refresh_per_second=10, screen=False) as live:
            def update_status(new_status: str, usage: float = None):
                if usage is not None:
                    self.update_usage(usage)
                live.update(self._get_status_content(new_status))

            task_func(update_status)

if __name__ == "__main__":
    sl = StatusLine()
    
    def demo_task(update_fn):
        for i in range(101):
            status = "Processing..." if i < 100 else "Idle"
            update_fn(status, usage=float(i))
            time.sleep(0.05)
        sl.console.print("[bold green]Success![/bold green] Status Line Updated.")

    sl.run_interactive(demo_task)
