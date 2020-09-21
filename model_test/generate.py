"""
Generate test cases and store as JSON for later execution.
"""
import json
from pathlib import Path
from typing import Callable, List, Tuple, Union

from model_test import CACHE_DIR, logger
from model_test.discovery import find_test_functions, find_test_modules
from model_test.fixtures import fill_fixtures
from model_test.schemas import Example, TestCase

SAVE_DIR = CACHE_DIR / "cases"


def validate_examples(examples):
    if isinstance(examples, Example):
        pass
    elif isinstance(examples, dict):
        _ = Example(**examples)
    elif isinstance(examples, (list, tuple)):
        for example in examples:
            validate_examples(example)
    else:
        raise ValueError(f"Unrecognized value ({type(examples)}) for test examples.\n{examples}")


def get_test_type(func):
    try:
        test_type = func.test_type
    except AttributeError:
        logger.warning(f"Test type not specified for {func.__name__}, setting to 'default'.")
        test_type = "default"
    return test_type


def collect_module_test_cases(functions_list: List[Tuple[str, Callable]]):
    cases = []
    for name, func in functions_list:
        examples = fill_fixtures(func)()
        test_type = get_test_type(func)
        try:
            validate_examples(examples)
        except ValueError as e:
            logger.error(f"Error collecting examples from {name}.\n{e}")
        test_case = TestCase(name=name, test_type=test_type, examples=examples).dict(
            exclude_unset=True
        )
        cases.append(test_case)
    return cases


def generate_module_tests(module_path: Union[str, Path], prefix: str = "test", suffix: str = None):
    module_path = Path(module_path)
    functions_list = find_test_functions(module_path=module_path, prefix=prefix, suffix=suffix)
    cases = collect_module_test_cases(functions_list)
    data = json.dumps(cases)
    output = SAVE_DIR / module_path.with_suffix(".json")
    output.parent.mkdir(exist_ok=True, parents=True)
    output.write_text(data)


def generate_tests(dir_path: str, prefix: str = "test", suffix: str = None):
    clear_cache(SAVE_DIR / dir_path)

    modules = find_test_modules(dir_path=dir_path, prefix=prefix, suffix=suffix)
    for module in modules:
        generate_module_tests(module_path=module, prefix=prefix, suffix=suffix)


def clear_cache(dir_path: str):
    import shutil

    shutil.rmtree(dir_path)
