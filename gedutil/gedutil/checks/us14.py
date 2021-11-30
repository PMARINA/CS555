from gedutil.base import Error_Type, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc
from .utils.individuals import get_birthdate


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
                continue
            array = []
            for c in child_ids:
                birth = get_birthdate(c)
                array.append(birth)
            f = len(array)
            err_msg = None
            for x in range(0, f):
                y = array.count(array[x])
                if y > 5:
                    err_msg = f"5 or more siblings with the same birth date present"
            if err_msg != None:
                errors.insert_one(
                    {
                        "user story": User_Story.US14.name,
                        "error type": Error_Type.ANOMALY.name,
                        "message": err_msg,
                    }
                )
