from gedutil.base import GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families

from .date import Date
from .fam import Fam


class Chil(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.CHIL:
            return
        if line.level != 1:
            raise Exception(f"CHIL: level ({line.level}) was expected to be 1")
        families.find_one_and_update(
            {"fam_id": Fam.last_inserted}, {"$push": {"chil": line.args}}
        )
