from gedutil.base import GED_Line, GED_Tag, Hook

from .date import Date


class Div(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.DIV or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(
                f"{GED_Tag.DIV.name}: level ({line.level}) was expected to be 1"
            )
        Date.fromType = GED_Tag.DIV.name
        Date.fromFam = line.args
        Date.isIndi = False
        Date.isMarr = False
        Date.isDiv = True
