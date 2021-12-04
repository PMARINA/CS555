# comment
from datetime import timedelta

from dateutil.parser import parse as parse_date

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check

WEEKS_IN_A_MONTH = 4.3452381  # Provided by Google

THIS_USER_STORY = User_Story.US08.name


class US08(Check):
    def __init__(self, months_after_divorce=9):
        self.months_after_divorce = months_after_divorce

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            if GED_Tag.CHIL.name in doc and (
                GED_Tag.MARR.name in doc or GED_Tag.DIV.name in doc
            ):
                strings = []
                dates = []
                for name in [GED_Tag.MARR.name, GED_Tag.DIV.name]:
                    if name in doc:
                        strings.append(doc[name])
                    else:
                        strings.append(None)
                for date_string in strings:
                    if date_string:
                        dates.append(parse_date(date_string))
                    else:
                        dates.append(None)
                children = doc[GED_Tag.CHIL.name]
                for child_id in children:
                    child = individuals.find_one({ID.IND_ID.name: child_id})
                    if GED_Tag.BIRT.name in child:
                        birth_date_string = child[GED_Tag.BIRT.name]
                        birth_date = parse_date(birth_date_string)
                        # Before marriage
                        if dates[0] and birth_date < dates[0]:
                            errors.insert_one(
                                {
                                    "user story": THIS_USER_STORY,
                                    "error type": Error_Type.ANOMALY.name,
                                    "message": f"Child born ({birth_date_string}) before marriage of parents on {strings[0]}.",
                                }
                            )
                        if dates[1] and birth_date > dates[1] + timedelta(
                            weeks=self.months_after_divorce * WEEKS_IN_A_MONTH
                        ):
                            errors.insert_one(
                                {
                                    "user story": THIS_USER_STORY,
                                    "error type": Error_Type.ANOMALY.name,
                                    "message": f"Child born ({birth_date_string}) after {self.months_after_divorce} months following divorce on {strings[1]}.",
                                }
                            )
