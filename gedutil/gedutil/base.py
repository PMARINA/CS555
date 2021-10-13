from dataclasses import dataclass
from enum import Enum, auto
from typing import *


class ID(Enum):
    IND_ID = auto()
    FAM_ID = auto()


class GED_Tag(Enum):
    INDI = auto()
    NAME = auto()
    SEX = auto()
    BIRT = auto()
    DEAT = auto()
    FAMC = auto()
    FAMS = auto()
    FAM = auto()
    MARR = auto()
    HUSB = auto()
    WIFE = auto()
    CHIL = auto()
    DIV = auto()
    DATE = auto()
    HEAD = auto()
    TRLR = auto()
    NOTE = auto()


@dataclass(frozen=True)
class GED_Line:
    __slots__ = "level", "tag", "args"
    level: int
    tag: Union[GED_Tag, str]
    args: str

    def is_valid(self):
        return not isinstance(self.tag, str)


class Hook:
    def __init__(self):
        raise NotImplementedError("Must be overridden by a hook")

    def process(self, line: GED_Line, last_was_valid: bool):
        raise NotImplementedError("Must be overridden by a hook")
