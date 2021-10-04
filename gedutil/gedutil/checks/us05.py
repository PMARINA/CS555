# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.mongo_client import families, individuals

from .check import Check


class US05(Check):
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
            if "marr" not in doc:
                continue
            marriage_date = parseDate(doc["marr"])
            # latest_birth_date = marriage_date - timedelta(days=365 * 14)
            for id in ids_of_people:
                person = individuals.find_one({"ged_id": id})
                if "deat" not in person:
                    f"This person does not have a recorded death date."
                    continue
                deat_date = parseDate(person["deat"])
                if deat_date < marriage_date:
                    raise ValueError(
                        f"US05 - {deat_date} occured before marriage on {marriage_date}."
                    )
