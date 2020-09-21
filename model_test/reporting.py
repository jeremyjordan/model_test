"""
Show results from a test run.
"""
from datetime import timedelta

from rich.console import Console
from rich.progress import BarColumn, Progress, ProgressColumn, Task, TextColumn
from rich.table import Table
from rich.text import Text

console = Console(log_path=False)


class ElapsedTimeColumn(ProgressColumn):
    """Renders time elapsed for a given task."""

    # Only refresh twice a second to prevent jitter
    max_refresh = 0.5

    def render(self, task: Task) -> Text:
        """Show time elapsed."""
        if not task.started:
            return Text("-:--:--", style="progress.remaining")
        elapsed = timedelta(seconds=int(task.elapsed))
        return Text(str(elapsed), style="progress.remaining")


progress = Progress(
    TextColumn("[bold]{task.fields[name]}", justify="right"),
    BarColumn(bar_width=None),
    # "[progress.percentage]{task.percentage:>3.1f}%",
    "{task.completed}",
    "/",
    "{task.total}",
    "•",
    ElapsedTimeColumn(),
    console=console,
)


def summarize_tests(results):
    results_table = Table(title="Model Test Results")
    results_table.add_column("Name", justify="left", no_wrap=True)
    results_table.add_column("Count")
    results_table.add_column("Score", justify="right", style="green")

    for test, result in results.items():
        count = len(result)
        score = sum(result) / len(result)
        results_table.add_row(test, str(count), f"{score:>3.4f}")

    console.print("\n")
    console.print(results_table)
