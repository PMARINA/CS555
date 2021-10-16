from gedutil.base import GED_Line, GED_Tag, Hook

from .date import Date
from .indi import Indi


class Birt(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.BIRT or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(
                f"{GED_Tag.BIRT.name}: level ({line.level}) was expected to be 1"
            )
        Date.fromType = GED_Tag.BIRT.name
        Date.fromIndi = Indi.last_inserted
        Date.isIndi = True
        Date.isMarr = False
        Date.isDiv = False
