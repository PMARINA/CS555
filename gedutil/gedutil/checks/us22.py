from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID
from gedutil.mongo_client import families, individuals

from .check import Check


class US22(Check):
    def __init__(self):
        pass

    def setup(self):
        pass

    def run(self):
        def check_db(collection, keyname):
            s = set()
            for record in collection.find():
                if keyname not in record:
                    continue
                if record[keyname] in s:
                    raise ValueError(f"Non unique {collection} id: {record[keyname]}")
                else:
                    s.add(record[keyname])

        check_db(families, ID.FAM_ID.name)
        check_db(individuals, ID.IND_ID.name)
