"""
Command line interface for generating and running tests.
"""
from typing import Optional

import typer

from model_test.execution import run_tests
from model_test.generate import generate_tests

app = typer.Typer()


@app.command()
def generate(dir_path: str, prefix: Optional[str] = "test", suffix: Optional[str] = None):
    generate_tests(dir_path, prefix=prefix, suffix=suffix)


@app.command()
def run(dir_path: str):
    run_tests(dir_path)


if __name__ == "__main__":
    app()
