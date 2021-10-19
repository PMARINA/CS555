from datetime import datetime, timedelta
from threading import current_thread

from dateutil.parser import parse as parseDate

from gedutil.base import Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check

THIS_USER_STORY = User_Story.US01.name


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

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        self.checkField(individuals, GED_Tag.BIRT.name)
        self.checkField(families, GED_Tag.MARR.name)
        self.checkField(families, GED_Tag.DIV.name)
        self.checkField(individuals, GED_Tag.DEAT.name)

    def check_field_in_future(self, s: str, datetype: str = ""):
        try:
            given = parseDate(s)
        except Exception as e:
            errors.insert_one(
                {
                    "user story": THIS_USER_STORY,
                    "error type": Error_Type.ERROR.name,
                    "message": f"{datetype} - invalid format - {s}",
                }
            )
            return
        if given >= self.tomorrow:
            errors.insert_one(
                {
                    "user story": THIS_USER_STORY,
                    "error type": Error_Type.ERROR.name,
                    "message": f"{datetype} in future: {s}",
                }
            )

    def checkField(self, database, field_name):
        for doc in database.find():
            if field_name in doc:
                self.check_field_in_future(doc[field_name], field_name)
