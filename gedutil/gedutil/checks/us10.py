# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.mongo_client import families, individuals

from .check import Check


class US10(Check):
    def __init__(self):
        pass

    def setup(self):
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            ids_of_people = doc["wife"]
            ids_of_people.extend(doc["husb"])
            # if ''
            marriage_date = parseDate(doc["marr"])
            latest_birth_date = marriage_date - timedelta(years=14)
            for id in ids_of_people:
                person = individuals.find_one({"ged_id": id})
                birth_date = parseDate(person["birt"])
                if birth_date >= latest_birth_date:
                    raise ValueError(
                        f"US10 - {birth_date} too close to marriage date: {marriage_date}"
                    )
