# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, individuals

from .check import Check

THIS_USER_STORY = User_Story.US03.name


class US03(Check):
    """
    The assignment:

    > Birth should occur before death of an individual

    Iterate through individuals and check for birth & death dates. Where they exist, check birthDay < deathDay
    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in individuals.find():
            # If the person has died, then we can perform the check
            # Otherwise, we don't have enough dates to compare/validate
            if not (GED_Tag.BIRT.name in doc and GED_Tag.DEAT.name in doc):
                continue

            # Get the strings from the database
            birth_date_str = doc[GED_Tag.BIRT.name]
            death_date_str = doc[GED_Tag.DEAT.name]

            # Parse into a comparable format
            birth_date = parseDate(birth_date_str)
            death_date = parseDate(death_date_str)

            # > and not >= because it's possible for neonatal death to occur
            if birth_date > death_date:
                errors.insert_one(
                    {
                        "user story": THIS_USER_STORY,
                        "error type": Error_Type.ERROR.name,
                        "message": f"Birth date ({birth_date_str}) was after death date ({death_date_str})",
                    }
                )
