"""
Decorator to mark what type of test to run.
Minimal implementation of pytest's mark feature.
"""


def store_mark(obj, mark_name: str) -> None:
    obj.test_type = mark_name


class MarkDecorator:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        store_mark(func, self.name)
        return func


class MarkGenerator:
    def __getattr__(self, name: str) -> MarkDecorator:
        if name[0] == "_":
            raise AttributeError("Marker cannot start with _")
        return MarkDecorator(name)


MARK_GEN = MarkGenerator()
