from gedutil.base import ID, GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families, individuals

from .fam import Fam
from .indi import Indi


class Date(Hook):
    fromType = None
    isIndi = None
    isMarr = None
    isDeat = None
    isDiv = None

    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.DATE or not last_was_valid:
            return
        if last_was_valid:
            if line.level == 2 and (Date.isIndi and not Date.isMarr and not Date.isDiv):
                individuals.update_one(
                    {ID.IND_ID.name: Indi.last_inserted},
                    {"$set": {Date.fromType: line.args}},
                )
            elif line.level == 2 and ((Date.isMarr or Date.isDiv) and not Date.isIndi):
                families.update_one(
                    {ID.FAM_ID.name: Fam.last_inserted},
                    {"$set": {Date.fromType: line.args}},
                )
