# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US10(Check):
    MINIMUM_MARRIAGE_AGE_YEARS = 14

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            if GED_Tag.MARR.name not in doc:
                continue
            marriage_date = parseDate(doc[GED_Tag.MARR.name])
            latest_birth_date = marriage_date - timedelta(
                days=365 * US10.MINIMUM_MARRIAGE_AGE_YEARS
            )

            ids_of_people = get_parents_from_doc(doc)
            for id in ids_of_people:
                person = individuals.find_one({ID.IND_ID.name: id})
                if GED_Tag.BIRT.name not in person:
                    f"This person does not have a recorded birth date."
                    continue
                birth_date = parseDate(person[GED_Tag.BIRT.name])
                if birth_date >= latest_birth_date:
                    errors.insert_one(
                        {
                            "user story": User_Story.US10.name,
                            "error type": Error_Type.ANOMALY.name,
                            "message": f"Birth date ({birth_date}) within {US10.MINIMUM_MARRIAGE_AGE_YEARS} years of marriage ({marriage_date})",
                        }
                    )
