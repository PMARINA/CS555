from dateutil.parser import parse as parse_date

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check

THIS_USER_STORY = User_Story.US02.name


class US02(Check):
    """
    The assignment:

    > Birth should occur before marriage of an individual
    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            # If the family isn't married (possible in GEDCOM), then we can't perform this check
            if not (GED_Tag.MARR.name in doc):
                continue

            marr_date_string = doc[GED_Tag.MARR.name]
            marr_date = parse_date(marr_date_string)
            individuals_to_check = []
            for name in [GED_Tag.WIFE.name, GED_Tag.HUSB.name]:
                individuals_to_check.extend(doc[name])
            for individual_id in individuals_to_check:
                individual = individuals.find_one({ID.IND_ID.name: individual_id})
                # Assume another test will catch this
                if not individual:
                    continue
                if GED_Tag.BIRT.name not in individual:
                    continue
                birth_date_string = individual[GED_Tag.BIRT.name]
                birth_date = parse_date(birth_date_string)
                if birth_date > marr_date:
                    errors.insert_one(
                        {
                            "user story": THIS_USER_STORY,
                            "error type": Error_Type.ERROR.name,
                            "message": f"Birth date ({birth_date_string}) was after date of marriage ({marr_date_string})",
                        }
                    )
