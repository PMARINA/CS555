# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.mongo_client import families, individuals

from .check import Check


class US06(Check):
    def __init__(self):
        pass

    def setup(self):
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            if "wife" not in doc:
                ids_of_people = []
            else:
                ids_of_people = doc["wife"]
            if "husb" in doc:
                ids_of_people.extend(doc["husb"])
            if "div" not in doc:
                continue
            divorce_date = parseDate(doc["div"])
            # latest_birth_date = marriage_date - timedelta(days=365 * 14)
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
