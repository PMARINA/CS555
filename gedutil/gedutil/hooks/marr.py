from gedutil.base import GED_Line, GED_Tag, Hook

from .date import Date


class Marr(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.MARR or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(
                f"{GED_Tag.MARR.name}: level ({line.level}) was expected to be 1"
            )
        Date.fromType = GED_Tag.MARR.name
        Date.fromFam = line.args
        Date.isIndi = False
        Date.isMarr = True
        Date.isDiv = False
