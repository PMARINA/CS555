from gedutil.base import ID, Error_Type, User_Story
from gedutil.mongo_client import errors, families

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc


class US18(Check):
    """
    Assignment:

    > Siblings should not marry one another
    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        family_collection = []
        # Go through the families
        for doc in families.find():
            child_ids = get_child_ids_from_doc(doc)
            if not child_ids or len(child_ids) <= 1:
                continue
            family_collection.append((doc[ID.FAM_ID.name], set(child_ids)))
        for doc in families.find():
            spouses = set(get_parents_from_doc(doc))
            if not spouses:
                continue
            for fam_id, children in family_collection:
                num_spouses_from_family = 0
                for child in children:
                    if child in spouses:
                        num_spouses_from_family += 1
                    if num_spouses_from_family > 1:
                        break
                if num_spouses_from_family > 1:
                    err_msg = (
                        f"Multiple children (from family ID: {fam_id}) were listed as spouses"
                        f" in a family (family ID: {doc[ID.FAM_ID.name]})"
                    )
                    errors.insert_one(
                        {
                            "user story": User_Story.US18.name,
                            "error type": Error_Type.ERROR.name,
                            "message": err_msg,
                        }
                    )
