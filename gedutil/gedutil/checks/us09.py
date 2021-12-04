# comment
from datetime import timedelta

from dateutil.parser import parse as parse_date

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check

THIS_USER_STORY = User_Story.US09.name
WEEKS_IN_A_MONTH = 4.3452381  # Provided by Google


class US09(Check):
    def __init__(self, months_after_husband_death=9):
        self.months_after_husband_death = months_after_husband_death

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            wife_id = None
            wife_death_date = None
            wife_death_date_string = None

            husband_id = None
            husband_death_date = None
            husband_death_date_string = None

            if GED_Tag.WIFE.name in doc:
                wife_id = doc[GED_Tag.WIFE.name][0]
            if GED_Tag.HUSB.name in doc:
                husband_id = doc[GED_Tag.HUSB.name][0]
            if wife_id:
                wife = individuals.find_one({ID.IND_ID.name: wife_id})
                if GED_Tag.DEAT.name in wife:
                    wife_death_date_string = wife[GED_Tag.DEAT.name]
                    try:
                        wife_death_date = parse_date(wife_death_date_string)
                    except ValueError:
                        pass
            if husband_id:
                husband_doc = individuals.find_one({ID.IND_ID.name: husband_id})
                if GED_Tag.DEAT.name in husband_doc:
                    husband_death_date_string = husband_doc[GED_Tag.DEAT.name]
                    try:
                        husband_death_date = parse_date(husband_death_date_string)
                    except ValueError:
                        pass
            if GED_Tag.CHIL.name not in doc:
                continue
            for child_id in doc[GED_Tag.CHIL.name]:
                child_doc = individuals.find_one({ID.IND_ID.name: child_id})
                if GED_Tag.BIRT.name not in child_doc:
                    continue
                birth_date_string = child_doc[GED_Tag.BIRT.name]
                birth_date = parse_date(birth_date_string)
                if wife_death_date and birth_date > wife_death_date:
                    errors.insert_one(
                        {
                            "user story": THIS_USER_STORY,
                            "error type": Error_Type.ERROR.name,
                            "message": f"Child born ({birth_date_string}) after death of mother on {wife_death_date_string}",
                        }
                    )
                if husband_death_date and birth_date > husband_death_date + timedelta(
                    weeks=WEEKS_IN_A_MONTH * self.months_after_husband_death
                ):
                    errors.insert_one(
                        {
                            "user story": THIS_USER_STORY,
                            "error type": Error_Type.ERROR.name,
                            "message": f"Child born ({birth_date_string}) after {self.months_after_husband_death} months following death of father on {husband_death_date_string}",
                        }
                    )
