from dateutil.parser import parse as parse_date

from gedutil.base import Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families

from .check import Check

THIS_USER_STORY = User_Story.US04.name


class US04(Check):
    """
    The assignment:

    > Marriage should occur before divorce of spouses, and divorce can only occur after marriage
    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            # If they haven't both married and divorced, then skip the doc
            if GED_Tag.MARR.name not in doc and GED_Tag.DIV.name in doc:
                errors.insert_one(
                    {
                        "user story": THIS_USER_STORY,
                        "error type": Error_Type.ERROR.name,
                        "message": f"A divorce date has been listed without a marriage date",
                    }
                )
            if not (GED_Tag.MARR.name in doc and GED_Tag.DIV.name in doc):
                continue

            # Get the strings from the database
            marr_date_string = doc[GED_Tag.MARR.name]
            divorce_date_string = doc[GED_Tag.DIV.name]

            # Parse into a comparable format
            marr_date = parse_date(marr_date_string)
            divorce_date = parse_date(divorce_date_string)

            # > because it's possible to divorce on the same day you marry (I think?)
            if marr_date > divorce_date:
                errors.insert_one(
                    {
                        "user story": THIS_USER_STORY,
                        "error type": Error_Type.ERROR.name,
                        "message": f"Marriage date ({marr_date_string}) was after divorce date ({divorce_date_string})",
                    }
                )
