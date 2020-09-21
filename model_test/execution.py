"""
Run the test cases.
"""
import json
from importlib import import_module
from pathlib import Path
from typing import List

from model_test.generate import SAVE_DIR
from model_test.reporting import progress, summarize_tests

TEST_CASE_DISPATCH = {}


def register(test_type: str):
    def decorator(func):
        TEST_CASE_DISPATCH[test_type] = func

    return decorator


def find_test_cases(dir_path: str) -> List[Path]:
    cases_dir = SAVE_DIR / dir_path
    cases = cases_dir.rglob("*.json")
    return cases


def load_model_funcs(dir_path: str):
    module_path = Path(dir_path) / "model_conf.py"
    module_path = str(module_path).replace("/", ".").strip(".py")
    import_module(module_path)


def collect_tests(dir_path: str):
    cases = find_test_cases(dir_path=dir_path)
    tests = {}
    for case in cases:
        test_cases = json.loads(Path(case).read_text())
        tests[case] = test_cases
    return tests


def run_tests(dir_path: str):
    with progress:
        load_model_funcs(dir_path)
        tests = collect_tests(dir_path)
        results = {}
        for test_module in tests:
            progress.log(f"Running tests in {test_module}")
            test_cases = tests[test_module]
            # initialize progress bars for tests
            task_ids = [
                progress.add_task(
                    "run test", name=test["name"], total=len(test["examples"]), start=False
                )
                for test in test_cases
            ]
            for test, task_id in zip(test_cases, task_ids):
                progress.start_task(task_id)
                test_fn = TEST_CASE_DISPATCH.get(test["test_type"])
                if test_fn is None:
                    raise ValueError(f'Unrecognized test type: {test["test_type"]}')
                outcomes = []
                for example in test["examples"]:
                    result = test_fn(example)
                    outcomes.append(result)
                    progress.update(task_id, advance=1)
                progress.stop_task(task_id)
                results[test["name"]] = outcomes

    summarize_tests(results)
