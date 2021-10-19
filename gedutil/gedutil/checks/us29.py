from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US29(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        for doc in individuals.find(
            {GED_Tag.DEAT.name: {"$exists": 1}},
            {GED_Tag.DEAT.name: 1, GED_Tag.NAME.name: 1, ID.IND_ID.name: 1},
        ):
            errors.insert_one(
                {
                    "user story": User_Story.US29.name,
                    "error type": Error_Type.RESULT.name,
                    "message": f"{doc[GED_Tag.NAME.name]} ({doc[ID.IND_ID.name]}) has passed away",
                }
            )
