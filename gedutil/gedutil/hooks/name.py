from gedutil.base import ID, GED_Line, GED_Tag, Hook
from gedutil.mongo_client import individuals

from .indi import Indi


class Name(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.NAME or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(
                f"{GED_Tag.NAME.name}: level ({line.level}) was expected to be 1"
            )
        individuals.find_one_and_update(
            {ID.IND_ID.name: Indi.last_inserted},
            {"$set": {GED_Tag.NAME.name: line.args}},
        )
