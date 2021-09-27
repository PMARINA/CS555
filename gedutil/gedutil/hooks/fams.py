from gedutil.base import GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families, individuals

from .fam import Fam
from .indi import Indi


class Fams(Hook):
    last_inserted = None

    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.FAMS:
            return
        if line.level != 1:
            raise Exception(f"FAMS: level ({line.level}) was expected to be 1")
        individuals.find_one_and_update(
            {"ged_id": Indi.last_inserted}, {"$push": {"fams": line.args}}
        )
