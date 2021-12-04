from datetime import timedelta

from gedutil.base import Error_Type, User_Story
from gedutil.mongo_client import errors, families

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc
from .utils.individuals import get_birthdate

WEEKS_IN_A_MONTH = 4.3452381  # Provided by Google


class US13(Check):
    """
    Assignment:

    > Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one
      day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)

    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            child_ids = get_child_ids_from_doc(doc)
            if not child_ids:
                # Either children or parents are not present = no parsing...
                continue
            child_birth_dates = [(c, get_birthdate(c)) for c in child_ids]
            child_birth_dates = sorted(child_birth_dates, key=lambda e: e[1])
            last_child = child_birth_dates[0]
            for i in range(1, len(child_birth_dates)):
                curr_child = child_birth_dates[i]
                time_between_births = curr_child[1] - last_child[1]
                if not time_between_births_legal(time_between_births):
                    err_msg = (
                        f"Child (ID: {last_child[0]}) was born too close to another child (ID: {curr_child[0]})"
                        f" (time: {time_between_births.total_seconds()/60/60/24} days) "
                    )
                    errors.insert_one(
                        {
                            "user story": User_Story.US13.name,
                            "error type": Error_Type.ERROR.name,
                            "message": err_msg,
                        }
                    )
                last_child = curr_child


def time_between_births_legal(
    duration, max_days_between_birth=2, min_months_between_birth=8
):
    min_weeks_between_birth = min_months_between_birth * WEEKS_IN_A_MONTH
    return duration < timedelta(days=max_days_between_birth) or duration > timedelta(
        weeks=min_weeks_between_birth
    )
