from gedutil.base import GED_Line, GED_Tag, Hook
from gedutil.mongo_client import individuals

from .indi import Indi


class Name(Hook):
    def __init__(self):
        pass

    def process(self, line: GED_Line):
        # level, tag, args
        if line.tag != GED_Tag.NAME:
            return
        if line.level != 1:
            raise Exception(f"NAME: level ({line.level}) was expected to be 1")
        individuals.find_one_and_update(
            {"ged_id": Indi.last_inserted}, {"$set": {"name": line.args}}
        )
