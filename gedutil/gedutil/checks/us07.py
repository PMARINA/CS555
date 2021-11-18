from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc
from .utils.individuals import get_age

THIS_USER_STORY = User_Story.US07.name


class US07(Check):
    def __init__(self):
        pass

    def setup(self):
        pass

    def run(self):

        for doc in individuals.find():
            yearsAlive = get_age(doc[ID.IND_ID.name])
            if yearsAlive == None:
                continue
            if yearsAlive.days / 365.25 > 150:
                errors.insert_one(
                    {
                        "user story": THIS_USER_STORY,
                        "error type": Error_Type.ERROR.name,
                        "message": f"US07 - {doc[GED_Tag.NAME.name]} was alive for more than 150 years.",
                    }
                )
