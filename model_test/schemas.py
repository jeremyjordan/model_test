from typing import Any, List, Union

from pydantic import BaseModel


class Example(BaseModel):
    data: Any
    label: Any = None
    metadata: Any = None


class TestCase(BaseModel):
    name: str
    test_type: str
    examples: List[Union[Example, List[Example]]]
