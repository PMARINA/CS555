from datetime import timedelta

from gedutil.base import Error_Type, User_Story
from gedutil.mongo_client import errors, families

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc
from .utils.individuals import get_birthdate

WEEKS_IN_A_MONTH = 4.3452381  # Provided by Google


class US14(Check):
    """
    Assignment:

    > No more than five siblings should be born at the same time

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
            groups_of_children = []
            current_group = []
            for i in range(1, len(child_birth_dates)):
                curr_child = child_birth_dates[i]
                time_between_births = curr_child[1] - last_child[1]
                if time_between_births < timedelta(days=2):
                    if not current_group:
                        current_group.append(last_child[0])
                    current_group.append(curr_child[0])
                else:
                    if current_group:
                        groups_of_children.append(current_group)
                    current_group = []
            if current_group:
                groups_of_children.append(current_group)
            for group in groups_of_children:
                if len(group) > 5:
                    ids = ", ".join(group)
                    err_msg = f"More than five children were born within a day of one another. Their IDs follow: {ids}"
                    errors.insert_one(
                        {
                            "user story": User_Story.US14.name,
                            "error type": Error_Type.ERROR.name,
                            "message": err_msg,
                        }
                    )
