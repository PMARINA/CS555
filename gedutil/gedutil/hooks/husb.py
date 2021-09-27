from gedutil.base import GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families

from .fam import Fam


class Husb(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.HUSB or not last_was_valid:
            return
        if line.level != 1:
            raise Exception(f"HUSB: level ({line.level}) was expected to be 1")
        families.find_one_and_update(
            {"fam_id": Fam.last_inserted}, {"$push": {"husb": line.args}}
        )
