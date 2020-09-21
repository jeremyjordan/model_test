"""
Discover all test cases to generate.
"""
from importlib import import_module
from inspect import getmembers, isfunction
from pathlib import Path
from typing import Callable, List, Tuple, Union


def find_test_modules(dir_path: str, prefix: str = "test", suffix: str = None) -> List[Path]:
    if not prefix:
        prefix = ""
    if not suffix:
        suffix = ""
    search_str = f"**/{prefix}*{suffix}.py"
    path = Path(dir_path)
    return list(path.rglob(search_str))


def find_test_functions(
    module_path: Union[str, Path], prefix: str = "test", suffix: str = None
) -> List[Tuple[str, Callable]]:
    if not prefix:
        prefix = ""
    if not suffix:
        suffix = ""

    module_path = str(module_path).replace("/", ".").strip(".py")
    module = import_module(module_path)
    functions_list = [
        (name, func)
        for name, func in getmembers(module)
        if (isfunction(func) and name.startswith(prefix) and name.endswith(suffix))
    ]
    return functions_list
