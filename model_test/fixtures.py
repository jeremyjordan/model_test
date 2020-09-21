from functools import partial
from inspect import signature

from model_test import USER_CACHE_DIR

REGISTERED_FIXTURES = {"cache_dir": USER_CACHE_DIR}


def fill_fixtures(func):
    sig = signature(func)
    args = set(sig.parameters)
    fixture_names = args.intersection(REGISTERED_FIXTURES.keys())
    fixture_kwargs = {fixture: REGISTERED_FIXTURES[fixture] for fixture in fixture_names}
    return partial(func, **fixture_kwargs)
