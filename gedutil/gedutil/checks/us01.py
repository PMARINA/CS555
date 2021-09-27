from datetime import datetime, timedelta
from threading import current_thread

from dateutil.parser import parse as parseDate

from gedutil.mongo_client import families, individuals

from .check import Check


class US01(Check):
    """
    US01: Ensure no dates are in the future
    """

    def __init__(self, tomorrows_date=None):
        if not tomorrows_date:
            today = datetime.today()
            today_day_only = datetime(year=today.year, month=today.month, day=today.day)
            self.tomorrow = today_day_only + timedelta(days=1)
        else:
            self.tomorrow = tomorrows_date

    def setup(self):
        pass

    def run(self):
        self.checkField(individuals, "birt")
        self.checkField(families, "marr")
        self.checkField(families, "div")
        self.checkField(individuals, "deat")

    def check_field_in_future(self, s: str, datetype: str = ""):
        try:
            given = parseDate(s)
        except Exception as e:
            raise ValueError(f"US01 - {datetype} - invalid format - {s}")
        if given >= self.tomorrow:
            raise ValueError(f"US01 - {datetype} in future: {s}")

    def checkField(self, database, field_name):
        for doc in database.find():
            if field_name in doc:
                self.check_field_in_future(doc[field_name], field_name)
