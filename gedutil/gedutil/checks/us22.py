from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check


class US22(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        def check_db(collection, keyname):
            s = set()
            for record in collection.find():
                if keyname not in record:
                    continue
                if record[keyname] in s:
                    errors.insert_one(
                        {
                            "user story": User_Story.US22.name,
                            "error type": Error_Type.ERROR.name,
                            "message": f"Non unique {keyname}: {record[keyname]}",
                        }
                    )
                else:
                    s.add(record[keyname])

        check_db(families, ID.FAM_ID.name)
        check_db(individuals, ID.IND_ID.name)
