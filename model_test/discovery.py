"""
Discover all test cases to generate.
"""
import importlib
import sys
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


def robust_module_import(module_path: Path):
    """
    From: pytest/pathlib.py:import_path
    """
    module_name = module_path.stem

    for meta_importer in sys.meta_path:
        if not hasattr(meta_importer, "find_spec"):
            continue
        spec = meta_importer.find_spec(module_name, [str(module_path.parent)])
        if spec is not None:
            break
        else:
            spec = importlib.util.spec_from_file_location(module_name, str(module_path))

    if spec is None:
        raise ImportError(
            "Can't find module {} at location {}".format(module_name, str(module_path))
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_test_functions(
    module_path: Union[str, Path], prefix: str = "test", suffix: str = None
) -> List[Tuple[str, Callable]]:
    if not prefix:
        prefix = ""
    if not suffix:
        suffix = ""

    module = robust_module_import(module_path)
    functions_list = [
        (name, func)
        for name, func in getmembers(module)
        if (isfunction(func) and name.startswith(prefix) and name.endswith(suffix))
    ]
    return functions_list
