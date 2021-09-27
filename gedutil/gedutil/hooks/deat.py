from gedutil.base import GED_Line, GED_Tag, Hook

from .date import Date
from .indi import Indi


class Deat(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.DEAT or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(f"DEAT: level ({line.level}) was expected to be 1")
        Date.fromType = "deat"
        Date.fromIndi = Indi.last_inserted
        Date.isIndi = True
        Date.isMarr = False
        Date.isDiv = False
