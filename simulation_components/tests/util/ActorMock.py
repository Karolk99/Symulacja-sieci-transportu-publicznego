import logging
from typing import Any
import pykka


class ActorMock(pykka.ThreadingActor):
    id: int

    @classmethod
    def cl(cls, *args, **kwargs):
        return cls()

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.id = -1
