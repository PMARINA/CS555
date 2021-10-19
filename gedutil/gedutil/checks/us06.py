# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc

THIS_USER_STORY = User_Story.US06.name


class US06(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            if GED_Tag.DIV.name not in doc:
                continue
            divorce_date = parseDate(doc[GED_Tag.DIV.name])

            ids_of_people = get_parents_from_doc(doc)
            for id in ids_of_people:
                person = individuals.find_one({ID.IND_ID.name: id})
                if GED_Tag.DEAT.name not in person:
                    f"This person does not have a recorded death date."
                    continue
                deat_date = parseDate(person[GED_Tag.DEAT.name])
                if deat_date < divorce_date:
                    errors.insert_one(
                        {
                            "user story": THIS_USER_STORY,
                            "error type": Error_Type.ERROR.name,
                            "message": f"Death date ({deat_date}) occured before divorce on {divorce_date}.",
                        }
                    )
