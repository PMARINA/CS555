from gedutil.base import ID, Error_Type, User_Story
from gedutil.mongo_client import errors, families

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc


class US15(Check):
    """
    Assignment:

    > There should be fewer than 15 siblings in a family
    """

    def __init__(self, max_number_children=15):
        self.max_number_children = max_number_children

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        for doc in families.find():
            children = get_child_ids_from_doc(doc)
            if len(children) >= self.max_number_children:
                msg = f"Family (ID: {doc[ID.FAM_ID.name]}) has more than {self.max_number_children} children"
                errors.insert_one(
                    {
                        "user story": User_Story.US15.name,
                        "error type": Error_Type.ERROR.name,
                        "message": msg,
                    }
                )
