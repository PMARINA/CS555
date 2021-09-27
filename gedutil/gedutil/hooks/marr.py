from gedutil.base import GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families, individuals

from .date import Date
from .fam import Fam
from .indi import Indi


class Marr(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.MARR:
            return
        if line.level != 1:
            raise Exception(f"MARR: level ({line.level}) was expected to be 1")
        Date.fromType = "marr"
        Date.fromFam = line.args
        Date.isIndi = False
        Date.isMarr = True
        Date.isDiv = False
        # if not families.find_one({'fam_id': line.args}):
        #     families.insert_one({'fam_id': line.args})
