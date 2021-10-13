from gedutil.base import ID, GED_Line, GED_Tag, Hook
from gedutil.mongo_client import families


class Fam(Hook):
    last_inserted = None

    def __init__(self):
        pass

    def process(self, line: GED_Line, last_was_valid):
        # level, tag, args
        if line.tag != GED_Tag.FAM or not last_was_valid:
            return
        if line.level != 0:
            raise Exception(
                f"{GED_Tag.FAM.name}: level ({line.level}) was expected to be 0"
            )
        families.insert_one({ID.FAM_ID.name: line.args})
        Fam.last_inserted = line.args
