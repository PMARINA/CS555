# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc

THIS_USER_STORY = User_Story.US02.name


class US02(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            ids_of_people = get_parents_from_doc(doc)
            if GED_Tag.MARR.name not in doc:
                continue
            marriage_date = parseDate(doc[GED_Tag.MARR.name])
            # latest_birth_date = marriage_date - timedelta(days=365 * 14)
            for id in ids_of_people:
                person = individuals.find_one({ID.IND_ID.name: id})
                if GED_Tag.BIRT.name not in person:
                    f"This person does not have a recorded death date."
                    continue
                birt_date = parseDate(person[GED_Tag.BIRT.name])
                if marriage_date < birt_date:
                    errors.insert_one(
                        {
                            "user story": THIS_USER_STORY,
                            "error type": Error_Type.ERROR.name,
                            "message": f"Marriage date ({marriage_date}) occured before birth on {birt_date}.",
                        }
                    )
