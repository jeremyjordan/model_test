import logging
import os
import random
from pathlib import Path

CACHE_DIR = Path(".model_test_cache")
USER_CACHE_DIR = CACHE_DIR / "data"
USER_CACHE_DIR.mkdir(exist_ok=True, parents=True)

# set a random seed
# TODO make this configurable by the user
seed = 14
os.environ["PYTHONHASHSEED"] = str(seed)
random.seed(seed)

logger = logging.getLogger("model_test")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# bump imports to top level
from model_test.execution import register  # noqa: F401, E402
from model_test.mark import MARK_GEN as mark  # noqa: F401, E402
