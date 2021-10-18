from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US29(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        dead_people = []
        for doc in individuals.find(
            {GED_Tag.DEAT.name: {"$exists": 1}},
            {GED_Tag.DEAT.name: 1, GED_Tag.NAME.name: 1, ID.IND_ID.name: 1},
        ):
            dead_people.append(doc)
        return dead_people
