from gedutil.base import ID, GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families

from .fam import Fam


class Chil(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.CHIL or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(
                f"{GED_Tag.CHIL.name}: level ({line.level}) was expected to be 1"
            )
        families.find_one_and_update(
            {ID.FAM_ID.name: Fam.last_inserted},
            {"$push": {GED_Tag.CHIL.name: line.args}},
        )
