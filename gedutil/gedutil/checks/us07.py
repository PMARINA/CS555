from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc
from .utils.individuals import get_age


class US07(Check):
    def __init__(self):
        pass

    def setup(self):
        pass

    def run(self):

        # Go through the families
        for doc in individuals.find():
            yearsAlive = get_age(doc[ID.IND_ID.name])
            if yearsAlive == None:
                continue
            if yearsAlive.days / 365.25 > 150:
                raise ValueError(
                    f"US07 - {doc[GED_Tag.NAME.name]} was alive for more than 150 years."
                )
