from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from explicitdev.config import Config


class AbstractWithConfig:
    def __init__(self, c: 'Config', *args, **kwargs):
        self.c = c
