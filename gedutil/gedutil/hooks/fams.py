from gedutil.base import ID, GED_Line, GED_Tag, Hook
from gedutil.mongo_client import individuals

from .indi import Indi


class Fams(Hook):
    last_inserted = None

    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.FAMS or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(
                f"{GED_Tag.FAMS.name}: level ({line.level}) was expected to be 1"
            )
        individuals.find_one_and_update(
            {ID.IND_ID.name: Indi.last_inserted},
            {"$push": {GED_Tag.FAMS.name: line.args}},
        )
