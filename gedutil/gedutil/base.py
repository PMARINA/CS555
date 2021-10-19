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


class Error_Type(Enum):
    ANOMALY = auto()
    ERROR = auto()
    RESULT = auto()


class User_Story(Enum):
    US01 = auto()
    US02 = auto()
    US03 = auto()
    US04 = auto()
    US05 = auto()
    US06 = auto()
    US07 = auto()
    US08 = auto()
    US09 = auto()
    US10 = auto()
    US11 = auto()
    US12 = auto()
    US13 = auto()
    US14 = auto()
    US15 = auto()
    US16 = auto()
    US17 = auto()
    US18 = auto()
    US19 = auto()
    US20 = auto()
    US21 = auto()
    US22 = auto()
    US23 = auto()
    US24 = auto()
    US25 = auto()
    US26 = auto()
    US27 = auto()
    US28 = auto()
    US29 = auto()
    US30 = auto()
    US31 = auto()
    US32 = auto()
    US33 = auto()
    US34 = auto()
    US35 = auto()
    US36 = auto()
    US37 = auto()
    US38 = auto()
    US39 = auto()
    US40 = auto()
    US41 = auto()
    US42 = auto()
    US43 = auto()
    US44 = auto()


@dataclass(frozen=True)
class GED_Line:
    __slots__ = "level", "tag", "args"
    level: int
    tag: Union[GED_Tag, str]
    args: str

    def is_valid(self):  # pragma: no cover
        return not isinstance(self.tag, str)


class Hook:
    def __init__(self):  # pragma: no cover
        raise NotImplementedError("Must be overridden by a hook")

    def process(self, line: GED_Line, last_was_valid: bool):  # pragma: no cover
        raise NotImplementedError("Must be overridden by a hook")
