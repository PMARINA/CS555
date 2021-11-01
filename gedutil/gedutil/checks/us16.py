# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc
from .utils.individuals import get_last_name_from_db, get_name, isMale


class US16(Check):
    """
    Assignment:

    > All male members of a family should have the same last name
    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        for doc in families.find():
            parentIds = get_parents_from_doc(doc)
            acceptable_last_names = [
                get_last_name_from_db(p) for p in parentIds if isMale(p)
            ]
            if not acceptable_last_names:
                continue  # No male members in the family
            for personId in get_child_ids_from_doc(doc):
                if isMale(personId):
                    person_last_name = get_last_name_from_db(personId)
                    if person_last_name not in acceptable_last_names:
                        errors.insert_one(
                            {
                                "user story": User_Story.US16.name,
                                "error type": Error_Type.ANOMALY.name,
                                "message": f"Expected child ({get_name(personId)}) of family: {doc[ID.FAM_ID.name]}: to carry a family name of ({acceptable_last_names})",
                            }
                        )
