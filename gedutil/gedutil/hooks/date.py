from loguru import logger

from gedutil.base import GED_Line, GED_Tag, Hook
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
        if line.tag != GED_Tag.DATE:
            return
        if last_was_valid:
            # if line.level != 2:
            #     raise NotImplementedError("Haven't accounted for other levels (than 2)")
            #     raise Exception(f"BIRT: level ({line.level}) was expected to be 1")
            if line.level == 2 and (Date.isIndi and not Date.isMarr and not Date.isDiv):
                individuals.update_one(
                    {"ged_id": Indi.last_inserted}, {"$set": {Date.fromType: line.args}}
                )
            elif line.level == 2 and ((Date.isMarr or Date.isDiv) and not Date.isIndi):
                result = families.update_one(
                    {"fam_id": Fam.last_inserted}, {"$set": {Date.fromType: line.args}}
                )
                # logger.debug(Date.fromType + str(result.matched_count))
            else:
                # logger.error("Last was valid but idk")
                pass
        else:
            # logger.error("Last was not valid: Date. Line was: " + f"{line.level} {line.tag} {line.args}")
            pass
