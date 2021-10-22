from datetime import datetime, timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US37(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        for doc in individuals.find():
            if GED_Tag.DEAT.name in doc:  # The person has died
                death_date = parseDate(doc[GED_Tag.DEAT.name])
                now = datetime.now()
                if (now - death_date).days <= 30:  # Check if they died recently
                    missed_people = get_info(doc)
                    if (
                        len(missed_people["children"]) != 0
                        or len(missed_people["spouses"]) != 0
                    ):
                        message = f"{doc[GED_Tag.NAME.name]} ({doc[ID.IND_ID.name]}) is missed by "
                        if "children" in missed_people:
                            message += "their children ("
                            message += ", ".join(missed_people["children"])
                            message += ")"
                        if "spouses" in missed_people:
                            if "children" in missed_people:
                                message += " and "
                            message += "their spouses ("
                            message += ", ".join(missed_people["spouses"])
                            message += ")"
                        errors.insert_one(
                            {
                                "user story": User_Story.US37.name,
                                "error type": Error_Type.RESULT.name,
                                "message": message,
                            }
                        )


def get_info(doc):
    """Doc is an individual's document"""
    # Assuming we want both current and past spouses
    # If we don't want to get old families, check if div in fam_doc.
    results = {"children": [], "spouses": []}
    if GED_Tag.FAMS.name in doc:
        for fam_id in doc[GED_Tag.FAMS.name]:
            fam_doc = families.find_one({ID.FAM_ID.name: fam_id})
            if GED_Tag.CHIL.name in fam_doc:
                for chil_id in fam_doc[GED_Tag.CHIL.name]:
                    if GED_Tag.DEAT.name not in individuals.find_one(
                        {ID.IND_ID.name: chil_id}
                    ):
                        results["children"].append(chil_id)  # If they're still alive...
            for spouse_id in get_parents_from_doc(fam_doc):
                if spouse_id == doc[ID.IND_ID.name]:
                    continue  # We know the original person died...
                if GED_Tag.DEAT.name not in individuals.find_one(
                    {ID.IND_ID.name: spouse_id}
                ):
                    results["spouses"].append(spouse_id)

    return results
