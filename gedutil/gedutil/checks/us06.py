# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.mongo_client import families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US06(Check):
    def __init__(self):
        pass

    def setup(self):
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            if "div" not in doc:
                continue
            divorce_date = parseDate(doc["div"])

            ids_of_people = get_parents_from_doc(doc)
            for id in ids_of_people:
                person = individuals.find_one({"ged_id": id})
                if "deat" not in person:
                    f"This person does not have a recorded death date."
                    continue
                deat_date = parseDate(person["deat"])
                if deat_date < divorce_date:
                    raise ValueError(
                        f"US06 - {deat_date} occured before divorce on {divorce_date}."
                    )
